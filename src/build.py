"""Build chapter quiz pages from src/chN.json.

Authoring convention: in each question, o[0] is the correct option and
x[i] explains why o[i+1] is wrong. The build shuffles question order and
option order with a fixed seed, balancing the correct letter across A-D.
"""
import base64, json, random, sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TEMPLATE = (SRC / "template.html").read_text(encoding="utf-8")
NEED = {"NB": 8, "TH": 15, "VD": 17, "VDC": 10}

CHAPTERS = {
    1: "Chiến lược & Kiến trúc dữ liệu hiện đại",
    2: "Mô hình hóa dữ liệu cho Cloud Warehousing",
    3: "Tích hợp dữ liệu và Pipeline tự động",
    4: "Tiền xử lý dữ liệu học thuật",
    5: "Thuật toán Khai thác dữ liệu cốt lõi",
    6: "In-Database Machine Learning và MLOps",
    7: "Quản trị, Bảo mật và Đạo đức dữ liệu",
    8: "Generative BI & AI-Driven Insights",
    9: "Tích hợp dữ liệu đa mô hình và Cơ sở dữ liệu hiện đại",
}


def validate(n, qs):
    errs, warns = [], []
    if len(qs) != 50:
        errs.append(f"có {len(qs)} câu, cần 50")
    cnt = {k: 0 for k in NEED}
    seen = set()
    for i, q in enumerate(qs, 1):
        for f in ("lv", "t", "q", "o", "w", "x", "trap", "mem"):
            if f not in q or q[f] in ("", None):
                errs.append(f"câu {i}: thiếu {f}")
        if q.get("lv") not in NEED:
            errs.append(f"câu {i}: lv sai {q.get('lv')}")
        else:
            cnt[q["lv"]] += 1
        if len(q.get("o", [])) != 4 or len(set(q.get("o", []))) != 4:
            errs.append(f"câu {i}: cần 4 phương án khác nhau")
        if len(q.get("x", [])) != 3:
            errs.append(f"câu {i}: cần 3 giải thích phương án sai")
        key = q.get("q", "")[:80]
        if key in seen:
            errs.append(f"câu {i}: trùng đề")
        seen.add(key)
        o = q.get("o", [])
        if len(o) == 4:
            lens = [len(s) for s in o]
            mean_d = sum(lens[1:]) / 3
            if lens[0] > 1.45 * mean_d and lens[0] - mean_d > 25:
                warns.append(f"câu {i}: đáp án đúng dài hơn hẳn ({lens[0]} vs {mean_d:.0f})")
        for o_ in o:
            low = o_.lower()
            if "tất cả" in low and "đều" in low or low.startswith("cả a") or "cả a và b" in low:
                errs.append(f"câu {i}: phương án cấm '{o_[:40]}'")
    for k, v in NEED.items():
        if cnt[k] != v:
            errs.append(f"mức {k}: {cnt[k]} câu, cần {v}")
    return errs, warns


def shuffle(n, qs):
    rng = random.Random(1000 + n)
    order = list(range(len(qs)))
    rng.shuffle(order)
    targets = [i % 4 for i in range(len(qs))]
    rng.shuffle(targets)
    out = []
    for slot, src in enumerate(order):
        q = qs[src]
        distract = [(q["o"][k + 1], q["x"][k]) for k in range(3)]
        rng.shuffle(distract)
        a = targets[slot]
        opts, xs = [], []
        d = iter(distract)
        for pos in range(4):
            if pos == a:
                opts.append(q["o"][0]); xs.append("")
            else:
                o_, x_ = next(d); opts.append(o_); xs.append(x_)
        out.append({"lv": q["lv"], "t": q["t"], "q": q["q"], "o": opts, "a": a,
                    "w": q["w"], "x": xs, "trap": q["trap"], "mem": q["mem"]})
    return out


SPECIAL = {"ontap": (99, "Ôn tập trọng tâm: 40 chủ đề trong đề ôn tập", "on-tap.html")}


