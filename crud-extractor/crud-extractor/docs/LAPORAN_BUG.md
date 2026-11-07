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

**Gejala.** Input `select id from t` menghasilkan token pertama
`IDENT 'select'`, padahal SPESIFIKASI.md bagian 2.2 mewajibkan
`KEYWORD 'SELECT'`: keyword tidak peka huruf besar/kecil dan nilainya
dinormalisasi ke huruf besar. Tes yang gagal: `test_keyword_huruf_kecil`.

**Reproduksi minimal.**

```sql
select 1
```

**Akar masalah.** Kode lama di `_word()` memeriksa `if text in KEYWORDS`
dengan teks apa adanya, sehingga `select` (huruf kecil) tidak cocok
dengan `SELECT` di tabel `KEYWORDS` dan diklasifikasikan sebagai IDENT.
Konsep yang dilanggar adalah *reserved words*: sekumpulan kata yang
dipesan bahasa sebagai keyword. Di *Crafting Interpreters* Bab 4
(Scanning), penentuan keyword dilakukan setelah lexeme identifier
terkumpul, dengan membandingkan ke tabel keyword. Agar keyword tidak
peka huruf besar/kecil, perbandingan itu harus menormalkan kedua sisi.

**Perbaikan.** File `crud/lexer.py`, fungsi `_word`. Pemeriksaan
`if text in KEYWORDS` diubah menjadi `if text.upper() in KEYWORDS`, dan
nilai token disimpan sebagai `text.upper()` agar konsisten dengan
SPESIFIKASI 2.2. Alternatif yang dipertimbangkan: memasukkan semua
kombinasi huruf besar/kecil ke tabel `KEYWORDS`. Tidak dipilih karena
untuk keyword sepanjang 6 huruf kombinasi bisa mencapai 64 entri, dan
tabel menjadi cepat membengkak setiap kali ada keyword baru.

**Test regresi.** `test_keyword_campuran_huruf_dinormalisasi_besar` dan
`test_kata_berawalan_keyword_tetap_ident`. Keduanya gagal sebelum
perbaikan (token pertama IDENT) dan lulus sesudahnya.

**Peran AI.** AI membantu. Verifikasi dengan `python -m pytest`: saat
AI keliru mengira `tests/test_tambahan.py` sudah punya `import pytest`,
error `NameError: name 'pytest' is not defined` muncul di output pytest,
lalu kami perbaiki sendiri dan tes hijau.

---

## Bug 2: Komentar blok `/* ... */` belum didukung (TODO T3)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Setiap file SQL yang memuat `/* ... */` langsung gagal di
lexer sebelum parser berjalan, dengan pesan
`LexError: Baris L, kolom K: komentar blok belum didukung`. Karena
hampir semua file SQL produksi memuat komentar blok sebagai dokumentasi,
seluruh pipeline terhenti untuk file-file tersebut.

**Reproduksi minimal.**

```sql
/* x */ SELECT 1;
```

**Akar masalah.** Cabang `if ch == "/" and self._peek() == "*":` di
`_scan_token()` berisi stub TODO(T3) yang sengaja melempar `LexError`
untuk setiap `/*`. Konsep penanganan komentar baris `//` di
*Crafting Interpreters* Bab 4 §4.6 (Longer Lexemes) belum diterapkan:
ketika scanner membaca `/`, ia tidak langsung memutuskan "ini operator
pembagian", tetapi melihat satu karakter ke depan untuk menentukan
apakah ini operator atau komentar. Pola yang sama berlaku untuk
`/* ... */`: deteksi awal, konsumsi sampai penutup, jangan panggil
`addToken` karena komentar tidak menghasilkan token (SPESIFIKASI 2.3).

**Perbaikan.** File `crud/lexer.py`, fungsi `_scan_token()`, cabang
`if ch == "/" and self._peek() == "*":`. Setelah mendeteksi `/*`,
scanner masuk ke `while True` dan mengonsumsi karakter demi karakter
sampai menemukan `*/`. Jika mencapai EOF sebelum penutup, lexer
melempar `LexError` di posisi `/*` pembuka, konsisten dengan cara
`_string()` melaporkan string tak tertutup. Alternatif yang
dipertimbangkan: memakai `str.find("*/")` untuk melompat ke penutup.
Tidak dipilih karena `str.find` tidak menaikkan `self.line` untuk
setiap `\n` di dalam komentar, sehingga baris token berikutnya akan
keliru (SPESIFIKASI 2.1).

**Test regresi.** `test_komentar_blok_didukung`,
`test_komentar_blok_lintas_baris`, dan
`test_komentar_blok_tidak_ditutup_error`. Semuanya gagal sebelum
perbaikan (`LexError`) dan lulus sesudahnya.

