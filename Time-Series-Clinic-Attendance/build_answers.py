"""Assemble the answers page: inline CSS + embed every figure as a data URI."""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).parent
FIGS = ROOT / "partC_output"

CSS = """
<style>
:root{
  --bg:#FAFBFC; --surface:#F0F3F6; --surface2:#E7ECF1; --line:#D9E0E7;
  --ink:#12181F; --muted:#5C6873; --accent:#1D3557; --accent-soft:#e5ebf3;
  --flag:#A8401C; --flag-soft:#f6e7e1; --pass:#1B6152; --pass-soft:#e2efeb;
  --bar-ink:#F2F5F8;
  --measure:68ch;
  --sans:ui-sans-serif,-apple-system,"Helvetica Neue","Segoe UI",Arial,sans-serif;
  --serif:Charter,"Bitstream Charter","Iowan Old Style","Palatino Linotype",Georgia,serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#0E1319; --surface:#161D25; --surface2:#1D2630; --line:#2A343F;
    --ink:#E2E8EE; --muted:#94A2AF; --accent:#87ABD6; --accent-soft:#1a2530;
    --flag:#E28B63; --flag-soft:#2c1f1a; --pass:#5CB6A0; --pass-soft:#16261f;
    --bar-ink:#DDE5EC;
  }
}
:root[data-theme="dark"]{
  --bg:#0E1319; --surface:#161D25; --surface2:#1D2630; --line:#2A343F;
  --ink:#E2E8EE; --muted:#94A2AF; --accent:#87ABD6; --accent-soft:#1a2530;
  --flag:#E28B63; --flag-soft:#2c1f1a; --pass:#5CB6A0; --pass-soft:#16261f;
  --bar-ink:#DDE5EC;
}
*{box-sizing:border-box}
body{
  background:var(--bg); color:var(--ink);
  font-family:var(--serif); font-size:17px; line-height:1.66;
  margin:0; padding:0 20px 6rem;
  -webkit-font-smoothing:antialiased;
  display:grid; grid-template-columns:1fr min(var(--measure),100%) 1fr;
}
body > *{grid-column:2}
h1,h2,h3,.eyebrow,.partbar,th,.errtag,.errno,figcaption,dt{font-family:var(--sans)}

/* ---------- masthead ---------- */
.masthead{padding:4.5rem 0 2rem; display:flex; flex-direction:column; gap:.9rem}
.eyebrow{
  margin:0; font-size:.72rem; font-weight:650; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent);
}
h1{
  margin:0; font-size:clamp(2.1rem,6vw,3rem); line-height:1.05;
  letter-spacing:-.028em; font-weight:750; text-wrap:balance;
}
.standfirst{margin:0; color:var(--muted); font-size:1.06rem; max-width:62ch}
.runmeta{
  margin:.9rem 0 0; padding-top:1.1rem; border-top:1px solid var(--line);
  display:flex; flex-wrap:wrap; gap:.35rem 2.4rem;
}
.runmeta > div{display:flex; flex-direction:column; gap:.1rem}
.runmeta dt{
  font-size:.66rem; font-weight:650; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted);
}
.runmeta dd{margin:0; font-family:var(--mono); font-size:.8rem; color:var(--ink)}

/* ---------- part bars ---------- */
.part{display:contents}
.partbar{
  grid-column:1/-1; margin:3.5rem 0 2rem;
  background:var(--accent); color:var(--bar-ink);
  display:flex; align-items:baseline; gap:1rem; flex-wrap:wrap;
  padding:.85rem clamp(1rem,5vw,2rem);
}
.partname{font-size:.74rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase}
.parttitle{font-size:1.05rem; font-weight:600; letter-spacing:-.01em; flex:1}
.partmarks{font-family:var(--mono); font-size:.75rem; opacity:.8}

/* ---------- questions ---------- */
.q{display:contents}
.q > *{grid-column:2}
h2{
  grid-column:2; margin:3rem 0 1.1rem; padding-bottom:.5rem;
  border-bottom:2px solid var(--ink);
  font-size:1.4rem; font-weight:700; letter-spacing:-.02em;
  display:flex; align-items:baseline; gap:.65rem; text-wrap:balance;
}
.qid{
  font-family:var(--mono); font-size:.82rem; font-weight:700;
  background:var(--accent); color:var(--bar-ink);
  padding:.16em .5em; border-radius:2px; letter-spacing:.02em;
  position:relative; top:-.15em;
}
.marks{
  margin-left:auto; font-family:var(--mono); font-size:.72rem;
  font-weight:600; color:var(--muted); white-space:nowrap;
}
.marks::after{content:" marks"}
h3{
  margin:2rem 0 .6rem; font-size:1.02rem; font-weight:650;
  letter-spacing:-.005em; color:var(--accent); text-wrap:balance;
}
p{margin:0 0 .95rem}
ol.sub{margin:0 0 1rem; padding-left:1.4rem; display:flex; flex-direction:column; gap:.7rem}
ol.sub > li{padding-left:.25rem}
ul{margin:0 0 1rem; padding-left:1.3rem; display:flex; flex-direction:column; gap:.5rem}
b{font-weight:650}
em{font-style:italic}
code{
  font-family:var(--mono); font-size:.86em;
  background:var(--surface2); padding:.08em .32em; border-radius:2px;
}

/* ---------- callouts ---------- */
.note{
  background:var(--surface); border-left:3px solid var(--accent);
  padding:.8rem 1rem; margin:1.2rem 0; font-size:.95rem;
}
.verdict{
  background:var(--accent-soft); border-left:3px solid var(--accent);
  padding:.7rem 1rem; margin:1.1rem 0; font-size:1rem;
}
blockquote.answer,blockquote.review{
  margin:1.1rem 0; padding:1rem 1.2rem;
  background:var(--surface); border-left:3px solid var(--pass);
  display:flex; flex-direction:column; gap:.7rem;
}
blockquote.answer p,blockquote.review p{margin:0}
blockquote.review{border-left-color:var(--flag); font-style:italic}
.setup{color:var(--muted); font-size:.95rem}
.eq{
  font-family:var(--mono); font-size:.86rem; text-align:center;
  background:var(--surface); padding:.7rem .8rem; margin:1rem 0;
  overflow-x:auto; white-space:nowrap;
}
pre.code{
  grid-column:1/-1; width:min(100%,88ch); justify-self:center;
  font-family:var(--mono); font-size:.79rem; line-height:1.6;
  background:var(--surface); border:1px solid var(--line);
  padding:.9rem 1.1rem; margin:1.1rem auto; overflow-x:auto;
}
.term{color:var(--flag); font-weight:700; letter-spacing:.01em}

/* ---------- tables ---------- */
.tablewrap{
  grid-column:1/-1; width:min(100%,105ch); justify-self:center;
  margin:1.2rem auto; overflow-x:auto; border:1px solid var(--line);
}
table{border-collapse:collapse; width:100%; font-family:var(--sans); font-size:.83rem}
th{
  background:var(--surface2); text-align:left; font-weight:650;
  padding:.55rem .7rem; border-bottom:1px solid var(--line);
  letter-spacing:.01em; vertical-align:bottom;
}
td{padding:.55rem .7rem; border-bottom:1px solid var(--line); vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:nth-child(even){background:var(--surface)}
table.tight td,table.tight th{white-space:nowrap}
.mono{font-family:var(--mono); font-size:.94em; font-variant-numeric:tabular-nums}
td.b,span.b,.mono.b{font-weight:700}
th.hl,td.hl{background:var(--flag-soft)}
.ok{color:var(--pass); font-weight:650}
.no,.bad{color:var(--flag); font-weight:650}
.real{color:var(--flag); font-weight:700; font-family:var(--mono); font-size:.9em}
.fa{color:var(--muted); font-family:var(--mono); font-size:.9em}
.tag-s,.tag-c,.tag-n{
  font-family:var(--mono); font-size:.78rem; font-weight:700;
  padding:.14em .45em; border-radius:2px; white-space:nowrap;
}
.tag-s{background:var(--pass-soft); color:var(--pass)}
.tag-c{background:var(--accent-soft); color:var(--accent)}
.tag-n{background:var(--surface2); color:var(--muted)}

/* ---------- figures ---------- */
figure{
  grid-column:1/-1; width:min(100%,112ch); justify-self:center;
  margin:1.4rem auto; display:flex; flex-direction:column; gap:.45rem;
}
figure img{
  display:block; width:100%; height:auto;
  border:1px solid var(--line); background:#fff;
}
figcaption{font-size:.78rem; color:var(--muted); line-height:1.5}

/* ---------- Part D error blocks ---------- */
.err{
  grid-column:1/-1; width:min(100%,var(--measure)); justify-self:center;
  margin:1.8rem auto; padding:0 0 .3rem;
  border-top:2px solid var(--flag);
}
.err > *{max-width:100%}
.errhead{
  display:flex; align-items:baseline; flex-wrap:wrap; gap:.55rem;
  margin:.8rem 0 .7rem;
}
.errno{
  font-family:var(--mono); font-size:.74rem; font-weight:700;
  background:var(--flag); color:var(--bg); padding:.14em .5em; border-radius:2px;
}
.errtag{
  font-size:.65rem; font-weight:650; letter-spacing:.12em; text-transform:uppercase;
  color:var(--flag); background:var(--flag-soft); padding:.2em .5em; border-radius:2px;
}
.errhead h3{margin:0; width:100%; color:var(--ink); font-size:1.06rem}
.err .tablewrap,.err pre.code,.err figure{width:100%; margin-left:0; margin-right:0}

/* ---------- colophon ---------- */
.colophon{
  margin-top:4rem; padding-top:1.2rem; border-top:1px solid var(--line);
  color:var(--muted); font-size:.85rem;
}
.colophon p{margin:0}

@media (max-width:640px){
  body{font-size:16px; padding:0 14px 4rem}
  h2{flex-wrap:wrap}
  .marks{margin-left:0}
}
@media print{
  body{background:#fff; color:#000}
  .partbar{background:#1D3557 !important; -webkit-print-color-adjust:exact; print-color-adjust:exact}
  .err,figure,.tablewrap{break-inside:avoid}
  h2{break-after:avoid}
}
</style>
"""

body = (ROOT / "answers_body.html").read_text()


def embed(m):
    name = m.group(1)
    data = base64.b64encode((FIGS / name).read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'


body, n = re.subn(r'src="FIG:([^"]+)"', embed, body)
out = ROOT / "CS3621_L05_Answers.html"
out.write_text(CSS + "\n" + body)
print(f"embedded {n} figures -> {out.name}  ({out.stat().st_size/1e6:.2f} MB)")
