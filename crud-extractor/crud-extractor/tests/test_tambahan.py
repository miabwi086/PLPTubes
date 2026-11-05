"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""
from crud.lexer import TokenType as T, tokenize

def test_keyword_campuran_huruf_dinormalisasi_besar():
    # Regresi Bug 1: keyword harus tidak peka huruf besar/kecil (SPESIFIKASI 2.2)
    toks = tokenize("select Select SELECT")
    assert [t.type for t in toks[:3]] == [T.KEYWORD] * 3
    assert [t.value for t in toks[:3]] == ["SELECT"] * 3


def test_kata_berawalan_keyword_tetap_ident():
    # Kasus tepi: 'selection' hanya diawali keyword, harus tetap IDENT (SPESIFIKASI 2.2)
    toks = tokenize("selection fromage")
    assert [t.type for t in toks[:2]] == [T.IDENT, T.IDENT]