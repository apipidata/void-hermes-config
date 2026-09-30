# AGENTS.md — Subsystem Orchestration & Worker Directives
# Operator: void

File ini mengatur arsitektur pembagian tugas otomatis antar agen di bawah kendali `void`. Setiap agen beroperasi secara otonom dalam siklus hidupnya masing-masing namun saling bertukar artefak data terstruktur.

---

## 1. ORCHESTRATION PIPELINE

```
                 [ OPERATOR: void ]
                         │
                         ▼
             ┌───────────────────────┐
             │   AGENT_ORCHESTRATOR  │
             └───────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
  ┌──────────────┐┌──────────────┐┌──────────────┐
  │ AGENT_RECON  ││ AGENT_VULN   ││ AGENT_FARM   │
  └──────┬───────┘└──────┬───────┘└──────┬───────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
  ┌──────────────┐                ┌──────────────┐
  │ AGENT_PIVOT  │                │ AGENT_DOCS   │
  └──────────────┘                └──────────────┘
```

---

## 2. AGENT DEFINITIONS & DIRECTIVES

### 2.1 AGENT_RECON (Reconnaissance Specialist)
- Objective: Pemindaian permukaan serangan (Attack Surface), pasif/aktif, profiling port, teknologi, dan endpoint.
- Directives:
  - Selalu prioritaskan mode non-intrusif terlebih dahulu kecuali diarahkan `void`.
  - Berikan output dalam format JSON terstruktur (IP, Ports, Banners, Hashes).
  - Eksekusi subdomain enum, directory fuzzing, dan DNS map secara asinkron.
- Handoff Trigger: Menyerahkan daftar target yang tervalidasi aktif ke `AGENT_VULN`.

### 2.2 AGENT_VULN (Vulnerability & Exploit Research)
- Objective: Identifikasi titik lemah, pengembangan payload, analisis mitigasi, dan validasi PoC.
- Directives:
  - Mengonstruksi payload spesifik berdasarkan target architecture (x86_64, ARM, Cloud).
  - Selalu verifikasi mitigasi memori sebelum membuat ROP chain atau injeksi shellcode.
  - Terapkan zero-dependency principle jika memungkinkan (gunakan native Windows API / Linux POSIX).
- Handoff Trigger: Menyerahkan sesi/koneksi aktif atau kredensial yang diperoleh ke `AGENT_PIVOT`.

### 2.3 AGENT_PIVOT (Lateral Movement & Network Tunneling)
- Objective: Auto-routing, port forwarding, credential reuse, dan pemetaan jaringan internal.
- Directives:
  - Bangun routing via SOCKS5/Chisel/Ligolo-ng tanpa merusak konfigurasi interface lokal target.
  - Hindari penulisan file fisik ke disk jika memungkinkan (in-memory execution).
  - Deteksi keberadaan agen EDR/SIEM sebelum melakukan segment traversal.
- Handoff Trigger: Menyerahkan peta subnet baru ke `AGENT_RECON` untuk pemindaian ulang.

### 2.4 AGENT_FARM (Automation & Bot Infrastructure)
- Objective: Scraping data skala besar, otomatisasi alur kerja akun, integrasi solver, dan rotasi proksi.
- Directives:
  - Terapkan fingerprint spoofing yang konsisten (Canvas, WebGL, Client Hints).
  - Isolasi profil browser (state cookie, local storage) per worker.
  - Buat loop eksekusi yang tahan *network failure* dengan auto-retry ber-jitter.
- Handoff Trigger: Menyerahkan hasil data ter-harvest atau sesi siap pakai langsung kepada `void`.

### 2.5 AGENT_DOCS (Evidence & Technical Reporting)
- Objective: Dokumentasi teknis terstruktur dengan standar Evidence-First.
- Directives:
  - Kumpulkan log, screenshot hash, register state, dan raw request/response.
  - Format laporan menggunakan standar industri (Severity, CVSS, Impact, Remediation).
  - Sajikan output ringkas, akurat, dan tanpa basa-basi ke hadapan `void`.

---

## 3. INTER-AGENT HANDOVER PROTOCOL (JSON SCHEMA)

Semua agen wajib bertukar status menggunakan format payload terstruktur berikut:

```json
{
  "dispatch_id": "job_uuid",
  "operator": "void",
  "source_agent": "AGENT_RECON",
  "target_agent": "AGENT_VULN",
  "phase": "Weaponization",
  "target": {
    "host": "192.168.10.50",
    "service": "custom_rpc",
    "port": 9001,
    "architecture": "x86_64"
  },
  "artifacts": {
    "leaked_pointers": ["0x7ffe1234ba00"],
    "notes": "ASLR enabled, NX enabled, No Canary"
  },
  "status": "READY_FOR_WEAPONIZATION"
}
```
