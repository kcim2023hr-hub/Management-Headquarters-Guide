import datetime
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# ================================================
# 개선된 CSS
# ================================================
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #17384b;
  --bg: #f5f7fb;
  --card: #ffffff;
  --line: #dbe4ee;
  --text: #1f2a35;
  --muted: #708191;
  --cyan: #11a8c7;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp { background: var(--bg); }

.block-container {
  padding-top: 1.2rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 1.2rem !important;
  padding-right: 1.2rem !important;
}

/* Hero Header */
.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff;
  border-radius: 20px;
  padding: 2rem 2rem 1.8rem 2rem;
  margin-bottom: 1.8rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(23, 56, 75, 0.25);
}

.hero-title {
  font-size: 1.95rem;
  font-weight: 800;
  margin: 0 0 0.6rem 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.55;
  opacity: 0.95;
  margin-bottom: 1.4rem;
}

.chip-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.25);
  color: #fff;
  border-radius: 9999px;
  padding: 0.55rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.date-chip {
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  border-radius: 9999px;
  padding: 0.55rem 1.2rem;
  font-size: 0.9rem;
  font-weight: 600;
  margin-left: auto;
}

/* Left Card */
.left-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.4rem 1.2rem;
  box-shadow: 0 8px 25px rgba(23, 43, 64, 0.06);
}

/* Main Area */
.quick-panel {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 16px;
  margin-bottom: 1.6rem;
}

.quick-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.4rem;
  box-shadow: 0 8px 22px rgba(23, 43, 64, 0.05);
}

.quick-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.9rem;
}

.guide-box {
  background: #f4fbfe;
  border: 1px solid #d0ecf8;
  border-radius: 16px;
  padding: 1.1rem 1.3rem;
  line-height: 1.7;
  font-size: 0.97rem;
}

.status-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.status-box {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1.1rem 1rem;
  text-align: center;
}

.status-label {
  font-size: 0.8rem;
  color: var(--muted);
  margin-bottom: 6px;
}

.status-value {
  font-size: 1.02rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1.4;
}

.main-card, .faq-card, .chat-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: 0 8px 22px rgba(23, 43, 64, 0.05);
}

.main-card-header {
  padding: 1.3rem 1.4rem;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  gap: 16px;
}

.step-badge {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.35rem;
}

.main-title {
  font-size: 1.32rem;
  font-weight: 800;
  color: var(--text);
}

.item-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 0.75rem 0;
  border-bottom: 1px solid #edf2f7;
  font-size: 0.96rem;
}

.item-row:last-child { border-bottom: 0; }

.warn-box {
  border-radius: 16px;
  border: 1px solid #ffd7de;
  background: #fff6f8;
  padding: 1rem;
  line-height: 1.65;
  font-size: 0.93rem;
  color: #9a2948;
  margin-bottom: 0.8rem;
}

.form-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: #f8fafc;
  padding: 0.55rem 0.9rem;
  font-size: 0.86rem;
  color: var(--navy);
}

