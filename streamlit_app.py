import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="KCIM 출산 육아 실무 응대 가이드",
    page_icon="⚖️",
    layout="wide",
)

# --------------------------------------------------
# 스타일 및 테마 설정 (이레 안심 가이드 스타일 + KCIM 컬러)
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #193D52;
  --cyan: #00A8C0;
  --light-blue: #8CCEE7;
  --bg: #F8F9FA;
  --white: #ffffff;
  --point: #E63946;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp { background: var(--bg); }

/* 상단 히어로 배너 */
.hero {
  background: linear-gradient(135deg, var(--navy) 0%, var(--cyan) 100%);
  color: #fff;
  border-radius: 22px;
  padding: 1.5rem 2rem;
  box-shadow: 0 10px 25px rgba(25, 61, 82, 0.15);
  margin-bottom: 1.5rem;
  text-align: center;
}

.hero-title { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem; }
.hero-desc { font-size: 1rem; opacity: 0.9; }

/* 단계별 네비게이션 카드 */
.stage-tab {
  text-align: center;
  border-radius: 16px;
  border: 1px solid #dbe4ee;
  background: #fff;
  padding: 1rem 0.5rem;
  transition: 0.3s;
  cursor: pointer;
}
.stage-tab.active {
  border-color: var(--cyan);
  box-shadow: 0 8px 20px rgba(0, 168, 192, 0.15);
  background: #f0fbff;
}

/* 실무 응대 메인 카드 */
.main-card {
  background: var(--white);
  border-radius: 24px;
  padding: 2rem;
  border: 1px solid #E2E8F0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.guide-box {
  border-radius: 16px;
  border-left: 6px solid var(--cyan);
  background: #F1F9FB;
  padding: 1.5rem;
  font-size: 1.15rem;
  line-height: 1.8;
  color: #1e293b;
}

.highlight { color: var(--point); font-weight: 800; text-decoration: underline; }

/* 사이드바 글씨 색상 */
[data-testid="stSidebar"] { background-color: var(--navy); }
[data-testid="stSidebar"] .stMarkdown p { color: white !important; font-size: 1.05rem; }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 2025 개정 지침 데이터 (고용노동부 가이드북 기반)
# --------------------------------------------------
STEPS = [
    {
        "id": 1,
        "short": "임신 확인",
        "title": "임신 확인 및 초기 응대",
        "guide": "축하와 함께 <span class='highlight'>개인정보 비공개 원칙</span>을 먼저 확인하세요. 현재 12주 이내라면 바로 단축근무가 가능함을 안내해 심리적 안정을 주는 것이 핵심입니다.",
        "details": [
            "임신기 근로시간 단축: 임신 후 12주 이내 및 32주 이후(개정) 사용 가능 [cite: 13, 76]",
            "임금 삭감 없이 하루 2시간 단축 가능 [cite: 74]",
            "고위험 임신부(19대 질환)는 전 기간 단축 가능 [cite: 13, 77, 438]"
        ],
        "faq": "Q. 32주 이전에는 단축근무가 아예 안 되나요? \nA. 원칙적으로는 12주 이내/32주 이후지만, 의사 진단서가 있는 고위험 임신부는 기간 제한 없이 사용 가능합니다. [cite: 77]"
    },
    {
        "id": 2,
        "short": "출산/배우자",
        "title": "출산휴가 및 배우자 지원",
        "guide": "남성 직원에게는 <span class='highlight'>유급 20일</span>로 확대된 배우자 출산휴가를 안내하세요. 4번까지 나눠 쓸 수 있어 조리원 퇴소 시기에 맞춰 쓰면 매우 유용합니다.",
        "details": [
            "배우자 출산휴가: 유급 20일(기존 10일)로 확대 [cite: 27, 103]",
            "분할 사용: 총 4회(분할 3회)까지 나누어 사용 가능 [cite: 30, 106]",
            "미숙아 출산 시: 출산전후휴가 100일(기존 90일)로 확대 [cite: 18, 93]"
        ],
        "faq": "Q. 배우자 휴가는 언제까지 써야 하나요? \nA. 출산일로부터 120일 이내에 휴가를 종료해야 합니다. [cite: 105]"
    },
    {
        "id": 3,
        "short": "육아휴직",
        "title": "육아휴직 급여 및 기간",
        "guide": "경제적 걱정을 덜어주세요. <span class='highlight'>첫 3개월 최대 250만 원</span>이 지급되며, 사후지급금이 폐지되어 휴직 중에 전액을 다 받을 수 있습니다.",
        "details": [
            "급여 상한: 1~3개월(250만), 4~6개월(200만), 7~12개월(160만) [cite: 38, 39, 40, 113]",
            "사후지급금 폐지: 복직 후 6개월 대기 없이 휴직 중 100% 지급 [cite: 41, 113, 257]",
            "기간 연장: 부모 각각 3개월 이상 사용 시 최대 1.5년으로 연장 [cite: 35, 111, 316]"
        ],
        "faq": "Q. 2024년에 시작한 사람도 인상된 급여를 받나요? \nA. 네, 2025.1.1. 이후 사용하는 기간에 대해서는 인상된 금액이 적용됩니다. [cite: 281, 282]"
    },
    {
        "id": 4,
        "short": "복직/단축",
        "title": "복직 및 육아기 단축근무",
        "guide": "초등학생 부모님의 경력단절을 막아주세요. 자녀가 <span class='highlight'>초등학교 6학년(만 12세)</span>이 될 때까지 단축근무를 쓸 수 있어 유연한 복직이 가능합니다.",
        "details": [
            "대상 확대: 만 8세 이하 -> 만 12세(초6) 이하 자녀까지 [cite: 48, 118, 119]",
            "사용 기간: 최대 3년까지 사용 가능 (육휴 미사용분 가산) [cite: 45, 119]",
            "급여 지원: 매주 최초 10시간 단축분 기준금액 상한 220만원 상향 [cite: 119, 259]"
        ],
        "faq": "Q. 육아휴직을 1년 다 썼는데 단축근무를 더 쓸 수 있나요? \nA. 네, 육아휴직 1년을 다 썼더라도 육아기 단축근무는 기본 1년이 보장되어 추가 사용이 가능합니다. [cite: 124]"
    }
]

# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --------------------------------------------------
# 화면 구성
# --------------------------------------------------

# 사이드바
with st.sidebar:
    st.markdown("## 🛡️ 관리자 정보")
    st.write(f"📅 기준일: {datetime.date.today()}")
    st.divider()
    st.info("💡 **응대 Tip**\n임직원에게 '축하'를 먼저 건네는 것이 원활한 노무 관리의 시작입니다.")
    st.divider()
    st.markdown("### 📞 실무 지원 내선")
    st.write("• 인사팀: 102\n• IT지원: 105")

# 메인 헤더
st.markdown(
    f"""
<div class="hero">
  <div class="hero-title">👶 KCIM 출산 육아 실무 응대 가이드</div>
  <div class="hero-desc">사장님과 팀장님이 직원의 상황에 맞춰 즉각 응대할 수 있는 2025년 개정판 매뉴얼입니다.</div>
</div>
""",
    unsafe_allow_html=True,
)

# 단계 선택 (가로 레이아웃)
nav_cols = st.columns(len(STEPS))
for idx, col in enumerate(nav_cols):
    s = STEPS[idx]
    is_active = (idx == st.session_state.active_step)
    with col:
        if st.button(f"STEP {s['id']}\n{s['short']}", key=f"btn_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()

# 메인 콘텐츠 카드
step = STEPS[st.session_state.active_step]
st.markdown(f"""
<div class="main-card">
    <h3 style="color:var(--navy); margin-bottom:1.5rem;">📍 {step['title']}</h3>
    <div style="margin-bottom:2rem;">
        <p style="font-weight:700; color:var(--cyan); margin-bottom:0.5rem;">📣 바로 안내할 말</p>
        <div class="guide-box">{step['guide']}</div>
    </div>
    <div class="grid-2" style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
        <div style="background:#fff; padding:1.2rem; border-radius:15px; border:1px solid #eee;">
            <p style="font-weight:700; color:var(--navy);">✅ 실무 체크리스트</p>
            {"".join([f"<p style='font-size:0.95rem; margin-bottom:8px;'>• {d}</p>" for d in step['details']])}
        </div>
        <div style="background:#FFF9FA; padding:1.2rem; border-radius:15px; border:1px solid #FFE5E9;">
            <p style="font-weight:700; color:var(--point);">❓ 자주 묻는 질문</p>
            <p style="font-size:0.95rem; white-space: pre-wrap;">{step['faq']}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 하단 통합 검색/상담창
# --------------------------------------------------
st.markdown("---")
st.subheader("🤖 상세 내용 검색 및 AI 노무 상담")
st.caption(f"현재 안내 중인 단계: {step['short']} (2025년 개정 법령 기반)")

# 채팅 내역 표시 (높이 제한)
chat_container = st.container(height=250)
with chat_container:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("문의 내용을 입력하세요 (예: 쌍둥이 출산 시 배우자 휴가 일수는?)"):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                # 최신 데이터를 강제 주입하는 시스템 프롬프트
                system_instr = (
                    "너는 KCIM 경영관리본부의 전문 노무 상담사야. "
                    "반드시 2025년 개정 법령을 기준으로 답변해. "
                    "1. 육아휴직 상한 250만 원, 사후지급금 폐지(25.1.1) [cite: 38, 41, 113] "
                    "2. 배우자 휴가 20일, 육아기 단축 자녀연령 만 12세 확대(25.2.23) [cite: 27, 48, 119] "
                    "사장님과 팀장님이 직원에게 친절하고 명확하게 설명할 수 있도록 답변해줘."
                )
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_instr}] + st.session_state.chat_messages
                )
                res_content = response.choices[0].message.content
                st.markdown(res_content)
                st.session_state.chat_messages.append({"role": "assistant", "content": res_content})
            except:
                st.warning("상세 상담을 위해 OpenAI API Key 설정이 필요합니다.")