**Peran AI.** Kami menemukan bug saat menjalankan `python -m pytest`.
AI membantu menunjuk stub TODO(T3) sebagai lokasi dan mengusulkan blok
pengganti; kami mengetik dan memverifikasi dengan
`python -m pytest tests/test_tambahan.py -v` sampai tiga tes regresi
hijau.

---

## Bug 3: `<>` dipecah menjadi `<` dan `>`

**Ditemukan oleh:** Fadhil · **Diperbaiki oleh:** Fadhil

**Gejala.** Di `laporan_penjualan.sql` baris 6 kolom 41, token `<>`
terbaca sebagai `<` lalu `>`. SPESIFIKASI.md bagian 2.5 menyatakan
lexer selalu mengambil operator terpanjang yang cocok (*maximal
munch*): `<>` adalah satu token, bukan `<` lalu `>`.

**Reproduksi minimal.**

```sql
a <> b
```

**Akar masalah.** Lexer membaca `<`, lalu mengecek apakah karakter
berikutnya `=` (untuk `<=`). Karena bukan, ia memutuskan "ini `<`"
tanpa pernah mengecek apakah karakter berikutnya `>` (untuk `<>`).
Konsep yang dilanggar adalah *maximal munch* (Crafting Interpreters
Bab 4 §4.7): bila beberapa aturan leksikal cocok, aturan yang
mencocokkan karakter terbanyak menang, sehingga `<>` (2 karakter)
harus mengalahkan `<` (1 karakter). Lexer tidak menganggap ini salah
karena `<` dan `>` masing-masing token yang sah; kesalahan baru
terlihat di parser yang tidak menerima `>` berdiri sendiri di awal
ekspresi. Akarnya di lexer, gejalanya muncul di tahap berikutnya.

**Perbaikan.** File `crud/lexer.py`, fungsi `_scan_token()`, cabang
`<`. Ditambahkan pengecekan `elif self._peek() == ">": self._advance();
op = "<>"` sebelum jatuh ke `<`. Alternatif yang dipertimbangkan:
tabel operator dua karakter dan pencocokan dari yang terpanjang.
Tidak dipilih karena perubahan lebih besar dan gaya kode yang ada
sudah memakai `_match` untuk operator lain (`>=`, `!=`).

**Test regresi.** `test_operator_tidak_sama_satu_token`. Gagal sebelum
perbaikan (2 token, bukan 1) dan lulus sesudahnya.

**Peran AI.** AI membantu menunjuk lokasi bug dan mengusulkan
perbaikan tiga cabang. Kami mengetik perbaikan sendiri dan
memverifikasi dengan `python -m pytest`: pesan error `>` di baris 6
hilang dan tes regresi hijau.

---

## Bug 4: `INSERT ... SELECT` belum didukung (TODO T1)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Test bawaan
`tests/test_analyzer.py::test_matrix_laporan_penjualan` gagal dengan:

```
assert (None is None and [ParseError("...an 'SELECT'")] == [])
```

`data/sample/laporan_penjualan.sql` baris 10 memuat
`INSERT INTO ... SELECT ...`. Parser menolaknya, sehingga seluruh
statement setelahnya tidak dianalisis dan CRUD matrix file itu tidak
lengkap.

**Reproduksi minimal.**

```sql
INSERT INTO t (a) SELECT b FROM s;
```

**Akar masalah.** Stub TODO(T1) di `Parser._insert()` sengaja melempar
`ParseError` untuk cabang `SELECT`. Konsep yang belum diterapkan
adalah *recursive descent* (Crafting Interpreters Bab 6 §6.2): setiap
aturan grammar diterjemahkan menjadi satu method, dan aturan yang
punya beberapa alternatif diterjemahkan menjadi cabang `if/else` di
dalam method itu. SPESIFIKASI 3 mendefinisikan `insert_stmt` dengan
dua alternatif sumber data, `VALUES` dan `select_stmt`. Method
`_insert()` hanya menerjemahkan alternatif pertama dan melempar error
untuk alternatif kedua, padahal `_select()` yang dibutuhkan untuk
cabang kedua sudah ada dan bisa dipanggil langsung.

