# Laporan Akhir

## 1. Hasil evaluasi

Keluaran `python evaluate.py` setelah `data/ground_truth.csv` dilengkapi (27 triple, 4 file).
Label `audit.sql` dan `pemeliharaan.sql` dibuat manual dari SPESIFIKASI 5 dan 8, bukan disalin
dari keluaran tool.

```text
Dievaluasi: audit.sql, campuran_error.sql, laporan_penjualan.sql, pemeliharaan.sql
(27 triple)
Metode Precision Recall F1
parser  1.00 1.00 1.00
regex   0.65 0.81 0.72
[regex]
 salah ditemukan (FP): ('audit.sql', 16, 'sesi', 'R')
 salah ditemukan (FP): ('campuran_error.sql', 4, 'pesanan', 'R')
 salah ditemukan (FP): ('campuran_error.sql', 8, 'keranjang', 'R')
 salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'D')
 salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'R')
 salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pesanan', 'R')
 salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'rahasia', 'R')
 salah ditemukan (FP): ('laporan_penjualan.sql', 15, 'pesanan', 'R')
 salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.alamat', 'R')
 salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.pelanggan', 'R')
 salah ditemukan (FP): ('pemeliharaan.sql', 2, 'pelanggan_lama', 'U')
 salah ditemukan (FP): ('pemeliharaan.sql', 15, 'crm.alamat', 'R')
 terlewat (FN): ('audit.sql', 2, 'pesanan', 'R')
 terlewat (FN): ('laporan_penjualan.sql', 3, 'pelanggan', 'R')
 terlewat (FN): ('laporan_penjualan.sql', 3, 'pesanan', 'R')
 terlewat (FN): ('pemeliharaan.sql', 3, 'crm.alamat', 'R')
 terlewat (FN): ('pemeliharaan.sql', 3, 'crm.pelanggan', 'R')
```

Blok `[parser]` kosong: tidak ada FP maupun FN. Catatan: evaluasi ini hanya mengukur level
(file, baris, tabel, operasi), jadi tidak menguji presedensi `AND`/`OR` maupun urutan scope
alias; keduanya diperiksa lewat tes dan pembacaan kode.

## 2. Tiga kasus di mana regex salah

**Kasus 1: perintah di dalam komentar (`laporan_penjualan.sql` baris 2).**

```sql
-- DELETE FROM pelanggan   (baris ini komentar, bukan perintah)
SELECT p.nama, SUM(o.total) AS omzet
FROM pelanggan p
JOIN pesanan o ON o.pelanggan_id = p.id
```

Regex memotong teks di tiap `;`, lalu mencari kata `SELECT/INSERT/UPDATE/DELETE` pertama sebagai
awal statement. Kata `DELETE` di dalam komentar yang ditemukan lebih dulu, sehingga statement
dianggap mulai di baris 2, bukan baris 3. Akibatnya ada empat temuan palsu di baris 2 (termasuk
`pelanggan, D`, padahal tidak ada penghapusan) dan dua temuan benar di baris 3 yang terlewat
(`pelanggan, R` dan `pesanan, R`). Parser benar karena lexer membuang komentar sebelum parsing:
komentar adalah lexeme yang dikonsumsi lalu dibuang, tidak pernah menjadi token (Crafting
Interpreters bab 4, Scanning, bagian komentar). Parser tidak pernah melihat kata `DELETE` itu,
dan nomor baris statement diambil dari token `SELECT` yang asli. Regex bekerja pada teks mentah
sehingga tidak bisa membedakan kode dari komentar.

**Kasus 2: kata kunci di dalam string literal (`laporan_penjualan.sql` baris 6).**

```sql
WHERE o.status = 'LUNAS' AND o.catatan <> 'FROM rahasia'
```

Pola `FROM <nama>` pada regex cocok dengan isi string, sehingga `rahasia` dilaporkan sebagai tabel
yang dibaca (`rahasia, R`). Tabel itu tidak ada. Lexer membaca `'FROM rahasia'` sebagai satu token
`STRING` utuh (SPESIFIKASI 2.4), jadi `FROM` di dalamnya hanyalah isi teks, bukan keyword. Ini
inti pemisahan lexing dari parsing: keputusan "ini keyword atau data" dibuat sekali di lexer,
lewat aturan bahwa isi string dibaca sampai kutip penutup. Regex tidak punya konsep token.

**Kasus 3: konteks tata bahasa, `FROM` setelah `DELETE` (`laporan_penjualan.sql` baris 15).**

```sql
DELETE FROM pesanan WHERE tanggal < :batas;
```

Regex punya pola `\bFROM\s+nama` (untuk membaca) dan `\bDELETE\s+FROM\s+nama` (untuk menghapus).
Pada statement ini kedua pola cocok, jadi `pesanan` dilaporkan `R` dan `D`, padahal kebenarannya
hanya `D` (FP: `('laporan_penjualan.sql', 15, 'pesanan', 'R')`). Regex tidak tahu bahwa `FROM`
di sini adalah bagian dari produksi `DELETE FROM tabel`, bukan klausa `FROM` milik `SELECT`.
Parser memakai grammar: `FROM` setelah `DELETE` dikonsumsi oleh aturan `delete_statement` dan
tabelnya menjadi target, sedangkan klausa `FROM` hanya ada di dalam aturan `select`. Makna
sebuah kata ditentukan oleh posisinya dalam struktur, dan struktur itulah yang dibangun parser
sebagai AST.

