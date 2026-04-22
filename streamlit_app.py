<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KCIM 출산 육아 응대 가이드 - 개선 버전</title>
</head>
<body>
<pre style="background:#f8f9fa; padding:20px; border-radius:12px; font-size:13px; line-height:1.5; overflow:auto; max-height:90vh;">

```python
import datetime
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# ================================================
# 개선된 CSS (헤더, 여백, 좌측 단계, 빠른확인 3카드 반영)
# ================================================
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #17384b;
  --navy-soft: #1e4d68;
  --bg: #f5f7fb;
  --card: #ffffff;
  --line: #dbe4ee;
  --text: #1f2a35;
  --muted: #708191;
  --cyan: #11a8c7;
  --green: #1f9d63;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp {
  background: var(--bg);
}

/* 전체 여백 확대 (스크린샷과 더 비슷하게) */
.block-container {
  max-width: 100% !important;
  padding-top: 1.2rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 1.2rem !important;
  padding-right: 1.2rem !important;
}

/* ==================== HERO HEADER ==================== */
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

.hero::after {
  content: "";
  position: absolute;
  right: -60px;
  top: -60px;
  width: 260px;
  height: 260px;
  background: rgba(255,255,255,0.08);
  border-radius: 50%;
}

.hero-title {
  font-size: 1.95rem;
  font-weight: 800;
  margin: 0 0 0.6rem 0;
  letter-spacing: -0.03em;
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
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

/* ==================== LEFT CARD ==================== */
.left-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(23, 43, 64, 0.06);
  padding: 1.4rem 1.2rem;
  height: 100%;
}

.card-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 1rem;
}

.stage-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: #fff;
  transition: all 0.2s;
  cursor: pointer;
}

.stage-item:hover {
  border-color: var(--cyan);
  transform: translateY(-1px);
}

.stage-item.active {
  border-color: transparent;
  background: linear-gradient(90deg, #f0f9ff, #e0f2fe);
  box-shadow: 0 8px 20px rgba(17, 168, 199, 0.15);
}

.stage-num {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1rem;
  flex-shrink: 0;
  color: #fff;
}

.stage-label {
  font-weight: 700;
  font-size: 0.97rem;
  color: var(--text);
  line-height: 1.4;
}

/* ==================== MAIN AREA ==================== */
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
  color: var(--text);
}

/* 빠른 확인 3카드 */
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
  box-shadow: 0 6px 18px rgba(23, 43, 64, 0.04);
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

/* 나머지 기존 스타일 유지 + 약간 보강 */
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
  line-height: 1.05;
  font-weight: 800;
  flex-shrink: 0;
  font-size: 1.35rem;
}

.main-title {
  font-size: 1.32rem;
  font-weight: 800;
  color: var(--text);
}

.main-body {
  padding: 1.4rem;
}

.section-box {
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1.2rem;
  background: #fff;
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

.faq-item {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 1.1rem;
  background: #fff;
  margin-bottom: 1rem;
}

.stButton > button {
  border-radius: 14px !important;
  font-weight: 700 !important;
}

/* 모바일 최적화 */
@media (max-width: 1100px) {
  .quick-panel, .status-row {
    grid-template-columns: 1fr;
  }
  .block-container {
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

# ================================================
# 데이터 (기존 그대로 유지)
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

STEPS = [ ... ]   # ← 기존 STEPS 리스트 전체 그대로 복사 (7개 단계 모두)

# ================================================
# 세션 상태 안전 처리
# ================================================
if "active_step" not in st.session_state:
    st.session_state.active_step = 0

active_step = st.session_state.active_step
if not (0 <= active_step < len(STEPS)):
    st.session_state.active_step = 0
    active_step = 0

step = STEPS[active_step]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ================================================
# HERO HEADER (스크린샷과 최대한 유사하게 개선)
# ================================================
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-title">
        👶 KCIM 출산 육아 응대 가이드
      </div>
      <div class="hero-desc">
        임신 확인부터 복직까지 관리자 입장에서 빠르게 응대할 수 있도록<br>
        단계별 핵심만 정리한 페이지입니다.
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
# 메인 레이아웃
# ================================================
left_col, main_col = st.columns([1.05, 3.7], gap="medium")

with left_col:
    st.markdown('<div class="left-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">단계 선택</div>', unsafe_allow_html=True)

    st.markdown('<div class="stage-list">', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        active_class = "active" if idx == active_step else ""
        color = s["color"]
        if st.button(f"STEP {s['id']} {s['short']}", key=f"step_btn_{idx}", use_container_width=True):
            st.session_state.active_step = idx
            st.rerun()

        st.markdown(
            f"""
            <div class="stage-item {active_class}" onclick="this.closest('.stButton').querySelector('button').click()">
              <div class="stage-num" style="background:{color};">{s['id']}</div>
              <div class="stage-label">{s['short']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # 양식 안내 (기존 그대로)
    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">양식 안내</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:#f8fbff;border:1px solid #dbe4ee;border-radius:16px;padding:1.2rem 1.1rem;line-height:1.65;font-size:0.9rem;">
          <b>경로</b><br>{COMMON_FORM_GUIDE['location']}<br><br>
          <b>양식명</b><br>{COMMON_FORM_GUIDE['form_name']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card-title" style="margin-top:1.2rem;">신청서 탭</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="background:#f8fbff;border:1px solid #dbe4ee;border-radius:16px;padding:1.1rem 1.1rem;line-height:1.7;font-size:0.9rem;">' +
        '<br>'.join([f'• {x}' for x in COMMON_FORM_GUIDE['tabs']]) +
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with main_col:
    # 바로 안내할 말 + 빠른 확인 (3카드)
    st.markdown('<div class="quick-panel">', unsafe_allow_html=True)

    # 바로 안내할 말
    st.markdown(
        f"""
        <div class="quick-card">
          <div class="quick-title">바로 안내할 말</div>
          <div class="guide-box">{step['guide']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 빠른 확인 (3개 카드)
    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 메인 카드 (기존 로직 유지)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="main-card-header">
          <div style="display:flex; align-items:center; gap:18px;">
            <div class="step-badge" style="background:{step['color']}">
              <small>STEP</small>{step['id']}
            </div>
            <div>
              <div class="main-title">{step['title']}</div>
              <div style="color:#708191; font-size:0.95rem;">{step['period']} · {step['summary']}</div>
            </div>
          </div>
          <div style="margin-left:auto; background:#f1f5f9; color:#475569; padding:6px 14px; border-radius:9999px; font-size:0.82rem; font-weight:600;">
            현재 단계 응대 가이드
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-body">', unsafe_allow_html=True)

    # 체크리스트 + 필요서류 + 주의사항
    col_check, col_form = st.columns([1.1, 0.9])
    with col_check:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:1rem;">✅ HR 담당자 체크</div>', unsafe_allow_html=True)
        for item in step["check"]:
            st.markdown(f'<div class="item-row"><span style="color:#11a8c7;font-size:1.2rem;">✔</span> {item}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:1rem;">🧾 필요 서류</div>', unsafe_allow_html=True)
        for form in step["forms"]:
            st.markdown(f'<div class="form-chip">📄 {form}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1.4rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:0.8rem;">⚠️ 주의사항</div>', unsafe_allow_html=True)
        for warn in step["warn"]:
            st.markdown(f'<div class="warn-box">{warn}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # main-body

    # 이전/다음 버튼
    prev_col, center_col, next_col = st.columns([1, 1.2, 1])
    with prev_col:
        if active_step > 0:
            if st.button("← 이전 단계", use_container_width=True):
                st.session_state.active_step -= 1
                st.rerun()
    with center_col:
        st.markdown(f"<div style='text-align:center; margin-top:12px; color:#708191; font-size:0.9rem;'>STEP {step['id']} / {len(STEPS)}</div>", unsafe_allow_html=True)
    with next_col:
        if active_step < len(STEPS) - 1:
            if st.button("다음 단계 →", use_container_width=True):
                st.session_state.active_step += 1
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # main-card

    # FAQ
    st.markdown('<div class="faq-card" style="margin-top:1.8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:1rem;">❓ 자주 받는 질문</div>', unsafe_allow_html=True)
    for q, a in step["faq"]:
        st.markdown(
            f"""
            <div class="faq-item">
              <div style="font-weight:700;color:#17384b;margin-bottom:0.6rem;">Q. {q}</div>
              <div style="line-height:1.65;color:#1f2a35;">{a}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # 챗봇
    st.markdown('<div class="chat-card" style="margin-top:1.8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#17384b;margin-bottom:0.6rem;">🤖 추가 상담</div>', unsafe_allow_html=True)
    st.caption(f"현재 선택된 단계 : STEP {step['id']} {step['title']}")

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
                "답변은 한국어로 작성하고, 관리자가 임직원에게 설명하기 쉽게 짧고 친절하게 정리한다. "
                "법령 해석이 필요한 부분은 최신 기준과 사내 규정 확인이 필요하다고 함께 안내한다."
            )
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
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
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"상담 서비스 오류가 발생했습니다.\n\n{str(e)[:120]}")

    st.markdown('</div>', unsafe_allow_html=True)

</pre>
</body>
</html>