**Perbaikan.** File `crud/parser.py`, method `Parser._insert()`. Baris
`raise ParseError("INSERT ... SELECT belum didukung", self._peek())`
diganti dengan `query = self._select()` lalu
`return ast.Insert(table, columns, [], query, line=start.line)`.
Field `values` dikosongkan karena bentuk ini tidak punya baris
`VALUES`. Tidak ada perubahan di `ast_nodes.py` maupun `analyzer.py`:
`analyze_statement()` sudah memeriksa `stmt.query is not None` dan
menandai tabel di dalamnya `R`, sesuai SPESIFIKASI 5. Alternatif yang
ditolak: menambah field AST baru untuk membedakan `VALUES` dari
`SELECT` (mengubah API publik 7 tanpa manfaat), dan mem-*parse*
`SELECT` manual di dalam `_insert` (menduplikasi `_select()` dan
menyimpang dari pola *recursive descent* Bab 6).

**Test regresi.** `test_insert_select_didukung` dan
`test_insert_select_matrix_target_c_sumber_r`. Keduanya gagal sebelum
perbaikan (`parse_errors` tidak kosong) dan lulus sesudahnya.

**Peran AI.** AI hanya membantu memperbaiki bug. Lokasi ditemukan
sendiri dari traceback `test_matrix_laporan_penjualan` di pytest, dan
perbaikan diketik dengan merujuk SPESIFIKASI 3 dan 5 serta
*Crafting Interpreters* Bab 6 §6.2. AI merekomendasikan alternatif
yang kami tolak. Verifikasi dengan `python -m pytest`:
`test_matrix_laporan_penjualan` lulus dan dua tes regresi hijau.

---

## Bug 5: Subquery di UPDATE ditandai U, seharusnya R

**Ditemukan oleh:** Fadhil · **Diperbaiki oleh:** Fadhil

**Gejala.** Di `laporan_penjualan.sql`, tabel `pesanan` menghasilkan
operasi `RUD`, padahal seharusnya `RD`. Statement
`UPDATE ... WHERE id IN (SELECT ... FROM pesanan ...)` menandai
`pesanan` sebagai `U`. Menurut SPESIFIKASI bagian 5, tabel yang dibaca
lewat subquery selalu `R`, apa pun jenis statement luarnya.

**Reproduksi minimal.**

```sql
UPDATE pelanggan SET level = 'gold'
WHERE id IN (SELECT pelanggan_id FROM pesanan)
```

**Akar masalah.** `analyze_statement()` cabang `Update` meneruskan
operasi `"U"` ke seluruh ekspresi yang ditelusuri, termasuk subquery
di `WHERE`. Akibatnya tabel di dalam subquery ikut ditandai `"U"`
meskipun hanya dibaca. Aturan proyek (SPESIFIKASI 5) menyatakan
membaca tabel lewat subquery selalu `R`, apa pun jenis statement
luarnya. Operasi tabel target tidak boleh menular ke tabel lain di
dalam subquery.

**Perbaikan.** File `crud/analyzer.py`, fungsi `analyze_statement()`,
cabang `ast.Update`. Dua pemanggilan `_collect` untuk `SET` dan
`WHERE` diubah dari `"U"` menjadi `"R"`. Baris yang menandai tabel
target (`usage[stmt.table.name].add("U")`) tidak diubah. Alternatif
yang dipertimbangkan: menghapus parameter operasi di `_collect`
karena subquery di ekspresi selalu `R`. Tidak dipilih karena
perubahannya lebih besar dan cabang `Insert` dan `Delete` sudah
memakai pola yang sama dengan parameter `"R"`.

**Test regresi.** `test_subquery_di_update_adalah_read`. Gagal sebelum
perbaikan (`pesanan` bertanda `RUD`) dan lulus sesudahnya.

**Peran AI.** AI menjalankan statement `UPDATE` kecil di salinan
sementara untuk membuktikan sumber bug, menunjuk `analyzer.py`
baris 19 sampai 23 sebagai lokasi, dan mengusulkan penggantian `"U"`
menjadi `"R"`. Kami mengetik perbaikan sendiri dan memverifikasi
dengan `python -m pytest`.

---

## Bug 6: Kolom tanpa qualifier tidak di-resolve (TODO T2)

**Ditemukan oleh:** Fatih · **Diperbaiki oleh:** Fatih

**Gejala.** Test bawaan
`tests/test_resolver.py::test_kolom_tanpa_qualifier_satu_tabel` gagal
dengan:

```
assert {c.resolved for c in columns(script)} == {"pelanggan"}
E   AssertionError: assert {None} == {'pelanggan'}
E   Extra items in the left set:
E   None
E   Extra items in the right set:
E   'pelanggan'
```

Query `SELECT nama FROM pelanggan WHERE aktif = 1` punya satu tabel
pada scope terdalam (`pelanggan`), sehingga menurut SPESIFIKASI 4.3
kolom `nama` dan `aktif` harus di-resolve ke `"pelanggan"`. Kenyataannya
`ColumnRef.resolved` tetap `None` untuk keduanya.