Kasus lain yang terlihat di keluaran dan menguatkan poin yang sama: pada `campuran_error.sql`
baris 4 (`SELECT id nama, FROM pesanan` yang rusak) regex tetap melaporkan `pesanan, R`,
sedangkan parser menolak statement itu lewat panic mode dan tidak menghitungnya (SPESIFIKASI
5 dan 6).

## 3. Batas pendekatan kami

Semua batas di bawah tetap ada walau semua bug sudah diperbaiki. Contoh 2 sampai 4 diuji pada
kode kami dan hasilnya dicantumkan.

1. **Tanpa skema database, kolom tanpa qualifier tidak bisa dikaitkan ke tabel bila ada lebih
   dari satu tabel.**
   `SELECT nama FROM pelanggan p, pesanan o`: kolom `nama` bisa milik `pelanggan` atau
   `pesanan`. Sesuai SPESIFIKASI 4.3 resolver memberi peringatan "ambigu" dan `resolved` tetap
   `None`. Akibatnya: matriks CRUD tingkat tabel tetap benar (keduanya `R`), tetapi informasi
   tingkat kolom (`columns`) tidak lengkap, jadi tool tidak bisa menjawab "kolom mana milik
   tabel mana". Informasi yang dibutuhkan: definisi kolom setiap tabel (DDL atau katalog
   database).
2. **Konstruksi di luar grammar: `WITH`, `UNION`, `MERGE`, dan pemanggilan prosedur
   (SPESIFIKASI 9).** Kami menjalankan beberapa contoh, dan hasilnya selalu error parse
   sehingga seluruh statement tidak masuk matriks:
   `WITH t AS (SELECT id FROM pesanan) SELECT id FROM t` ditolak di kata `WITH`;
   `SELECT id FROM a UNION SELECT id FROM b` ditolak di `UNION` (kolom 24);
   `MERGE INTO a USING b ...` dan `EXEC sp_hapus` ditolak di kata pertama.
   Akibatnya tabel `pesanan`, `a`, `b` yang sebenarnya dibaca tidak tercatat sama sekali
   (false negative). Informasi yang dibutuhkan: perluasan grammar (CTE, operator himpunan,
   `MERGE`) dan aturan resolusinya, misalnya nama CTE adalah scope sementara, bukan tabel.
3. **View, trigger, dan stored procedure tidak terlihat.**
   `SELECT * FROM v_laporan` dilaporkan sebagai tabel `v_laporan` dengan operasi `R` (kami
   uji), padahal itu mungkin view atas beberapa tabel dasar. Begitu pula `INSERT INTO pesanan`
   bisa memicu trigger yang mengubah `log_pesanan`, yang tidak tertulis di teks query. Akibatnya
   matriks salah menghitung nama objek (view dianggap tabel) dan tidak melihat efek samping
   (tabel yang dimodifikasi trigger terlewat). Informasi yang dibutuhkan: definisi view dan
   trigger dari katalog database, lalu perluas matriks lewat dependensi.
4. **SQL dinamis dan SQL yang dirangkai di kode aplikasi.**
   `query = "DELETE FROM " + nama_tabel` di kode Python atau PHP tidak ada di berkas `.sql`
   yang dibaca, dan nama tabelnya baru diketahui saat program berjalan. Akibatnya operasi itu
   tidak muncul di matriks. Informasi yang dibutuhkan: analisis kode aplikasi (data-flow) atau
   log query nyata dari database saat runtime.

## 4. Pembagian kerja

Kami memakai pair programming murni: tidak ada pembagian modul, dan peran Driver dan Navigator
bergantian sekitar tiap 30 menit. Pada praktiknya pekerjaan terbagi berikut (sesuai riwayat
kerja dan log AI):

- **Fadhil:** Bug 1 (keyword huruf kecil), Bug 3 (`<>` terpecah di lexer), Bug 5 (subquery
  `UPDATE` bertanda `U`), Bug 7 (`''` di dalam string terbaca dua token), Bug 8 (`LEFT OUTER
  JOIN` ditolak parser), `_synchronize` (panic mode), serta pelabelan `ground_truth.csv`.

- **Fatih:** Bug 2 (komentar blok, TODO T3), Bug 4 (`INSERT ... SELECT`, TODO T1), dan Bug 6
  (resolusi kolom tanpa qualifier, TODO T2).

Cara memastikan keduanya paham seluruh kode: [ISI DENGAN YANG BENAR-BENAR DILAKUKAN. Contoh yang
sesuai riwayat: sebelum bergantian Driver, Navigator menjelaskan ulang bug yang baru
diperbaiki (misalnya Bug 2 dijelaskan ke Fadhil sebelum giliran Fadhil mengetik); setiap
selesai satu bug kami menjalankan `python -m pytest` bersama, dan 44 tes lulus di akhir.
Tambahkan hanya latihan demo lisan atau penelusuran pipeline tanpa melihat kode kalau memang
sudah dilakukan.]
