import datetime
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KCIM 출산 육아 여정 가이드",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
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
  --navy-2: #204a61;
  --cyan: #11a8c7;
  --bg: #f4f7fb;
  --card: #ffffff;
  --line: #dbe4ee;
  --text: #1d2a35;
  --muted: #6f8092;
  --danger: #e4586e;
  --success: #1f9d63;
}

html, body, [class*="css"]  {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp {
  background: var(--bg);
}

.block-container {
  max-width: 1180px;
  padding-top: 1.5rem;
  padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--navy) 0%, #143246 100%);
  border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] * {
  color: #e8f0f5 !important;
}

.sidebar-section-title {
  font-size: 0.88rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  margin: 0.25rem 0 0.7rem 0;
}

.hero {
  background: linear-gradient(135deg, #18384c 0%, #156a8d 100%);
  border-radius: 24px;
  padding: 1.7rem 1.8rem;
  color: white;
  position: relative;
  overflow: hidden;
  box-shadow: 0 12px 28px rgba(20, 48, 70, 0.16);
  margin-bottom: 1.2rem;
}

.hero::after {
  content: '';
  position: absolute;
  right: -60px;
  top: -40px;
  width: 220px;
  height: 220px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
}

.hero-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.35rem;
  letter-spacing: -0.02em;
}

.hero-sub {
  color: rgba(255,255,255,0.82);
  font-size: 0.95rem;
  line-height: 1.6;
}

.top-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 1rem;
}

.inline-chip-wrap {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.inline-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.45rem 0.8rem;
  font-size: 0.8rem;
  color: var(--muted);
}

.timeline-wrap {
  background: white;
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 1.2rem 1rem 1rem 1rem;
  box-shadow: 0 8px 22px rgba(25, 40, 60, 0.05);
  margin-bottom: 1rem;
}

.timeline-line {
  height: 4px;
  background: linear-gradient(90deg, #dfe7ef 0%, #dfe7ef 100%);
  border-radius: 999px;
  margin: 1.05rem 22px 0.2rem 22px;
}

.timeline-label {
  text-align: center;
  font-size: 0.75rem;
  color: var(--muted);
  line-height: 1.35;
  min-height: 2.4rem;
}

.timeline-num {
  width: 44px;
  height: 44px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.45rem auto;
  border: 2px solid var(--line);
  background: #fff;
  color: var(--muted);
  font-weight: 800;
}

.timeline-num.active {
  color: #fff;
  border-color: transparent;
  box-shadow: 0 10px 22px rgba(0,0,0,0.12);
}

.section-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 24px;
  box-shadow: 0 10px 24px rgba(20, 41, 64, 0.06);
  overflow: hidden;
}

.section-head {
  padding: 1.2rem 1.35rem;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.section-head-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-badge {
  min-width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  flex-direction: column;
  line-height: 1.05;
  box-shadow: inset 0 -6px 18px rgba(0,0,0,0.08);
}

.step-badge small {
  font-size: 0.68rem;
  opacity: 0.95;
}

.step-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 0.2rem;
}

.step-period {
  font-size: 0.9rem;
  color: var(--muted);
}

.step-body {
  padding: 1.2rem 1.35rem 1.35rem 1.35rem;
}

.sub-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 16px;
}

.info-block {
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1rem 1rem;
  background: #fff;
}

.info-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.8rem;
}

.check-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 0.58rem 0;
  border-bottom: 1px solid #eef3f8;
  color: var(--text);
  font-size: 0.92rem;
  line-height: 1.55;
}

.check-item:last-child {
  border-bottom: 0;
}

.warn-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: #fff6f8;
  border: 1px solid #ffd5de;
  color: #8e2442;
  padding: 0.78rem 0.9rem;
  border-radius: 14px;
  font-size: 0.9rem;
  line-height: 1.55;
  margin-bottom: 0.55rem;
}

.point-item {
  background: #f3fbff;
  border: 1px solid #d8eef7;
  border-left: 4px solid var(--cyan);
  padding: 0.85rem 0.95rem;
  border-radius: 14px;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--text);
  margin-bottom: 0.6rem;
}

.form-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0.65rem 0.85rem;
  border-radius: 999px;
  background: #f8fafc;
  border: 1px solid var(--line);
  color: var(--navy);
  font-size: 0.86rem;
  margin: 0 0.45rem 0.45rem 0;
}

