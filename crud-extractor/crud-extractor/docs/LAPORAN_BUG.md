# Laporan Bug

Salin blok di bawah untuk setiap bug. Bagian **Akar masalah** wajib ditulis dengan kata-kata
sendiri dan memakai konsep dari *Crafting Interpreters* (sebutkan bab). Bagian ini diuji lisan.

---

## Bug 1: (judul singkat)

**Ditemukan oleh:** (nama) · **Diperbaiki oleh:** (nama)

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql

```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?


## Bug 1: Keyword huruf kecil dikenali sebagai IDENT

**Ditemukan oleh:** Fadhil · **Diperbaiki oleh:** Fadhil

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).
Input `select id from t`. Token pertama yang dihasilkan adalah
`IDENT 'select'`, padahal SPESIFIKASI bagian 2.2 mewajibkan `KEYWORD 'SELECT'`
(keyword tidak peka huruf besar/kecil dan nilainya dinormalisasi ke huruf besar).
Tes yang gagal: `test_keyword_huruf_kecil`.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
select 1
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Berdasarkan spesifikasi.md seharusnya keyword bebas, tidak harus kapital. tapi di kode yang sebelumnya keyword 'select' dengan huruf kecil dianggap ident. konsep yang dilanggar adalah Reserved Words, pada lexer.py setiap keyword dipesan dalam huruf kapital, padahal di spesifikasi.md bisa besar/kecil.

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.
kami mengbah fungsi _word pada file lexer.py pada bagian if text in keyword kami menambahkan .upper() untuk mengkonversi setiap hurufnya menjadi kapital agar sesuai dengan keyword yang sudah ditentukan. alternatif nya bisa dengan memasukan setiap kombinasi huruf kecil dan besar pada tabel reserved word (keyword), kami tidak memilih cara tersebut karena jika begitu untuk setiap keyword yang di pesan harus mamasukan banyak sekali kombinasi huruf besar/kecil agar sesuai dengan spesifikasi.md

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.
test_keyword_campuran_huruf_dinormalisasi_besar 
test_kata_berawalan_keyword_tetap_ident

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?
ya, membantu.
kami memferifikasi dengan pytest, jika hasil nya sudah memenuhi semua test berarti bener. seperti ketika AI keliru mengira `tests/test_tambahan.py` sudah punya import, kesalahan itu baru diketahui dari error pytest lalu kami perbaiki sendiri.


## Bug 2: Komentar blok `/* ... */` belum didukung (TODO T3)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).
Setiap file SQL yang memuat `/* ... */` langsung gagal di lexer sebelum
parser sempat berjalan dengan menampilakn pesan `LexError: Baris L, kolom K: komentar blok belum didukung`. Karena hampir semua file SQL produksi memuat komentar blok sebagai dokumentasi, seluruh pipeline terhenti untuk file-file tersebut.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
/* dokumentasi */ SELECT 1;
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Karena kami belum mengimplementasikan TODO(T3). Stub di _scan_token() sengaja melempar LexError untuk setiap /*.

Konsep penanganan komentar baris // di Crafting Interpreters Bab 4 4.6 ini belum diterapkan, konsep ketika scanner membaca /, scanner tidak langsung memutuskan "ini operator pembagian", tetapi melihat satu karakter selanjutnya untuk menentukan apakah ini operator atau komentar. Pola ini berlaku juga untuk /* ... */, deteksi dulu sampai akhir dan jangan panggil addToken (komentar tidak menghasilkan token).

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.
Kami mengubah file crud/lexer.py, method Lexer._scan_token(), cabang
if ch == "/" and self._peek() == "*": Agar setelah mendeteksi "/*" masuk ke While loop memeriksa sampai EOF, sehingga komentar yang tidak ditutup melempar LexError di posisi /*

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus sesudahnya.
tests/test_tambahan.py::test_komentar_blok_didukung, gagal sebelum
perbaikan (melempar LexError), lulus sesudahnya. Ditambahkan juga coverage
test_komentar_blok_lintas_baris untuk memastikan line tetap akurat untuk
token sesudahnya dan test_komentar_blok_tidak_ditutup_error.

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?
Ya membantu memperbaiki, kami menjalankan test_tambahan.py untuk melihat jika semua test tercapai maka terverifikasi.
---
