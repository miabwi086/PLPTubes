"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""
import pytest;

from crud.parser import parse_sql
from crud.pipeline import analyze_source
from crud.lexer import LexError, TokenType as T, tokenize

def test_keyword_campuran_huruf_dinormalisasi_besar():
    # Regresi Bug 1: keyword harus tidak peka huruf besar/kecil (SPESIFIKASI 2.2)
    toks = tokenize("select Select SELECT")
    assert [t.type for t in toks[:3]] == [T.KEYWORD] * 3
    assert [t.value for t in toks[:3]] == ["SELECT"] * 3


def test_kata_berawalan_keyword_tetap_ident():
    # Kasus tepi: 'selection' hanya diawali keyword, harus tetap IDENT (SPESIFIKASI 2.2)
    toks = tokenize("selection fromage")
    assert [t.type for t in toks[:2]] == [T.IDENT, T.IDENT]


# regresi bug

def test_komentar_blok_didukung():
    # Regresi Bug 1 (TODO T3): /* ... */ tidak menghasilkan token (SPESIFIKASI 2.3)
    toks = tokenize("/* hi */ SELECT 1;")
    assert [t.type for t in toks] == [T.KEYWORD, T.NUMBER, T.SEMICOLON, T.EOF]


def test_komentar_blok_lintas_baris():
    # Kasus tepi: komentar blok boleh lintas baris; line token berikutnya harus akurat
    toks = tokenize("/* multi\n line */ SELECT 1;")
    assert toks[0].type is T.KEYWORD
    assert toks[0].line == 2


def test_komentar_blok_berisi_bintang():
    # Kasus tepi: '*' di dalam komentar bukan penutup; hanya '*/' yang menutup
    toks = tokenize("/* ** *** */ SELECT 1;")
    assert toks[0].type is T.KEYWORD
    assert toks[0].value == "SELECT"


def test_komentar_blok_tidak_bersarang():
    # Kasus tepi: '*/' pertama menutup (SPESIFIKASI 2.3: tidak bersarang)
    toks = tokenize("/* /* */ SELECT 1;")
    assert toks[0].type is T.KEYWORD
    assert toks[0].value == "SELECT"


def test_komentar_blok_tidak_ditutup_error():
    # Kasus tepi: komentar blok tidak ditutup -> LexError (SPESIFIKASI 2.3)
    with pytest.raises(LexError):
        tokenize("/* belum ditutup")


def test_komentar_baris_tetap_works():
    # Kasus tepi: perbaikan komentar blok tidak merusak komentar baris '--'
    toks = tokenize("-- ini komentar\nSELECT 1;")
    assert toks[0].type is T.KEYWORD
    assert toks[0].line == 2

def test_operator_tidak_sama_satu_token():
    # Regresi Bug 3: '<>' harus satu token OP (maximal munch, SPESIFIKASI 2.5)
    toks = tokenize("a <> b")
    assert [t.value for t in toks[:3]] == ["a", "<>", "b"]
    assert toks[1].type == T.OP

def test_insert_select_didukung():
    # Regresi Bug 2 (TODO T1): INSERT ... SELECT harus di-parse (SPESIFIKASI 3)
    script = parse_sql("INSERT INTO t (a) SELECT b FROM s;")
    assert script.errors == []
    assert len(script.statements) == 1


def test_insert_select_matrix_target_c_sumber_r():
    # Regresi Bug 2 (TODO T1): CRUD matrix INSERT ... SELECT (SPESIFIKASI 5)
    res = analyze_source("INSERT INTO t (a) SELECT b FROM s;")
    assert res.parse_errors == []
    assert res.matrix() == {"t": "C", "s": "R"}