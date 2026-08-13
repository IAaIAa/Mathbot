# -*- coding: utf-8 -*-
"""მათბოტის იერსახე: მასკოტი და ინტერფეისის სტილი."""

LAV_50, LAV_100, LAV_400, LAV_600, LAV_900 = "#EEEDFE", "#CECBF6", "#7F77DD", "#534AB7", "#26215C"
SAGE_100, SAGE_600, SAGE_900 = "#C0DD97", "#639922", "#173404"
PEACH_100, PEACH_400, PEACH_600 = "#F5C4B3", "#F0997B", "#993C1D"
SAND_50, SAND_200, INK = "#F7F5F0", "#E4E0D6", "#2C2C2A"


def mascot(mood: str = "hello", size: int = 44) -> str:
    """მათბოტი სამ განწყობაში: hello / thinking / happy."""
    if mood == "thinking":
        face = (
            f'<circle cx="38" cy="78" r="9" fill="#fff" stroke="{LAV_600}" stroke-width="2"/>'
            f'<circle cx="72" cy="78" r="9" fill="#fff" stroke="{LAV_600}" stroke-width="2"/>'
            f'<circle cx="38" cy="74" r="4" fill="{LAV_900}"/><circle cx="72" cy="74" r="4" fill="{LAV_900}"/>'
            f'<path d="M42 102 L68 102" fill="none" stroke="{LAV_900}" stroke-width="3" stroke-linecap="round"/>'
        )
    elif mood == "happy":
        face = (
            f'<path d="M29 80 Q38 69 47 80" fill="none" stroke="{LAV_900}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M63 80 Q72 69 81 80" fill="none" stroke="{LAV_900}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M38 98 Q55 114 72 98" fill="none" stroke="{LAV_900}" stroke-width="3" stroke-linecap="round"/>'
        )
    else:
        face = (
            f'<circle cx="38" cy="78" r="9" fill="#fff" stroke="{LAV_600}" stroke-width="2"/>'
            f'<circle cx="72" cy="78" r="9" fill="#fff" stroke="{LAV_600}" stroke-width="2"/>'
            f'<circle cx="40" cy="79" r="4" fill="{LAV_900}"/><circle cx="74" cy="79" r="4" fill="{LAV_900}"/>'
            f'<path d="M40 100 Q55 112 70 100" fill="none" stroke="{LAV_900}" stroke-width="3" stroke-linecap="round"/>'
        )
    h = int(size * 1.25)
    return (
        f'<svg width="{size}" height="{h}" viewBox="0 0 110 135" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="მათბოტი"><title>მათბოტი</title>'
        f'<polygon points="55,8 92,44 18,44" fill="{SAGE_100}" stroke="{SAGE_600}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<circle cx="55" cy="20" r="4" fill="{SAGE_900}"/>'
        f'<rect x="12" y="50" width="86" height="72" rx="12" fill="{LAV_100}" stroke="{LAV_600}" stroke-width="2.5"/>'
        f'<circle cx="22" cy="63" r="3.5" fill="{PEACH_400}"/><circle cx="88" cy="63" r="3.5" fill="{PEACH_400}"/>'
        f"{face}</svg>"
    )


CSS = f"""
<style>
.stApp {{ background: {SAND_50}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; max-width: 900px; }}

html, body, [class*="css"] {{ color: {INK}; }}

.mb-head {{ display:flex; align-items:center; gap:14px; margin-bottom:4px; }}
.mb-head h1 {{ font-size:26px; font-weight:600; margin:0; color:{LAV_900}; }}
.mb-head p {{ margin:0; font-size:14px; color:#6B6A65; }}

section[data-testid="stSidebar"] {{ background:#fff; border-right:1px solid {SAND_200}; }}
section[data-testid="stSidebar"] h2 {{ font-size:15px; color:{LAV_900}; }}

.mb-chapter {{ border-radius:10px; padding:9px 12px; margin-bottom:7px; }}
.mb-chapter p {{ margin:0; font-size:13px; font-weight:500; }}
.mb-bar {{ height:4px; border-radius:2px; margin-top:6px; }}
.mb-bar > div {{ height:4px; border-radius:2px; }}

.stChatMessage {{ background:transparent; border:none; padding:2px 0; }}
.stChatMessage [data-testid="stChatMessageContent"] {{ font-size:15px; line-height:1.65; }}
.stChatMessage img[data-testid="chatAvatarIcon-assistant"],
.stChatMessage img[data-testid="chatAvatarIcon-user"] {{
  background:transparent; object-fit:contain; width:38px; height:38px; border-radius:0;
}}

div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {{
  background:{LAV_50}; border-radius:14px 14px 14px 4px; padding:12px 16px; color:{LAV_900};
}}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {{
  background:#F1EFE8; border-radius:14px 14px 4px 14px; padding:12px 16px; color:{INK};
}}

.mb-src {{ font-size:12px; color:#8A8880; margin-top:6px; padding-left:4px; }}

.stChatInput textarea {{ border-radius:12px !important; border:1px solid {SAND_200} !important; font-size:15px !important; }}
.stChatInput textarea:focus {{ border-color:{LAV_400} !important; box-shadow:0 0 0 3px {LAV_50} !important; }}

div.stButton > button {{
  background:#fff; border:1px solid {SAND_200}; border-radius:20px;
  color:{LAV_600}; font-size:13px; padding:5px 16px; font-weight:500;
}}
div.stButton > button:hover {{ background:{LAV_50}; border-color:{LAV_400}; color:{LAV_900}; }}

.mb-stars {{ background:#FAEEDA; border-radius:10px; padding:10px 12px; text-align:center; }}
.mb-stars p {{ margin:0; }}
.mb-stars .n {{ font-size:22px; font-weight:600; color:#854F0B; }}
.mb-stars .l {{ font-size:12px; color:#8A6314; }}

@media (max-width: 640px) {{ .block-container {{ padding:1rem 0.6rem; }} }}
</style>
"""

CHAPTER_STYLE = [
    (LAV_50, LAV_900, LAV_100, LAV_400),
    ("#EAF3DE", SAGE_900, SAGE_100, SAGE_600),
    ("#FAECE7", "#4A1B0C", PEACH_100, "#D85A30"),
    ("#FBEAF0", "#4B1528", "#F4C0D1", "#D4537E"),
]

CHAPTER_NAMES = [
    "რაციონალური რიცხვები",
    "ფიგურები და კუთხე",
    "პროცენტი, განტოლება",
    "სამკუთხედი",
]

QUICK_ACTIONS = ["მაგალითი მაჩვენე", "სხვანაირად ამიხსენი", "სავარჯიშო მომეცი"]
