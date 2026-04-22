import datetime
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# --------------------------------------------------
# 스타일
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #17384b;
  --navy-soft: #24566f;
  --bg: #f5f7fb;
  --card: #ffffff;
  --line: #dbe4ee;
  --text: #1f2a35;
  --muted: #708191;
  --cyan: #11a8c7;
  --green: #1f9d63;
  --red: #e65a70;
  --amber: #f4a62a;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp {
  background: var(--bg);
}

.block-container {
  max-width: 1120px;
  padding-top: 1.4rem;
  padding-bottom: 3rem;
}

.hero {
  background: linear-gradient(135deg, var(--navy) 0%, #156a8d 100%);
  color: #fff;
  border-radius: 22px;
  padding: 1.4rem 1.6rem;
  box-shadow: 0 12px 28px rgba(22, 48, 71, 0.14);
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
}

.hero::after {
  content: "";
  position: absolute;
  right: -60px;
  top: -50px;
  width: 220px;
  height: 220px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
}

.hero-title {
  font-size: 1.55rem;
  font-weight: 800;
  margin-bottom: 0.35rem;
  letter-spacing: -0.02em;
}

.hero-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(255,255,255,0.88);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 0.8rem;
  flex-wrap: wrap;
}

.meta-chip-wrap {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.12);
  color: #fff;
  border-radius: 999px;
  padding: 0.42rem 0.78rem;
  font-size: 0.8rem;
}

.stage-nav {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 0.9rem;
  box-shadow: 0 8px 22px rgba(23, 43, 64, 0.05);
  margin-bottom: 1rem;
}

.stage-nav-title {
  font-size: 0.92rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.75rem;
}

.stage-tab {
  text-align: center;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: #fff;
  padding: 0.75rem 0.5rem 0.85rem 0.5rem;
  min-height: 96px;
}

.stage-tab.active {
  border-color: transparent;
  box-shadow: 0 12px 26px rgba(20, 49, 72, 0.12);
}

.stage-num {
  width: 34px;
  height: 34px;
  margin: 0 auto 0.45rem auto;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border: 2px solid var(--line);
  color: var(--muted);
  background: #fff;
}

.stage-label {
  font-size: 0.8rem;
  line-height: 1.35;
  color: var(--text);
  font-weight: 700;
}

.quick-panel {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 14px;
  margin-bottom: 1rem;
}

.quick-card, .main-card, .faq-card, .chat-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: 0 8px 22px rgba(23, 43, 64, 0.05);
}

.quick-card {
  padding: 1rem 1.05rem;
}

.quick-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.65rem;
}

.quick-text {
  font-size: 0.94rem;
  line-height: 1.65;
  color: var(--text);
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.status-box {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 0.9rem;
  background: linear-gradient(180deg, #fff 0%, #f8fbff 100%);
}

.status-label {
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 0.3rem;
}

.status-value {
  font-size: 0.96rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1.45;
}

.main-card-header {
  padding: 1rem 1.1rem;
  border-bottom: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.main-card-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-badge {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.05;
  font-weight: 800;
}

.step-badge small {
  font-size: 0.66rem;
}

.main-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 0.2rem;
}

.main-sub {
  font-size: 0.9rem;
  color: var(--muted);
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  border: 1px solid var(--line);
  padding: 0.42rem 0.8rem;
  font-size: 0.8rem;
  color: var(--muted);
  background: #fff;
}

.main-body {
  padding: 1rem 1.1rem 1.15rem 1.1rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.section-box {
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 0.95rem 1rem;
  background: #fff;
}

.section-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.8rem;
}

.item-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 0.58rem 0;
  border-bottom: 1px solid #edf2f7;
  font-size: 0.92rem;
  color: var(--text);
  line-height: 1.6;
}

.item-row:last-child {
  border-bottom: 0;
}

.guide-box {
  border-radius: 16px;
  border: 1px solid #d7ecf4;
  background: #f4fbfe;
  padding: 0.95rem 1rem;
  line-height: 1.65;
  font-size: 0.94rem;
  color: var(--text);
}

.warn-box {
  border-radius: 16px;
  border: 1px solid #ffd7de;
  background: #fff6f8;
  padding: 0.9rem 0.95rem;
  line-height: 1.6;
  font-size: 0.9rem;
  color: #9a2948;
  margin-bottom: 0.55rem;
}

.form-chip-wrap {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.form-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: #f8fafc;
  padding: 0.48rem 0.8rem;
  font-size: 0.82rem;
  color: var(--navy);
}

.faq-card, .chat-card {
  padding: 1rem 1.05rem;
  margin-top: 1rem;
}

.faq-item {
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.85rem 0.95rem;
  background: #fff;
  margin-bottom: 0.7rem;
}

.faq-q {
  font-size: 0.88rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.35rem;
}

.faq-a {
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.6;
}

.bottom-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 1rem;
}