@media (max-width: 1100px) {
  .quick-panel, .status-row {
    grid-template-columns: 1fr;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

# ================================================
# 데이터
# ================================================
COMMON_FORM_GUIDE = {
    "location": "플로우 내 [KCIM] 전체 공지사항 > 상단고정 > [공지] 사내 주요 양식 안내 > 2. 휴가 및 휴직",
    "form_name": "KCIM_임신•육아기 관련 지원 신청서",
    "tabs": [
        "임신기/육아기 근로시간 단축신청서",
        "임산부 정기건강진단 신청서",
        "유산/사산 휴가 신청서",
        "임신기/육아기 근로시간 단축 변경신청서",
    ],
}

STEPS = [
    {
        "id": 1,
        "title": "임신 확인 및 초기 안내",
        "short": "임신 확인",
        "period": "임신 확인 직후",
        "color": "#4FACCC",
        "summary": "임신 사실 확인 직후 개인정보 보호 원칙과 바로 신청 가능한 지원 제도를 안내하는 단계입니다.",
        "guide": "먼저 축하 인사를 전한 뒤 임신 사실 공유 범위를 확인하고, 플로우 상단고정에 있는 신청서 위치와 현재 바로 신청 가능한 제도를 함께 안내해 주세요.",
        "check": [
            "임신 사실 공유 범위를 당사자와 먼저 확인하기",
            "임신기 근로시간 단축 신청 가능 여부 안내하기",
            "플로우 내 신청서 위치와 작성 방법 안내하기",
            "향후 출산휴가와 육아휴직 흐름을 간단히 설명하기",
        ],
        "forms": ["임신기/육아기 근로시간 단축신청서"],
        "warn": [
            "임신을 이유로 한 불이익 조치나 업무 배제는 금지됩니다.",
            "당사자 동의 없이 임신 사실 공유하지 않도록 주의해 주세요.",
        ],
        "faq": [
            ("처음 문의가 오면 무엇부터 안내하면 되나요", "개인정보 보호 원칙과 신청서 위치를 먼저 안내한 뒤 현재 바로 신청 가능한 제도를 설명해 주는 것이 좋습니다."),
            ("신청서는 어디에서 찾나요", "플로우 내 [KCIM] 전체 공지사항 상단고정의 [공지] 사내 주요 양식 안내에서 2. 휴가 및 휴직 항목을 확인하면 됩니다."),
            ("처음 단계에서 바로 신청 가능한 것은 무엇인가요", "개별 상황에 따라 다르지만 대표적으로 임신기 근로시간 단축 여부를 먼저 확인해 안내하면 좋습니다."),
        ],
        "next_step": "단축근무 여부 확인",
        "target": "임신 확인한 임직원",
    },
    {
        "id": 2,
        "title": "임신기 근로시간 단축",
        "short": "임신기 단축",
        "period": "적용 가능 시기 확인 후",
        "color": "#37B89A",
        "summary": "임신기 중 근로시간 단축 신청 가능 여부를 확인하고 실제 운영 시간을 조율하는 단계입니다.",
        "guide": "직원의 임신 주수와 근무 상황을 먼저 확인한 뒤, 플로우 양식의 임신기/육아기 근로시간 단축신청서 또는 변경신청서를 안내해 주세요.",
        "check": [
            "적용 가능 시기와 현재 임신 주수 먼저 확인하기",
            "단축 시간대와 업무 공백 조율하기",
            "최초 신청인지 변경 신청인지 구분하기",
            "필요 시 변경신청서 사용 여부 안내하기",
        ],
        "forms": ["임신기/육아기 근로시간 단축신청서", "임신기/육아기 근로시간 단축 변경신청서"],
        "warn": [
            "신청 내용이 바뀌는 경우 최초 신청서가 아니라 변경신청서 사용 여부를 같이 확인해 주세요.",
            "법령 기준과 사내 운영 기준을 함께 확인한 뒤 안내해야 혼선이 줄어듭니다.",
        ],
        "faq": [
            ("처음 신청과 변경 신청은 어떻게 구분하나요", "처음 단축근무를 신청하는 경우는 신청서를, 이미 운영 중인 시간을 변경하는 경우는 변경신청서를 안내하는 것이 좋습니다."),
            ("신청서는 어디에서 찾나요", "플로우 내 [KCIM] 전체 공지사항 상단고정의 [공지] 사내 주요 양식 안내에서 2. 휴가 및 휴직 항목을 확인하면 됩니다."),
            ("직원이 시간 조정을 다시 원하면 어떻게 하나요", "운영 중 변경이 필요한 경우 임신기/육아기 근로시간 단축 변경신청서를 안내해 주세요."),
        ],
        "next_step": "건강진단 시간 안내",
        "target": "단축근무 희망자",
    },
    {
        "id": 3,
        "title": "임산부 정기건강진단",
        "short": "건강진단",
        "period": "임신 주수별 검진 시기",
        "color": "#F5A623",
        "summary": "정기 검진 시간 인정과 신청서 작성 안내를 빠르게 처리하는 단계입니다.",
        "guide": "검진 일정이 확인되면 플로우 양식의 임산부 정기건강진단 신청서를 안내하고, 검진 일정과 근무시간 처리 기준을 함께 설명해 주세요.",
        "check": [
            "검진 일정과 진료 예정일 확인하기",
            "임산부 정기건강진단 신청서 작성 위치 안내하기",
            "근로시간 인정 방식과 사후 확인 방법 설명하기",
            "누락 없이 내부 기록 남기기",
        ],
        "forms": ["임산부 정기건강진단 신청서"],
        "warn": [
            "증빙 없이 구두 처리만 하면 나중에 해석 차이가 생길 수 있습니다.",
            "정기 검진 관련 안내는 신청서 작성과 일정 확인을 함께 설명하는 편이 좋습니다.",
        ],
        "faq": [
            ("정기 검진 때 어떤 양식을 쓰나요", "플로우 내 KCIM_임신•육아기 관련 지원 신청서에서 임산부 정기건강진단 신청서 탭을 작성하면 됩니다."),
            ("매번 신청서를 받아야 하나요", "반복되는 경우에도 내부 기록을 남기는 방식이 가장 안전합니다."),
            ("신청서 위치를 어떻게 설명하면 좋나요", "플로우 내 [KCIM] 전체 공지사항 상단고정의 [공지] 사내 주요 양식 안내에서 2. 휴가 및 휴직 항목이라고 안내하면 찾기 쉽습니다."),
        ],
        "next_step": "연차 일정 점검",
        "target": "정기 검진 대상자",
    },
    {
        "id": 4,
        "title": "잔여 연차 및 일정 정리",
        "short": "연차 정리",
        "period": "출산휴가 시작 전",
        "color": "#9B59B6",
        "summary": "출산휴가 전에 남은 연차와 전체 일정 흐름을 정리해 실제 사용 계획을 맞추는 단계입니다.",
        "guide": "잔여 연차를 먼저 확인하고 출산휴가 시작일과 이어지는 전체 일정을 같이 정리해 주세요. 이 단계는 별도 탭 양식보다는 일정 조율과 다음 신청 준비가 핵심입니다.",
        "check": [
            "당해 연도 잔여 연차 확인하기",
            "연차 사용 희망 일정 확인하기",
            "출산휴가 시작일과 연결 일정 정리하기",
            "다음 단계 신청서 작성 시점을 미리 안내하기",
        ],
        "forms": ["다음 단계 신청서 사전 안내"],
        "warn": [
            "연차 사용은 직원 의사를 우선 확인해야 하며 강제 소진처럼 보이지 않도록 주의해 주세요.",
        ],
        "faq": [
            ("연차 정리 단계에서도 별도 양식이 있나요", "이 단계는 주로 일정 조율과 다음 신청 준비가 중심이며, 이후 단계에서 필요한 양식을 미리 안내해 주는 방식이 좋습니다."),
            ("무엇을 먼저 정리하면 좋나요", "잔여 연차 종료일 출산휴가 시작일 인수인계 시점을 한 번에 볼 수 있게 정리하면 좋습니다."),
        ],
        "next_step": "출산 관련 신청",
        "target": "출산휴가 예정자",
    },
    {
        "id": 5,
        "title": "출산 전후 관련 신청 안내",
        "short": "출산 관련",
        "period": "출산 전후 상황 발생 시",
        "color": "#E8556D",
        "summary": "출산 전후 상황에 맞춰 관련 신청서를 정확히 안내하는 단계입니다.",
        "guide": "출산 관련 문의가 오면 먼저 상황을 확인한 뒤, 현재 플로우 양식 탭 기준으로 필요한 신청서를 정확히 안내해 주세요.",
        "check": [
            "현재 문의가 출산휴가인지 유산 사산 휴가인지 먼저 구분하기",
            "플로우 양식 탭 중 해당 신청서 존재 여부 확인하기",
            "유산 사산 관련 문의 시 유산/사산 휴가 신청서 안내하기",
            "그 외 출산 전후 문의는 별도 내부 운영 절차와 함께 설명하기",
        ],
        "forms": ["유산/사산 휴가 신청서"],
        "warn": [
            "출산휴가 자체 양식이 별도로 있는지는 내부 공지 추가 확인이 필요합니다.",
        ],
        "faq": [
            ("출산 관련 문의 시 어떤 양식을 먼저 봐야 하나요", "현재 제공된 플로우 탭 기준으로는 유산 사산 관련 상황에서 유산/사산 휴가 신청서를 안내할 수 있습니다."),
        ],
        "next_step": "육아기 지원 안내",
        "target": "출산 전후 문의자",
    },
    {
        "id": 6,
        "title": "육아기 지원 및 변경 안내",
        "short": "육아기 지원",
        "period": "육아기 제도 운영 중",
        "color": "#2980B9",
        "summary": "육아기 근로시간 단축 운영과 변경 문의를 빠르게 처리하는 단계입니다.",
        "guide": "육아기 지원 문의가 오면 현재 운영 중인지 최초 신청인지 변경인지부터 확인한 뒤, 플로우 양식의 임신기/육아기 근로시간 단축신청서 또는 변경신청서를 안내해 주세요.",
        "check": [
            "최초 신청인지 변경 요청인지 구분하기",
            "육아기 근로시간 단축신청서 또는 변경신청서 안내하기",
            "현재 근무 형태와 변경 희망사항 확인하기",
            "다음 복직 계획이 있는지도 함께 확인하기",
        ],
        "forms": ["임신기/육아기 근로시간 단축신청서", "임신기/육아기 근로시간 단축 변경신청서"],
        "warn": [
            "육아기 문의도 동일 양식 내 탭을 사용하는 구조이므로 탭 명칭을 정확히 안내하는 것이 중요합니다.",
        ],
        "faq": [
            ("육아기에도 같은 신청서를 쓰나요", "네 현재 제공된 정보 기준으로 임신기/육아기 근로시간 단축신청서와 변경신청서를 함께 사용하는 구조입니다."),
            ("근무시간을 바꾸고 싶다고 하면 무엇을 안내하나요", "이미 운영 중인 조건을 조정하는 경우에는 변경신청서를 먼저 안내하는 것이 좋습니다."),
        ],
        "next_step": "복직 준비 점검",
        "target": "제도 이용자",
    },
    {
        "id": 7,
        "title": "복직 및 최종 일정 확인",
        "short": "복직 준비",
        "period": "복직 전후",
        "color": "#27AE60",
        "summary": "복직 일정 확인과 필요 시 육아기 단축 변경 여부를 함께 점검하는 단계입니다.",
        "guide": "복직 의사를 먼저 확인한 뒤 현재 육아기 제도 운영 중이면 유지 변경 종료 여부를 같이 확인해 주세요. 필요 시 변경신청서 사용 여부를 함께 안내하면 좋습니다.",
        "check": [
            "복직일과 복직 의사 먼저 확인하기",
            "현재 육아기 단축근무 운영 여부 확인하기",
            "복직 전 변경 또는 종료가 필요한지 점검하기",
            "필요 시 변경신청서 또는 후속 절차 안내하기",
        ],
        "forms": ["임신기/육아기 근로시간 단축 변경신청서"],
        "warn": [
            "복직 단계는 제도 설명보다 실제 일정과 운영 변경 여부를 함께 확인하는 것이 더 중요합니다.",
        ],
        "faq": [
            ("복직 전에 무엇을 먼저 확인하면 좋나요", "복직일 현재 근무 형태 그리고 육아기 제도 유지 변경 종료 여부를 먼저 확인하면 좋습니다."),
            ("복직하면서 단축조건을 바꾸는 경우는요", "현재 운영 조건을 변경하는 경우에는 변경신청서 사용 여부를 함께 안내하면 좋습니다."),
        ],
        "next_step": "사후 관리",
        "target": "복직 예정자",
    },
]

# ================================================
# 세션 상태
# ================================================
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

active_step = st.session_state.active_step
if not (0 <= active_step < len(STEPS)):
    st.session_state.active_step = 0
    active_step = 0

step = STEPS[active_step]

# ================================================
# 헤더
# ================================================
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-title">👶 KCIM 출산 육아 응대 가이드</div>
      <div class="hero-desc">
        임신 확인부터 복직까지 관리자 입장에서 빠르게 응대할 수 있도록 단계별 핵심만 정리한 페이지입니다.
      </div>
      <div class="chip-container">
        <div class="chip">📌 단계별 빠른 응대 중심</div>
        <div class="chip">🧾 필요 서류 즉시 확인</div>
        <div class="date-chip">기준일 {datetime.date.today()}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================================
# 레이아웃 구성
# ================================================
left_col, main_col = st.columns([1.1, 3.6], gap="medium")

# --- 좌측 메뉴 영역 ---
with left_col:
    st.markdown('<div class="left-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1.1rem; font-weight:800; color:var(--navy); margin-bottom:1rem;">단계 선택</div>', unsafe_allow_html=True)

    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"step_btn_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    
    # 아코디언(Expander)으로 양식 안내 숨기기 (공간 최적화)
    with st.expander("📂 주요 양식 및 경로 안내"):
        st.markdown(
            f"""
            <div style="line-height:1.65;font-size:0.85rem;">
              <b>경로:</b><br>{COMMON_FORM_GUIDE['location']}<br><br>
              <b>양식명:</b><br>{COMMON_FORM_GUIDE['form_name']}
            </div>
            <div style="font-weight:700; margin-top:0.8rem; margin-bottom:0.4rem; font-size:0.85rem;">[신청서 탭]</div>
            <div style="line-height:1.7;font-size:0.85rem;">
            """ +
            '<br>'.join([f'• {x}' for x in COMMON_FORM_GUIDE['tabs']]) +
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

# --- 우측 메인 콘텐츠 영역 (탭 분리 적용) ---
with main_col:
    tab_guide, tab_chat = st.tabs(["📖 단계별 가이드", "🤖 AI 비서 상담"])

    # 1. 가이드 탭
    with tab_guide:
        # 빠른 확인 뱃지와 메인 스크립트 박스 상단 배치
        st.markdown(
            f"""
            <div class="main-card" style="padding:1.4rem; margin-bottom:1.6rem; border-left: 6px solid {step['color']};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="color:var(--muted); font-size:0.9rem; font-weight:700; margin-bottom:0.2rem;">STEP {step['id']}</div>
                        <div class="main-title" style="margin-bottom:0.4rem;">{step['title']}</div>
                        <div style="color:var(--muted); font-size:0.95rem;">{step['summary']}</div>
                    </div>
                    <div style="text-align:right;">
                        <span class="form-chip">👤 대상: {step['target']}</span>
                        <span class="form-chip">➡️ 다음: {step['next_step']}</span>
                    </div>
                </div>
                
                <div style="margin-top:1.5rem;">
                    <div style="font-size:0.95rem;font-weight:800;color:var(--navy);margin-bottom:0.6rem;">🗣️ 담당자 안내 스크립트</div>
                    <div style="background:#f4fbfe; border:1px solid #d0ecf8; border-radius:12px; padding:1.2rem; font-size:1.05rem; line-height:1.6; font-weight:500; color:#0e5a78;">
                        {step['guide']}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 체크리스트와 필요 서류 좌우 배치
        col_chk, col_doc = st.columns([1.1, 0.9])
        with col_chk:
            st.markdown('<div style="border:1px solid var(--line);border-radius:16px;padding:1.2rem;background:#fff;height:100%;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:1rem;">✅ HR 담당자 체크리스트</div>', unsafe_allow_html=True)
            for item in step["check"]:
                st.markdown(f'<div class="item-row"><span style="color:#11a8c7">✔</span> {item}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_doc:
            st.markdown('<div style="border:1px solid var(--line);border-radius:16px;padding:1.2rem;background:#fff;height:100%;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:0.8rem;">🧾 필요 서류</div>', unsafe_allow_html=True)
            for form in step["forms"]:
                st.markdown(f'<div class="form-chip" style="margin-bottom:0.6rem;">📄 {form}</div>', unsafe_allow_html=True)
            
            if step["warn"]:
                st.markdown('<div style="margin-top:1.5rem; font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:0.6rem;">⚠️ 주의사항</div>', unsafe_allow_html=True)
                for warn in step["warn"]:
                    st.markdown(f'<div style="color:#9a2948; font-size:0.88rem; line-height:1.5; padding:0.6rem; background:#fff6f8; border-radius:8px; margin-bottom:0.4rem;">{warn}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # FAQ 영역 (아코디언 형태)
        st.markdown('<div style="margin-top:2rem; font-size:1.1rem;font-weight:800;color:var(--navy);margin-bottom:1rem;">❓ 자주 받는 질문 (FAQ)</div>', unsafe_allow_html=True)
        for q, a in step["faq"]:
            with st.expander(f"Q. {q}"):
                st.write(a)
        
        # 하단 네비게이션 버튼
        st.markdown('<hr style="margin:2rem 0; border:none; border-top:1px solid var(--line);">', unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if active_step > 0:
                if st.button("← 이전 단계", use_container_width=True):
                    st.session_state.active_step -= 1
                    st.rerun()
        with nav2:
            st.markdown(f"<div style='text-align:center; padding-top:8px; color:var(--muted); font-size:0.9rem;'>{active_step+1} / {len(STEPS)} 단계</div>", unsafe_allow_html=True)
        with nav3:
            if active_step < len(STEPS) - 1:
                if st.button("다음 단계 →", use_container_width=True):
                    st.session_state.active_step += 1
                    st.rerun()

    # 2. 챗봇 상담 탭 (가장 상단에서 탭 클릭 시 바로 보임)
    with tab_chat:
        st.markdown(
            f"""
            <div style="background:#eaf5fa; border-radius:12px; padding:1.2rem; margin-bottom:1.5rem;">
                <div style="font-size:1.1rem; font-weight:800; color:var(--navy); margin-bottom:0.4rem;">🤖 AI 비서에게 질문하기</div>
                <div style="font-size:0.9rem; color:#4a5d6e;">현재 선택된 <b>[STEP {step['id']} {step['title']}]</b> 단계에 대해 궁금한 점을 편하게 물어보세요!</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # st.chat_input은 탭 안에 배치해도 정상 동작합니다.
        if prompt := st.chat_input(f"예: {step['short']} 관련 문의를 입력하세요"):
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
                    with st.spinner("답변 생성 중..."):
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "system", "content": system_prompt}, *st.session_state.chat_messages],
                        )
                        answer = response.choices[0].message.content
                        st.write(answer)
                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                with st.chat_message("assistant"):
                    st.error(f"상담 서비스 오류가 발생했습니다: {str(e)[:100]}")
