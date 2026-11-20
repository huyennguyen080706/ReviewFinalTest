"""Sinh đề thi thử 5–10 (src/de5.json … de10.json) từ ngân hàng câu pool_c1_3/4_6/7_9.

Trong file pool, mỗi chủ đề là một khối câu bắt đầu bằng dòng chú thích "# ---" (≤ 6 câu,
các câu cùng khối hỏi cùng một ý theo cách khác nhau). Ràng buộc khi chia đề:
  * mỗi đề có đúng len(chương)/6 câu của mỗi chương (4,4,5,5,6,5,4,3,4 = 40 câu);
  * hai câu cùng khối chủ đề không bao giờ nằm chung một đề.
Bắt đầu từ cách chia vòng tròn (câu j → đề j % 6), sau đó đổi chỗ câu cùng chương giữa
các đề (seed cố định) để số câu từng mức độ ở 6 đề sát nhau nhất.
Chạy: python de_gen2.py  →  rồi python build.py de5 de6 de7 de8 de9 de10
"""
import json
import pathlib
import random
import re
from collections import Counter

from pool_c1_3 import CH1, CH2, CH3
from pool_c4_6 import CH4, CH5, CH6
from pool_c7_9 import CH7, CH8, CH9

SRC = pathlib.Path(__file__).resolve().parent
POOLS = [CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9]
NAMES = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "CH9"]
FILES = ["pool_c1_3.py"] * 3 + ["pool_c4_6.py"] * 3 + ["pool_c7_9.py"] * 3
N_EXAM = 6
LV = ("NB", "TH", "VD", "VDC")


def blocks(fname, var, n):
    """Số khối chủ đề cho từng câu của danh sách var, đọc từ các dòng '# ---' trong file."""
    src = (SRC / fname).read_text(encoding="utf-8")
    body = src[src.index(f"\n{var} = ["):]
    body = body[:body.index("\n]\n")]
    out, b = [], -1
    for line in body.splitlines():
        if line.strip().startswith("# ---"):
            b += 1
        elif line.startswith("    Q("):
            out.append(b)
    assert len(out) == n and min(out) >= 0, (var, len(out), n)
    return out


for i, p in enumerate(POOLS, 1):
    assert len(p) % N_EXAM == 0, f"Chương {i}: {len(p)} câu, phải chia hết cho {N_EXAM}"
allq = [q for p in POOLS for q in p]
dup = [k for k, v in Counter(q["q"] for q in allq).items() if v > 1]
assert not dup, dup

# items: (chương, khối, mức) ; asg[i] = đề của câu i
items, asg = [], []
for c, (p, name, f) in enumerate(zip(POOLS, NAMES, FILES)):
    bl = blocks(f, name, len(p))
    assert max(Counter(bl).values()) <= N_EXAM, name
    for j, q in enumerate(p):
        items.append((c, bl[j], q["lv"]))
        asg.append(j % N_EXAM)
total = Counter(lv for _, _, lv in items)
target = {k: total[k] / N_EXAM for k in LV}


def cost(a):
    cnt = [Counter() for _ in range(N_EXAM)]
    for (_, _, lv), e in zip(items, a):
        cnt[e][lv] += 1
    return sum((cnt[e][k] - target[k]) ** 2 for e in range(N_EXAM) for k in LV)


def valid(a):
    seen = set()
    for (c, b, _), e in zip(items, a):
        if (c, b, e) in seen:
            return False
        seen.add((c, b, e))
    return True


assert valid(asg)
rng = random.Random(2026)
best = cost(asg)
by_ch = {}
for i, (c, _, _) in enumerate(items):
    by_ch.setdefault(c, []).append(i)
for _ in range(40000):
    c = rng.randrange(len(POOLS))
    i, j = rng.sample(by_ch[c], 2)
    if asg[i] == asg[j] or items[i][2] == items[j][2]:
        continue
    asg[i], asg[j] = asg[j], asg[i]
    if valid(asg):
        new = cost(asg)
        if new <= best:
            best = new
            continue
    asg[i], asg[j] = asg[j], asg[i]
assert valid(asg)

exams = [[] for _ in range(N_EXAM)]
for q, e in zip(allq, asg):
    exams[e].append(q)
for e, qs in enumerate(exams, 5):
    lv = Counter(q["lv"] for q in qs)
    ch = Counter(q["t"][-3:-1] for q in qs)
    print(f"de{e}: {len(qs)} câu · " + " · ".join(f"{k} {lv[k]}" for k in LV)
          + " · theo chương " + ",".join(str(ch[f"C{k}"]) for k in range(1, 10)))
    (SRC / f"de{e}.json").write_text(json.dumps({"questions": qs}, ensure_ascii=False, indent=1), encoding="utf-8")
