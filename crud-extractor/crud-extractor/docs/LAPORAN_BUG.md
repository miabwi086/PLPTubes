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
/* x */ SELECT 1;
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Karena kami belum mengimplementasikan TODO(T3). Stub di _scan_token() sengaja melempar LexError untuk setiap /*.

Konsep penanganan komentar baris // di Crafting Interpreters Bab 4 4.6 ini belum diterapkan, konsep ketika scanner membaca /, scanner tidak langsung memutuskan "ini operator pembagian", tetapi melihat satu karakter selanjutnya untuk menentukan apakah ini operator atau komentar. Pola ini berlaku juga untuk /* ... */, deteksi dulu sampai akhir dan jangan panggil addToken (komentar tidak menghasilkan token).

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.
Kami mengubah file crud/lexer.py, method Lexer._scan_token(), cabang
if ch == "/" and self._peek() == "*": Agar setelah mendeteksi "/*" masuk ke While loop memeriksa sampai EOF, sehingga komentar yang tidak ditutup melempar LexError di posisi /*

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus sesudahnya.  
test_komentar_blok_didukung  
test_komentar_blok_lintas_baris  
test_komentar_blok_tidak_ditutup_error

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?  
Kami menemukan bug saat melakukan pytest, AI membantu pada memperbaiki code dan alternatif coda yang bisa menjadi opsi, kami menjalankan test_tambahan.py untuk menguji kembali dan hasilnya sukses melewati test.



## Bug 3: <> dipecah jadi < dan >

**Ditemukan oleh:** Fadhil  · **Diperbaiki oleh:** Fadhil

**Gejala.** inputnya dari yang Baris 6, kolom 41 di laporan_penjualan.sql. yang mana di situ menggunakan token '<>' tapi kebaca nya malah '<' sama '>' padahal di spesifikasi.md baigian 2.5 disebutkan Lexer selalu mengambil operator **terpanjang** yang cocok (maximal munch): `<>` adalah satu token, bukan `<` lalu `>`.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
a <> b
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
masalahnya karena lexer hanya membaca '<' kemudian cek setelah nya '=' bukan? setelah tahu bukan, di tidak ngecek apakah setelah nya '>' atau bukan? hal ini melanggar konsep maximal munch yang menyatakan bahwa bila beberapa aturan leksikal cocok, aturan yang mencocokkan karakter terbanyak menang, sehingga `<>` (2 karakter) harus mengalahkan `<` (1 karakter). Kode lama melanggarnya. Lexer tidak menganggap ini salah karena `<` dan `>` masing-masing token yang sah. Kesalahan baru terlihat di parser, yang tidak menerima `>` berdiri sendiri di awal ekspresi. Jadi akarnya di lexer tetapi gejalanya muncul di tahap berikutnya.

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.
perbaikan nya tambahkan pengecekan '>' setelah muncul setelah pengecekan '='. 
Alternatif yang dipertimbangkan: membuat tabel operator dua karakter dan mencocokkan dari
yang terpanjang. Tidak dipilih karena perubahan lebih besar dan gaya kode yang ada sudah
memakai `_match` untuk operator lain (`>=`, `!=`). 

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.
test_operator_tidak_sama_satu_token

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?
AI membantu menunjuk lokasi bug dan mengusulkan perbaikan tiga cabang. Kami mengetik perbaikan sendiri dan memverifikasi dengan `python -m pytest`: pesan error `'>'` di baris 6 hilang dan tes regresi hijau.



## Bug 4: `INSERT ... SELECT` (TODO T1)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md (sebutkan bagiannya).  
Test bawaan `tests/test_analyzer.py::test_matrix_laporan_penjualan`  
gagal dengan:

```error
assert (None is None and [ParseError("...an 'SELECT'")] == []  
+  where None = FileResult(statements=[StatementResult(line=3, kind='SELECT', tables={'pelanggan': 'R', 'pesanan': 'R'}, columns={('pe...ParseError("Baris 10, kolom 1: INSERT ... SELECT belum didukung, ditemukan 'SELECT'")], diagnostics=[], lex_error=None).lex_error
```

File `data/sample/laporan_penjualan.sql` pada baris ke-10 memuat
`INSERT INTO ... SELECT ...`. Parser menolak, membuat seluruh
statement setelahnya tidak pernah dianalisis dan CRUD matrix file tersebut tidak lengkap.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
INSERT INTO t (a) SELECT b FROM s;
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Karena belum ada implementasi, konsep yang belum diimplementasi adalah recursive descent pada Crafting Interpreters Bab 6 6.2, di sini aturan insert_stmt punya dua alternatif(VALUES dan SELECT). /
Tetapi method _insert() hanya menerjemahkan alternatif pertama dan melempar error untuk alternatif kedua, sedagnakn method _select() yang dibutuhkan untuk cabang kedua tersedia dan bisa dipanggil.

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.  
Mengubah `parser.py`, pada method `Parser._insert()`, diganti dengan pemanggilan `self._select()` yang sudah ada. Method mereturn `ast.Select` berisi seluruh sumber, join, where, dan subquery yang sudah di-*parse*, lalu hasilnya dibungkus menjadi `ast.Insert(table, columns, [], query, line=start.line)`, `values` dikosongkan karena bentuk ini tidak punya baris `VALUES`.  
Tidak ada perubahan pada `ast_nodes.py` ataupun di `analyzer.py` (`analyze_statement()` sudah memeriksa `stmt.query is not None` dan menandai tabel di dalamnya `R`, sesuai SPESIFIKASI 5).  
Alternatif yang ditolak: menambah field AST baru untuk membedakan `VALUES` vs `SELECT` (mengubah API publik 7 tanpa manfaat), dan mem-*parse* `SELECT` manual di dalam `_insert` (menduplikasi `_select()` dan menyimpang dari pola *recursive descent* Bab 6).

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus sesudahnya.  
test_insert_select_didukung  
test_insert_select_matrix_target_c_sumber_r

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?
AI hanya membantu pada memperbaiki bug. Lokasi ditemukan sendiri dari traceback `test_matrix_laporan_penjualan` di pytest, dan kami memperbaiki dengan merujuk SPESIFIKASI.md 3 dan 5 serta *Crafting Interpreters* Bab 6 6.2. AI merekomendasikan alternatif tapi kami tolak. Verifikasi dengan `python -m pytest`: `test_matrix_laporan_penjualan` passed dan dua test regresi.


## Bug 5: subquery di UPDATE ditandai U, seharusnya R

**Ditemukan oleh:** Fadhil  · **Diperbaiki oleh:** Fadhil

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).
Pada laporan_penjualan.sql , tabel pesanan menghasilkan operasi`RUD`, padahal seharusnya `RD`. Penyebabnya statement `UPDATE ... WHERE id IN (SELECT ... FROM pesanan ...)` menandai pesanan sebagai `U`. Menurut SPESIFIKASI bagian 5, tabel yang dibaca lewat subquery selalu `R`, apa pun jenis statement luarnya.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
UPDATE pelanggan SET level = 'gold' WHERE id IN (SELECT pelanggan_id FROM pesanan)
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Analyzer mengumpulkan operasi per tabel dengan menelusuri AST. Untuk UPDATE, subquery di SET dan WHERE ikut diteruskan dengan operasi "U", padahal subquery hanya membaca tabel. Aturan proyek (SPESIFIKASI §5) menyatakan membaca tabel lewat subquery selalu R apa pun jenis statement luarnya. Jadi operasi yang diwariskan dari statement luar ke subquery salah: operasi tabel target tidak boleh “menular” ke tabel lain di dalam subquery.

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.
fungsi `analyze_statement`, cabang `ast.Update`. Dua pemanggilan `_collect` untuk `SET` dan `WHERE` diubah dari `"U"` menjadi `"R"`. Baris yang menandai tabel target (`add("U")`) tidak diubah. Alternatif yang dipertimbangkan: menghapus
parameter operasi di `_collect` karena subquery di ekspresi selalu `R`. Tidak dipilih karena perubahannya lebih besar dan cabang `Insert` dan `Delete` sudah memakai pola yang sama dengan parameter `"R"`.

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.
test_subquery_di_update_adalah_read

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?
AI menjalankan statement `UPDATE` kecil di salinan sementara untuk membuktikan sumber bug, menunjuk `analyzer.py` baris 19-23 sebagai lokasi, dan mengusulkan penggantian `"U"` menjadi `"R"`. Kami mengetik perbaikan sendiri dan memverifikasi dengan `python -m pytest`


## Bug 6: Kolom tanpa qualifier tidak di-resolve (TODO T2)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).  
Test bawaan `tests/test_resolver.py::test_kolom_tanpa_qualifier_satu_tabel`  
gagal dengan:

```
AssertionError: assert {'arsip_pesan...sanan': 'RUD'} == {'arsip_pesan...esanan': 'RD'}  

    Omitting 2 identical items, use -vv to show
    Differing items:
    {'pesanan': 'RUD'} != {'pesanan': 'RD'}
```

Query `SELECT nama FROM pelanggan WHERE aktif = 1` punya satu tabel pada scope terdalam (`pelanggan`), sehingga menurut SPESIFIKASI.md 4.3 kolom `nama` dan `aktif` harus di-resolve ke `"pelanggan"`. Nyatanya `ColumnRef.resolved` tetap `None` untuk keduanya.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
SELECT nama FROM pelanggan
```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?
Kode masuk error pada pytest karena belum diimplementasikan, setelah kode yang memenuhi TODO (T2) dibuat, baru passed. Konsep yang belum diterapkan adalah pola resolver yang dinyatakan di Crafting Interpreters Bab 11 11.3.3 (Resolving variable expressions).  
Untuk kolom tanpa qualifier, pola yang sama berlaku, resolver harus memeriksa scope terdalam terlebih dahulu, lalu memutuskan berdasarkan isi scope tersebut, bukan melompatinya.

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.  
Perbaikan ada di `resolver.py`, method `Resolver._column()`, cabang `col.qualifier is None`. Awalnya yang berisi `pass` diganti dengan langsung membaca `self.scope.entries`, bukan `_lookup(...)`. Ini karena SPESIFIKASI.md 4.3 membatasi pandangan kolom tanpa qualifier pada scope terdalam saja. Tiga kasus ditangani: nol entri → warning, `resolved` tetap `None`; lebih dari satu → warning `kolom '<nama>' ambigu tanpa skema`, `resolved` tetap `None`; tepat satu → `col.resolved = _target_of(entries[0])`. Hasilnya, `SELECT nama FROM pelanggan` menghasilkan `resolved = "pelanggan"`, sedangkan `SELECT nama FROM pelanggan, pesanan` menghasilkan `None` plus warning, sesuai pasal yang sama.

Tiga alternatif ditolak. Memakai `_lookup(col.name)` ditolak karena menelusuri scope ke luar, melanggar 4.3 yang hanya mengizinkan scope terdalam. Mengisi `resolved` dengan string kosong saat ambigu ditolak karena 4.3 menyatakan tetap `None`, dan `analyzer.py` sudah memanfaatkan `None` itu. Melempar exception saat ambigu ditolak karena 4.3 menyatakan kasus itu warning, bukan error — exception akan menghentikan pipeline untuk query yang sintaksnya sah.

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.  
test_kolom_tanpa_qualifier_satu_tabel_resolve  
test_kolom_tanpa_qualifier_dua_tabel_ambigu

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?  
Kami menemukannya saat melakukan pytest dan AI membantu memperbaiki bugnya. Perbaikan yang diambil adalah membaca self.scope.entries langsung sesuai pasal tersebut. Verifikasi dengan `python -m pytest: test_kolom_tanpa_qualifier_satu_tabel` lulus, dua tes regresi hijau, dan seluruh suite tetap hijau. 