def build(n):
    if n in SPECIAL:
        seed, title, outname = SPECIAL[n]
        data = json.loads((SRC / f"{n}.json").read_text(encoding="utf-8"))
    else:
        seed, title, outname = n, f"Chương {n}: {CHAPTERS[n]}", f"chuong-{n}.html"
        data = json.loads((SRC / f"ch{n}.json").read_text(encoding="utf-8"))
    qs = data["questions"]
    errs, warns = validate(n, qs)
    for w in warns:
        print(f"  [cảnh báo] Ch{n} {w}")
    if errs:
        print(f"Ch{n} LỖI:\n  " + "\n  ".join(errs))
        return False
    out = shuffle(seed, qs)
    dist = [sum(1 for q in out if q["a"] == k) for k in range(4)]
    payload = base64.b64encode(json.dumps(out, ensure_ascii=False).encode("utf-8")).decode("ascii")
    page = (TEMPLATE.replace("__TITLE__", html.escape(title))
            .replace("__KEY__", f"dwquiz-{n if n in SPECIAL else 'ch' + str(n)}-v1")
            .replace("__DATA__", payload))
    (ROOT / outname).write_text(page, encoding="utf-8")
    print(f"Ch{n} OK · 50 câu · đáp án A/B/C/D = {dist}")
    return True


def index():
    built = [n for n in CHAPTERS if (ROOT / f"chuong-{n}.html").exists()]
    items = "\n".join(
        f'<a class="ch" href="chuong-{n}.html"><span class="n">{n}</span><span><b>Chương {n}</b><br>{html.escape(t)}</span></a>'
        if n in built else
        f'<div class="ch off"><span class="n">{n}</span><span><b>Chương {n}</b><br>{html.escape(t)}<br><i>Đang soạn</i></span></div>'
        for n, t in CHAPTERS.items())
    page = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ôn tập Nhà kho dữ liệu</title>
<style>
:root{{--bg:#f4f6fb;--card:#fff;--ink:#1f2937;--muted:#6b7280;--line:#e5e7eb;--brand:#1d4ed8;--soft:#e0e7ff}}
@media (prefers-color-scheme: dark){{:root{{--bg:#0f172a;--card:#111827;--ink:#e5e7eb;--muted:#9ca3af;--line:#1f2937;--brand:#60a5fa;--soft:#1e3a8a}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Times New Roman",Times,serif;font-size:13pt}}
.wrap{{max-width:860px;margin:0 auto;padding:24px 16px 50px}}
h1{{font-size:20pt;margin:0 0 4px}} p.sub{{color:var(--muted);margin:0 0 18px;font-family:"Segoe UI",Arial,sans-serif;font-size:11pt}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}
.ch{{display:flex;gap:12px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;color:var(--ink);text-decoration:none;transition:border-color .15s,transform .15s}}
a.ch:hover{{border-color:var(--brand);transform:translateY(-2px)}}
.ch .n{{flex:none;width:36px;height:36px;border-radius:50%;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-family:"Segoe UI",Arial,sans-serif}}
.ch.off{{opacity:.55}} .ch i{{color:var(--muted);font-size:10.5pt}}
.note{{margin-top:22px;font-size:10.5pt;color:var(--muted);font-family:"Segoe UI",Arial,sans-serif;line-height:1.6}}
</style></head><body><div class="wrap">
<h1>Ôn tập Nhà kho dữ liệu và tích hợp</h1>
<p class="sub">Trắc nghiệm 50 câu mỗi chương · Nhận biết 8 · Thông hiểu 15 · Vận dụng 17 · Vận dụng cao 10</p>
<a class="ch" href="on-tap.html" style="margin-bottom:14px"><span class="n">★</span><span><b>Trắc nghiệm ôn tập trọng tâm</b><br>50 câu xoay quanh 40 chủ đề trong đề ôn tập · <span style="white-space:nowrap">kèm <u>bảng đáp án tự luận</u></span></span></a>
<div class="grid">
{items}
</div>
<div class="note">Mỗi câu khóa lựa chọn ngay khi trả lời và hiện lời giải chi tiết. Tiến độ được lưu trên trình duyệt của bạn.
Sau khi xong có thể chọn “Làm lại câu sai” hoặc “Làm lại toàn bộ”. Nội dung soạn theo slide và tài liệu giảng giải của học phần.</div>
</div></body></html>"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    nums = [a if a in SPECIAL else int(a) for a in sys.argv[1:]] or ([n for n in CHAPTERS if (SRC / f"ch{n}.json").exists()] + list(SPECIAL))
    ok = all([build(n) for n in nums])
    index()
    sys.exit(0 if ok else 1)