.metric-box {
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1rem;
  text-align: center;
  background: linear-gradient(180deg, #fff 0%, #f8fbff 100%);
}

.metric-label {
  color: var(--muted);
  font-size: 0.8rem;
  margin-bottom: 0.3rem;
}

.metric-value {
  font-size: 1.45rem;
  font-weight: 900;
}

.bottom-nav-note {
  font-size: 0.86rem;
  color: var(--muted);
  text-align: center;
  padding-top: 0.65rem;
}

.chat-shell {
  background: white;
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 1rem 1rem 0.6rem 1rem;
  box-shadow: 0 8px 22px rgba(25, 40, 60, 0.05);
}

.chat-title {
  font-size: 0.98rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 0.35rem;
}

.chat-desc {
  font-size: 0.86rem;
  color: var(--muted);
  margin-bottom: 0.8rem;
}

.stButton > button {
  border-radius: 12px !important;
  border: 1px solid var(--line) !important;
  font-weight: 700 !important;
}

[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  color: #fff !important;
  text-align: left !important;
  min-height: 50px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.12) !important;
}

@media (max-width: 900px) {
  .sub-grid {
    grid-template-columns: 1fr;
  }
  .hero-title {
    font-size: 1.28rem;
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
        "icon": "🤰",
        "title": "임신 확인 및 신고",
        "period": "임신 확인 즉시",
        "color": "#4FACCC",
        "checklist": [
            "임신 사실 확인 후 축하 및 비공개 원칙 안내",
            "임신기 근로시간 단축 가능 여부 안내",
            "임산부 보호 규정과 신청 절차 설명",
            "인사 상태값과 내부 관리 일정 등록",
        ],
        "warnings": [
            "임신을 이유로 한 불이익 조치나 업무 배제는 금지됩니다.",
            "당사자 동의 없는 임신 사실 공유는 피해야 합니다.",
        ],
        "points": [
            "임신 확인 직후부터 안내를 시작하면 이후 출산휴가와 육아휴직 연결이 훨씬 매끄럽습니다.",
        ],
        "forms": ["임신 사실 확인 및 초기 상담 체크리스트"],
    },
    {
        "id": 2,
        "icon": "⏰",
        "title": "임신기 근로시간 단축",
        "period": "12주 이내 또는 32주 이후",
        "color": "#37B89A",
        "checklist": [
            "신청서 접수 및 적용 가능 시기 확인",
            "단축 시간대와 업무 공백 조정",
            "급여 삭감 금지 원칙 재확인",
            "팀장과 실무 인수 범위 공유",
        ],
        "warnings": [
            "적용 구간과 신청 사유는 법령 기준과 사내 운영 기준을 함께 확인해야 합니다.",
            "임금 삭감이나 사용 거부는 분쟁으로 이어질 수 있습니다.",
        ],
        "points": [
            "안내 문구는 법령상 기준과 사내 운영 원칙을 분리해 표기하는 방식이 가장 안전합니다.",
        ],
        "forms": ["임신기 육아기 근로시간 단축 신청서"],
    },
    {
        "id": 3,
        "icon": "🏥",
        "title": "임산부 정기건강진단",
        "period": "임신 주수별 허용",
        "color": "#F5A623",
        "checklist": [
            "신청서 접수와 검진 일정 확인",
            "근로시간 인정 여부와 증빙 수령 안내",
            "사후 확인서 제출 기준 정리",
        ],
        "warnings": [
            "유급 처리와 증빙 기준이 누락되면 추후 해석 차이가 생길 수 있습니다.",
        ],
        "points": [
            "주수별 허용 시간은 별도 표로 정리해 한 번에 보이게 구성하는 편이 좋습니다.",
        ],
        "forms": ["임산부 정기건강진단 신청서"],
    },
    {
        "id": 4,
        "icon": "📅",
        "title": "잔여 연차 선 소진",
        "period": "출산휴가 시작 전",
        "color": "#9B59B6",
        "checklist": [
            "잔여 연차와 선사용 가능 여부 확인",
            "출산휴가 시작일과 연속 일정표 정리",
            "팀 업무 공백 최소화 일정 조율",
        ],
        "warnings": [
            "연차 소진은 직원 선택이 우선이며 강제 운영은 피해야 합니다.",
        ],
        "points": [
            "연차와 출산휴가가 이어지는 달력형 화면이 있으면 이해도가 크게 높아집니다.",
        ],
        "forms": ["연차 사용 계획 확인표"],
    },
    {
        "id": 5,
        "icon": "🍼",
        "title": "출산휴가",
        "period": "단태아 90일 다태아 120일",
        "color": "#E8556D",
        "checklist": [
            "출산휴가 신청서와 예정일 증빙 접수",
            "급여 처리 구간과 보험 신청 구분",
            "실제 출산일 변경 시 정정 절차 안내",
        ],
        "warnings": [
            "출산 후 의무 사용기간은 별도로 눈에 띄게 강조하는 편이 좋습니다.",
        ],
        "points": [
            "단태아 다태아 기준은 숫자 카드 형태로 배치하면 가독성이 좋아집니다.",
        ],
        "forms": ["출산휴가 신청서"],
        "metrics": [
            {"label": "단태아", "value": "90일"},
            {"label": "다태아", "value": "120일"},
        ],
    },
    {
        "id": 6,
        "icon": "🤱",
        "title": "육아휴직",
        "period": "부모 각각 최대 1년",
        "color": "#2980B9",
        "checklist": [
            "휴직 시작 전 신청서와 가족관계 확인",
            "급여 중지와 4대보험 변동 처리 점검",
            "인수인계와 복직 예정일 관리",
        ],
        "warnings": [
            "급여 안내는 반드시 최신 기준으로 별도 검토 후 반영해야 합니다.",
        ],
        "points": [
            "정책 개편이 잦으므로 화면 내 기준일과 안내 문구를 함께 노출하는 것이 안전합니다.",
        ],
        "forms": ["육아휴직 신청서"],
    },
    {
        "id": 7,
        "icon": "🏢",
        "title": "복직 및 육아기 단축근무",
        "period": "복직 후 연계 운영",
        "color": "#27AE60",
        "checklist": [
            "복직 의사 확인과 인사발령 준비",
            "원하는 경우 단축근무 신청 접수",
            "업무 범위 재설계와 팀 공유",
            "급여와 보험 신청 안내 연결",
        ],
        "warnings": [
            "복직 후 운영은 사내 제도와 실제 팀 업무 여건을 함께 반영해야 합니다.",
        ],
        "points": [
            "복직 이후는 제도 설명보다 실제 업무 복귀 흐름 중심으로 구성하는 편이 효과적입니다.",
        ],
        "forms": ["복직 사전 확인서", "육아기 근로시간 단축 신청서"],
    },
]

