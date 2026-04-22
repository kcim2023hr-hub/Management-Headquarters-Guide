import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 (Full Width 활용)
st.set_page_config(
    page_title="KCIM 출산 육아 실무 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# --------------------------------------------------
# 스타일 (가시성 및 레이아웃 최적화)
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #193D52;
  --cyan: #00A8C0;
  --light-blue: #F1F9FB;
  --bg: #F8F9FA;
  --white: #ffffff;
  --point: #E63946;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp { background: var(--bg); }

/* 중앙 몰림 방지를 위해 최대 너비 확장 */
.block-container {
  max-width: 1400px !important;
  padding-top: 1.5rem;
  padding-bottom: 5rem;
}

/* 히어로 배너 */
.hero {
  background: linear-gradient(135deg, var(--navy) 0%, var(--cyan) 100%);
  color: #fff;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(25, 61, 82, 0.15);
  margin-bottom: 2rem;
  text-align: center;
}

/* 단계별 네비게이션 버튼 스타일 */
.stButton > button {
  border-radius: 12px !important;
  height: 80px !important;
  font-weight: 700 !important;
  white-space: pre-line !important;
  border: 1px solid #dbe4ee !important;
  transition: 0.3s !important;
}

/* 현재 선택된 단계 하이라이트 */
div[data-testid="stColumn"] > div > button[kind="primary"] {
    background-color: var(--cyan) !important;
    color: white !important;
}

/* 대시보드 메인 카드 */
.main-card {
  background: var(--white);
  border-radius: 24px;
  padding: 2.5rem;
  border: 1px solid #E2E8F0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

/* 응대 가이드 박스 */
.guide-box {
  border-radius: 16px;
  border-left: 6px solid var(--cyan);
  background: var(--light-blue);
  padding: 1.5rem;
  font-size: 1.2rem;
  line-height: 1.8;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.highlight { color: var(--point); font-weight: 800; text-decoration: underline; }

/* 섹션 타이틀 */
.section-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* FAQ 카드 */
.faq-item {
  background: #fdfdfd;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 0.8rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 2025 개정 지침 반영 데이터 (고용노동부 가이드북 준수)
# --------------------------------------------------
STEPS = [
    {
        "id": 1,
        "short": "임신 확인\n초기 안내",
        "title": "임신 확인 및 초기 응대",
        "guide": "축하와 함께 <span class='highlight'>개인정보 비공개 원칙</span>을 확인하세요. 현재 12주 이내라면 즉시 단축근무 신청이 가능함을 안내하여 심리적 안정을 주는 것이 가장 중요합니다.",
        "checklist": [
            "임신 사실 공유 범위를 당사자와 우선 확인",
            "임신기 근로시간 단축 제도 및 신청 절차 안내",
            "향후 출산휴가/육아휴직 대략적인 일정 상담"
        ],
        "law": [
            "임신기 근로시간 단축: 임신 후 12주 이내 및 32주 이후(25.2.23 개정) [cite: 13, 76]",
            "고위험 임신부: 임신 전 기간 사용 가능 [cite: 77]",
            "임금 삭감 없이 1일 2시간 단축 가능 [cite: 74]"
        ],
        "faq": [
            ("32주 이전에는 단축이 안 되나요?", "원칙은 12주 이내/32주 이후이나, 의사 진단서가 있는 고위험 임신부는 전 기간 가능합니다."),
            ("검진 시간도 보장되나요?", "네, 임산부 정기건강진단 시간을 유급으로 보장해야 합니다.")
        ]
    },
    {
        "id": 2,
        "short": "출산휴가\n배우자 지원",
        "title": "출산전후휴가 및 배우자 출산휴가",
        "guide": "남성 직원에게는 <span class='highlight'>유급 20일</span>로 확대된 배우자 휴가를 안내하세요. 120일 이내에 총 4번까지 나눠 쓸 수 있어 조리원 퇴소 시기에 맞춰 유연하게 활용 가능합니다.",
        "checklist": [
            "출산예정일 증빙서류 접수 및 휴가 기간 확정",
            "배우자 출산휴가 분할 사용 계획 확인",
            "급여 지원금(중소기업 20일분) 신청 안내"
        ],
        "law": [
            "배우자 출산휴가: 유급 20일 확대 (기존 10일) [cite: 27, 103]",
            "휴가 분할: 총 3회 분할(4번 나누어 사용) 가능 [cite: 30, 106]",
            "미숙아 출산 시: 출산전후휴가 100일 확대 [cite: 18, 93]"
        ],
        "faq": [
            ("배우자 휴가는 언제까지 써야 하나요?", "출산일로부터 120일 이내에 휴가를 종료해야 합니다. [cite: 105]"),
            ("휴가 중 급여는 누가 주나요?", "최초 60일은 전액 유급이며, 배우자 휴가는 중소기업 대상 20일치 급여 지원이 신설되었습니다. [cite: 107]")
        ]
    },
    {
        "id": 3,
        "short": "육아휴직\n급여 안내",
        "title": "육아휴직 및 급여 인상 개편",
        "guide": "경제적 걱정을 덜어주세요. <span class='highlight'>첫 3개월 최대 250만 원</span>이 지급되며, 사후지급금이 폐지되어 휴직 중에 급여 100%를 모두 받을 수 있음을 강조하세요.",
        "checklist": [
            "육아휴직 개시일 30일 전 신청서 접수",
            "기간 연장(1.5년) 대상자 여부 확인 (부모 각각 3개월 사용 시)",
            "개편된 월별 급여 상한액 안내"
        ],
        "law": [
            "급여 상한: 1~3개월(250만), 4~6개월(200만), 7~12개월(160만) [cite: 38, 113]",
            "사후지급금 폐지: 복직 후 6개월 뒤 주던 25%를 휴직 중 전액 지급 [cite: 41, 113, 257]",
            "기간 연장: 부모 각각 3개월 이상 사용 시 최대 1.5년 [cite: 35, 111]"
        ],
        "faq": [
            ("2024년에 시작한 사람도 인상되나요?", "네, 25.1.1. 이후 사용하는 기간에 대해서는 인상된 상한액이 적용됩니다. [cite: 282]"),
            ("한부모 가족 혜택은요?", "첫 3개월 상한액이 300만 원으로 우대 적용됩니다. [cite: 113]")
        ]
    },
    {
        "id": 4,
        "short": "복직 및\n단축근무",
        "title": "복직 지원 및 육아기 근로시간 단축",
        "guide": "복귀하는 직원의 커리어 유지를 돕는 단계입니다. 자녀가 <span class='highlight'>초등학교 6학년(만 12세)</span>이 될 때까지 단축근무가 가능하므로, 유연한 업무 복귀를 독려해 주세요.",
        "checklist": [
            "복직 예정일 1개월 전 사전 연락 및 면담",
            "육아기 근로시간 단축 희망 시간대 조율",
            "단축근무에 따른 업무 분담자 지원금 신청 검토"
        ],
        "law": [
            "대상 확대: 만 8세 이하 -> 만 12세(초6) 이하 자녀까지 [cite: 48, 118]",
            "사용 기간: 최대 3년까지 사용 가능 (육휴 미사용분 가산) [cite: 45, 119]",
            "급여 지원: 주 10시간 단축 시 월 최대 55만 원 지원 [cite: 119]"
        ],
        "faq": [
            ("단축근무 중 연차가 깎이나요?", "아니요. 24.10.22. 이후에는 단축된 시간도 연차 산정 시 근무로 인정됩니다. [cite: 119, 254]"),
            ("최소 사용 기간은요?", "기존 3개월에서 1개월 단위로 짧게 나누어 쓸 수 있습니다. [cite: 50, 119]")
        ]
    }
]

# --------------------------------------------------
# 세션 상태 및 네비게이션
# --------------------------------------------------
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# 사이드바 (정보 업데이트)
with st.sidebar:
    st.markdown(f"### 🏢 KCIM 실무 지원")
    st.write(f"오늘: {datetime.date.today()}")
    st.divider()
    st.info("💡 **관리자 응대 포인트**\n임직원에게 가장 먼저 건네는 말은\n'축하합니다'가 되어야 합니다.")
    st.divider()
    st.markdown("📞 **내부 내선**\n- 인사지원팀: 102\n- IT시스템팀: 105")

# 메인 헤더
st.markdown(
    f"""
<div class="hero">
  <div style="font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem;">⚖️ KCIM 출산 육아 실무 응대 대시보드</div>
  <div style="font-size: 1.1rem; opacity: 0.9;">경영관리본부 실무진 및 경영진을 위한 2025년 고용노동부 개정판 통합 매뉴얼</div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 1단계: 네비게이션 (가로 배치)
# --------------------------------------------------
nav_cols = st.columns(len(STEPS))
for idx, col in enumerate(nav_cols):
    s = STEPS[idx]
    with col:
        # 현재 활성화된 단계 버튼 색상 변경
        button_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}\n{s['short']}", key=f"nav_{idx}", use_container_width=True, type=button_type):
            st.session_state.active_step = idx
            st.rerun()

# --------------------------------------------------
# 2단계: 메인 대시보드 콘텐츠 (와이드 레이아웃)
# --------------------------------------------------
step = STEPS[st.session_state.active_step]

st.markdown(f"""
<div class="main-card">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem;">
        <div>
            <h2 style="color:var(--navy); margin:0;">📍 {step['title']}</h2>
            <p style="color:var(--muted); font-size: 1rem; margin-top:0.5rem;">실무진은 아래 가이드에 따라 임직원에게 즉각 답변하십시오.</p>
        </div>
        <div style="background:var(--navy); color:white; padding: 8px 16px; border-radius: 10px; font-weight:700;">
            2025-2026 최신 지침 적용 중
        </div>
    </div>
    
    <p class="section-title">📣 바로 안내할 말 (Best Practice)</p>
    <div class="guide-box">{step['guide']}</div>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 25px; margin-top: 2rem;">
        <div style="background:#fff; border:1px solid #E2E8F0; padding:1.5rem; border-radius:20px;">
            <p class="section-title">✅ 실무 체크리스트</p>
            {"".join([f"<p style='font-size:1rem; margin-bottom:12px; display:flex; align-items:start;'><span style='color:var(--cyan); margin-right:8px;'>✔</span>{d}</p>" for d in step['checklist']])}
        </div>
        
        <div style="background:#fff; border:1px solid #E2E8F0; padding:1.5rem; border-radius:20px;">
            <p class="section-title">⚖️ 주요 법적 기준</p>
            {"".join([f"<p style='font-size:0.95rem; margin-bottom:12px; color:#4a5568;'>• {l}</p>" for l in step['law']])}
        </div>

        <div style="background:#fff; border:1px solid #E2E8F0; padding:1.5rem; border-radius:20px;">
            <p class="section-title" style="color:var(--point);">❓ 빈번한 질문 (FAQ)</p>
            {"".join([f"<div class='faq-item'><p style='font-weight:700; font-size:0.9rem; color:var(--navy); margin-bottom:4px;'>Q. {q}</p><p style='font-size:0.85rem; color:#4a5568;'>A. {a}</p></div>" for q, a in step['faq']])}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3단계: 최하단 AI 상담창 (와이드 검색바 형태)
# --------------------------------------------------
st.markdown("<h3 style='color:var(--navy); margin-left:10px;'>🤖 상세 내용 검색 및 AI 노무 상담</h3>", unsafe_allow_html=True)
st.caption(f"  현재 선택된 단계({step['title']})를 기준으로 사장님과 팀장님의 응대를 돕습니다.")

# 채팅 이력 컨테이너
chat_container = st.container(height=300, border=True)
with chat_container:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("위 매뉴얼 외에 궁금한 점을 검색하거나 질문하세요..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                system_instr = (
                    "너는 KCIM 경영관리본부의 전문 노무 상담사야. "
                    "2025년 개정된 최신 법령을 기준으로 관리자가 직원에게 친절하게 설명할 수 있게 답변해. "
                    "1. 육아휴직 상한 250만 원 & 사후지급금 폐지(25.1.1) "
                    "2. 배우자 휴가 유급 20일 & 육아기 단축 자녀연령 만 12세 확대(25.2.23) "
                    "위 핵심 수치를 절대 틀리지 말고 반영해서 답변하라."
                )
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_instr}] + st.session_state.chat_messages
                )
                res_content = response.choices[0].message.content
                st.markdown(res_content)
                st.session_state.chat_messages.append({"role": "assistant", "content": res_content})
            except:
                st.warning("상세 상담을 위해서는 OpenAI API Key 설정이 필요합니다.")

# 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:0.9rem;'>© 2026 KCIM Management Support Division | 실무 응대 대시보드 v2.0</center>", unsafe_allow_html=True)
