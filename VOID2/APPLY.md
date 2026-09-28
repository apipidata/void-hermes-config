# Tahap 2 — penerapan pada paket, bukan instalasi Hermes

## Yang diterapkan
- Persona operator void dan kontrak kerja konsisten.
- 108 SKILL.md berupa workflow scaffold, tanpa klaim implementasi spesialis atau pemasangan.
- Workflow tujuh fase dan prosedur bypass research, AI red team, serta worker lokal.
- Runner inventory offline: hashing, metadata, auto-pivot tautan file relatif,
  deduplikasi, batas worker, bukti JSON, laporan Markdown, manifest SHA-256.
- Konfigurasi rich_messages Telegram tetap true; belum diuji pada runtime tujuan.

## Menjalankan demo
Dari direktori paket, gunakan Python 3 pada lingkungan lab:
```sh
python3 -m unittest discover -s tests -v
python3 tools/lab.py --root fixtures --seed start.md --output demo-new
```
Output harus belum ada dan di luar root input. Runner menerima root eksplisit sebagai
otorisasi lokal; runner tidak membaca scope.yaml. Pastikan root cocok dengan persetujuan
void. Tidak ada shell atau jaringan yang dipanggil runner. Ini bukan sandbox OS;
gunakan input immutable dan VM untuk mencegah perubahan path bersamaan oleh pihak lain.

## Pemasangan Hermes
Ikuti README.md untuk backup dan penggabungan config. skill-library/ belum dipasang ke
skills home. Periksa kompatibilitas format skill pada versi Hermes tujuan terlebih dahulu.
Tidak ada instalasi Hermes di workspace ini yang telah dikonfigurasi atau dijalankan.
Model/provider dan path host belum diketahui, sehingga integrasi tidak dapat diverifikasi.
Jangan menganggap terminal.backend local menyediakan isolasi.

## Telegram versus offline
Flag rich message disiapkan, bukan koneksi Telegram yang diaktifkan. Offline penuh
memerlukan local inference dan gateway berhenti. Penggunaan Telegram perlu perubahan
mode yang disengaja dan kredensial tersimpan di luar artefak ini.
