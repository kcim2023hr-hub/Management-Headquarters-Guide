import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(
    page_title="Kcim 육아지원 실무 안심 대시보드",
    page_icon="⚖️",
    layout="wide"
)

KCIM_DARK    = "#193D52"
KCIM_MEDIUM  = "#00A8C0"
KCIM_POINT   = "#FF4B6B"

st.markdown(f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {{
  --dark:   {KCIM_DARK};
  --medium: {KCIM_MEDIUM};
  --point:  {KCIM_POINT};
  --bg:     #F0F4F8;
  --card:   #FFFFFF;
  --border: #DDE3EA;
  --text:   #2D3748;
  --muted:  #718096;
}}

* {{ font-family: 'Pretendard', sans-serif !important; box-sizing: border-box; }}

/* ── 앱 배경 ───────────────────────────────────── */
.stApp {{ background: var(--bg) !important; }}

/* ── 사이드바 ──────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: var(--dark) !important;
    border-right: none !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 2rem 1.2rem;
}}
[data-testid="stSidebar"] * {{ color: #E8EDF2 !important; }}
[data-testid="stSidebar"] .stRadio label {{
    font-size: 0.9rem;
    padding: 6px 0;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: color .2s;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.12) !important;
    margin: 1.2rem 0;
}}

/* Streamlit 기본 padding 줄이기 */
.block-container {{
    padding: 2rem 2.5rem 6rem 2.5rem !important;
    max-width: 860px !important;
}}

/* ── 헤더 배너 ─────────────────────────────────── */
.kcim-header {{
    background: linear-gradient(120deg, var(--dark) 0%, #1e5470 55%, #0a7a96 100%);
    border-radius: 20px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 1.4rem;
}}
.kcim-header::after {{
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(0,168,192,.18);
    pointer-events: none;
}}
.kcim-header-icon {{
    font-size: 2.8rem;
    flex-shrink: 0;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,.3));
}}
.kcim-header-text h1 {{
    margin: 0 0 4px 0;
    font-size: 1.65rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.25;
}}
.kcim-header-text p {{
    margin: 0;
    font-size: 0.9rem;
    color: rgba(255,255,255,.7);
    font-weight: 400;
}}

/* ── 상태 배지 행 ──────────────────────────────── */
.badge-row {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1.8rem;
}}
.badge {{
    display: flex;
    align-items: center;
    gap: 6px;
    background: white;
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--dark);
    box-shadow: 0 1px 4px rgba(0,0,0,.05);
}}
.badge-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}

/* ── 가이드 카드 ────────────────────────────────── */
.gcard {{
    background: var(--card);
    border-radius: 16px;
    border: 1px solid var(--border);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
    transition: box-shadow .2s, transform .2s;
}}
.gcard:hover {{
    box-shadow: 0 6px 24px rgba(0,0,0,.09);
    transform: translateY(-2px);
}}
.gcard-top {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}}
.gcard-tag {{
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: .4px;
    padding: 3px 10px;
    border-radius: 6px;
    background: rgba(0,168,192,.1);
    color: var(--medium);
    text-transform: uppercase;
}}
.gcard-q {{
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--dark);
    margin: 0 0 .9rem 0;
    line-height: 1.5;
}}
.gcard-a {{
    font-size: 0.95rem;
    color: var(--text);
    line-height: 1.85;
    padding: .9rem 1.1rem;
    background: #F7FAFC;
    border-radius: 10px;
    border-left: 3px solid var(--medium);
    margin: 0;
}}
.hl {{ color: var(--point); font-weight: 700; }}

