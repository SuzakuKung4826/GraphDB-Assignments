"""
Graph Database Assignments Hub
เว็บรวมการบ้านและโปรเจกต์วิชา Graph Database ของ นายจิรภัทร จันทร์มล (664245026)

วิธีเพิ่มการบ้านชิ้นใหม่: เพิ่ม dict ใหม่ลงใน ASSIGNMENTS ด้านล่าง แล้ว push ขึ้น GitHub
"""
from __future__ import annotations

import base64
import html
import re
from functools import lru_cache
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Graph DB Assignments · 664245026",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).parent
GH = "https://github.com/SuzakuKung4826"
MANGA_REPO = f"{GH}/MangaGraph"
NB = f"{MANGA_REPO}/blob/main/homework"
COLAB = "https://colab.research.google.com/github/SuzakuKung4826/MangaGraph/blob/main/homework"
HUB_REPO = f"{GH}/GraphDB-Assignments"
REPORTS = f"{HUB_REPO}/blob/main/reports"

STUDENT = {
    "name": "นายจิรภัทร จันทร์มล",
    "id": "664245026",
    "section": "66/43",
    "school": "มหาวิทยาลัยราชภัฏนครปฐม",
}

# ---------------------------------------------------------------------------
# ข้อมูลการบ้าน — เพิ่ม/แก้ตรงนี้ที่เดียว
#   kind   : "hw" = การบ้าน, "project" = โปรเจกต์
#   image  : ไฟล์ใน assets/ (ถ้าไม่มี ใส่ code แทนเพื่อโชว์ตัวอย่างโค้ด)
#   status : "live" = ส่งแล้ว/ออนไลน์, "soon" = กำลังทำ
# ---------------------------------------------------------------------------
ASSIGNMENTS = [
    {
        "no": "HW 01",
        "kind": "hw",
        "title": "Assignment 1 — วิเคราะห์ Workload เพื่อเลือกฐานข้อมูล",
        "tag": "Data Modeling · Polyglot",
        "status": "live",
        "image": "a1.jpg",
        "desc": "เลือกฐานข้อมูลให้เหมาะกับ workload 5 ระบบ เทียบ Table กับ Graph ออกแบบ Social Graph "
                "สำหรับ Mini Project และวิเคราะห์ 3 แอปพลิเคชันแบบ Polyglot Persistence",
        "learned": ["Relational / Document / Graph", "SQL JOIN vs Cypher", "ออกแบบ Social Graph",
                    "Polyglot Persistence"],
        "links": [
            ("📄 ดูรายงาน (PDF)", f"{REPORTS}/Assignment1_664245026.pdf"),
        ],
    },
    {
        "no": "HW 02",
        "kind": "hw",
        "title": "Assignment 2 — Transaction, Concurrency & Recovery",
        "tag": "MySQL · InnoDB",
        "status": "live",
        "image": None,
        "code": (
            "START TRANSACTION;\n"
            "SELECT * FROM posts\n"
            "  WHERE post_id = %s FOR UPDATE;\n"
            "INSERT INTO reports VALUES (...);\n"
            "UPDATE posts SET report_count =\n"
            "  report_count + 1;  COMMIT;"
        ),
        "desc": "Lab สัปดาห์ที่ 2 ทดลองบน MySQL ผ่าน Python: dirty read, atomic transaction, "
                "autocommit vs explicit, deadlock + retry, isolation level และ redo/undo log",
        "learned": ["ACID", "Locking + MVCC", "Isolation Level", "Deadlock & Retry", "Redo / Undo"],
        "links": [
            ("📂 เปิดใน Google Drive", "https://drive.google.com/file/d/1-LYLigMgURWqnDd925X0xamGXVh8Tuh6/view?usp=sharing"),
            ("📄 ดูรายงาน (PDF)", f"{REPORTS}/Assignment2_664245026.pdf"),
        ],
    },
    {
        "no": "HW 03",
        "kind": "hw",
        "title": "Club System — ระบบแนะนำหนังสือและชมรมด้วย Cypher",
        "tag": "Neo4j · Cypher",
        "status": "live",
        "image": "club.jpg",
        "desc": "สร้างกราฟนักเรียน หนังสือ หมวดหนังสือ และชมรมบน Neo4j แล้วใช้ traversal 1–2 hop "
                "ผ่าน FRIEND_OF แนะนำหนังสือและชมรมที่เพื่อนเป็นสมาชิก",
        "learned": ["CREATE CONSTRAINT", "Traversal 1–2 hop", "count(DISTINCT)", "WHERE NOT EXISTS"],
        "links": [
            ("📄 ดูรายงาน (PDF)", f"{REPORTS}/664245026_Club_System.pdf"),
        ],
    },
    {
        "no": "HW 04",
        "kind": "hw",
        "title": "Manga Recommender ด้วย NetworkX",
        "tag": "NetworkX · Python",
        "status": "live",
        "image": "hw1.jpg",
        "desc": "สร้างกราฟผู้ใช้ 10 คน กับมังงะ/มังฮวา 20 เรื่อง ด้วย NetworkX "
                "แล้วแนะนำเรื่องใหม่จากผู้ใช้ที่ชอบเรื่องเดียวกัน (collaborative filtering บนกราฟ)",
        "learned": ["สร้าง Node / Edge", "หาเพื่อนบ้านในกราฟ", "นับเส้นทาง 3 ขั้น", "วาดกราฟด้วย matplotlib"],
        "links": [
            ("📓 ดูโน้ตบุ๊กบน GitHub", f"{NB}/HW1_Manga_Recommender_NetworkX.ipynb"),
            ("▶ เปิดใน Google Colab", f"{COLAB}/HW1_Manga_Recommender_NetworkX.ipynb"),
        ],
    },
    {
        "no": "HW 05",
        "kind": "hw",
        "title": "Manga Recommender ด้วย Neo4j Aura",
        "tag": "Neo4j · Cypher",
        "status": "live",
        "image": None,
        "code": (
            "MATCH (me:User {name:'Bank'})\n"
            "  -[:LIKES]->()<-[:LIKES]-(o:User)\n"
            "  -[:LIKES]->(rec:Manga)\n"
            "WHERE NOT (me)-[:LIKES]->(rec)\n"
            "RETURN rec.title, count(*) AS score\n"
            "ORDER BY score DESC LIMIT 5"
        ),
        "desc": "ย้ายข้อมูลชุดเดียวกันขึ้น Neo4j Aura เชื่อมต่อด้วย Python Driver "
                "ใช้ความสัมพันธ์ LIKES และ BE_FRIEND แล้วเขียน Cypher แนะนำมังงะ",
        "learned": ["MERGE ข้อมูลลง Neo4j", "Cypher pattern matching", "BE_FRIEND ระหว่างผู้ใช้",
                    "ทำ query เป็น Python function"],
        "links": [
            ("📓 ดูโน้ตบุ๊กบน GitHub", f"{NB}/HW2_Manga_Recommender_Neo4j.ipynb"),
            ("▶ เปิดใน Google Colab", f"{COLAB}/HW2_Manga_Recommender_Neo4j.ipynb"),
        ],
    },
    {
        "no": "FINAL",
        "kind": "project",
        "title": "MangaGraph — เว็บแนะนำมังงะด้วย Graph Database",
        "tag": "Streamlit · Neo4j Aura",
        "status": "live",
        "image": "project.jpg",
        "desc": "เว็บไซต์แนะนำมังงะพร้อมภาพปก ให้คะแนนแบบ Hybrid 5 สัญญาณ อธิบายเหตุผลได้ทุกเรื่อง "
                "กดชอบแล้วบันทึกลง Neo4j ทันที และวาดเส้นทางในกราฟที่ทำให้เกิดคำแนะนำ",
        "learned": ["Hybrid explainable score", "กราฟโต้ตอบ (vis-network)", "CRUD ผ่านเว็บ",
                    "Deploy Streamlit Cloud"],
        "links": [
            ("🚀 เปิดเว็บระบบ (Streamlit)", "https://mangagraph-664245026.streamlit.app"),
            ("📊 PowerPoint นำเสนอ", f"{MANGA_REPO}/blob/main/slides/MangaGraph_Presentation.pptx"),
            ("💻 Source code (GitHub)", MANGA_REPO),
            ("🏠 หน้าสรุปโปรเจกต์", "https://suzakukung4826.github.io/MangaGraph/"),
        ],
    },
]