.stButton > button {
  border-radius: 12px !important;
  font-weight: 700 !important;
}

[data-testid="stChatInput"] textarea {
  border-radius: 14px !important;
}

@media (max-width: 900px) {
  .quick-panel,
  .grid-2 {
    grid-template-columns: 1fr;
  }
  .status-grid {
    grid-template-columns: 1fr;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 데이터
# --------------------------------------------------
STEPS = [
    {
        "id": 1,
        "title": "임신 확인 및 초기 안내",
        "short": "임신 확인",
        "period": "임신 확인 직후",
        "color": "#4FACCC",
        "summary": "임신 사실 확인 직후 비공개 원칙과 신청 가능한 제도를 안내하는 단계입니다.",
        "guide": "먼저 축하 인사를 전한 뒤 개인정보 보호 원칙을 설명하고 현재 바로 신청 가능한 제도가 있는지 순서대로 안내해 주세요.",
        "check": [
            "임신 사실 공유 범위를 당사자와 먼저 확인하기",
            "임신기 근로시간 단축 가능 여부 안내하기",
            "보호 규정과 내부 신청 절차 설명하기",
            "향후 출산휴가와 육아휴직 흐름 간단히 안내하기",
        ],
        "forms": ["초기 상담 체크리스트", "임신기 근로시간 단축 신청서"],
        "warn": [
            "임신을 이유로 한 불이익 조치나 업무 배제는 금지됩니다.",
            "당사자 동의 없이 임신 사실을 공유하지 않도록 주의해 주세요.",
        ],
        "faq": [
            ("언제부터 제도 안내를 시작하면 좋나요", "임신 사실 확인 직후부터 안내하는 것이 가장 좋습니다. 초기 안내가 빠를수록 이후 휴가와 단축근무 연결이 쉬워집니다."),
            ("팀에는 바로 알려야 하나요", "반드시 당사자 의사를 먼저 확인한 뒤 필요한 범위에서만 공유하는 것이 안전합니다."),
            ("처음에 가장 먼저 안내할 것은 무엇인가요", "비공개 원칙과 현재 신청 가능한 제도 여부를 가장 먼저 안내해 주세요."),
        ],
        "next_step": "임신기 근로시간 단축 여부 확인",
        "target": "임신 확인한 임직원",
    },
    {
        "id": 2,
        "title": "임신기 근로시간 단축",
        "short": "임신기 단축",
        "period": "적용 가능 시기 확인 후",
        "color": "#37B89A",
        "summary": "임신기 중 단축근무가 가능한 시기에 맞춰 근로시간과 업무 조정을 안내하는 단계입니다.",
        "guide": "직원 주수와 적용 가능 시기를 먼저 확인한 뒤 신청서 접수와 단축 시간대를 같이 조율해 주세요.",
        "check": [
            "적용 가능 시기와 신청 사유 먼저 확인하기",
            "단축 시간대와 업무 공백 조율하기",
            "임금 삭감 금지 원칙 안내하기",
            "팀장과 실무 인수 범위 공유하기",
        ],
        "forms": ["임신기 근로시간 단축 신청서"],
        "warn": [
            "법령 기준과 사내 운영 기준을 함께 확인한 뒤 안내해야 혼선이 줄어듭니다.",
            "사용 거부나 불이익으로 받아들여질 수 있는 표현은 피하는 것이 좋습니다.",
        ],
        "faq": [
            ("단축근무 시간은 어떻게 정하나요", "직원 요청과 부서 운영 상황을 함께 보고 무리 없는 시간대로 협의하는 것이 좋습니다."),
            ("급여가 줄어드나요", "기본적으로 임금 처리 기준은 별도 확인이 필요하므로 사내 기준과 최신 제도를 함께 안내해 주세요."),
            ("팀에 어떻게 설명하면 좋나요", "업무 공백 최소화와 개인정보 보호를 함께 고려해 필요한 범위만 공유해 주세요."),
        ],
        "next_step": "정기건강진단 시간 안내",
        "target": "임신기 단축근무 희망자",
    },
    {
        "id": 3,
        "title": "임산부 정기건강진단",
        "short": "건강진단",
        "period": "임신 주수별 검진 시기",
        "color": "#F5A623",
        "summary": "정기 검진 시간 인정과 증빙 서류 수령 기준을 정리해 빠르게 응대하는 단계입니다.",
        "guide": "검진 일정이 확인되면 유급 처리 기준과 사후 제출 서류를 같이 안내해 주세요.",
        "check": [
            "신청서 접수와 검진 일정 확인하기",
            "근로시간 인정 방식 안내하기",
            "사후 확인서 제출 기준 설명하기",
            "누락 없이 기록 남기기",
        ],
        "forms": ["정기건강진단 신청서", "검진 확인서 제출 안내"],
        "warn": [
            "증빙 없이 구두 처리만 하면 나중에 해석 차이가 생길 수 있습니다.",
        ],
        "faq": [
            ("매번 신청서를 받아야 하나요", "반복되는 경우에도 내부 기록을 남기는 방식이 가장 안전합니다."),
            ("진료 확인서는 언제 받나요", "검진 후 가능한 빠르게 제출받도록 안내하면 누락을 줄일 수 있습니다."),
            ("근무시간 인정 여부가 헷갈립니다", "사내 기준과 최신 제도를 함께 확인해 일관되게 처리해 주세요."),
        ],
        "next_step": "출산휴가 전 연차 일정 점검",
        "target": "임신 중 정기 검진 대상자",
    },
    {
        "id": 4,
        "title": "잔여 연차 및 일정 정리",
        "short": "연차 정리",
        "period": "출산휴가 시작 전",
        "color": "#9B59B6",
        "summary": "출산휴가 전에 남은 연차와 전체 일정 흐름을 정리해 실제 사용 계획을 맞추는 단계입니다.",
        "guide": "잔여 연차를 먼저 확인하고 출산휴가 시작일과 이어지는 전체 일정을 같이 정리해 주세요.",
        "check": [
            "당해 연도 잔여 연차 확인하기",
            "연차 사용 희망 일정 확인하기",
            "출산휴가 시작일과 연결 일정 정리하기",
            "팀 업무 인수 시점 조율하기",
        ],
        "forms": ["연차 사용 계획표"],
        "warn": [
            "연차 사용은 직원 의사를 우선 확인해야 하며 강제 소진처럼 보이지 않도록 주의해 주세요.",
        ],
        "faq": [
            ("연차를 꼭 먼저 써야 하나요", "반드시 그런 것은 아니며 직원 의사를 먼저 확인해 일정에 맞춰 조율하는 것이 좋습니다."),
            ("출산휴가와 붙여서 쓸 수 있나요", "실제 일정이 자연스럽게 이어지도록 사전 조율하면 응대가 쉬워집니다."),
            ("무엇을 표로 정리하면 좋나요", "연차 종료일 출산휴가 시작일 인수인계 시점을 한 번에 볼 수 있게 정리하면 좋습니다."),
        ],
        "next_step": "출산휴가 신청 접수",
        "target": "출산휴가 예정 임직원",
    },
    {
        "id": 5,
        "title": "출산휴가",
        "short": "출산휴가",
        "period": "출산 전후 휴가 운영",
        "color": "#E8556D",
        "summary": "출산휴가 신청 접수와 일정 변경 대응 그리고 급여 처리 안내가 핵심인 단계입니다.",
        "guide": "예정일 기준으로 먼저 접수하고 실제 출산일 변동 가능성을 함께 안내해 주세요.",
        "check": [
            "신청서와 예정일 증빙 서류 접수하기",
            "휴가 시작일과 종료일 안내하기",
            "급여 처리와 보험 신청 구간 설명하기",
            "실제 출산일 변경 시 정정 절차 알려주기",
        ],
        "forms": ["출산휴가 신청서", "예정일 증빙 서류 안내"],
        "warn": [
            "출산일이 바뀌는 경우가 있어 정정 절차를 미리 설명해 두는 것이 좋습니다.",
            "급여 안내는 최신 기준을 다시 확인한 뒤 설명하는 것이 안전합니다.",
        ],
        "faq": [
            ("출산일이 바뀌면 어떻게 하나요", "실제 출산일에 맞춰 서류와 일정을 정정하면 됩니다."),
            ("연차와 이어서 사용할 수 있나요", "사전 계획표가 있으면 훨씬 자연스럽게 운영할 수 있습니다."),
            ("급여 안내는 어떻게 하나요", "사내 처리 기준과 최신 제도를 함께 확인해 설명하는 방식이 가장 안전합니다."),
        ],
        "next_step": "육아휴직 여부 확인",
        "target": "출산휴가 예정자",
    },
    {
        "id": 6,
        "title": "육아휴직",
        "short": "육아휴직",
        "period": "출산휴가 이후 또는 육아 시점",
        "color": "#2980B9",
        "summary": "육아휴직 신청 접수와 복직 시점 관리 그리고 관련 제도 안내를 빠르게 처리하는 단계입니다.",
        "guide": "희망 시작일을 먼저 확인하고 휴직 중 급여 안내와 복직 예정일 관리를 함께 설명해 주세요.",
        "check": [
            "신청 시점과 희망 시작일 확인하기",
            "필요 서류와 가족관계 증빙 접수하기",
            "휴직 중 급여와 보험 변경사항 안내하기",
            "복직 예정일 관리 일정 등록하기",
        ],
        "forms": ["육아휴직 신청서", "가족관계 증빙 제출 안내"],
        "warn": [
            "급여 설명은 연도별 개편이 있을 수 있어 최신 기준을 다시 확인해야 합니다.",
        ],
        "faq": [
            ("언제 신청받는 것이 좋나요", "가능하면 시작일보다 여유 있게 접수받아 인수인계를 준비하는 것이 좋습니다."),
            ("복직일은 언제 확인하나요", "휴직 시작 시점부터 복직 예정일을 같이 관리하면 응대가 수월합니다."),
            ("부부가 함께 쓰는 경우도 있나요", "가능 여부와 세부 기준은 최신 제도 확인 후 안내해 주세요."),
        ],
        "next_step": "복직 및 단축근무 협의",
        "target": "육아휴직 예정자",
    },
    {
        "id": 7,
        "title": "복직 및 육아기 단축근무",
        "short": "복직 단축근무",
        "period": "복직 전후",
        "color": "#27AE60",
        "summary": "복직 일정 확인과 업무 복귀 준비 그리고 단축근무 희망 여부를 함께 조율하는 단계입니다.",
        "guide": "복직 의사를 먼저 확인한 뒤 바로 근무 형태와 단축근무 희망 여부를 함께 체크해 주세요.",
        "check": [
            "복직 의사와 복직일 확인하기",
            "업무 복귀 범위와 인계 계획 정리하기",
            "육아기 단축근무 희망 여부 확인하기",
            "필요 시 급여와 보험 신청 안내 연결하기",
        ],
        "forms": ["복직 사전 확인서", "육아기 근로시간 단축 신청서"],
        "warn": [
            "복직 이후 운영은 제도 설명보다 실제 업무 복귀 흐름을 함께 조율하는 것이 중요합니다.",
        ],
        "faq": [
            ("복직 전 언제 연락하면 좋나요", "보통 복직 전 충분한 여유를 두고 확인하면 가장 안정적입니다."),
            ("단축근무도 같이 안내해야 하나요", "복직 상담 시 함께 안내하면 재문의가 줄어듭니다."),
            ("팀 조율은 언제 시작하나요", "복직일 확정 전부터 업무 범위를 미리 조율하면 좋습니다."),
        ],
        "next_step": "운영 종료 후 개별 상황 관리",
        "target": "복직 예정자",
    },
]

if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

step = STEPS[st.session_state.active_step]

# --------------------------------------------------
# 헤더
# --------------------------------------------------
st.markdown(
    f"""
<div class="hero">
  <div class="hero-title">👶 KCIM 출산 육아 응대 가이드</div>
  <div class="hero-desc">
    임신 확인부터 복직까지 관리자 입장에서 빠르게 응대할 수 있도록 단계별 핵심만 정리한 페이지입니다.
  </div>
  <div class="header-row">
    <div class="meta-chip-wrap">
      <div class="meta-chip">📌 단계별 빠른 응대 중심</div>
      <div class="meta-chip">🧾 필요 서류 즉시 확인</div>
      <div class="meta-chip">💬 FAQ와 상담 연계</div>
    </div>
    <div class="meta-chip">기준일 {datetime.date.today()}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 단계 선택
# --------------------------------------------------
st.markdown('<div class="stage-nav">', unsafe_allow_html=True)
st.markdown('<div class="stage-nav-title">단계 선택</div>', unsafe_allow_html=True)
nav_cols = st.columns(len(STEPS))
for idx, col in enumerate(nav_cols):
    s = STEPS[idx]
    with col:
        active_class = "active" if idx == st.session_state.active_step else ""
        st.markdown(
            f"""
            <div class="stage-tab {active_class}">
                <div class="stage-num" style="background:{s['color'] if idx == st.session_state.active_step else '#fff'}; color:{'#fff' if idx == st.session_state.active_step else '#708191'}; border-color:{s['color'] if idx == st.session_state.active_step else '#dbe4ee'};">{s['id']}</div>
                <div class="stage-label">{s['short']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("열기", key=f"step_btn_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 빠른 응대 요약
# --------------------------------------------------
st.markdown(
    f"""
    <div class="quick-panel">
      <div class="quick-card">
        <div class="quick-title">바로 안내할 말</div>
        <div class="guide-box">{step['guide']}</div>
      </div>
      <div class="quick-card">
        <div class="quick-title">빠른 확인</div>
        <div class="status-grid">
          <div class="status-box">
            <div class="status-label">현재 단계</div>
            <div class="status-value">STEP {step['id']}<br>{step['short']}</div>
          </div>
          <div class="status-box">
            <div class="status-label">대상자</div>
            <div class="status-value">{step['target']}</div>
          </div>
          <div class="status-box">
            <div class="status-label">다음 단계</div>
            <div class="status-value">{step['next_step']}</div>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 메인 카드
# --------------------------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="main-card-header">
        <div class="main-card-title-wrap">
            <div class="step-badge" style="background:{step['color']}">
                <small>STEP</small>
                {step['id']}
            </div>
            <div>
                <div class="main-title">{step['title']}</div>
                <div class="main-sub">{step['period']} · {step['summary']}</div>
            </div>
        </div>
        <div class="pill">현재 단계 응대 가이드</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-body">', unsafe_allow_html=True)
st.markdown('<div class="grid-2">', unsafe_allow_html=True)

# 왼쪽
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">✅ HR 담당자 체크</div>', unsafe_allow_html=True)
for item in step["check"]:
    st.markdown(f'<div class="item-row"><span>✅</span><span>{item}</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 오른쪽
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧾 필요 서류</div>', unsafe_allow_html=True)
st.markdown('<div class="form-chip-wrap">', unsafe_allow_html=True)
for form in step["forms"]:
    st.markdown(f'<span class="form-chip">📄 {form}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="height:0.9rem"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚠️ 주의사항</div>', unsafe_allow_html=True)
for warn in step["warn"]:
    st.markdown(f'<div class="warn-box">{warn}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

prev_col, center_col, next_col = st.columns([1, 1, 1])
with prev_col:
    if st.session_state.active_step > 0:
        if st.button("← 이전 단계", use_container_width=True):
            st.session_state.active_step -= 1
            st.rerun()
with center_col:
    st.markdown(f"<div style='text-align:center; color:#708191; font-size:0.86rem; padding-top:0.6rem;'>STEP {step['id']} / {len(STEPS)}</div>", unsafe_allow_html=True)
with next_col:
    if st.session_state.active_step < len(STEPS) - 1:
        if st.button("다음 단계 →", use_container_width=True):
            st.session_state.active_step += 1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FAQ
# --------------------------------------------------
st.markdown('<div class="faq-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">❓ 자주 받는 질문</div>', unsafe_allow_html=True)
for q, a in step["faq"]:
    st.markdown(
        f"""
        <div class="faq-item">
            <div class="faq-q">Q. {q}</div>
            <div class="faq-a">{a}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 챗봇
# --------------------------------------------------
st.markdown('<div class="chat-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🤖 추가 상담</div>', unsafe_allow_html=True)
st.caption(f"현재 선택된 단계는 STEP {step['id']} {step['title']} 입니다.")

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input(f"예: {step['short']} 관련 문의를 입력하세요")
if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        system_prompt = (
            "너는 KCIM 경영관리본부 내부 응대 가이드 챗봇이다. "
            f"현재 단계는 STEP {step['id']} {step['title']} 이다. "
            "답변은 한국어로 작성하고 관리자가 임직원에게 설명하기 쉽게 짧고 친절하게 정리한다. "
            "법령 해석이 필요한 부분은 최신 기준과 사내 규정 확인이 필요하다고 함께 안내한다."
        )
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중"):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.chat_messages,
                    ],
                )
                answer = response.choices[0].message.content
                st.write(answer)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
    except KeyError:
        with st.chat_message("assistant"):
            st.warning("OPENAI_API_KEY 설정 후 상담 기능을 사용할 수 있습니다.")
    except Exception as e:
        with st.chat_message("assistant"):
            st.warning(f"일시적인 오류가 발생했습니다: {e}")

st.markdown('</div>', unsafe_allow_html=True)
