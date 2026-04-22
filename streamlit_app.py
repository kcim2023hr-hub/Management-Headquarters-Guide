import datetime
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# ================================================
# CSS - 사이드바 중복 완전 제거 버전
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

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; }
.stApp { background: var(--bg); }

.block-container { padding: 1.2rem 1.2rem 2.5rem 1.2rem !important; }

/* Hero Header */
.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff;
  border-radius: 20px;
  padding: 2rem 2rem 1.8rem 2rem;
  margin-bottom: 1.8rem;
  position: relative;
  overflow: hidden;
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

.chip-container { display: flex; flex-wrap: wrap; gap: 10px; }
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

/* 좌측 단계 선택 - 버튼 완전 제거, 카드 리스트만 */
.left-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.5rem 1.2rem;
  box-shadow: 0 8px 25px rgba(23, 43, 64, 0.06);
  height: 100%;
}

.stage-list {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 15px 16px;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: #fff;
  cursor: pointer;
  transition: all 0.25s ease;
}

.stage-item:hover {
  border-color: var(--cyan);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(17, 168, 199, 0.15);
}

.stage-item.active {
  border-color: transparent;
  background: linear-gradient(90deg, #f0f9ff, #e0f2fe);
  box-shadow: 0 10px 25px rgba(17, 168, 199, 0.22);
}

.stage-num {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.15rem;
  color: #fff;
  flex-shrink: 0;
}

.stage-label {
  font-weight: 700;
  font-size: 0.98rem;
  color: var(--text);
  line-height: 1.35;
}

/* 메인 영역 스타일 */
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

.status-label { font-size: 0.8rem; color: var(--muted); margin-bottom: 6px; }
.status-value { font-size: 1.02rem; font-weight: 800; color: var(--text); line-height: 1.4; }

.main-card, .faq-card, .chat-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: 0 8px 22px rgba(23, 43, 64, 0.05);
}

.step-badge {
  width: 64px; height: 64px; border-radius: 18px;
  color: white; font-weight: 800; font-size: 1.35rem;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}

.item-row {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 0.75rem 0; border-bottom: 1px solid #edf2f7; font-size: 0.96rem;
}
.item-row:last-child { border-bottom: 0; }

.warn-box {
  border-radius: 16px; border: 1px solid #ffd7de; background: #fff6f8;
  padding: 1rem; line-height: 1.65; font-size: 0.93rem; color: #9a2948; margin-bottom: 0.8rem;
}

.form-chip {
  display: inline-flex; align-items: center; gap: 6px;
  border-radius: 999px; border: 1px solid var(--line); background: #f8fafc;
  padding: 0.55rem 0.9rem; font-size: 0.86rem; color: var(--navy);
}

.faq-item {
  border: 1px solid var(--line); border-radius: 16px; padding: 1.1rem;
  background: #fff; margin-bottom: 1rem;
}