# งานที่อาจารย์สั่งในโปรเจกต์สุดท้าย + หลักฐานว่าอยู่ตรงไหน
CHECKLIST = [
    ("นำเสนอด้วย PowerPoint + สาธิตระบบ + แสดงภาพในระบบแนะนำ",
     "เว็บ MangaGraph แสดงภาพปกมังงะทุกหน้า", "https://mangagraph-664245026.streamlit.app"),
    ("ไฟล์ PowerPoint อยู่ใน GitHub",
     "slides/MangaGraph_Presentation.pptx", f"{MANGA_REPO}/tree/main/slides"),
    ("การบ้านทุกชิ้นอยู่ใน GitHub",
     "reports/ — Assignment 1, 2, Club System · MangaGraph/homework/ — NetworkX, Neo4j",
     f"{HUB_REPO}/tree/main/reports"),
    ("หน้า index ลิงก์ไปการบ้านทุกชิ้น",
     "หน้านี้ + README ของ repo", HUB_REPO),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def img_uri(name: str) -> str:
    """แปลงไฟล์รูปใน assets/ เป็น data URI เพื่อฝังใน HTML ได้ทันที"""
    p = ROOT / "assets" / name
    if not p.exists():
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def e(text: str) -> str:
    return html.escape(text, quote=True)


# ---------------------------------------------------------------------------
# Style — โทนกระดาษมังงะ ขาว-ดำ-แดง ให้เข้าชุดกับโปรเจกต์ MangaGraph
# ---------------------------------------------------------------------------

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Kanit:wght@400;500;600;700&family=IBM+Plex+Sans+Thai:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root { --paper:#FBF7EE; --ink:#141414; --red:#E63946; --muted:#6B6458; --line:#E3DCCB;
        --teal:#2A9D8F; --orange:#F4A261; }

html, body, [class*="css"], .stMarkdown, p, li { font-family:'IBM Plex Sans Thai', 'Kanit', sans-serif; }
.stApp { background: var(--paper)
         radial-gradient(rgba(20,20,20,.07) 1px, transparent 1.2px) 0 0/16px 16px; color: var(--ink); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility:hidden; height:0; }
.block-container { padding-top:2rem; max-width:1180px; }

/* ---------- hero ---------- */
.hero { position:relative; overflow:hidden; background:#fff; border:3px solid var(--ink);
        border-radius:14px; box-shadow:8px 8px 0 var(--ink); padding:2.2rem 2.4rem; margin-bottom:1.6rem; }
.hero:after { content:""; position:absolute; right:-40px; top:-40px; width:360px; height:360px;
        background: radial-gradient(var(--red) 1.6px, transparent 1.8px) 0 0/12px 12px;
        opacity:.22; border-radius:50%; }
.hero-grid { position:relative; z-index:1; display:flex; gap:2rem; align-items:center; flex-wrap:wrap; }
.kicker { display:inline-block; background:var(--ink); color:#fff; font:600 .78rem 'Kanit';
          letter-spacing:.12em; padding:.25rem .8rem; border-radius:4px; }
.hero h1 { font-family:'Bangers', 'Kanit', cursive; font-weight:400; font-size:3.4rem; line-height:1;
           letter-spacing:.03em; margin:.7rem 0 .4rem; color:var(--ink); padding:0; }
.hero h1 span { color:var(--red); }
.hero .sub { font-family:'Kanit'; font-size:1.12rem; color:var(--ink); margin:0 0 .3rem; }
.hero p { color:var(--muted); max-width:620px; margin:0; }
.me { display:flex; gap:1rem; align-items:center; background:var(--paper); border:2px solid var(--ink);
      border-radius:12px; padding:.8rem 1.1rem .8rem .8rem; box-shadow:4px 4px 0 var(--ink); margin-left:auto; }
.me img { width:74px; height:74px; border-radius:50%; border:3px solid var(--ink); object-fit:cover; }
.me b { font-family:'Kanit'; font-size:1.05rem; display:block; }
.me small { color:var(--muted); line-height:1.5; display:block; }

/* ---------- stats ---------- */
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.4rem; }
.stat { background:#fff; border:2px solid var(--ink); border-radius:10px; padding:.8rem 1rem;
        box-shadow:4px 4px 0 var(--ink); }
.stat .n { font-family:'Bangers'; font-size:2.3rem; line-height:1; color:var(--red); }
.stat .l { font:500 .9rem 'Kanit'; color:var(--ink); }

/* ---------- section title ---------- */
.sec { display:flex; align-items:center; gap:.7rem; margin:1.4rem 0 .9rem; }
.sec h2 { font-family:'Kanit'; font-weight:700; font-size:1.5rem; margin:0; padding:0; color:var(--ink); }
.sec .pill { background:var(--red); color:#fff; font:600 .72rem 'Kanit'; letter-spacing:.1em;
             padding:.15rem .55rem; border-radius:4px; }
.sec .rule { flex:1; height:3px; background:var(--ink); border-radius:2px; }

/* ---------- card ---------- */
[class*="st-key-card_"] {
    background:#fff; border:3px solid var(--ink); border-radius:14px; box-shadow:6px 6px 0 var(--ink);
    padding:0 0 1.1rem 0; gap:.55rem; overflow:hidden; transition:transform .15s ease, box-shadow .15s ease; }
[class*="st-key-card_"]:hover { transform:translate(-2px,-2px); box-shadow:8px 8px 0 var(--red); }
.cover { position:relative; aspect-ratio:16/10; border-bottom:3px solid var(--ink); background:var(--paper); overflow:hidden; }
.cover img { width:100%; height:100%; object-fit:cover; object-position:top; display:block; }
.cover .code { height:100%; box-sizing:border-box; padding:3.4rem 1.1rem 1rem; background:#1B1B1F; color:#EDEDED;
             font:400 .7rem/1.7 'JetBrains Mono', monospace; overflow:hidden; }
.cover .code div { white-space:pre; }
.cover .code .k { color:#FF7A85; font-weight:600; } .cover .code .s { color:#8BD5CA; } .cover .code .c { color:#F4A261; }
.no { position:absolute; left:12px; top:12px; background:var(--red); color:#fff; font-family:'Bangers';
      font-size:1.3rem; letter-spacing:.06em; padding:.05rem .6rem; border:2px solid var(--ink);
      border-radius:6px; box-shadow:3px 3px 0 var(--ink); transform:rotate(-3deg); }
.no.final { background:var(--ink); }
.body { padding:1rem 1.2rem 0; }
.badges { display:flex; gap:.4rem; flex-wrap:wrap; margin-bottom:.5rem; }
.badge { font:600 .74rem 'Kanit'; padding:.12rem .6rem; border-radius:999px; border:2px solid var(--ink); }
.badge.tag { background:var(--paper); }
.badge.live { background:#D8F3EC; color:#14594F; border-color:#14594F; }
.badge.soon { background:#FFF1D6; color:#8A5A00; border-color:#8A5A00; }
.title { font-family:'Kanit'; font-weight:700; font-size:1.18rem; line-height:1.35; color:var(--ink); margin:.1rem 0 .4rem; }
.desc { color:#3A372F; font-size:.92rem; line-height:1.6; min-height:4.8em; }
.learned { margin:.7rem 0 .5rem; display:flex; flex-wrap:wrap; gap:.35rem; }
.learned span { font-size:.76rem; background:#FFE3E5; color:#8E1B26; border-radius:4px; padding:.1rem .45rem; }
[class*="st-key-card_"] [data-testid="stLinkButton"] { padding:0 1.2rem; }
div[data-testid="stLinkButton"] a { border:2px solid var(--ink) !important; border-radius:8px !important;
      background:#fff !important; color:var(--ink) !important; font-family:'Kanit' !important; font-weight:500;
      box-shadow:3px 3px 0 var(--ink); transition:all .12s ease; }
div[data-testid="stLinkButton"] a:hover { background:var(--red) !important; color:#fff !important;
      transform:translate(-1px,-1px); box-shadow:4px 4px 0 var(--ink); }
div[data-testid="stLinkButton"] a[kind="primary"], div[data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-primary"] {
      background:var(--red) !important; color:#fff !important; }

/* ---------- checklist ---------- */
.check { background:#fff; border:2px solid var(--ink); border-radius:12px; box-shadow:5px 5px 0 var(--ink); overflow:hidden; }
.check a.row { display:grid; grid-template-columns:44px 1fr auto; gap:1rem; align-items:center; padding:.8rem 1.1rem;
               border-top:1px dashed var(--line); color:var(--ink); text-decoration:none; }
.check a.row:first-child { border-top:0; }
.check a.row:hover { background:#FFF4F4; }
.check .tick { width:34px; height:34px; border-radius:50%; background:var(--teal); color:#fff; display:grid;
               place-items:center; font-weight:700; border:2px solid var(--ink); }
.check b { font-family:'Kanit'; font-weight:600; display:block; }
.check small { color:var(--muted); font-family:'JetBrains Mono', monospace; font-size:.78rem; }
.check .go { font:600 .85rem 'Kanit'; color:var(--red); white-space:nowrap; }

.foot { text-align:center; color:var(--muted); font-size:.85rem; margin:2.4rem 0 .5rem; padding-top:1rem;
        border-top:2px dashed var(--line); }

/* segmented filter */
div[data-testid="stButtonGroup"] button { font-family:'Kanit' !important; border:2px solid var(--ink) !important; }
div[data-testid="stButtonGroup"] button[aria-checked="true"], div[data-testid="stButtonGroup"] button[kind*="Active"] {
      background:var(--ink) !important; color:#fff !important; }

@media (max-width: 900px) {
  .stats { grid-template-columns:repeat(2,1fr); }
  .hero { padding:1.6rem 1.3rem; } .hero h1 { font-size:2.5rem; }
  .me { margin-left:0; }
  .check a.row { grid-template-columns:40px 1fr; } .check .go { grid-column:2; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

st.markdown(
    f"""
<div class="hero"><div class="hero-grid">
  <div style="flex:1;min-width:280px">
    <span class="kicker">ADVANCED DATABASE SYSTEMS · ระบบฐานข้อมูลขั้นสูง</span>
    <h1>GRAPH DB <span>ASSIGNMENTS</span></h1>
    <div class="sub">รวมการบ้านและโปรเจกต์ วิชาระบบฐานข้อมูลขั้นสูง</div>
    <p>ตั้งแต่เลือกฐานข้อมูลให้เหมาะกับ workload → Transaction &amp; Recovery บน MySQL →
       Cypher บน Neo4j → จบด้วยเว็บไซต์แนะนำมังงะด้วย Graph Database</p>
  </div>
  <div class="me">
    <img src="{img_uri('profile.jpg')}" alt="profile">
    <div><b>{e(STUDENT['name'])}</b>
      <small>รหัสนักศึกษา {STUDENT['id']}<br>หมู่เรียน {STUDENT['section']} · {e(STUDENT['school'])}</small></div>
  </div>
</div></div>
""",
    unsafe_allow_html=True,
)

n_hw = sum(a["kind"] == "hw" for a in ASSIGNMENTS)
n_project = sum(a["kind"] == "project" for a in ASSIGNMENTS)
n_links = sum(len(a["links"]) for a in ASSIGNMENTS)
n_live = sum(a["status"] == "live" for a in ASSIGNMENTS)
st.markdown(
    f"""
<div class="stats">
  <div class="stat"><div class="n">{n_hw}</div><div class="l">การบ้าน</div></div>
  <div class="stat"><div class="n">{n_project}</div><div class="l">โปรเจกต์</div></div>
  <div class="stat"><div class="n">{n_live}/{len(ASSIGNMENTS)}</div><div class="l">ส่งแล้ว</div></div>
  <div class="stat"><div class="n">{n_links}</div><div class="l">ลิงก์ผลงาน</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------


def section(title: str, pill: str) -> None:
    st.markdown(f'<div class="sec"><h2>{e(title)}</h2><span class="pill">{pill}</span>'
                f'<span class="rule"></span></div>', unsafe_allow_html=True)


KEYWORDS = ("MATCH", "WHERE", "NOT", "EXISTS", "RETURN", "ORDER", "BY", "DESC", "LIMIT", "AS", "count",
            "START", "TRANSACTION", "SELECT", "FROM", "FOR", "UPDATE", "INSERT", "INTO", "VALUES", "SET",
            "COMMIT", "ROLLBACK")
TOKEN = re.compile(r"('[^']*')|(:[A-Z_][A-Za-z_]*)|\b(" + "|".join(KEYWORDS) + r")\b")


def highlight_code(code: str) -> str:
    """ใส่สีโค้ด Cypher/SQL แบบง่าย ๆ: keyword = แดง, label = ส้ม, string = เขียว"""
    out, pos = [], 0
    for m in TOKEN.finditer(code):
        out.append(e(code[pos:m.start()]))
        cls = "s" if m.group(1) else "c" if m.group(2) else "k"
        out.append(f'<span class="{cls}">{e(m.group(0))}</span>')
        pos = m.end()
    out.append(e(code[pos:]))
    return "".join(out)


def card(i: int, a: dict) -> None:
    with st.container(key=f"card_{i}"):
        if a.get("image"):
            visual = f'<img src="{img_uri(a["image"])}" alt="{e(a["title"])}">'
        else:
            lines = "".join(f"<div>{ln or '&nbsp;'}</div>" for ln in highlight_code(a.get("code", "")).split("\n"))
            visual = f'<div class="code">{lines}</div>'
        no_cls = "no final" if a["kind"] == "project" else "no"
        status = ('<span class="badge live">● ส่งแล้ว</span>' if a["status"] == "live"
                  else '<span class="badge soon">◐ กำลังทำ</span>')
        learned = "".join(f"<span>{e(x)}</span>" for x in a.get("learned", []))
        st.markdown(
            f"""
<div class="cover">{visual}<span class="{no_cls}">{e(a['no'])}</span></div>
<div class="body">
  <div class="badges"><span class="badge tag">{e(a['tag'])}</span>{status}</div>
  <div class="title">{e(a['title'])}</div>
  <div class="desc">{e(a['desc'])}</div>
  <div class="learned">{learned}</div>
</div>""",
            unsafe_allow_html=True,
        )
        for j, (label, url) in enumerate(a["links"]):
            st.link_button(label, url, width="stretch", type="primary" if j == 0 else "secondary")


section("ผลงานทั้งหมด", "PORTFOLIO")
choice = st.segmented_control(
    "กรอง", ["ทั้งหมด", "การบ้าน", "โปรเจกต์"], default="ทั้งหมด", label_visibility="collapsed"
)
kind = {"การบ้าน": "hw", "โปรเจกต์": "project"}.get(choice or "ทั้งหมด")
shown = [(i, a) for i, a in enumerate(ASSIGNMENTS) if kind is None or a["kind"] == kind]

# วางทีละแถว แถวละ 3 การ์ด ให้ขอบบนของแต่ละแถวตรงกัน
for start in range(0, len(shown), 3):
    cols = st.columns(3, gap="large")
    for col, (i, a) in zip(cols, shown[start:start + 3]):
        with col:
            card(i, a)

# ---------------------------------------------------------------------------
# Checklist งานที่อาจารย์สั่ง
# ---------------------------------------------------------------------------

section("เช็กลิสต์งานโปรเจกต์สุดท้าย", "CHECKLIST")
rows = "".join(
    f'<a class="row" href="{e(url)}" target="_blank"><span class="tick">✓</span>'
    f"<span><b>{e(task)}</b><small>{e(where)}</small></span><span class='go'>เปิดดู ↗</span></a>"
    for task, where, url in CHECKLIST
)
st.markdown(f'<div class="check">{rows}</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="foot">© 2026 {e(STUDENT["name"])} · {STUDENT["id"]} · '
    f'<a href="{GH}" target="_blank" style="color:inherit">github.com/SuzakuKung4826</a> · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
