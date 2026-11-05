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
---