**Reproduksi minimal.**

```sql
SELECT nama FROM pelanggan
```

**Akar masalah.** Cabang `if col.qualifier is not None:` di
`Resolver._column()` menangani kolom berqualifier, tetapi cabang
`col.qualifier is None` (kolom tanpa qualifier) hanya berisi `pass`
(stub TODO T2). Konsep yang belum diterapkan adalah pola resolver di
*Crafting Interpreters* Bab 11 §11.3.3 (Resolving variable
expressions): resolver menelusuri scope dari terdalam ke luar untuk
menemukan deklarasi yang cocok. Untuk kolom tanpa qualifier, pola
yang sama berlaku: resolver harus memeriksa scope terdalam dulu, lalu
memutuskan berdasarkan isinya (SPESIFIKASI 4.3). Stub saat ini
melewati seluruh langkah itu, sehingga `ColumnRef.resolved` tidak
pernah diisi.

**Perbaikan.** File `crud/resolver.py`, method `Resolver._column()`,
cabang `col.qualifier is None`. Isi `pass` diganti dengan membaca
`self.scope.entries` langsung, bukan `_lookup(...)`, karena
SPESIFIKASI 4.3 membatasi pandangan kolom tanpa qualifier pada scope
terdalam saja. Tiga kasus ditangani: nol entri memberi warning dan
`resolved` tetap `None`; lebih dari satu entri memberi warning
`kolom '<nama>' ambigu tanpa skema` dan `resolved` tetap `None`;
tepat satu entri mengisi `col.resolved` dengan
`_target_of(entries[0])`. Hasilnya, `SELECT nama FROM pelanggan`
menghasilkan `resolved = "pelanggan"`, sedangkan
`SELECT nama FROM pelanggan, pesanan` menghasilkan `None` plus
warning. Tiga alternatif ditolak. Memakai `_lookup(col.name)` ditolak
karena menelusuri scope ke luar, melanggar 4.3 yang hanya
mengizinkan scope terdalam. Mengisi `resolved` dengan string kosong
saat ambigu ditolak karena 4.3 menyatakan tetap `None`, dan
`analyzer.py` sudah memanfaatkan `None` itu. Melempar exception saat
ambigu ditolak karena 4.3 menyatakan kasus itu warning, bukan error;
exception akan menghentikan pipeline untuk query yang sintaksnya sah.

**Test regresi.** `test_kolom_tanpa_qualifier_satu_tabel_resolve` dan
`test_kolom_tanpa_qualifier_dua_tabel_ambigu`. Keduanya gagal sebelum
perbaikan (`resolved` tetap `None` dan warning tidak muncul) dan
lulus sesudahnya.

**Peran AI.** Kami menemukannya saat `python -m pytest`. AI membantu
menunjuk stub dan mengusulkan logika tiga kasus. Perbaikan yang
diambil membaca `self.scope.entries` langsung sesuai pasal.
Verifikasi dengan `python -m pytest`:
`test_kolom_tanpa_qualifier_satu_tabel` lulus, dua tes regresi hijau,
dan seluruh suite tetap hijau.

---

## Bug 7: `''` di dalam string terbaca sebagai dua token STRING

**Ditemukan oleh:** Fadhil · **Diperbaiki oleh:** Fadhil

**Gejala.** Input `'O''Brien'` menghasilkan dua token `STRING` (`O`
dan `Brien`), padahal SPESIFIKASI 2.4 menyatakan dua kutip
berturut-turut di dalam string mewakili satu karakter kutip, sehingga
hasil yang diharapkan satu token `STRING` bernilai `O'Brien`.
Dampaknya parser melihat dua string berurutan, menolak statement
`UPDATE ... SET nama = 'O''Neil'`, lalu panic mode membuang sisanya.
Di `data/sample/pemeliharaan.sql` ini membuat baris 8 (`UPDATE`)
hilang dari hasil. Bug ini tidak tertangkap tes lokal mana pun;
ketahuan dari `python evaluate.py` (FN
`('pemeliharaan.sql', 8, 'crm.pelanggan', 'U')`).

**Reproduksi minimal.**

```sql
SELECT 'O''Brien'
```

Sebelum perbaikan `tokenize` menghasilkan 2 token `STRING` (`O`,
`Brien`); sesudahnya 1 token `STRING` bernilai `O'Brien`.