@media (max-width: 1100px) {
  .quick-panel, .status-row { grid-template-columns: 1fr; }
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
        "id": 1, "title": "임신 확인 및 초기 안내", "short": "임신 확인", "period": "임신 확인 직후",
        "color": "#4FACCC", "summary": "임신 사실 확인 직후 개인정보 보호 원칙과 바로 신청 가능한 지원 제도를 안내하는 단계입니다.",
        "guide": "먼저 축하 인사를 전한 뒤 임신 사실 공유 범위를 확인하고, 플로우 상단고정에 있는 신청서 위치와 현재 바로 신청 가능한 제도를 함께 안내해 주세요.",
        "check": ["임신 사실 공유 범위를 당사자와 먼저 확인하기", "임신기 근로시간 단축 신청 가능 여부 안내하기", "플로우 내 신청서 위치와 작성 방법 안내하기", "향후 출산휴가와 육아휴직 흐름을 간단히 설명하기"],
        "forms": ["임신기/육아기 근로시간 단축신청서"],
        "warn": ["임신을 이유로 한 불이익 조치나 업무 배제는 금지됩니다.", "당사자 동의 없이 임신 사실을 공유하지 않도록 주의해 주세요."],
        "faq": [("처음 문의가 오면 무엇부터 안내하면 되나요", "개인정보 보호 원칙과 신청서 위치를 먼저 안내한 뒤 현재 바로 신청 가능한 제도를 설명해 주는 것이 좋습니다.")],
        "next_step": "임신기 근로시간 단축 여부 확인", "target": "임신 확인한 임직원"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "period": "적용 가능 시기 확인 후",
        "color": "#37B89A", "summary": "임신기 중 근로시간 단축 신청 가능 여부를 확인하고 실제 운영 시간을 조율하는 단계입니다.",
        "guide": "직원의 임신 주수와 근무 상황을 먼저 확인한 뒤, 플로우 양식의 임신기/육아기 근로시간 단축신청서 또는 변경신청서를 안내해 주세요.",
        "check": ["적용 가능 시기와 현재 임신 주수 먼저 확인하기", "단축 시간대와 업무 공백 조율하기", "최초 신청인지 변경 신청인지 구분하기", "필요 시 변경신청서 사용 여부 안내하기"],
        "forms": ["임신기/육아기 근로시간 단축신청서", "임신기/육아기 근로시간 단축 변경신청서"],
        "warn": ["신청 내용이 바뀌는 경우 최초 신청서가 아니라 변경신청서 사용 여부를 같이 확인해 주세요."],
        "faq": [("처음 신청과 변경 신청은 어떻게 구분하나요", "처음 단축근무를 신청하는 경우는 신청서를, 이미 운영 중인 시간을 변경하는 경우는 변경신청서를 안내하는 것이 좋습니다.")],
        "next_step": "정기건강진단 시간 안내", "target": "임신기 단축근무 희망자"
    },
    {
        "id": 3, "title": "임산부 정기건강진단", "short": "건강진단", "period": "임신 주수별 검진 시기",
        "color": "#F5A623", "summary": "정기 검진 시간 인정과 신청서 작성 안내를 빠르게 처리하는 단계입니다.",
        "guide": "검진 일정이 확인되면 플로우 양식의 임산부 정기건강진단 신청서를 안내하고, 검진 일정과 근무시간 처리 기준을 함께 설명해 주세요.",
        "check": ["검진 일정과 진료 예정일 확인하기", "임산부 정기건강진단 신청서 작성 위치 안내하기", "근로시간 인정 방식과 사후 확인 방법 설명하기", "누락 없이 내부 기록 남기기"],
        "forms": ["임산부 정기건강진단 신청서"],
        "warn": ["증빙 없이 구두 처리만 하면 나중에 해석 차이가 생길 수 있습니다."],
        "faq": [("정기 검진 때 어떤 양식을 쓰나요", "플로우 내 KCIM_임신•육아기 관련 지원 신청서에서 임산부 정기건강진단 신청서 탭을 작성하면 됩니다.")],
        "next_step": "출산휴가 전 연차 일정 점검", "target": "임신 중 정기 검진 대상자"
    },
    {
        "id": 4, "title": "잔여 연차 및 일정 정리", "short": "연차 정리", "period": "출산휴가 시작 전",
        "color": "#9B59B6", "summary": "출산휴가 전에 남은 연차와 전체 일정 흐름을 정리해 실제 사용 계획을 맞추는 단계입니다.",
        "guide": "잔여 연차를 먼저 확인하고 출산휴가 시작일과 이어지는 전체 일정을 같이 정리해 주세요.",
        "check": ["당해 연도 잔여 연차 확인하기", "연차 사용 희망 일정 확인하기", "출산휴가 시작일과 연결 일정 정리하기", "다음 단계 신청서 작성 시점을 미리 안내하기"],
        "forms": ["다음 단계 신청서 사전 안내"],
        "warn": ["연차 사용은 직원 의사를 우선 확인해야 하며 강제 소진처럼 보이지 않도록 주의해 주세요."],
        "faq": [("연차 정리 단계에서도 별도 양식이 있나요", "이 단계는 주로 일정 조율과 다음 신청 준비가 중심입니다.")],
        "next_step": "출산 관련 신청 안내", "target": "출산휴가 예정 임직원"
    },
    {
        "id": 5, "title": "출산 전후 관련 신청 안내", "short": "출산 관련", "period": "출산 전후 상황 발생 시",
        "color": "#E8556D", "summary": "출산 전후 상황에 맞춰 관련 신청서를 정확히 안내하는 단계입니다.",
        "guide": "출산 관련 문의가 오면 먼저 상황을 확인한 뒤, 현재 플로우 양식 탭 기준으로 필요한 신청서를 정확히 안내해 주세요.",
        "check": ["현재 문의가 출산휴가인지 유산 사산 휴가인지 먼저 구분하기", "플로우 양식 탭 중 해당 신청서 존재 여부 확인하기", "유산 사산 관련 문의 시 유산/사산 휴가 신청서 안내하기"],
        "forms": ["유산/사산 휴가 신청서"],
        "warn": ["출산휴가 자체 양식이 별도로 있는지는 내부 공지 추가 확인이 필요합니다."],
        "faq": [("출산 관련 문의 시 어떤 양식을 먼저 봐야 하나요", "현재 제공된 플로우 탭 기준으로는 유산/사산 휴가 신청서를 안내할 수 있습니다.")],
        "next_step": "육아기 지원 또는 복직 관련 안내", "target": "출산 전후 관련 문의자"
    },
    {
        "id": 6, "title": "육아기 지원 및 변경 안내", "short": "육아기 지원", "period": "육아기 제도 운영 중",
        "color": "#2980B9", "summary": "육아기 근로시간 단축 운영과 변경 문의를 빠르게 처리하는 단계입니다.",
        "guide": "육아기 지원 문의가 오면 현재 운영 중인지 최초 신청인지 변경인지부터 확인한 뒤, 플로우 양식의 임신기/육아기 근로시간 단축신청서 또는 변경신청서를 안내해 주세요.",
        "check": ["최초 신청인지 변경 요청인지 구분하기", "육아기 근로시간 단축신청서 또는 변경신청서 안내하기", "현재 근무 형태와 변경 희망사항 확인하기"],
        "forms": ["임신기/육아기 근로시간 단축신청서", "임신기/육아기 근로시간 단축 변경신청서"],
        "warn": ["육아기 문의도 동일 양식 내 탭을 사용하는 구조입니다."],
        "faq": [("육아기에도 같은 신청서를 쓰나요", "네, 임신기/육아기 근로시간 단축신청서와 변경신청서를 함께 사용합니다.")],
        "next_step": "복직 준비 및 최종 일정 확인", "target": "육아기 지원 제도 이용자"
    },
    {
        "id": 7, "title": "복직 및 최종 일정 확인", "short": "복직 준비", "period": "복직 전후",
        "color": "#27AE60", "summary": "복직 일정 확인과 필요 시 육아기 단축 변경 여부를 함께 점검하는 단계입니다.",
        "guide": "복직 의사를 먼저 확인한 뒤 현재 육아기 제도 운영 중이면 유지 변경 종료 여부를 같이 확인해 주세요.",
        "check": ["복직일과 복직 의사 먼저 확인하기", "현재 육아기 단축근무 운영 여부 확인하기", "복직 전 변경 또는 종료가 필요한지 점검하기"],
        "forms": ["임신기/육아기 근로시간 단축 변경신청서"],
        "warn": ["복직 단계는 실제 일정과 운영 변경 여부를 함께 확인하는 것이 중요합니다."],
        "faq": [("복직 전에 무엇을 먼저 확인하면 좋나요", "복직일, 현재 근무 형태, 육아기 제도 유지 여부를 먼저 확인합니다.")],
        "next_step": "개별 상황 후속 관리", "target": "복직 예정자"
    }
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
        <div class="chip">💬 FAQ와 상담 연계</div>
        <div class="date-chip">기준일 {datetime.date.today()}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================================
