# Log Penggunaan AI

Catat setiap penggunaan AI atau coding agent yang memengaruhi kode atau laporan.

| No | Siapa | Prompt / tugas (ringkas) | Hasil: diterima, diubah, atau ditolak | Alasan | Cara verifikasi |
| --- | --- | --- | --- | --- | --- |
| 1 | Fadhil | Minta penjelasan error ModuleNotFoundError saat pytest | Diterima: jalankan pytest dari folder proyek | Sesuai pytest.ini (pythonpath) | Pytest mengumpulkan 30 tes |
| 2 | Fadhil | Minta cara membaca output pytest dan mencari lokasi bug | Diterima | Bisa kami telusuri sendiri di lexer.py | Ctrl+F dan cek KEYWORDS di terminal |
| 3 | Fadhil | Minta perbaikan Bug 1 keyword huruf kecil | Diterima | Sesuai SPESIFIKASI 2.2 | test_keyword_huruf_kecil hijau |
| 4 | Fadhil | Minta draf laporan dan tes regresi | Diubah: import di test_tambahan.py harus ditambah | AI mengira import sudah ada | pytest menunjukkan TypeError, kami perbaiki |
| 5 | Fadhil | Minta rujukan bab Crafting Interpreters | Diubah: nomor bab kami cek sendiri | Teks buku hasil ekstraksi PDF acak | Cek daftar isi buku |
**Refleksi (3-5 kalimat).** Di bagian mana AI paling membantu? Di mana AI keliru atau
menyesatkan, dan bagaimana kalian mengetahuinya?