# --------------------------------------------------
# 세션
# --------------------------------------------------
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

current_step = STEPS[st.session_state.active_step]

# --------------------------------------------------
# 사이드바
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 👶 KCIM 육아 여정")
    st.caption("출산부터 복직까지 단계별 안내")
    st.markdown("<div class='sidebar-section-title'>단계 선택</div>", unsafe_allow_html=True)

    for idx, step in enumerate(STEPS):
        label = f"{step['icon']} STEP {step['id']}  {step['title']}"
        if st.button(label, key=f"side_step_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()

    st.divider()
    st.markdown("<div class='sidebar-section-title'>실무 Tip</div>", unsafe_allow_html=True)
    st.info("한 화면에 모든 정보를 몰아넣기보다 단계별 핵심과 서식을 구분하면 실제 사용성이 좋아집니다.")
    st.caption(f"기준일  {datetime.date.today()}")

# --------------------------------------------------
# 헤더
# --------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="hero-title">👶 KCIM 출산 육아 여정 가이드</div>
  <div class="hero-sub">
    임신 확인부터 복직 이후까지 단계별로 안내하는 내부 가이드입니다.<br>
    화면 구조를 단순화하고 현재 단계에만 집중할 수 있도록 레이아웃을 재구성했습니다.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 상단 툴바
# --------------------------------------------------
col_a, col_b = st.columns([3, 1])
with col_a:
    st.markdown(
        """
        <div class="inline-chip-wrap">
            <div class="inline-chip">📌 단계별 요약 중심</div>
            <div class="inline-chip">🧾 관련 서식 분리</div>
            <div class="inline-chip">🤖 단계 기반 질문 가능</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    view_all = st.toggle("전체 단계 보기", value=False)

# --------------------------------------------------
# 타임라인
# --------------------------------------------------
st.markdown('<div class="timeline-wrap">', unsafe_allow_html=True)
line_cols = st.columns(len(STEPS))
for idx, col in enumerate(line_cols):
    step = STEPS[idx]
    with col:
        active_cls = "active" if idx == st.session_state.active_step else ""
        st.markdown(
            f"""
            <div class="timeline-num {active_cls}" style="background:{step['color'] if idx == st.session_state.active_step else '#fff'};">
                {step['id']}
            </div>
            <div class="timeline-label">{step['title']}</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("선택", key=f"top_step_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()
st.markdown('<div class="timeline-line"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# 렌더링 함수
# --------------------------------------------------
def render_step_card(step: dict):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-head">
            <div class="section-head-left">
                <div class="step-badge" style="background:{step['color']}">
                    <small>STEP</small>
                    {step['id']}
                </div>
                <div>
                    <div class="step-title">{step['icon']} {step['title']}</div>
                    <div class="step-period">📅 {step['period']}</div>
                </div>
            </div>
            <div class="inline-chip">현재 단계 안내</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="step-body">', unsafe_allow_html=True)

    if step.get("metrics"):
        metric_cols = st.columns(len(step["metrics"]))
        for metric_col, metric in zip(metric_cols, step["metrics"]):
            with metric_col:
                st.markdown(
                    f"""
                    <div class="metric-box">
                      <div class="metric-label">{metric['label']}</div>
                      <div class="metric-value" style="color:{step['color']}">{metric['value']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        st.markdown('<div class="info-title">✅ HR 담당자 체크</div>', unsafe_allow_html=True)
        for item in step["checklist"]:
            st.markdown(
                f'<div class="check-item"><span>✅</span><span>{item}</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        st.markdown('<div class="info-title">⚠️ 주의사항</div>', unsafe_allow_html=True)
        for item in step["warnings"]:
            st.markdown(
                f'<div class="warn-item"><span>⛔</span><span>{item}</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="info-title" style="margin-top:0.9rem;">💡 안내 포인트</div>', unsafe_allow_html=True)
        for item in step["points"]:
            st.markdown(f'<div class="point-item">{item}</div>', unsafe_allow_html=True)
        if step.get("forms"):
            st.markdown('<div class="info-title" style="margin-top:0.9rem;">📎 관련 서식</div>', unsafe_allow_html=True)
            form_html = "".join([f'<span class="form-chip">📄 {x}</span>' for x in step['forms']])
            st.markdown(form_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# 본문
# --------------------------------------------------
if view_all:
    for step in STEPS:
        render_step_card(step)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
else:
    render_step_card(current_step)
    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        if st.session_state.active_step > 0:
            if st.button("← 이전 단계", use_container_width=True):
                st.session_state.active_step -= 1
                st.rerun()
    with nav2:
        st.markdown(
            f"<div class='bottom-nav-note'>STEP {st.session_state.active_step + 1} / {len(STEPS)}</div>",
            unsafe_allow_html=True,
        )
    with nav3:
        if st.session_state.active_step < len(STEPS) - 1:
            if st.button("다음 단계 →", use_container_width=True):
                st.session_state.active_step += 1
                st.rerun()

# --------------------------------------------------
# 챗봇
# --------------------------------------------------
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
st.markdown('<div class="chat-title">🤖 단계 기반 상담</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="chat-desc">현재 선택된 단계는 <b>{current_step["title"]}</b> 입니다. 이 단계와 관련된 실무 질문을 입력해 주세요.</div>',
    unsafe_allow_html=True,
)

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input(f"예: {current_step['title']} 관련 문의를 입력하세요")
if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        system_prompt = (
            "너는 KCIM 경영관리본부 내부 가이드 챗봇이다. "
            f"현재 단계는 STEP {current_step['id']} {current_step['title']} 이다. "
            "답변은 한국어로 작성하고, 단정적 법률 자문처럼 말하지 말고 실무 참고용으로 간결하게 설명한다. "
            "사내 규정 확인이 필요한 부분은 반드시 별도 확인이 필요하다고 안내한다."
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