# 레이아웃
# ================================================
left_col, main_col = st.columns([1.05, 3.7], gap="medium")

with left_col:
    st.markdown('<div class="left-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:1.2rem;">단계 선택</div>', unsafe_allow_html=True)

    for idx, s in enumerate(STEPS):
        active_class = "active" if idx == active_step else ""
        
        # 숨겨진 버튼 (클릭용)
        if st.button(f"select_{idx}", key=f"step_select_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()

        # 실제로 보이는 카드
        st.markdown(
            f"""
            <div class="stage-item {active_class}" 
                 style="border-left: 5px solid {s['color']};"
                 onclick="document.querySelector('button[key=\\'step_select_{idx}\\']').click()">
              <div class="stage-num" style="background:{s['color']};">{s['id']}</div>
              <div class="stage-label">{s['short']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 양식 안내
    st.markdown('<div style="height:2.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:1rem;">양식 안내</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:#f8fbff; border:1px solid #dbe4ee; border-radius:16px; padding:1.3rem; line-height:1.65; font-size:0.9rem;">
          <b>경로</b><br>{COMMON_FORM_GUIDE['location']}<br><br>
          <b>양식명</b><br>{COMMON_FORM_GUIDE['form_name']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top:1.3rem; font-size:0.95rem; font-weight:800; color:#17384b;">신청서 탭</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="background:#f8fbff; border:1px solid #dbe4ee; border-radius:16px; padding:1.2rem; line-height:1.7; font-size:0.9rem;">' +
        '<br>'.join([f'• {x}' for x in COMMON_FORM_GUIDE['tabs']]) +
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with main_col:
    # 바로 안내할 말 + 빠른 확인
    st.markdown(
        f"""
        <div class="quick-panel">
          <div class="quick-card">
            <div class="quick-title">바로 안내할 말</div>
            <div class="guide-box">{step['guide']}</div>
          </div>
          <div class="quick-card">
            <div class="quick-title">빠른 확인</div>
            <div class="status-row">
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

    # 메인 카드
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="padding:1.4rem 1.5rem; border-bottom:1px solid var(--line); display:flex; align-items:center; gap:18px;">
          <div class="step-badge" style="background:{step['color']}"><small>STEP</small>{step['id']}</div>
          <div>
            <div style="font-size:1.32rem; font-weight:800;">{step['title']}</div>
            <div style="color:var(--muted); font-size:0.95rem;">{step['period']} · {step['summary']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="padding:1.5rem;">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.95])
    with col1:
        st.markdown('<div style="border:1px solid var(--line); border-radius:18px; padding:1.3rem; background:#fff;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:1rem;">✅ HR 담당자 체크</div>', unsafe_allow_html=True)
        for item in step["check"]:
            st.markdown(f'<div class="item-row"><span style="color:#11a8c7">✔</span> {item}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="border:1px solid var(--line); border-radius:18px; padding:1.3rem; background:#fff;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:1rem;">🧾 필요 서류</div>', unsafe_allow_html=True)
        for form in step["forms"]:
            st.markdown(f'<div class="form-chip">📄 {form}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:0.8rem;">⚠️ 주의사항</div>', unsafe_allow_html=True)
        for warn in step["warn"]:
            st.markdown(f'<div class="warn-box">{warn}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 이전 / 다음 버튼
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c1:
        if active_step > 0:
            if st.button("← 이전 단계", use_container_width=True):
                st.session_state.active_step -= 1
                st.rerun()
    with c2:
        st.markdown(f"<div style='text-align:center; margin-top:12px; color:#708191; font-size:0.9rem;'>STEP {step['id']} / {len(STEPS)}</div>", unsafe_allow_html=True)
    with c3:
        if active_step < len(STEPS) - 1:
            if st.button("다음 단계 →", use_container_width=True):
                st.session_state.active_step += 1
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # main-card

    # FAQ
    st.markdown('<div class="faq-card" style="margin-top:1.8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:1rem;">❓ 자주 받는 질문</div>', unsafe_allow_html=True)
    for q, a in step.get("faq", []):
        st.markdown(
            f"""
            <div class="faq-item">
                <div style="font-weight:700; color:#17384b; margin-bottom:0.6rem;">Q. {q}</div>
                <div style="line-height:1.65;">{a}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # 챗봇
    st.markdown('<div class="chat-card" style="margin-top:1.8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem; font-weight:800; color:#17384b; margin-bottom:0.6rem;">🤖 추가 상담</div>', unsafe_allow_html=True)
    st.caption(f"현재 선택된 단계: STEP {step['id']} {step['title']}")

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input(f"예: {step['short']} 관련 문의를 입력하세요"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            system_prompt = f"너는 KCIM 경영관리본부 내부 응대 가이드 챗봇이다. 현재 단계는 STEP {step['id']} {step['title']} 이다. 답변은 한국어로 작성하고 관리자가 임직원에게 설명하기 쉽게 짧고 친절하게 정리한다."
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": system_prompt}, *st.session_state.chat_messages]
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"상담 서비스 오류가 발생했습니다.")

    st.markdown('</div>', unsafe_allow_html=True)
