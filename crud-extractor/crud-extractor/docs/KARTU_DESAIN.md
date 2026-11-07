# Kartu Desain

Tuliskan lima keputusan desain penting dalam pekerjaan kalian. Untuk tiap keputusan, sebutkan
alternatif yang ditolak dan alasannya. Contoh topik (boleh memilih yang lain):

- bagaimana parser membedakan `*` sebagai "semua kolom" dan sebagai perkalian;
- di mana dan bagaimana presedensi `AND`/`OR` dinyatakan;
- mengapa error recovery berhenti di `;`, bukan di keyword `SELECT` berikutnya;
- urutan pencarian scope dan akibatnya pada shadowing serta correlated subquery;
- mengapa kolom tanpa qualifier hanya dilihat di scope terdalam, dan apa kelemahannya;
- bagaimana implementasi `INSERT ... SELECT` atau komentar blok kalian.

| No | Keputusan | Alternatif yang ditolak | Alasan |
| --- | --- | --- | --- |
| 1 | Kami menormalisasi keyword dengan `.upper()` di lexer sebelum mencocokkan ke tabel reserved word. | Memasukkan semua kombinasi huruf besar dan kecil ke tabel reserved word. | Jumlah kombinasi tumbuh cepat dan sulit dirawat. Normalisasi sekali di lexer lebih sederhana dan sesuai SPESIFIKASI bagian 2.2. |
| 2 | Lexer memproses komentar blok `/* ... */` tanpa menghasilkan token. Scanner membaca sampai `*/` dan melempar `LexError` di posisi `/*` jika mencapai EOF. | Menghasilkan token `COMMENT` lalu membuangnya di parser, atau memakai regex sebelum lexer. | Komentar bukan token yang dibutuhkan parser. Regex terpisah lebih rawan untuk komentar lintas baris dan pelacakan posisi. Pola ini mengikuti *Crafting Interpreters* Bab 4 tentang scanner yang melihat karakter berikutnya sebelum memutuskan. |
| 3 | Kami menerapkan maximal munch untuk `<>` dengan mengecek `>` setelah `<`. | Membuat tabel operator dua karakter dan mencocokkan dari yang terpanjang. | Perubahan tabel lebih besar. Gaya kode yang ada sudah memakai `_match` untuk operator lain seperti `>=` dan `!=`. |
| 4 | Kami mengimplementasikan `INSERT ... SELECT` dengan memanggil `self._select()` di dalam `Parser._insert()`, lalu membungkus hasilnya menjadi `ast.Insert` dengan `values` kosong. | Menambah field AST baru untuk membedakan `VALUES` dan `SELECT`, atau mem-parsing `SELECT` manual di `_insert()`. | Field AST baru mengubah API publik tanpa manfaat. Parsing manual menduplikasi `_select()` dan menyimpang dari recursive descent. |
| 5 | Kami hanya me-resolve kolom tanpa qualifier di scope terdalam. Cabang `qualifier is None` membaca `self.scope.entries`: nol entri menghasilkan warning, lebih dari satu menghasilkan warning ambigu, tepat satu mengisi `resolved`. | Memakai `_lookup()` yang menelusuri scope ke luar, mengisi `resolved` dengan string kosong saat ambigu, atau melempar exception. | SPESIFIKASI bagian 4.3 membatasi kolom tanpa qualifier pada scope terdalam. String kosong tidak sesuai karena spec menyatakan `None`. Exception salah karena kasus ambigu adalah warning. |
