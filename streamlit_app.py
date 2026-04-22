import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정: 스크롤 절대 방지 및 폰트 최적화
st.set_page_config(
    page_title="KCIM 출산 육아 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 고효율 레이아웃을 위한 CSS (초슬림 모드)
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 기본 여백 및 스크롤 억제 */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0rem !important;
    max-height: 100vh;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --line: #dbe4ee; --cyan: #11a8c7; --red: #c53030;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; font-size: 14px; }

/* 상단 슬림 배너 */
.slim-header {
    background: linear-gradient(90deg, #17384b 0%, #156a8d 100%);
    color: white; padding: 0.5rem 1rem; border-radius: 10px; margin-bottom: 0.5rem;
    display: flex; justify-content: space-between; align-items: center;
}

/* 카드 및 섹션 타이틀 */
.compact-card {
    background: white; border: 1px solid var(--line); border-radius: 10px;
    padding: 0.7rem 0.9rem; margin-bottom: 0.4rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.section-title {
    font-weight: 800; color: var(--navy); font-size: 0.85rem; margin-bottom: 0.3rem;
    display: flex; align-items: center; gap: 4px;
}

/* 스크립트 박스 최적화 */
.script-box {
    background: #f0f9ff; border-left: 4px solid var(--cyan); padding: 0.6rem 0.8rem;
    border-radius: 8px; font-weight: 500; line-height: 1.5; color: #0e5a78; font-size: 0.92rem;
}

.item-row { display: flex; gap: 6px; padding: 0.2rem 0; border-bottom: 1px solid #f0f4f8; font-size: 0.82rem; }

.chip {
    background: #f1f5f9; color: var(--navy); padding: 0.1rem 0.5rem;
    border-radius: 4px; font-size: 0.75rem; font-weight: 700; border: 1px solid var(--line);
}

/* 챗봇 입력창 높이 조정 */
.stChatInput { padding-bottom: 10px !important; }
</style>
""",
    unsafe_allow_html=True,
)

# 3. 데이터 (7단계 완결)
STEPS = [
    {"id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC", "guide": "“축하드립니다! 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 먼저 단축근무 제도부터 안내해 드릴까요?”", "check": ["공유 범위 확인 (비밀 유지)", "임신기 근로시간 단축 안내", "플로우 내 신청서 경로 설명"], "forms": ["임신기 단축신청서"], "warn": ["비밀 엄수 필수", "임신 이유 불이익 금지"], "target": "임신 확인 직원", "next": "단축 조율"},
    {"id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A", "guide": "“초기(12주 이내)와 말기(36주 이후)는 하루 2시간 단축이 가능합니다. 급여 삭감은 없으니 편하신 시간대를 알려주세요.”", "check": ["주수 확인 (증빙 수령)", "단축 시간대 협의 및 팀 공유", "플로우 신청서 작성 확인"], "forms": ["임신기 단축신청서"], "warn": ["주수 경과 시 변경 신청"], "target": "단축 희망자", "next": "검진 안내"},
    {"id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623", "guide": "“검진 시간은 유급으로 보장됩니다. 검진일 전 플로우의 '건강진단 신청서'를 통해 미리 공유해 주시면 됩니다.”", "check": ["검진 주기별 시간 부여", "유급 인정 및 증빙 안내", "신청 경로 가이드"], "forms": ["정기건강진단 신청서"], "warn": ["진료 영수증 등 확인"], "target": "검진 대상자", "next": "연차 조율"},
    {"id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6", "guide": "“출산휴가 전 남은 연차를 사용하실 수 있습니다. 인수인계 마무리 시점을 고려하여 편하신 날짜를 정해주세요.”", "check": ["잔여 연차 계산", "출산휴가 시작일 확정", "인수인계 리스트 점검"], "forms": ["연차 신청서"], "warn": ["연차 강제 소진 금지"], "target": "휴가 예정자", "next": "출산휴가 신청"},
    {"id": 5, "title": "출산 전후 휴가 등록", "short": "출산 관련", "color": "#E8556D", "guide": "“출산휴가는 90일입니다. 출산 후 45일 이상이 확보되어야 하니 시작일을 잘 조정해 보아요. 지원금 안내도 드릴게요.”", "check": ["휴가 기간(90일) 등록", "출산 후 45일 보장 확인", "급여 지원금 신청 안내"], "forms": ["출산휴가 신청서"], "warn": ["다태아는 120일 보장"], "target": "출산 전후 직원", "next": "육아 지원 안내"},
    {"id": 6, "title": "육아기 근로시간 단축", "short": "육아 지원", "color": "#2980B9", "guide": "“복직 후 육아기 단축 근무가 가능합니다. 육아휴직과 별개로 사용 가능하니 필요하시면 언제든 말씀해주세요.”", "check": ["단축 시간대 협의", "급여 지원금 안내", "변경 신청 프로세스"], "forms": ["육아기 단축신청서"], "warn": ["단축 중 연장근로 제한"], "target": "육아기 부모", "next": "복직 준비"},
    {"id": 7, "title": "복직 및 최종 확인", "short": "복직 준비", "color": "#27AE60", "guide": "“복직을 진심으로 환영합니다! 자리는 세팅해 두었습니다. 업무 적응을 위해 가벼운 면담부터 시작해 볼까요?”", "check": ["복직일 확정 공지", "자리/PC/권한 세팅 완료", "복직 면담 실시"], "forms": ["복직원 (사내 서식)"], "warn": ["부당 처우 절대 금지"], "target": "복직 예정자", "next": "사후 관리"}
]

# 4. 세션 관리
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

step = STEPS[st.session_state.active_step]

# 5. 메인 레이아웃 구성
st.markdown(f'<div class="slim-header"><div><b>👶 KCIM 출산 육아 응대 가이드</b></div><div style="font-size:0.75rem;">{datetime.date.today()} | 경영관리본부</div></div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 4.5], gap="small")

with col_left:
    st.markdown('<div class="section-title">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.75rem;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

with col_right:
    # 상단 요약 바 (높이 축소)
    st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; background:#fff; padding:0.4rem 0.8rem; border-radius:8px; border:1px solid var(--line);"><div style="font-weight:800; color:var(--navy);">STEP {step['id']}. {step['title']}</div><div><span class="chip">👤 대상: {step['target']}</span> <span class="chip">➡️ 다음: {step['next']}</span></div></div>""", unsafe_allow_html=True)

    # 스크립트 박스
    st.markdown('<div class="section-title">💬 담당자 핵심 안내 문구</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="script-box">{step["guide"]}</div>', unsafe_allow_html=True)

    # 체크리스트 & 서류 (가로 배치, 높이 고정)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="compact-card" style="height:140px;"><div class="section-title">✅ 필수 체크</div>' + "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="compact-card" style="height:140px;"><div class="section-title">🧾 서류/주의</div>' + "".join([f'<div style="margin-bottom:2px;"><span class="chip">📄 {f}</span></div>' for f in step['forms']]) + f'<div style="margin-top:5px; font-size:0.8rem; color:var(--red); font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # 챗봇 (높이 조절하여 한 페이지 완성)
    st.markdown('<div class="section-title" style="margin-top:0.2rem;">🤖 AI 비서 상담</div>', unsafe_allow_html=True)
    chat_container = st.container(height=240) # 240px로 확장하여 가시성 확보
    with chat_container:
        if not st.session_state.messages:
            st.write(f"<div style='font-size:0.8rem; color:#888;'>현재 <b>{step['short']}</b> 단계에 대해 질문해주세요.</div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).markdown(f"<div style='font-size:0.85rem;'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("이 단계에 대해 질문하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container: st.chat_message("user").write(prompt)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": f"너는 KCIM HR 챗봇이야. 단계:{step['title']}. 짧고 간결하게 전문가답게 답변해."}, *st.session_state.messages])
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except: st.error("API 연결 실패")
