import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from lab import run
class LabTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.root=self.base/'input';self.root.mkdir()
        (self.root/'start.md').write_text('[next](next.txt) [remote](https://example.com) [escape](../secret.txt)')
        (self.root/'next.txt').write_text('synthetic fixture')
        (self.base/'secret.txt').write_text('synthetic outside fixture')
    def test_pivot_and_evidence(self):
        r=run(self.root,self.base/'report',['start.md'])
        self.assertEqual(len(r['records']),2); self.assertEqual(len(r['transitions']),1)
        self.assertEqual(r['network_requests'],0)
        self.assertTrue((self.base/'report'/'SHA256.json').is_file())
    def test_depth_zero(self):
        self.assertEqual(len(run(self.root,self.base/'report',['start.md'],depth=0)['records']),1)
    def test_traversal(self):
        with self.assertRaises(ValueError): run(self.root,self.base/'report',['../secret.txt'])
    def test_symlink(self):
        (self.root/'link.txt').symlink_to(self.base/'secret.txt')
        r=run(self.root,self.base/'report',['link.txt'])
        self.assertEqual(r['records'][0]['status'],'not_read')
    def test_output_inside_input(self):
        with self.assertRaises(ValueError):run(self.root,self.root/'report',['start.md'])
    def test_no_overwrite(self):
        out=self.base/'report';out.mkdir()
        with self.assertRaises(FileExistsError):run(self.root,out,['start.md'])
    def test_duplicate_seed(self):
        r=run(self.root,self.base/'report',['next.txt','next.txt'])
        self.assertEqual(len(r['records']),1)
    def test_worker_bound(self):
        with self.assertRaises(ValueError):run(self.root,self.base/'report',['start.md'],workers=3)
if __name__=='__main__':unittest.main()
