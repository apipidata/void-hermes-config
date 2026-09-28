#!/usr/bin/env python3
"""Offline inventory worker. Does not execute samples or follow discovered URLs."""
import argparse, concurrent.futures, datetime, hashlib, json, os, re, stat
from pathlib import Path

def inspect(root, relative, limit):
    path = root / relative
    # Reject links in all path components; O_NOFOLLOW also guards the final open.
    if any(x.is_symlink() for x in [path, *path.parents]):
        raise ValueError('symlink rejected')
    path.resolve().relative_to(root)
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        before = os.fstat(f.fileno())
        if not stat.S_ISREG(before.st_mode): raise ValueError('not a regular file')
        if before.st_size > limit: raise ValueError('file exceeds size limit')
        data = f.read(limit + 1)
        after = os.fstat(f.fileno())
    if len(data) > limit: raise ValueError('file grew beyond limit')
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise ValueError('file changed during read')
    result = {'path':str(relative),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
              'kind':'PE candidate' if data.startswith(b'MZ') else 'ELF' if data.startswith(b'\x7fELF') else 'other',
              'status':'observed','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    # Literal relative Markdown links only. These are candidates, never shell commands.
    candidates=[]
    if path.suffix.lower() in ('.md','.txt'):
        text=data.decode('utf-8',errors='replace')
        for link in re.findall(r'\]\(([^\s()]+)\)',text):
            if ':' in link or link.startswith(('/', '#')): continue
            candidate=path.parent / link.split('#')[0]
            if any(x.is_symlink() for x in [candidate,*candidate.parents]): continue
            try: rel=candidate.resolve().relative_to(root)
            except ValueError: continue
            if candidate.is_file(): candidates.append(str(rel))
    return result, sorted(set(candidates))

def run(root, output, seeds, workers=2, depth=3, max_files=200, limit=1048576):
    root=Path(root).resolve(strict=True); output=Path(output).resolve()
    if not root.is_dir(): raise ValueError('root must be a directory')
    if output==root or root in output.parents: raise ValueError('output must be outside input root')
    if not 1<=workers<=2 or not 0<=depth<=3 or not 1<=max_files<=200 or not 1<=limit<=1048576:
        raise ValueError('budget exceeds allowed bounds')
    if not seeds: raise ValueError('explicit seed required')
    pending=[]
    for seed in seeds:
        rel=Path(seed)
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('seed must be relative and contained')
        pending.append((str(rel),0,None))
    output.mkdir(parents=True,exist_ok=False)
    records=[]; edges=[]; seen=set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        while pending and len(seen)<max_files:
            batch=[]
            while pending and len(batch)<workers and len(seen)<max_files:
                rel,level,parent=pending.pop(0)
                if rel in seen: continue
                seen.add(rel); batch.append((rel,level,parent,pool.submit(inspect,root,rel,limit)))
            for rel,level,parent,future in batch:
                eid=f'E{len(records)+1:04}'
                try:
                    result,links=future.result()
                    result['id']=eid; records.append(result)
                    if parent: edges.append({'source':parent,'destination':eid,'reason':'contained literal file link'})
                    if level<depth:
                        pending.extend((link,level+1,eid) for link in links)
                except (OSError,ValueError) as error:
                    records.append({'id':eid,'path':rel,'status':'not_read','error':type(error).__name__})
    result={'mode':'offline_artifact_inventory','records':records,'transitions':edges,
            'budget_exhausted':bool(pending),'sample_execution':False,'network_requests':0,
            'limitations':['Not a vulnerability scanner.','Metadata and hashes only; no exploitability conclusion.',
            'Use immutable inputs in an isolated VM; this script is not an OS sandbox.']}
    (output/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Evidence-first inventory','',f'Artifacts considered: {len(records)}',
           '', '## Seven-phase status',
           '1. Scope: explicit input root and seeds.',
           '2. Recon: offline metadata and hashes recorded.',
           '3. Analysis: file signatures only; no vulnerability assertion.',
           '4. Test design: not performed.', '5. Validation: inventory only; no samples executed.',
           '6. Remediation: not assessed.', '7. Report: this report and evidence.json.',
           '', '## Evidence','']
    for row in records:
        lines.append(f"- {row['id']}: {json.dumps(row['path'])}; {row['status']}; SHA-256: {row.get('sha256','not available')}")
    lines+=['','## Limitations',*result['limitations']]
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n')
    manifest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in output.iterdir() if f.is_file()}
    (output/'SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',required=True); ap.add_argument('--output',required=True)
    ap.add_argument('--seed',action='append',required=True)
    ap.add_argument('--workers',type=int,default=2);ap.add_argument('--depth',type=int,default=3)
    args=ap.parse_args()
    result=run(args.root,args.output,args.seed,args.workers,args.depth)
    print(json.dumps({'records':len(result['records']),'output':args.output}))
if __name__=='__main__': main()
