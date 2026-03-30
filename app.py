import streamlit as st
from datetime import datetime
from nlp_engine import get_answer

st.set_page_config(
    page_title="CVR AI Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

#MainMenu, footer, header { visibility: hidden; height: 0; }
.block-container { padding-top:0!important; padding-bottom:0!important; padding-left:0!important; padding-right:0!important; max-width:100%!important; }
section[data-testid="stSidebar"] { display:none!important; }
[data-testid="stAppViewContainer"] { background:#070d1a!important; }
[data-testid="stVerticalBlock"] { gap:0!important; }
[data-testid="stVerticalBlock"] > div { padding:0!important; }
div[data-testid="stForm"] { border:none!important; padding:0!important; background:transparent!important; }
.element-container { margin:0!important; padding:0!important; }

:root {
  --bg:#070d1a; --bg2:#0d1526; --bg3:#111e35; --bg4:#192640;
  --teal:#00d4aa; --teal-dim:rgba(0,212,170,0.12); --teal-bdr:rgba(0,212,170,0.28);
  --violet:#7c6af7; --violet-dim:rgba(124,106,247,0.12);
  --text:#e8f0f8; --text2:#7a90b0; --text3:#3d5070;
  --bdr:rgba(255,255,255,0.06); --r:14px; --r-lg:20px; --r-xl:28px;
}

html, body, [class*="st-"] { font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stAppViewContainer"]::before { content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: radial-gradient(ellipse 70% 55% at 5% 0%, rgba(0,212,170,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 55% 45% at 95% 100%, rgba(124,106,247,0.08) 0%, transparent 55%); }

.top-strip { width:100%; display:flex; align-items:center; justify-content:space-between;
  padding:0.85rem 1.5rem; border-bottom:1px solid var(--bdr);
  background:rgba(7,13,26,0.95); backdrop-filter:blur(12px); }
.tbrand { display:flex; align-items:center; gap:0.7rem; }
.bico { width:36px; height:36px; border-radius:10px;
  background:linear-gradient(135deg,#00d4aa,#0099aa);
  display:flex; align-items:center; justify-content:center;
  font-family:'Syne',sans-serif; font-size:13px; font-weight:800; color:#070d1a; }
.bname { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; }
.btag  { font-size:0.68rem; color:var(--text3); margin-top:-2px; }
.opill { display:inline-flex; align-items:center; gap:5px; font-size:0.68rem; color:var(--teal);
  background:var(--teal-dim); border:1px solid var(--teal-bdr); border-radius:100px; padding:0.22rem 0.7rem; }
.odot  { width:6px; height:6px; border-radius:50%; background:var(--teal); animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;}50%{opacity:0.3;} }

.hero { width:100%; max-width:620px; margin:0 auto; padding:2rem 1.5rem 0; text-align:center; }
.hbadge { display:inline-flex; align-items:center; gap:0.4rem;
  background:var(--teal-dim); border:1px solid var(--teal-bdr); border-radius:100px;
  padding:0.28rem 0.85rem; font-size:0.7rem; font-weight:600; color:var(--teal);
  letter-spacing:0.04em; text-transform:uppercase; margin-bottom:1rem; }
.hlive { width:5px; height:5px; border-radius:50%; background:var(--teal); animation:blink 2s infinite; }
.htitle { font-family:'Syne',sans-serif; font-size:clamp(1.85rem,5.5vw,2.8rem);
  font-weight:800; line-height:1.1; letter-spacing:-0.03em; margin:0 0 0.65rem; }
.hteal { color:var(--teal); }
.hsub  { font-size:0.9rem; color:var(--text2); line-height:1.6; max-width:400px; margin:0 auto 1.5rem; }

.illus-wrap { width:100%; max-width:500px; margin:0 auto 1.25rem;
  border-radius:var(--r-lg); overflow:hidden; border:1px solid var(--bdr); background:var(--bg2); }

.acard { background:var(--bg2); border:1px solid var(--bdr); border-radius:var(--r-xl); padding:1.75rem 1.75rem; }
.awrap { width:100%; max-width:400px; margin:0 auto; padding:0 1rem 2rem; }

.divl { display:flex; align-items:center; gap:0.75rem; color:var(--text3); font-size:0.73rem; margin:0.9rem 0; }
.divl::before,.divl::after { content:''; flex:1; height:1px; background:var(--bdr); }

[data-testid="stTextInput"] input {
  background:var(--bg3)!important; border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:10px!important; color:var(--text)!important;
  font-family:'Space Grotesk',sans-serif!important; font-size:0.9rem!important;
  padding:0.72rem 1rem!important; box-shadow:none!important; caret-color:var(--teal)!important; }
[data-testid="stTextInput"] input:focus { border-color:var(--teal-bdr)!important; box-shadow:0 0 0 3px rgba(0,212,170,0.08)!important; }
[data-testid="stTextInput"] input::placeholder { color:var(--text3)!important; }
[data-testid="stTextInput"] label { color:var(--text2)!important; font-size:0.73rem!important; font-weight:600!important; letter-spacing:0.05em!important; text-transform:uppercase!important; font-family:'Space Grotesk',sans-serif!important; }
[data-testid="stTextInput"] { margin-bottom:0.65rem!important; }

.stButton > button { font-family:'Space Grotesk',sans-serif!important; font-weight:600!important; font-size:0.88rem!important; border-radius:10px!important; width:100%!important; transition:all 0.18s!important; letter-spacing:0.01em!important; }
.bp  .stButton>button { background:linear-gradient(135deg,#00d4aa,#0099aa)!important; color:#070d1a!important; border:none!important; padding:0.75rem!important; box-shadow:0 4px 20px rgba(0,212,170,0.22)!important; }
.bp  .stButton>button:hover { transform:translateY(-1px)!important; box-shadow:0 6px 26px rgba(0,212,170,0.32)!important; }
.bg  .stButton>button { background:transparent!important; color:var(--text2)!important; border:1px solid rgba(255,255,255,0.1)!important; padding:0.72rem!important; }
.bg  .stButton>button:hover { background:var(--bg3)!important; color:var(--text)!important; border-color:var(--teal-bdr)!important; }
.bd  .stButton>button { background:transparent!important; color:#f87171!important; border:1px solid rgba(248,113,113,0.25)!important; padding:0.72rem!important; }
.bd  .stButton>button:hover { background:rgba(248,113,113,0.07)!important; }
.bs  .stButton>button { background:var(--bg3)!important; color:var(--text2)!important; border:1px solid var(--bdr)!important; padding:0.45rem 0.75rem!important; font-size:0.75rem!important; }
.bs  .stButton>button:hover { border-color:var(--teal-bdr)!important; color:var(--teal)!important; }
.bsend .stButton>button { background:linear-gradient(135deg,#00d4aa,#0099aa)!important; color:#070d1a!important; border:none!important; padding:0.68rem!important; box-shadow:0 3px 14px rgba(0,212,170,0.2)!important; }
.bback .stButton>button { background:transparent!important; color:var(--text3)!important; border:none!important; font-size:0.8rem!important; padding:0.35rem 0.5rem!important; text-align:left!important; width:auto!important; }
.bback .stButton>button:hover { color:var(--text)!important; }

.hdr { display:flex; align-items:center; gap:0.75rem; padding:0.85rem 1.25rem;
  background:var(--bg2); border-bottom:1px solid var(--bdr); }
.hdr-r { margin-left:auto; display:flex; align-items:center; gap:0.6rem; }
.upill { display:inline-flex; align-items:center; gap:0.5rem; background:var(--bg3);
  border:1px solid var(--bdr); border-radius:100px; padding:0.25rem 0.7rem 0.25rem 0.25rem; font-size:0.73rem; color:var(--text2); }
.uav { width:26px; height:26px; border-radius:50%; background:linear-gradient(135deg,#00d4aa,#0099aa);
  display:inline-flex; align-items:center; justify-content:center; font-size:0.63rem; font-weight:700; color:#070d1a; }

.gbnd { padding:1.25rem 1.25rem 0; max-width:660px; margin:0 auto; }
.cg { display:grid; grid-template-columns:repeat(3,1fr); gap:0.45rem; margin:0.75rem 0 1.25rem; }
.tc { background:var(--bg3); border:1px solid var(--bdr); border-radius:10px; padding:0.55rem 0.75rem;
  font-size:0.76rem; color:var(--text2); display:flex; align-items:center; gap:0.4rem; }
.ac { display:flex; align-items:center; gap:0.85rem; padding:0.85rem 1.05rem;
  background:var(--bg3); border:1px solid var(--bdr); border-radius:var(--r); margin-bottom:0.5rem; }
.ai { width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }
.at { font-size:0.88rem; font-weight:600; }
.ad { font-size:0.72rem; color:var(--text3); margin-top:1px; }
.aa { margin-left:auto; color:var(--text3); }

.msgs-container { flex: 1 1 0; overflow-y: auto !important; display: flex; flex-direction: column; padding: 1.25rem; scrollbar-width: thin; margin-bottom: 0.5rem; }
.mr   { display:flex; gap:0.6rem; align-items:flex-start; margin-bottom:1rem; }
.mr.user { flex-direction:row-reverse; }
.mav { width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.66rem; font-weight:700; flex-shrink:0; margin-top:2px; }
.mr.bot  .mav { background:var(--teal-dim); border:1px solid var(--teal-bdr); color:var(--teal); }
.mr.user .mav { background:linear-gradient(135deg,#7c6af7,#4f3fbc); color:#fff; }

.bbl-wrap { max-width: 80%; display: flex; flex-direction: column; }
.mr.user .bbl-wrap { align-items: flex-end; }
.bbl { width: fit-content; padding:0.68rem 0.95rem; border-radius:15px; font-size:0.87rem; line-height:1.65; word-break: normal; overflow-wrap: break-word; white-space: normal; display: inline-block; }
.mr.bot  .bbl { background:var(--bg3); border:1px solid var(--bdr); border-bottom-left-radius:4px; color:var(--text); }
.mr.user .bbl { background:linear-gradient(135deg,#7c6af7,#4f3fbc); border-bottom-right-radius:4px; color:#fff; }
.mts { font-size:0.63rem; color:var(--text3); margin-top:3px; }

.ec { text-align:center; padding:2.5rem 1rem; color:var(--text3); }

.qbar { display:flex; flex-wrap:wrap; gap:0.38rem; padding:0.65rem 1.25rem; border-top:1px solid var(--bdr); background:var(--bg2); }
.qc   { padding:0.26rem 0.8rem; border-radius:100px; background:var(--bg3); border:1px solid var(--bdr);
  font-size:0.73rem; color:var(--text2); cursor:pointer; }
.iz   { padding:0.7rem 1.25rem 0.9rem; background:var(--bg2); border-top:1px solid var(--bdr); }

.hl  { display:flex; gap:0.6rem; align-items:flex-start; padding:0.72rem 0.95rem;
  background:var(--bg2); border:1px solid var(--bdr); border-radius:var(--r); margin-bottom:0.42rem; }
.hr  { font-size:0.63rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;
  padding:0.16rem 0.55rem; border-radius:100px; flex-shrink:0; margin-top:2px; }
.hr.user { background:rgba(124,106,247,0.14); color:#a89cf7; }
.hr.bot  { background:var(--teal-dim); color:var(--teal); }
.ht { font-size:0.82rem; color:var(--text2); line-height:1.5; }

.al { padding:0.55rem 0.85rem; border-radius:8px; font-size:0.82rem; margin-bottom:0.65rem; }
.ae { background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.25); color:#f87171; }
.ao { background:rgba(0,212,170,0.1);   border:1px solid rgba(0,212,170,0.25);   color:#00d4aa; }

div.element-container:has(.hidden-btn-marker) { display: none !important; }
div.element-container:has(.hidden-btn-marker) + div.element-container { display: none !important; }

.upill-wrapper { position: relative; display: inline-block; outline: none; }
.upill { cursor: pointer; transition: all 0.2s ease; }
.upill-wrapper:focus-within .upill, .upill:hover { border-color: #00c9a7; background: rgba(0, 201, 167, 0.15); }

.prof-drop { 
  position: absolute; right: 0; top: calc(100% + 12px); 
  opacity: 0; visibility: hidden; transform: translateY(-10px);
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  z-index: 1000;
  background: rgba(13, 17, 23, 0.88);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 201, 167, 0.2);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(0, 201, 167, 0.05);
  border-radius: 16px;
  width: 280px;
  text-align: left;
  padding: 1.25rem;
  pointer-events: none;
}
.upill-wrapper:focus-within .prof-drop, .prof-drop:hover {
  opacity: 1; visibility: visible; transform: translateY(0); pointer-events: auto;
}

.pd-hdr { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1.2rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); }
.pd-av { width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, #00c9a7, #0099aa); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 800; color: #070d1a; flex-shrink: 0; }
.pd-name { font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700; color: #e8f0f8; line-height: 1.2; margin-bottom: 0.15rem; }
.pd-email { font-size: 0.7rem; color: #7a90b0; }

.pd-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem; font-size: 0.8rem; }
.pd-row span { color: #7a90b0; }
.pd-row strong { color: #e8f0f8; font-weight: 600; font-family: 'Space Grotesk', sans-serif; }

.pd-logout { margin-top: 1.2rem; padding: 0.6rem; text-align: center; font-size: 0.82rem; font-weight: 600; color: #f87171; border: 1px solid rgba(248,113,113,0.25); border-radius: 8px; cursor: pointer; transition: all 0.2s ease; background: rgba(248,113,113,0.04); }
.pd-logout:hover { background: rgba(248,113,113,0.12); border-color: rgba(248,113,113,0.4); }

.qc:active { transform: scale(0.96); box-shadow: 0 0 10px rgba(0,201,167,0.3); border-color: rgba(0,201,167,0.6); }

@keyframes fu { from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);} }
div.block-container { animation:fu 0.3s ease; }
@media(max-width:480px){ .cg{grid-template-columns:1fr 1fr;} .htitle{font-size:1.8rem;} }

/* Home Dashboard Buttons */
.button-group { display: flex !important; flex-direction: row !important; justify-content: center !important; align-items: center !important; gap: 12px !important; flex-wrap: wrap !important; padding: 16px !important; width: 100% !important; box-sizing: border-box !important; }
.action-btn-wrapper { flex: 1 !important; min-width: 140px !important; max-width: 220px !important; width: auto !important; }
.action-btn { width: 100% !important; padding: 12px 20px !important; display: flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; border-radius: 10px !important; font-size: clamp(13px, 1.5vw, 15px) !important; white-space: nowrap !important; cursor: pointer !important; border: 1px solid rgba(255,255,255,0.1) !important; background: rgba(255,255,255,0.05) !important; color: #fff !important; transition: background 0.2s ease, transform 0.1s ease !important; }
.action-btn:hover { background: rgba(0, 201, 167, 0.15) !important; border-color: #00c9a7 !important; transform: translateY(-2px) !important; }
.sign-out-btn:hover { background: rgba(255, 80, 80, 0.15) !important; border-color: rgba(255, 80, 80, 0.4) !important; }
@media (max-width: 400px) { .action-btn-wrapper, .action-btn { max-width: 100% !important; width: 100% !important; } }
</style>
""", unsafe_allow_html=True)

# ── Session state (unchanged) ──
for key, default in {"page":"landing","nav_history":[],"user":None,"messages":[],"users_db":{"23b81a6699@cvr.ac.in": "Katta Poojitha", "23b81a6698@cvr.ac.in": "Katta Poojitha"}}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def go(page):
    st.session_state.nav_history.append(st.session_state.page)
    st.session_state.page = page
    st.rerun()

import streamlit.components.v1 as components

# Unlock layout conditionally on non-chat pages to prevent stuck pages!
if st.session_state.page != "chatbot":
    components.html("""
    <script>
        const d = window.parent.document;
        d.body.style.overflow = '';
        d.documentElement.style.overflow = '';
        const v = d.querySelector('[data-testid="stAppViewContainer"]');
        if(v) { v.style.overflow = ''; v.style.height = ''; v.style.display = ''; v.style.flexDirection = ''; }
        const b = d.querySelector('.block-container');
        if(b) { b.style.flex = ''; b.style.display = ''; b.style.flexDirection = ''; b.style.overflow = ''; b.style.paddingTop = ''; b.style.paddingBottom = ''; b.style.padding = ''; }
        
        // Remove structural classes from previous visits
        d.querySelectorAll('.chat-fixed-header').forEach(el => el.classList.remove('chat-fixed-header'));
        d.querySelectorAll('.chat-scroll-area').forEach(el => el.classList.remove('chat-scroll-area'));
        d.querySelectorAll('.chat-fixed-footer').forEach(el => el.classList.remove('chat-fixed-footer'));
    </script>
    """, height=0)


def go_back():
    protected = {"home", "chatbot", "history", "profile"}
    if st.session_state.nav_history:
        prev = st.session_state.nav_history.pop()
        if not st.session_state.user and prev in protected:
            st.session_state.page = "landing"
        else:
            st.session_state.page = prev
    else:
        st.session_state.page = "landing"
    st.rerun()

def now_str():
    return datetime.now().strftime("%I:%M %p")

# ── SVG assets ──
LANDING_SVG = """<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;">
  <defs>
    <linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0d1526"/><stop offset="100%" stop-color="#111e35"/></linearGradient>
    <linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#00d4aa"/><stop offset="100%" stop-color="#0099aa"/></linearGradient>
    <linearGradient id="vg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7c6af7"/><stop offset="100%" stop-color="#4f3fbc"/></linearGradient>
  </defs>
  <rect width="480" height="200" fill="url(#sk)"/>
  <!-- Stars — exactly original positions -->
  <circle cx="30" cy="18" r="1" fill="#00d4aa" opacity="0.6"/><circle cx="80" cy="8" r="0.8" fill="#fff" opacity="0.35"/>
  <circle cx="160" cy="13" r="1.1" fill="#7c6af7" opacity="0.5"/><circle cx="240" cy="6" r="0.9" fill="#fff" opacity="0.3"/>
  <circle cx="320" cy="11" r="1" fill="#00d4aa" opacity="0.4"/><circle cx="420" cy="7" r="0.8" fill="#fff" opacity="0.4"/>
  <circle cx="460" cy="19" r="1.1" fill="#7c6af7" opacity="0.5"/>
  <!-- Ground -->
  <rect x="0" y="165" width="480" height="35" fill="#0a1422"/>
  <rect x="0" y="163" width="480" height="2.5" fill="#00d4aa" opacity="0.12"/>

  <!-- ═══════════════════════════════
       COLLEGE BUILDING — original positions exactly
       ═══════════════════════════════ -->
  <rect x="55" y="72" width="185" height="93" fill="#0f1c30"/>
  <rect x="55" y="70" width="185" height="4" fill="#00d4aa" opacity="0.45"/>
  <rect x="63" y="76" width="7" height="89" fill="#192640"/><rect x="82" y="76" width="7" height="89" fill="#192640"/>
  <rect x="101" y="76" width="7" height="89" fill="#192640"/><rect x="120" y="76" width="7" height="89" fill="#192640"/>
  <rect x="139" y="76" width="7" height="89" fill="#192640"/><rect x="158" y="76" width="7" height="89" fill="#192640"/>
  <rect x="177" y="76" width="7" height="89" fill="#192640"/><rect x="196" y="76" width="7" height="89" fill="#192640"/>
  <rect x="215" y="76" width="7" height="89" fill="#192640"/>
  <rect x="68" y="88" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.35"/>
  <rect x="88" y="88" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.4"/>
  <rect x="108" y="88" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.28"/>
  <rect x="128" y="88" width="9" height="12" rx="2" fill="#fff" opacity="0.1"/>
  <rect x="148" y="88" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.32"/>
  <rect x="168" y="88" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.3"/>
  <rect x="188" y="88" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.2"/>
  <rect x="208" y="88" width="9" height="12" rx="2" fill="#fff" opacity="0.09"/>
  <rect x="68" y="108" width="9" height="12" rx="2" fill="#fff" opacity="0.09"/>
  <rect x="88" y="108" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.25"/>
  <rect x="108" y="108" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.32"/>
  <rect x="128" y="108" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.28"/>
  <rect x="148" y="108" width="9" height="12" rx="2" fill="#fff" opacity="0.1"/>
  <rect x="168" y="108" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.22"/>
  <rect x="188" y="108" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.28"/>
  <rect x="208" y="108" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.18"/>
  <rect x="68" y="128" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.2"/>
  <rect x="88" y="128" width="9" height="12" rx="2" fill="#fff" opacity="0.09"/>
  <rect x="108" y="128" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.28"/>
  <rect x="128" y="128" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.22"/>
  <rect x="148" y="128" width="9" height="12" rx="2" fill="#fff" opacity="0.1"/>
  <rect x="168" y="128" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.18"/>
  <rect x="188" y="128" width="9" height="12" rx="2" fill="#7c6af7" opacity="0.28"/>
  <rect x="208" y="128" width="9" height="12" rx="2" fill="#00d4aa" opacity="0.22"/>
  <rect x="130" y="147" width="35" height="18" rx="2" fill="#0d1526"/>
  <rect x="132" y="149" width="31" height="16" rx="2" fill="#192640"/>
  <circle cx="153" cy="158" r="1.5" fill="#00d4aa" opacity="0.5"/>
  <polygon points="147,50 55,72 240,72" fill="#0d1526"/>
  <polygon points="147,50 55,72 240,72" fill="none" stroke="#00d4aa" stroke-width="0.8" opacity="0.35"/>
  <rect x="138" y="43" width="18" height="9" fill="#0f1c30"/>
  <rect x="144" y="36" width="6" height="9" fill="#0f1c30"/>
  <rect x="146" y="28" width="2" height="9" fill="#00d4aa" opacity="0.65"/>
  <polygon points="147.5,28 157,32 147.5,36" fill="#00d4aa" opacity="0.75"/>
  <text x="147" y="68" text-anchor="middle" font-family="monospace" font-size="5.5" font-weight="bold" fill="#00d4aa" opacity="0.65">CVR COLLEGE OF ENGINEERING</text>

  <!-- ═══════════════════════════════════════════
       ROBOT — outline style, shifted right (cx=330)
       head + ears + visor + eyes + small smile
       neck + half body visible above ground
       ═══════════════════════════════════════════ -->
  <!-- Antenna stem -->
  <line x1="330" y1="14" x2="330" y2="28" stroke="#00d4aa" stroke-width="3" stroke-linecap="round"/>
  <!-- Antenna dot -->
  <circle cx="330" cy="10" r="5" fill="#00d4aa"/>

  <!-- HEAD -->
  <rect x="288" y="29" width="84" height="74" rx="24" fill="#070d1a" stroke="#00d4aa" stroke-width="3.5"/>

  <!-- EAR left -->
  <rect x="271" y="57" width="19" height="24" rx="7" fill="#070d1a" stroke="#00d4aa" stroke-width="3"/>
  <!-- EAR right -->
  <rect x="370" y="57" width="19" height="24" rx="7" fill="#070d1a" stroke="#00d4aa" stroke-width="3"/>

  <!-- VISOR -->
  <rect x="298" y="44" width="64" height="36" rx="9" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>

  <!-- Eye left -->
  <circle cx="315" cy="62" r="8.5" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>
  <circle cx="315" cy="62" r="3.5" fill="#00d4aa" opacity="0.9"/>
  <!-- Eye right -->
  <circle cx="345" cy="62" r="8.5" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>
  <circle cx="345" cy="62" r="3.5" fill="#00d4aa" opacity="0.9"/>

  <!-- SMILE — small subtle arc -->
  <path d="M316 90 Q330 97 344 90" stroke="#00d4aa" stroke-width="2.8" fill="none" stroke-linecap="round"/>

  <!-- NECK — centered at 330 -->
  <rect x="322" y="103" width="16" height="16" rx="4" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>

  <!-- HALF BODY — inverted U shape, two legs + rounded top arc -->
  <!-- Left leg -->
  <line x1="293" y1="163" x2="293" y2="140" stroke="#00d4aa" stroke-width="3.5" stroke-linecap="round"/>
  <!-- Right leg -->
  <line x1="367" y1="163" x2="367" y2="140" stroke="#00d4aa" stroke-width="3.5" stroke-linecap="round"/>
  <!-- Top arc connecting both legs -->
  <path d="M293 140 Q293 119 330 119 Q367 119 367 140"
        fill="none" stroke="#00d4aa" stroke-width="3.5" stroke-linecap="round"/>

  <!-- Chat bubble (right) -->
  <rect x="390" y="36" width="82" height="30" rx="7" fill="url(#vg)" opacity="0.9"/>
  <polygon points="394,66 402,66 397,74" fill="#4f3fbc" opacity="0.9"/>
  <text x="431" y="50" text-anchor="middle" font-family="monospace" font-size="7" fill="#fff" font-weight="bold">Hello! Ask me</text>
  <text x="431" y="60" text-anchor="middle" font-family="monospace" font-size="6" fill="rgba(255,255,255,0.75)">anything about CVR</text>

  <!-- User bubble (left) -->
  <rect x="18" y="48" width="66" height="26" rx="7" fill="#0f1c30" stroke="#00d4aa" stroke-width="0.7" opacity="0.85"/>
  <polygon points="52,74 60,74 56,82" fill="#0f1c30"/>
  <text x="51" y="61" text-anchor="middle" font-family="monospace" font-size="6" fill="#00d4aa">Fees? Hostel?</text>
  <text x="51" y="69" text-anchor="middle" font-family="monospace" font-size="6" fill="#7a90b0">Placements?</text>
  <circle cx="261" cy="48" r="3.5" fill="#7c6af7" opacity="0.55"/>
  <circle cx="251" cy="63" r="2.5" fill="#00d4aa" opacity="0.45"/>
  <circle cx="272" cy="65" r="2" fill="#7c6af7" opacity="0.38"/>
</svg>"""

HOME_SVG = """<svg viewBox="0 0 660 64" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0d1526"/><stop offset="100%" stop-color="#111e35"/></linearGradient>
    <linearGradient id="htl" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#00d4aa"/><stop offset="100%" stop-color="#0099aa"/></linearGradient>
  </defs>
  <rect width="660" height="64" fill="url(#hbg)"/>
  <line x1="0" y1="32" x2="90" y2="32" stroke="#00d4aa" stroke-width="0.5" opacity="0.18"/>
  <line x1="570" y1="32" x2="660" y2="32" stroke="#00d4aa" stroke-width="0.5" opacity="0.18"/>
  <circle cx="90" cy="32" r="1.5" fill="#00d4aa" opacity="0.28"/>
  <circle cx="570" cy="32" r="1.5" fill="#00d4aa" opacity="0.28"/>
  <rect x="108" y="16" width="48" height="38" fill="#192640"/>
  <rect x="113" y="22" width="8" height="9" rx="1" fill="#00d4aa" opacity="0.28"/>
  <rect x="125" y="22" width="8" height="9" rx="1" fill="#7c6af7" opacity="0.28"/>
  <rect x="137" y="22" width="8" height="9" rx="1" fill="#00d4aa" opacity="0.2"/>
  <rect x="113" y="35" width="8" height="9" rx="1" fill="#7c6af7" opacity="0.22"/>
  <rect x="125" y="35" width="8" height="9" rx="1" fill="#00d4aa" opacity="0.28"/>
  <rect x="120" y="49" width="16" height="5" rx="1" fill="#0d1526"/>
  <polygon points="132,10 108,16 156,16" fill="#111e35"/>
  <rect x="130" y="5" width="4" height="6" fill="#111e35"/>
  <rect x="131" y="2" width="2" height="4" fill="#00d4aa" opacity="0.55"/>
  <text x="330" y="26" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#00d4aa" letter-spacing="3">CVR COLLEGE OF ENGINEERING</text>
  <text x="330" y="42" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#7a90b0" letter-spacing="2">Ibrahimpatnam · Hyderabad · Est. 2001 · NAAC A</text>
  <rect x="215" y="46" width="230" height="1.5" rx="1" fill="url(#htl)" opacity="0.4"/>
  <rect x="506" y="18" width="28" height="30" rx="7" fill="url(#htl)" opacity="0.8"/>
  <rect x="510" y="22" width="20" height="15" rx="3" fill="#070d1a"/>
  <rect x="513" y="26" width="5" height="4" rx="1.5" fill="#00d4aa" opacity="0.85"/>
  <rect x="522" y="26" width="5" height="4" rx="1.5" fill="#00d4aa" opacity="0.85"/>
  <path d="M513 36 Q520 39.5 527 36" stroke="#00d4aa" stroke-width="1.3" fill="none" stroke-linecap="round"/>
  <rect x="503" y="26" width="4" height="9" rx="2" fill="url(#htl)" opacity="0.65"/>
  <rect x="537" y="26" width="4" height="9" rx="2" fill="url(#htl)" opacity="0.65"/>
  <rect x="511" y="47" width="7" height="9" rx="3" fill="url(#htl)" opacity="0.65"/>
  <rect x="522" y="47" width="7" height="9" rx="3" fill="url(#htl)" opacity="0.65"/>
  <rect x="519" y="12" width="2.5" height="7" rx="1" fill="#00d4aa" opacity="0.65"/>
  <circle cx="520" cy="10" r="3" fill="none" stroke="#00d4aa" stroke-width="1" opacity="0.55"/>
  <circle cx="520" cy="10" r="1.2" fill="#00d4aa"/>
  <rect x="0" y="62" width="660" height="2" fill="url(#htl)" opacity="0.15"/>
</svg>"""

CHAT_SVG = """<svg viewBox="0 0 660 44" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;">
  <rect width="660" height="44" fill="#0d1526"/>
  <line x1="0" y1="22" x2="130" y2="22" stroke="#00d4aa" stroke-width="0.5" opacity="0.13"/>
  <line x1="530" y1="22" x2="660" y2="22" stroke="#00d4aa" stroke-width="0.5" opacity="0.13"/>
  <circle cx="130" cy="22" r="1.5" fill="#00d4aa" opacity="0.22"/>
  <circle cx="530" cy="22" r="1.5" fill="#00d4aa" opacity="0.22"/>
  <rect x="308" y="8" width="28" height="26" rx="7" fill="rgba(0,212,170,0.12)" stroke="#00d4aa" stroke-width="0.7" opacity="0.55"/>
  <rect x="311" y="12" width="22" height="14" rx="3" fill="#070d1a"/>
  <rect x="314" y="15" width="5" height="4" rx="1.5" fill="#00d4aa" opacity="0.8"/>
  <rect x="324" y="15" width="5" height="4" rx="1.5" fill="#00d4aa" opacity="0.8"/>
  <path d="M314 23 Q322 27 330 23" stroke="#00d4aa" stroke-width="1.2" fill="none" stroke-linecap="round"/>
  <circle cx="258" cy="17" r="2" fill="#7c6af7" opacity="0.38"/>
  <circle cx="274" cy="27" r="2" fill="#00d4aa" opacity="0.32"/>
  <circle cx="290" cy="15" r="1.5" fill="#7c6af7" opacity="0.28"/>
  <circle cx="402" cy="19" r="2" fill="#00d4aa" opacity="0.38"/>
  <circle cx="386" cy="28" r="2" fill="#7c6af7" opacity="0.32"/>
  <circle cx="372" cy="14" r="1.5" fill="#00d4aa" opacity="0.28"/>
  <rect x="0" y="42" width="660" height="2" fill="#00d4aa" opacity="0.07"/>
</svg>"""

# ── Helpers ──
def top_strip(back=False):
    if back:
        c1, c2, c3 = st.columns([0.45, 2.2, 0.85], gap='small')
        with c1:
            if st.button("◀", key="top_back_btn", help="Back to landing", use_container_width=False):
                go("landing")
            components.html("""
            <style>
            button[kind='primary'] { margin: 0 !important; }
            #top_back_btn > button { margin: 0px !important; padding: 4px 8px !important; }
            </style>
            """, height=0)
        with c2:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:0.35rem; margin-left:-10px;">
              <div class="bico" style="width:40px;height:40px;border-radius:10px;font-size:14px;">IRA</div>
              <div><div class="bname">CVR AI Assistant</div><div class="btag">Campus Intelligence · CVRCE</div></div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="opill" style="justify-content:center;"> <div class="odot"></div>Online </div>
            """, unsafe_allow_html=True)

        components.html("""
        <script>
        const btn = [...document.querySelectorAll('button')].find(b => b.innerText.trim() === '◀');
        if (btn) {
            btn.style.width = '34px';
            btn.style.height = '34px';
            btn.style.padding = '0';
            btn.style.background = 'rgba(255,255,255,0.1)';
            btn.style.color = 'white';
            btn.style.border = '1px solid rgba(255,255,255,0.22)';
            btn.style.borderRadius = '11px';
            btn.style.boxShadow = '0 8px 20px rgba(0,0,0,0.32)';
            btn.style.fontSize = '1.05rem';
            btn.style.fontWeight = '700';
            btn.style.lineHeight = '1';
            btn.style.minWidth = '34px';
        }
        </script>
        """, height=0)
        return

    st.markdown("""
    <div class="top-strip">
      <div class="tbrand">
        <div class="bico">IRA</div>
        <div><div class="bname">CVR AI Assistant</div><div class="btag">Campus Intelligence · CVRCE</div></div>
      </div>
      <div class="opill"><div class="odot"></div>Online</div>
    </div>""", unsafe_allow_html=True)

def page_hdr(title, sub="", back=False):
    user = st.session_state.user
    init  = user["full_name"][0].upper() if user else "U"
    uname = user["full_name"] if user else ""
    email = user.get("email", "") if user else ""
    roll = email.split("@")[0].upper() if "@" in email else (email.upper() if email else "N/A")
    
    back_h = "<span id='back-arrow-id' style='cursor:pointer; padding-right:0.5rem;color:var(--text3);font-size:0.85rem;margin-right:0.2rem;'>◀</span>" if back else ""
    
    dropdown_html = f"""
<div class="prof-drop">
<div class="pd-hdr">
<div class="pd-av">{init}</div>
<div>
<div class="pd-name">{uname}</div>
<div class="pd-email">{email}</div>
</div>
</div>
<div class="pd-body">
<div class="pd-row"><span>ID / Roll No</span><strong>{roll}</strong></div>
<div class="pd-row"><span>Branch</span><strong>B.Tech - CSE</strong></div>
<div class="pd-row"><span>Year</span><strong>3rd Year</strong></div>
</div>
<div class="pd-logout" id="prof-logout-id">
<span style="display:inline-block; margin-right:0.4rem; vertical-align:middle;">🚪</span> Sign Out
</div>
</div>
"""

    hdr_html = f"""
<div class="hdr">
{back_h}
<div class="bico" style="width:32px;height:32px;border-radius:8px;font-size:11px;">IRA</div>
<div>
<div style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;">{title}</div>
<div style="font-size:0.67rem;color:var(--text3);">{sub}</div>
</div>
<div class="hdr-r" style="overflow:visible;">
<div class="upill-wrapper" tabindex="0">
<div class="upill"><div class="uav">{init}</div>{uname}</div>
{dropdown_html}
</div>
</div>
</div>
"""
    st.markdown(hdr_html, unsafe_allow_html=True)
    
    if back:
        st.markdown("<div class='hidden-btn-marker'></div>", unsafe_allow_html=True)
        if st.button("back_btn_123", key=f"hdr_bk_{title}"): go("home")
        
    st.markdown("<div class='hidden-btn-marker'></div>", unsafe_allow_html=True)
    if st.button("logout_btn_123", key=f"hdr_lo_{title}"):
        st.session_state.user = None
        st.session_state.messages = []
        go("landing")
    
    import streamlit.components.v1 as components
    components.html("""
    <script>
    function setupHandlers() {
        const doc = window.parent.document;
        
        // Setup Logout
        const logoutDiv = doc.getElementById('prof-logout-id');
        if (logoutDiv && !logoutDiv.dataset.wired) {
            logoutDiv.dataset.wired = "1";
            logoutDiv.addEventListener('click', () => {
                doc.querySelectorAll("button").forEach(b => {
                    if(b.innerText.includes("logout_btn_123")) b.click();
                });
            });
        }
        
        // Setup Back
        const backArrow = doc.getElementById('back-arrow-id');
        if (backArrow && !backArrow.dataset.wired) {
            backArrow.dataset.wired = "1";
            backArrow.addEventListener('click', () => {
                doc.querySelectorAll("button").forEach(b => {
                    if(b.innerText.includes("back_btn_123")) b.click();
                });
            });
        }
        
        // Setup Chips
        const chipsCount = doc.querySelectorAll('.qc').length;
        if(chipsCount > 0) {
            doc.querySelectorAll('.qc').forEach(chip => {
                if(!chip.dataset.wired) {
                    chip.dataset.wired = "1";
                    chip.addEventListener('click', () => {
                        const chipText = chip.innerText.trim();
                        doc.querySelectorAll("button").forEach(b => {
                            if(b.innerText.includes(`chip_btn_123_${chipText}`)) b.click();
                        });
                    });
                }
            });
        }

        setTimeout(setupHandlers, 500);
    }
    setupHandlers();
    </script>
    """, height=0)

def format_msg(role, text, ts=""):
    user = st.session_state.user
    av = (user["full_name"][0].upper() if user else "U") if role == "user" else "AI"
    return f"""
    <div class="mr {role}">
      <div class="mav">{av}</div>
      <div class="bbl-wrap"><div class="bbl">{text}</div><div class="mts">{ts}</div></div>
    </div>"""
# ══════════════════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    top_strip()
    st.markdown("""
    <div class="hero">
      <div class="hbadge"><span class="hlive"></span>AI Powered · NAAC A Grade</div>
      <h1 class="htitle">Smart Campus<br><span class="hteal">AI Assistant</span></h1>
      <p class="hsub">Instant answers on admissions, fees, placements, hostel &amp; more — from CVR's own knowledge base.</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='illus-wrap' style='max-width:500px;margin:0 auto 1.25rem;'>", unsafe_allow_html=True)
    st.markdown(LANDING_SVG, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='awrap'>", unsafe_allow_html=True)
    st.markdown("<div class='acard'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.68rem;color:var(--text3);text-align:center;margin-bottom:1rem;letter-spacing:0.05em;text-transform:uppercase;font-weight:600;'>Get Started</div>", unsafe_allow_html=True)
    st.markdown("<div class='bp'>", unsafe_allow_html=True)
    if st.button("🔐  Sign in", use_container_width=True):
        go("login")
    st.markdown("</div><div class='divl'>or</div><div class='bg'>", unsafe_allow_html=True)
    if st.button("✏️  Create account", use_container_width=True):
        go("signup")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:0.7rem;color:var(--text3);margin-top:0.9rem;'>Admissions · Fees · Placements · Hostel · Faculty</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    page_hdr("CVR Assistant", "Ask anything about campus", back=True)
    st.markdown("<div style='max-width:400px;margin:1.5rem auto 0;padding:0 1rem;'>", unsafe_allow_html=True)
    st.markdown("""
      <div style="text-align:center;margin-bottom:1.25rem;">
        <div class="bico" style="width:50px;height:50px;border-radius:13px;font-size:17px;margin:0 auto 0.8rem;">IRA</div>
        <h2 style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;letter-spacing:-0.02em;margin:0 0 0.2rem;">Welcome back</h2>
        <p style="font-size:0.82rem;color:var(--text2);">Sign in to your CVR account</p>
      </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='acard'>", unsafe_allow_html=True)
    email    = st.text_input("Email address", placeholder="you@cvr.ac.in", key="li_e")
    password = st.text_input("Password", placeholder="Enter your password", type="password", key="li_p")

    if "li_error" not in st.session_state:
        st.session_state.li_error = ""
    if st.session_state.li_error:
        st.markdown(f"<div class='al ae'>{st.session_state.li_error}</div>", unsafe_allow_html=True)

    st.markdown("<div class='bp' style='margin-top:0.4rem;'>", unsafe_allow_html=True)
    if st.button("Sign in →", use_container_width=True, key="li_signin"):
        if email and password:
            st.session_state.li_error = ""
            real_name = st.session_state.users_db.get(email, email.split("@")[0].capitalize())
            st.session_state.user = {"email": email, "full_name": real_name}
            go("home")
        else:
            st.session_state.li_error = "Please fill in all fields."
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)  # closes bp

    st.markdown("</div>", unsafe_allow_html=True)  # closes acard

    st.markdown("<div class='divl'>No account?</div>", unsafe_allow_html=True)

    st.markdown("<div class='bg'>", unsafe_allow_html=True)
    if st.button("Create account", use_container_width=True, key="li_signup"):
        go("signup")
    st.markdown("</div>", unsafe_allow_html=True)  # closes bg

    st.markdown("</div>", unsafe_allow_html=True)  # closes outer wrapper

# ══════════════════════════════════════════════════════════════════
# SIGNUP
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "signup":

    page_hdr("CVR Assistant", "Ask anything about campus", back=True)

    st.markdown(
        "<div style='max-width:400px;margin:1.5rem auto 0;padding:0 1rem;'>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="text-align:center;margin-bottom:1.25rem;">
        <div class="bico" style="width:50px;height:50px;border-radius:13px;font-size:17px;margin:0 auto 0.8rem;">IRA</div>
        <h2 style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;letter-spacing:-0.02em;margin:0 0 0.2rem;">Create account</h2>
        <p style="font-size:0.82rem;color:var(--text2);">Join CVR AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='acard'>", unsafe_allow_html=True)

    name = st.text_input("Full Name", placeholder="Your full name", key="su_n")
    email = st.text_input("Email address", placeholder="you@cvr.ac.in", key="su_e")
    password = st.text_input("Password", placeholder="Create a strong password", type="password", key="su_p")

    if "su_error" not in st.session_state:
        st.session_state.su_error = ""
    if "su_success" not in st.session_state:
        st.session_state.su_success = ""

    if st.session_state.su_error:
        st.markdown(f"<div class='al ae'>{st.session_state.su_error}</div>", unsafe_allow_html=True)
    if st.session_state.su_success:
        st.markdown(f"<div class='al ao'>{st.session_state.su_success}</div>", unsafe_allow_html=True)

    if st.button("Create account →", use_container_width=True, key="btn_signup"):
        if name and email and password:
            st.session_state.users_db[email] = name
            st.session_state.user = {"email": email, "full_name": name}
            st.session_state.su_success = "Account created! Signing you in…"
            st.session_state.su_error = ""
            go("home")
        else:
            st.session_state.su_error = "Please fill in all fields."
            st.session_state.su_success = ""

    st.markdown("</div>", unsafe_allow_html=True)  # ← closes acard

    # ↓ These are now correctly OUTSIDE the card
    st.markdown("<div class='divl'>Already have an account?</div>", unsafe_allow_html=True)

    if st.button("Sign in", use_container_width=True, key="btn_signin"):
        go("login")

    st.markdown("</div>", unsafe_allow_html=True)  # ← closes outer wrapper

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "home":
    if not st.session_state.user:
        go("landing")
    user  = st.session_state.user
    name  = user["full_name"]
    today = datetime.now().strftime("%A, %d %B %Y")
    init  = name[0].upper()
    page_hdr("CVR AI Assistant", "Campus Intelligence")
    st.markdown(HOME_SVG, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="gbnd">
      <h2 style="font-family:'Syne',sans-serif;font-size:1.42rem;font-weight:800;letter-spacing:-0.02em;margin:0 0 0.18rem;">
        Good day, <span style="color:var(--teal);">{name}</span> 👋
      </h2>
      <div style="font-size:0.72rem;color:var(--text3);">{today}</div>
      <div style="font-size:0.68rem;color:var(--text3);text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin:0.9rem 0 0.45rem;">You can ask about</div>
      <div class="cg">
        <div class="tc">💰 Fees</div><div class="tc">💼 Placements</div><div class="tc">🏠 Hostel</div>
        <div class="tc">📋 Admissions</div><div class="tc">🏫 Departments</div><div class="tc">📚 Academics</div>
      </div>
    </div>
    <div style="max-width:660px;margin:0 auto;padding:1.25rem;">
    """, unsafe_allow_html=True)

    # FIX 1: st.columns(3) = native Streamlit side-by-side — guaranteed to work
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='bp'>", unsafe_allow_html=True)
        if st.button("💬  Open Chatbot", use_container_width=True, key="hm_chat"):
            go("chatbot")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='bg'>", unsafe_allow_html=True)
        if st.button("📜  Chat History", use_container_width=True, key="hm_hist"):
            go("history")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='bd'>", unsafe_allow_html=True)
        if st.button("🚪  Sign out", use_container_width=True, key="hm_out"):
            st.session_state.user = None
            st.session_state.messages = []
            go("landing")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CHATBOT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "chatbot":
    if not st.session_state.user:
        go("landing")
    user = st.session_state.user
    page_hdr("CVR Assistant", "Ask anything about campus", back=True)
    
    # Render all messages concatenated into the scrolling container
    html_msgs = "<div class='chat-footer-marker' style='display:none;'></div>" # Activates app CSS
    html_msgs += "<div class='msgs-container' id='msgs-scroller'>"
    if not st.session_state.messages:
        html_msgs += """
        <div class="ec">
          <svg width="100" height="110" viewBox="0 0 100 110" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Antenna stem -->
            <line x1="50" y1="4" x2="50" y2="16" stroke="#00d4aa" stroke-width="2.5" stroke-linecap="round"/>
            <!-- Antenna dot -->
            <circle cx="50" cy="4" r="4" fill="#00d4aa"/>
            <!-- HEAD — big rounded rect -->
            <rect x="12" y="16" width="76" height="68" rx="22" fill="#070d1a" stroke="#00d4aa" stroke-width="3.2"/>
            <!-- EAR left -->
            <rect x="3" y="38" width="11" height="20" rx="5" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>
            <!-- EAR right -->
            <rect x="86" y="38" width="11" height="20" rx="5" fill="#070d1a" stroke="#00d4aa" stroke-width="2.8"/>
            <!-- VISOR -->
            <rect x="22" y="28" width="56" height="34" rx="9" fill="#070d1a" stroke="#00d4aa" stroke-width="2.6"/>
            <!-- Eye left -->
            <circle cx="38" cy="45" r="8" fill="#070d1a" stroke="#00d4aa" stroke-width="2.6"/>
            <circle cx="38" cy="45" r="3.5" fill="#00d4aa" opacity="0.9"/>
            <!-- Eye right -->
            <circle cx="62" cy="45" r="8" fill="#070d1a" stroke="#00d4aa" stroke-width="2.6"/>
            <circle cx="62" cy="45" r="3.5" fill="#00d4aa" opacity="0.9"/>
            <!-- Small smile -->
            <path d="M40 72 Q50 79 60 72" stroke="#00d4aa" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          </svg>
          <p style="font-size:0.87rem;font-weight:600;color:var(--text2);margin-top:0.6rem;">Start a conversation</p>
          <p style="font-size:0.76rem;">Ask anything about CVR College</p>
        </div>"""
    else:
        for msg in st.session_state.messages:
            html_msgs += format_msg(msg["role"], msg["text"], msg.get("ts", ""))
    html_msgs += "</div>"
    st.markdown(html_msgs, unsafe_allow_html=True)
    
    # CSS Classes for 3-Section Layout Constraints
    st.markdown("""<style>
/* Chatbot Structure */
.chat-fixed-header { flex-shrink: 0 !important; z-index: 1100; background: var(--bg); padding-top: 1rem; }
.chat-scroll-area { flex: 1 1 0 !important; overflow-y: auto !important; overflow-x: hidden !important; min-height: 0; }
.chat-fixed-footer { flex-shrink: 0 !important; z-index: 1000; background: var(--bg); padding: 0.5rem 0.5rem 1rem; border-top: 1px solid var(--bdr); margin-top:0.4rem; }
header[data-testid="stHeader"] { display: none !important; }

/* Inlined Chat Input Row */
.input-row {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 8px !important;
  width: 100%;
}
.input-field {
  flex: 1 !important;
  min-width: 0 !important;
  width: auto !important;
}
.send-button {
  flex-shrink: 0 !important;
  width: auto !important;
  flex-grow: 0 !important;
}
.send-button button {
  width: auto !important;
  padding: 10px 24px !important;
  white-space: nowrap !important;
  display: inline-flex !important;
}
</style>""", unsafe_allow_html=True)
    
    st.markdown("<div id='chatbot-page-marker' style='display:none;'></div>", unsafe_allow_html=True)
    import streamlit.components.v1 as components
    components.html("""
    <script>
        function applyChatLayout() {
            const doc = window.parent.document;
            const isChatActive = doc.getElementById('chatbot-page-marker');
            if(!isChatActive) return;
            
            doc.body.style.overflow = 'hidden';
            doc.documentElement.style.overflow = 'hidden';
            
            const appView = doc.querySelector('[data-testid="stAppViewContainer"]');
            if(appView) {
                appView.style.height = '100vh';
                appView.style.overflow = 'hidden';
                appView.style.display = 'flex';
                appView.style.flexDirection = 'column';
            }
            
            const block = doc.querySelector('.block-container');
            if(block) {
                block.style.flex = '1 1 0';
                block.style.display = 'flex';
                block.style.flexDirection = 'column';
                block.style.overflow = 'hidden';
                block.style.padding = '0 0.5rem';
            }
            
            const hdr = doc.querySelector('.hdr');
            if(hdr) {
                const hCont = hdr.closest('.element-container');
                if(hCont && !hCont.classList.contains('chat-fixed-header')) {
                    hCont.classList.add('chat-fixed-header');
                }
            }
            
            const msgs = doc.getElementById('msgs-scroller');
            if(msgs) {
                const mCont = msgs.closest('.element-container');
                if(mCont && !mCont.classList.contains('chat-scroll-area')) {
                    mCont.classList.add('chat-scroll-area');
                }
                
                const count = msgs.children.length;
                if(msgs.dataset.mCount !== String(count)) {
                    msgs.scrollTop = msgs.scrollHeight;
                    msgs.dataset.mCount = count;
                }
            }
            
            const footers = doc.querySelectorAll('.chat-footer-marker');
            if(footers.length > 0) {
                let fBlock = footers[footers.length - 1].closest('div[data-testid="stVerticalBlock"]');
                if(fBlock && fBlock !== block) {
                    const fCont = fBlock.closest('.element-container');
                    if(fCont && !fCont.classList.contains('chat-fixed-footer')) {
                        fCont.classList.add('chat-fixed-footer');
                    }
                }
            }
            
            const hBlocks = doc.querySelectorAll('div[data-testid="stHorizontalBlock"]');
            if(hBlocks.length > 0) {
                const hBlock = hBlocks[hBlocks.length - 1];
                if(!hBlock.classList.contains('input-row')) hBlock.classList.add('input-row');
                
                const cols = hBlock.querySelectorAll('div[data-testid="column"]');
                if(cols.length >= 2) {
                    if(!cols[0].classList.contains('input-field')) cols[0].classList.add('input-field');
                    if(!cols[1].classList.contains('send-button')) cols[1].classList.add('send-button');
                }
            }
            
            setTimeout(applyChatLayout, 100);
        }
        applyChatLayout();
    </script>
    """, height=0)
    
    footer = st.container()
    with footer:
        st.markdown("<div class='chat-footer-marker' style='display:none;'></div>", unsafe_allow_html=True)
        chips = ["Fees", "Placements", "Hostel", "Admissions", "Faculty", "Departments"]
        chips_html = "<div class='qbar' style='border:none; padding:0 0 0.6rem 0;'>" + "".join([f"<span class='qc'>{c}</span>" for c in chips]) + "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)
        
        for chip in chips:
            st.markdown("<div class='hidden-btn-marker'></div>", unsafe_allow_html=True)
            if st.button(f"chip_btn_123_{chip}", key=f"hdn_chip_{chip}"):
                ts = now_str()
                st.session_state.messages.append({"role":"user","text":chip,"ts":ts})
                st.session_state.messages.append({"role":"bot","text":get_answer(chip.lower()),"ts":now_str()})
                st.rerun()

        def submit_chat_msg():
            val = st.session_state.ci
            if val and val.strip():
                st.session_state.messages.append({"role": "user", "text": val, "ts": now_str()})
                st.session_state.messages.append({"role": "bot", "text": get_answer(val), "ts": now_str()})
                st.session_state.ci = "" # Natively clear the input

        st.markdown("<div class='iz' style='padding:0; border:none;'>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.text_input("", placeholder="Ask anything about CVR…", key="ci", on_change=submit_chat_msg, label_visibility="collapsed")
        with col2:
            st.button("✈  Send", on_click=submit_chat_msg)
            
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user:
        go("landing")
    msgs  = st.session_state.messages
    count = len(msgs)
    user  = st.session_state.user
    init  = user["full_name"][0].upper() if user else "U"
    uname = user["full_name"] if user else ""
    email = user.get("email", "") if user else ""
    roll  = email.split("@")[0].upper() if "@" in email else (email.upper() if email else "N/A")

    # Full dropdown — identical to page_hdr
    dropdown_html = f"""
<div class="prof-drop">
<div class="pd-hdr"><div class="pd-av">{init}</div>
<div><div class="pd-name">{uname}</div><div class="pd-email">{email}</div></div></div>
<div class="pd-body">
<div class="pd-row"><span>ID / Roll No</span><strong>{roll}</strong></div>
<div class="pd-row"><span>Branch</span><strong>B.Tech - CSE</strong></div>
<div class="pd-row"><span>Year</span><strong>3rd Year</strong></div>
</div>
<div class="pd-logout" id="prof-logout-id"><span style="display:inline-block;margin-right:0.4rem;vertical-align:middle;">🚪</span> Sign Out</div>
</div>"""

    st.markdown(f"""
    <div class="hdr">
      <span id='back-arrow-id' style='cursor:pointer;color:var(--text3);font-size:0.85rem;margin-right:0.4rem;'>◀</span>
      <div class="bico" style="width:32px;height:32px;border-radius:8px;font-size:11px;">IRA</div>
      <div><div style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;">Chat History</div>
        <div style="font-size:0.67rem;color:var(--text3);">{count} message{"s" if count!=1 else ""}</div></div>
      <div class="hdr-r" style="overflow:visible;">
        <div class="upill-wrapper" tabindex="0">
          <div class="upill"><div class="uav">{init}</div>{uname}</div>
          {dropdown_html}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Hidden back + logout buttons
    st.markdown("<div class='hidden-btn-marker'></div>", unsafe_allow_html=True)
    if st.button("back_btn_123", key="history_back"):
        go("home")
    st.markdown("<div class='hidden-btn-marker'></div>", unsafe_allow_html=True)
    if st.button("logout_btn_123", key="history_logout"):
        st.session_state.user = None
        st.session_state.messages = []
        go("landing")

    components.html("""
    <script>
    function setupHandlers() {
        const doc = window.parent.document;
        const backArrow = doc.getElementById('back-arrow-id');
        if (backArrow && !backArrow.dataset.wired) {
            backArrow.dataset.wired = "1";
            backArrow.addEventListener('click', () => { doc.querySelectorAll("button").forEach(b => { if(b.innerText.includes("back_btn_123")) b.click(); }); });
        }
        const logoutDiv = doc.getElementById('prof-logout-id');
        if (logoutDiv && !logoutDiv.dataset.wired) {
            logoutDiv.dataset.wired = "1";
            logoutDiv.addEventListener('click', () => { doc.querySelectorAll("button").forEach(b => { if(b.innerText.includes("logout_btn_123")) b.click(); }); });
        }
        setTimeout(setupHandlers, 500);
    }
    setupHandlers();
    </script>""", height=0)

    st.markdown("<div style='padding:1rem 1.25rem;max-width:760px;margin:0 auto;'>", unsafe_allow_html=True)
    if not msgs:
        st.markdown("""<div style="text-align:center;padding:3.5rem 2rem;color:var(--text3);">
          <div style="font-size:2.2rem;margin-bottom:0.65rem;opacity:0.22;">📜</div>
          <p style="font-size:0.85rem;">No history yet — start a conversation first.</p>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in msgs:
            label = "You" if msg["role"] == "user" else "Bot"
            ts_bit = f"<span style='font-size:0.62rem;color:var(--text3);margin-left:0.45rem;'>{msg.get('ts','')}</span>" if msg.get('ts') else ""
            st.markdown(f'<div class="hl"><span class="hr {msg["role"]}">{label}</span><div><span class="ht">{msg["text"]}</span>{ts_bit}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 1.25rem 1.25rem;max-width:760px;margin:0 auto;'>", unsafe_allow_html=True)
    st.markdown("<div class='bd'>", unsafe_allow_html=True)
    if st.button("🗑️  Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PROFILE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    if not st.session_state.user:
        go("landing")
    user = st.session_state.user
    name = user["full_name"] if user else ""
    email = user.get("email", "") if user else ""
    roll = email.split("@")[0].upper() if "@" in email else (email.upper() if email else "N/A")
    init = name[0].upper() if name else "U"
    
    page_hdr("Student Profile", "Academic & Personal Details", back=True)
    import textwrap
    style_html = """
    <style>
    .pcard { background:var(--bg2); border:1px solid var(--bdr); border-radius:var(--r-xl); padding:2rem; margin-top:1.5rem; text-align:center; position:relative; overflow:hidden; }
    .pcard::before { content:''; position:absolute; top:0; left:0; width:100%; height:80px; background:linear-gradient(135deg,rgba(0,212,170,0.15),rgba(124,106,247,0.15)); border-bottom:1px solid var(--bdr); z-index:0; }
    .pav { width:86px; height:86px; border-radius:50%; background:linear-gradient(135deg,#00d4aa,#0099aa); display:inline-flex; align-items:center; justify-content:center; font-size:2.5rem; font-weight:800; color:#070d1a; border:4px solid var(--bg2); position:relative; z-index:1; margin-top:20px; text-shadow:none; }
    .pti { font-family:'Space Grotesk',sans-serif; font-size:1.4rem; font-weight:700; margin:1rem 0 0.2rem; letter-spacing:0.04em; }
    .psu { color:var(--text2); font-size:0.85rem; letter-spacing:0.02em; }
    .pbdg { display:inline-flex; align-items:center; gap:0.4rem; background:rgba(124,106,247,0.12); border:1px solid rgba(124,106,247,0.28); color:#a89cf7; border-radius:100px; padding:0.2rem 0.75rem; font-size:0.7rem; font-weight:700; margin-top:0.8rem; text-transform:uppercase; letter-spacing:0.05em; }
    
    .stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-top:1.5rem; text-align:left; }
    .stat-box { background:var(--bg3); border:1px solid var(--bdr); border-radius:12px; padding:1rem; }
    .slbl { font-size:0.65rem; color:var(--text3); text-transform:uppercase; letter-spacing:0.05em; font-weight:700; margin-bottom:0.3rem; }
    .sval { font-size:1.1rem; font-weight:700; color:var(--text); font-family:'Syne',sans-serif; }
    .sico { float:right; opacity:0.3; }
    
    .inf-row { display:flex; justify-content:space-between; padding:0.9rem 0; border-bottom:1px solid var(--bdr); text-align:left; }
    .inf-row:last-child { border:none; padding-bottom:0; }
    .inf-l { color:var(--text2); font-size:0.85rem; }
    .inf-v { font-weight:600; font-size:0.85rem; text-align:right; }
    </style>
    """
    
    profile_html = f"""
<div style="padding:0 1.25rem 1.25rem; max-width:660px; margin:0 auto;">
  <div class="pcard">
    <div class="pav">{init}</div>
    <div class="pti">{name}</div>
    <div class="psu">{email}</div>
    <div class="pbdg">ID: {roll}</div>
    
    <div style="margin-top:1.5rem; background:var(--bg3); border:1px solid var(--bdr); border-radius:14px; padding:0.5rem 1.25rem;">
      <div class="inf-row"><span class="inf-l">Course</span><span class="inf-v">B.Tech - AIML</span></div>
      <div class="inf-row"><span class="inf-l">Year / Sem</span><span class="inf-v">3rd Year </span></div>
    </div>
  </div>
</div>
"""
    st.markdown(style_html + profile_html, unsafe_allow_html=True)