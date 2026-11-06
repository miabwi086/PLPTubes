# Log Penggunaan AI

Catat setiap penggunaan AI atau coding agent yang memengaruhi kode atau laporan.

| No | Siapa | Prompt / tugas (ringkas) | Hasil: diterima, diubah, atau ditolak | Alasan | Cara verifikasi |
| --- | --- | --- | --- | --- | --- |
| 1 | Fadhil | Minta penjelasan error ModuleNotFoundError saat pytest | Diterima: jalankan pytest dari folder proyek | Sesuai pytest.ini (pythonpath) | Pytest mengumpulkan 30 tes |
| 2 | Fadhil | Minta cara membaca output pytest dan mencari lokasi bug | Diterima | Bisa kami telusuri sendiri di lexer.py | Ctrl+F dan cek KEYWORDS di terminal |
| 3 | Fadhil | Minta perbaikan Bug 1 keyword huruf kecil | Diterima | Sesuai SPESIFIKASI 2.2 | test_keyword_huruf_kecil hijau |
| 4 | Fadhil | Minta draf laporan dan tes regresi | Diubah: import di test_tambahan.py harus ditambah | AI mengira import sudah ada | pytest menunjukkan TypeError, kami perbaiki |
| 5 | Fadhil | Minta rujukan bab Crafting Interpreters | Diubah: nomor bab kami cek sendiri | Teks buku hasil ekstraksi PDF acak | Cek daftar isi buku |
| 6 | Fatih | Minta penjelasan error `LexError: komentar blok belum didukung` di `crud/lexer.py:111` | Diterima: itu stub TODO(T3) yang sengaja di-`raise`, bukan bug logika | Sesuai komentar `# TODO(T3)` di kode dan SPESIFIKASI 2.3 | `python -c "from crud.lexer import tokenize; tokenize('/* hi */ SELECT 1;')"` melempar `LexError` yang sama |
| 7 | Fatih | Minta blok kode pengganti stub `/* ... */` | Diubah: usulan AI memakai `str.find("*/")`, kami ganti dengan loop `_advance()` | `str.find` tidak menaikkan `self.line` untuk `\n` di dalam komentar, melanggar SPESIFIKASI 2.1 | `test_komentar_blok_lintas_baris` lolos: token setelah komentar multi-baris ada di `line == 2` |
| 8 | Fatih | Minta kerangka test regresi untuk komentar blok | Diubah: AI hanya usul 1 test, kami tambah 4 kasus tepi (multi-baris, isi `*`, tidak bersarang, tidak ditutup) | Kasus tepi ini yang paling rawan rusak oleh perbaikan, usulan AI tidak mencakupnya | `python -m pytest tests/test_tambahan.py -v`, 6 PASSED; dua test FAILED saat perbaikan di-*revert* sementara |
| 9 | Fatih | Minta kerangka `LAPORAN_BUG.md` untuk bug komentar blok | Diterima untuk format; diubah untuk isi (bagian akar masalah ditulis sendiri) | Deskripsi tugas halaman 9: akar masalah wajib pakai kata-kata sendiri dan konsep buku | Kedua anggota membaca ulang, memastikan bisa jelaskan tanpa catatan |
| 10 | Fatih | Minta rujukan pasal spesifikasi dan bab buku untuk bug komentar blok | Diubah: AI usul Bab 4 §4.6; kami cek sendiri dan tambahkan Challenge #4 di akhir Bab 4 serta SPESIFIKASI §2.3 | Buku hasil ekstraksi PDF bisa salah nomor halaman/bab; wajib dicek manual | Buka daftar isi buku, cocokkan dengan kutipan di `LAPORAN_BUG.md` |

**Refleksi (3-5 kalimat).** Di bagian mana AI paling membantu? Di mana AI keliru atau
menyesatkan, dan bagaimana kalian mengetahuinya?