/* ── 섹션 제목 ─────────────────────────────────── */
.sec-title {{
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.6rem 0 .9rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.sec-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* ── 채팅 영역 ─────────────────────────────────── */
.chat-wrap {{
    background: white;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1rem;
    margin-top: 1.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
}}
.chat-label {{
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--medium);
    margin-bottom: .8rem;
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* chat_input 스타일 */
[data-testid="stChatInput"] {{
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    background: #F7FAFC !important;
    font-size: 0.9rem !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: var(--medium) !important;
    box-shadow: 0 0 0 3px rgba(0,168,192,.12) !important;
}}

/* chat message 버블 */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}

/* Streamlit 기본 여백 정리 */
.element-container {{ margin-bottom: 0 !important; }}
div[data-testid="stVerticalBlock"] > div {{ gap: 0 !important; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# 사이드바
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🛡️ 관리자 메뉴")
    st.caption("문의 직원의 상황을 선택하세요")

    menu = st.radio(
        "",
        ["🏠 전체 한눈에 보기",
         "🤰 임신 사실을 알렸을 때",
         "👨‍🍼 출산이 임박했을 때",
         "🤱 본격적인 육아기",
         "💰 급여/복직 문의"],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**💡 실무 Tip**")
    st.info("임직원에게 '축하'를 먼저 건네는 것이 원활한 노무 관리의 시작입니다.")
    st.caption(f"📅 기준일: {datetime.date.today()}")

# ═══════════════════════════════════════════
# 헤더 배너
# ═══════════════════════════════════════════
st.markdown("""
<div class="kcim-header">
    <div class="kcim-header-icon">⚖️</div>
    <div class="kcim-header-text">
        <h1>육아지원제도 즉각 응대 가이드</h1>
        <p>사장님과 팀장님을 위한 2025년 최신판 실무 매뉴얼 &nbsp;·&nbsp; Kcim 경영관리본부</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 배지 행
st.markdown("""
<div class="badge-row">
    <div class="badge"><div class="badge-dot" style="background:#10b981"></div>2025년 법령 최신 반영</div>
    <div class="badge"><div class="badge-dot" style="background:#00A8C0"></div>총 4개 상황 가이드</div>
    <div class="badge"><div class="badge-dot" style="background:#FF4B6B"></div>AI 노무사 상담 가능</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# 가이드 데이터
# ═══════════════════════════════════════════
guides = [
    {
        "cat": "🤰 임신 사실을 알렸을 때",
        "cat_short": "임신",
        "q": "직원이 임신 초기라 몸이 힘들다고 합니다. 어떤 혜택이 있죠?",
        "a": "가장 먼저 <span class='hl'>임신기 근로시간 단축</span>을 안내하세요. 12주 이내라면 임금 삭감 없이 하루 2시간 일찍 퇴근할 수 있습니다. 2025년부터는 <span class='hl'>32주 이후</span>에도 동일하게 적용됩니다.",
    },
    {
        "cat": "👨‍🍼 출산이 임박했을 때",
        "cat_short": "출산",
        "q": "남성 직원이 아내 출산으로 자리를 비워야 한다면?",
        "a": "최근 법 개정으로 <span class='hl'>배우자 출산휴가가 유급 20일</span>로 대폭 늘어났습니다. 한 번에 다 안 써도 되며, <span class='hl'>120일 내에 4번까지</span> 나누어 쓸 수 있다고 알려주시면 매우 좋아할 것입니다.",
    },
    {
        "cat": "🤱 본격적인 육아기",
        "cat_short": "육아기",
        "q": "초등학교 다니는 자녀가 있는데 단축근무가 되나요?",
        "a": "네, 가능합니다. 대상 자녀 연령이 <span class='hl'>초등학교 6학년(만 12세)</span>까지 확대되었습니다. 육아기 근로시간 단축은 최대 <span class='hl'>3년</span>까지 가능하니 업무 스케줄 조정을 함께 논의해 보세요.",
    },
    {
        "cat": "💰 급여/복직 문의",
        "cat_short": "급여",
        "q": "육아휴직 들어가면 돈은 어떻게 나오나요?",
        "a": "2025년부터 급여가 인상되었습니다. <span class='hl'>첫 3개월은 최대 250만 원</span>까지 나옵니다. 특히 복직 후에 주던 사후지급금 제도가 폐지되어, 이제 <span class='hl'>휴직 중에 100% 다 받을 수 있어</span> 걱정을 덜어주셔도 됩니다.",
    },
]

# ═══════════════════════════════════════════
# 카드 렌더링
# ═══════════════════════════════════════════
filtered = guides if menu == "🏠 전체 한눈에 보기" else [g for g in guides if g["cat"] == menu]

if filtered:
    st.markdown(f'<div class="sec-title">{"전체 가이드" if menu == "🏠 전체 한눈에 보기" else menu.split(" ", 1)[1]}</div>', unsafe_allow_html=True)
    for g in filtered:
        st.markdown(f"""
        <div class="gcard">
            <div class="gcard-top">
                <span class="gcard-tag">{g['cat_short']}</span>
            </div>
            <div class="gcard-q">{g['q']}</div>
            <p class="gcard-a">{g['a']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("해당 메뉴에 등록된 가이드가 없습니다.")

# ═══════════════════════════════════════════
# AI 상담 챗봇
# ═══════════════════════════════════════════
st.markdown("""
<div class="chat-wrap">
    <div class="chat-label">🤖 &nbsp;AI 노무사 상담 &nbsp;—&nbsp; 더 구체적인 사례나 법령 근거가 궁금하시면 바로 질문하세요</div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("예: 육아휴직 중 4대보험은 어떻게 처리하나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": (
                            "너는 Kcim 경영진을 보좌하는 전문 노무사야. "
                            "2025년 최신 근로기준법·남녀고용평등법·고용보험법 기준으로 "
                            "친절하고 명확하게 실무 답변을 해줘. 답변은 한국어로 해줘."
                        )}
                    ] + st.session_state.messages,
                )
                ans = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
    except Exception:
        with st.chat_message("assistant"):
            st.warning("💡 상세 AI 답변을 위해 관리자에게 API 설정을 요청하세요. 기본 매뉴얼은 위 카드를 참고해 주세요.")
