# -*- coding: utf-8 -*-
"""
მათბოტი — მათემატიკა VII სახელმძღვანელოს AI ასისტენტი
გაშვება:  python3 -m streamlit run app.py
"""
import json
import os
from pathlib import Path

import streamlit as st
from anthropic import Anthropic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import theme

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1200
TOP_K = 3
HISTORY_TURNS = 12

BOT_AVATAR = "assets/mathboti-hello.png"
BOT_THINKING = "assets/mathboti-thinking.png"
BOT_HAPPY = "assets/mathboti-happy.png"
PUPIL_AVATAR = "assets/pupil.png"

st.set_page_config(page_title="მათბოტი — მათემატიკა VII", page_icon=BOT_AVATAR, layout="centered")
st.markdown(theme.CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------ პაროლის კარიბჭე
def check_password():
    """პილოტის მარტივი დაცვა — ერთი საერთო პაროლი."""
    expected = os.environ.get("APP_PASSWORD") or st.secrets.get("APP_PASSWORD", "")
    if not expected:  # პაროლი არ არის დაყენებული — თავისუფალი შესვლა
        return True
    if st.session_state.get("auth_ok"):
        return True

    st.markdown(
        f'<div class="mb-head">{theme.mascot("hello", 52)}'
        f"<div><h1>მათბოტი</h1><p>მათემატიკა VII — ვმეცადინეობთ ერთად</p></div></div>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.info("ეს გვერდი პილოტის მონაწილეებისთვისაა. გთხოვ, შეიყვანე კოდი.")
    pw = st.text_input("კოდი", type="password", key="pw_input")
    if st.button("შესვლა"):
        if pw == expected:
            st.session_state.auth_ok = True
            st.rerun()
        else:
            st.error("კოდი არასწორია. სცადე კიდევ ერთხელ.")
    st.stop()


check_password()


@st.cache_resource
def load_kb():
    chunks = json.loads(Path("data/chunks.json").read_text(encoding="utf-8"))
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    matrix = vec.fit_transform([c["section_title"] + "\n" + c["text"] for c in chunks])
    return chunks, vec, matrix


@st.cache_resource
def load_system_prompt():
    return Path("system_prompt.md").read_text(encoding="utf-8")


def toc_string(chunks):
    return "\n".join(
        f"- [{c['section']}] {c['section_title']} (გვ. {c['page_start']}-{c['page_end']})" for c in chunks
    )


def retrieve(query, history_text, chunks, vec, matrix, k=TOP_K):
    q = vec.transform([query + "\n" + history_text[-500:]])
    sims = cosine_similarity(q, matrix)[0]
    return [chunks[i] for i in sims.argsort()[::-1][:k] if sims[i] > 0.02]


chunks, vec, matrix = load_kb()
SYSTEM = load_system_prompt()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "pending" not in st.session_state:
    st.session_state.pending = None

# ------------------------------------------------------------------ სათაური
mood = "thinking" if st.session_state.pending else ("happy" if st.session_state.stars >= 5 else "hello")
st.markdown(
    f'<div class="mb-head">{theme.mascot(mood, 52)}'
    f"<div><h1>მათბოტი</h1><p>მათემატიკა VII — ვმეცადინეობთ ერთად</p></div></div>",
    unsafe_allow_html=True,
)
st.write("")

# ------------------------------------------------------------------ გვერდითი პანელი
with st.sidebar:
    st.markdown("## წიგნის თავები")
    seen = {}
    for c in chunks:
        if 1 <= c["chapter"] <= 4:
            seen.setdefault(c["chapter"], 0)
            seen[c["chapter"]] += 1
    for i, name in enumerate(theme.CHAPTER_NAMES):
        bg, fg, track, fill = theme.CHAPTER_STYLE[i]
        st.markdown(
            f'<div class="mb-chapter" style="background:{bg}">'
            f'<p style="color:{fg}">{name}</p>'
            f'<div class="mb-bar" style="background:{track}"><div style="width:0%;background:{fill}"></div></div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="mb-stars"><p class="n">★ {st.session_state.stars}</p>'
        f'<p class="l">ვარსკვლავი მცდელობისთვის</p></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("ახალი საუბარი"):
        st.session_state.messages = []
        st.session_state.stars = 0
        st.rerun()

# ------------------------------------------------------------------ საუბარი
if not st.session_state.messages:
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(
            "გამარჯობა! მათბოტი ვარ და მეშვიდე კლასის მათემატიკაში დაგეხმარები.\n\n"
            "დამისვი კითხვა ნებისმიერ თემაზე — მაგალითად: "
            "**„ვერ გავიგე, რა არის რიცხვის მოდული“** ან **„დამეხმარე ამ ამოცანაში…“**"
        )

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=BOT_AVATAR if m["role"] == "assistant" else PUPIL_AVATAR):
        st.markdown(m["content"])
        if m.get("source"):
            st.markdown(f'<p class="mb-src">📖 {m["source"]}</p>', unsafe_allow_html=True)

# სწრაფი ღილაკები
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    cols = st.columns(len(theme.QUICK_ACTIONS))
    for col, label in zip(cols, theme.QUICK_ACTIONS):
        if col.button(label, key=f"qa_{label}"):
            st.session_state.pending = label
            st.rerun()

typed = st.chat_input("დაწერე შენი კითხვა ან პასუხი…")
query = st.session_state.pending or typed
st.session_state.pending = None

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=PUPIL_AVATAR):
        st.markdown(query)

    history_text = "\n".join(m["content"] for m in st.session_state.messages[-4:])
    hits = retrieve(query, history_text, chunks, vec, matrix)

    context = "\n\n".join(
        f"<section id='{h['id']}' title='{h['section_title']}' pages='{h['page_start']}-{h['page_end']}'>\n"
        f"{h['text']}\n</section>"
        for h in hits
    ) or "(რელევანტური სექცია ვერ მოიძებნა)"

    system = (
        SYSTEM
        + "\n\n## წიგნის სარჩევი\n" + toc_string(chunks)
        + "\n\n## მოძიებული სექციები ამ შეკითხვისთვის\n"
        + "პასუხი ააგე მხოლოდ ამ მასალაზე დაყრდნობით:\n\n" + context
    )

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"))
    api_messages = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-HISTORY_TURNS:]
    ]

    with st.chat_message("assistant", avatar=BOT_THINKING):
        placeholder = st.empty()
        answer = ""
        try:
            with client.messages.stream(
                model=MODEL, max_tokens=MAX_TOKENS, system=system, messages=api_messages
            ) as stream:
                for delta in stream.text_stream:
                    answer += delta
                    placeholder.markdown(answer + "▌")
            placeholder.markdown(answer)
        except Exception as e:
            answer = f"⚠️ ვერ დავუკავშირდი. შეამოწმე გასაღები. ({e})"
            placeholder.error(answer)

        source = ""
        if hits:
            h = hits[0]
            source = f"§{h['section']} — გვერდი {h['page_start']}"
            st.markdown(f'<p class="mb-src">📖 {source}</p>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer, "source": source})
    st.session_state.stars += 1
    st.rerun()
