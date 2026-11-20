"""Tiện ích dùng chung cho bộ sinh đề thi thử 5–10 (de_gen2.py và các file pool_*.py).

Quy ước như build.py: o[0] là đáp án đúng, x[i] giải thích vì sao o[i+1] sai.
"""
from fractions import Fraction as Fr


def num(x, nd=4):
    """Số thập phân kiểu Việt Nam (dấu phẩy), bỏ số 0 thừa."""
    if isinstance(x, Fr):
        x = float(x)
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace(".", ",")


def Q(lv, t, q, o, x, w, trap, mem):
    assert lv in ("NB", "TH", "VD", "VDC"), (t, lv)
    assert len(o) == 4 and len(set(o)) == 4, (t, o)
    assert len(x) == 3, t
    return {"lv": lv, "t": t, "q": q, "o": o, "w": w, "x": x, "trap": trap, "mem": mem}


def table(header, rows):
    h = "".join(f"<th>{c}</th>" for c in header)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{b}</table>"