**Akar masalah.** Lexer membaca string karakter demi karakter dan
berhenti pada kutip pertama yang ditemui. Ia tidak melihat karakter
sesudah kutip itu, sehingga tidak bisa membedakan kutip penutup dari
kutip yang di-escape (`''`). Akibatnya satu literal terpecah menjadi
dua lexeme. Konsep yang dilanggar: aturan lexing string literal
dengan escape, di mana lexer harus mengintip satu karakter ke depan
(lookahead) sebelum memutuskan lexeme berakhir (*Crafting
Interpreters* Bab 4, bagian string literal). Bug ada di lexer, bukan
parser: token yang dihasilkan sudah salah sejak awal, parser hanya
menampakkan gejalanya.

**Perbaikan.** File `crud/lexer.py`, fungsi `_string()`. Setelah
menemukan kutip, kami mengintip karakter berikutnya dengan
`self._peek()`: bila juga kutip, kami konsumsi kutip itu, menambahkan
satu `'` ke isi string, dan lanjut membaca; bila bukan, itu kutip
penutup dan loop berhenti. Alternatif yang dipertimbangkan:
menggabungkan dua `STRING` yang berurutan di parser. Tidak dipilih
karena parser tidak bisa membedakan `'O''Neil'` dari dua string yang
memang berurutan, dan aturan escape adalah urusan lexeme, jadi
tempatnya di lexer.

**Test regresi.** `test_kutip_ganda_dalam_string_satu_token`. Gagal
sebelum perbaikan (dua token) dan lulus sesudahnya.

**Peran AI.** AI menelusuri dari output `evaluate.py` bahwa FN baris 8
berasal dari `''`, lalu menunjuk `_string` dan mengusulkan perbaikan
intip-karakter. Kami mengetik perbaikannya sendiri dan memverifikasi
dengan perintah `tokenize` untuk `'O''Brien'` (hasil 2: satu `STRING`
plus `EOF`) dan `python evaluate.py` (FN baris 8 hilang).

---

## Bug 8: `LEFT OUTER JOIN` ditolak parser

**Ditemukan oleh:** Fadhil · **Diperbaiki oleh:** Fadhil

**Gejala.** `select ... from crm.pelanggan c left outer join
crm.alamat a on ...` (`pemeliharaan.sql` baris 5) ditolak dengan
pesan `diharapkan JOIN, ditemukan 'OUTER'`. SPESIFIKASI 3 menulis
grammar join sebagai `"LEFT" [ "OUTER" ] "JOIN"`, jadi `OUTER`
opsional dan input itu valid. Karena statement ditolak, `SELECT` di
baris 3 tidak masuk hasil (FN `('pemeliharaan.sql', 3,
'crm.pelanggan', 'R')` dan `crm.alamat`), dan panic mode menyebabkan
statement sesudahnya ikut terpengaruh.

**Reproduksi minimal.**

```sql
SELECT a.id FROM a LEFT OUTER JOIN b ON b.id = a.id
```

Sebelum perbaikan: 1 error parse, 0 statement. Sesudahnya: 0 error,
1 statement.

**Akar masalah.** Fungsi `_join()` mengonsumsi `LEFT`, lalu langsung
menuntut `JOIN` lewat `_expect_kw`. Bagian `[ "OUTER" ]` pada grammar
tidak pernah diterjemahkan ke kode, sehingga token `OUTER` tidak
dimakan dan `_expect_kw("JOIN")` gagal. Konsep: dalam *recursive
descent* (*Crafting Interpreters* Bab 6, bagian *recursive descent
parsing*), bagian opsional `[...]` pada grammar harus ditulis sebagai
pengecekan "kalau token ini ada, konsumsi; kalau tidak, lanjut".
Melupakannya membuat input yang valid menurut grammar ditolak
(*false rejection*).

**Perbaikan.** File `crud/parser.py`, fungsi `_join()`: menambah
`self._match_kw("OUTER")` tepat setelah `kind = "LEFT"`. Pemanggilan
`_match_kw` tidak melempar error bila `OUTER` tidak ada, sehingga
`LEFT JOIN` biasa tetap diterima. Alternatif yang dipertimbangkan:
membuat jenis join baru `LEFT OUTER`. Tidak dipilih karena maknanya
sama dengan `LEFT` dan cabang tambahan hanya menggandakan kode.

**Test regresi.** `test_left_outer_join_diterima`. Gagal sebelum
perbaikan (ada error parse) dan lulus sesudahnya.

**Peran AI.** AI menemukan bug ini saat mencocokkan label
`ground_truth.csv` dengan grammar 3, dan menunjuk `_join()` serta
baris yang perlu ditambah. Kami mengetik perubahan sendiri dan
memverifikasi dengan `python evaluate.py` (parser Precision 1.00,
Recall 1.00) serta `python -m pytest`.