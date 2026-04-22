import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정: 스크롤 최소화 및 와이드 레이아웃
st.set_page_config(
    page_title="2025 KCIM 모성보호 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 고효율 레이아웃을 위한 CSS (공간 낭비 제거)
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 여백 압축 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-height: 100vh;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --line: #dbe4ee; --cyan: #11a8c7; --purple: #7d5fb2;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; font-size: 14px; }

/* 헤더/배너 슬림화 */
.slim-header {
    background: linear-gradient(90deg, #17384b 0%, #156a8d 100%);
    color: white; padding: 0.5rem 1rem; border-radius: 10px; margin-bottom: 0.8rem;
    display: flex; justify-content: space-between; align-items: center;
}

/* 카드 디자인 최적화 */
.compact-card {
    background: white; border: 1px solid var(--line); border-radius: 10px;
    padding: 0.8rem 1rem; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.section-title {
    font-weight: 800; color: var(--navy); font-size: 0.9rem; margin-bottom: 0.4rem;
    display: flex; align-items: center; gap: 5px;
}

/* 2025 개정 강조 뱃지 */
.new-badge {
    background: var(--purple); color: white; padding: 0.1rem 0.4rem;
    border-radius: 4px; font-size: 0.7rem; font-weight: 700; margin-left: 5px;
}

.script-box {
    background: #f0f9ff; border-left: 4px solid var(--cyan); padding: 0.7rem;
    border-radius: 8px; font-weight: 500; line-height: 1.5; color: #0e5a78;
}

.item-row { display: flex; gap: 8px; padding: 0.25rem 0; border-bottom: 1px solid #f0f4f8; font-size: 0.85rem; }

.chip {
    background: #f1f5f9; color: var(--navy); padding: 0.1rem 0.5rem;
    border-radius: 999px; font-size: 0.75rem; font-weight: 700; border: 1px solid var(--line);
}
</style>
""",
    unsafe_allow_html=True,
)

# 3. 2025 개정 데이터 반영 (이미지 내용 기반)
STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC",
        "guide": "축하 인사와 함께 개인정보 보호 원칙을 안내하세요. 고위험 임신부 여부를 확인하여 전 기간 단축 가능성을 먼저 체크합니다.",
        "check": ["임신 사실 공유 범위 확인", "난임치료휴가(6일/유급2일) 안내", "고위험 임신부 여부 확인 (전 기간 단축 가능)"],
        "forms": ["임신기 단축신청서", "임신확인서"],
        "warn": ["비밀유지 의무 신설('24.10)", "고위험군 19대 질환 여부 확인"],
        "target": "임신 확인 임직원", "next": "단축근무 설정"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "guide": "2025년부터 단축 가능 기간이 확대되었습니다. 12주 이내 및 32주 이후(기존 36주)임을 정확히 안내하세요.",
        "check": ["임신 12주 이내 또는 32주 이후 확인", "하루 2시간 단축 시간대 협의", "급여 100% 보전 안내"],
        "forms": ["임신기 단축신청서"],
        "warn": ["32주 이후 확대 적용 확인", "고위험군은 주수 상관없이 상시 신청 가능"],
        "target": "임신기 전 직원", "next": "검진 시간 안내"
    },
    {
        "id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623",
        "guide": "검진 시간은 유급입니다. 검진일 전 플로우를 통해 신청하도록 안내하고 내부 기록을 남겨주세요.",
        "check": ["검진 주기별 시간 부여 확인", "유급 인정 기준 설명", "신청 경로 가이드"],
        "forms": ["정기건강진단 신청서"],
        "warn": ["검진 시간 사용에 대한 불이익 금지"],
        "target": "검진 대상 직원", "next": "연차/휴가 조율"
    },
    {
        "id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6",
        "guide": "출산휴가 전 남은 연차 사용을 확인하세요. 인수인계 마무리 시점을 정하는 것이 효율적입니다.",
        "check": ["잔여 연차 일수 계산", "출산휴가 전 연차 사용일 확정", "업무 인수인계 시점 조율"],
        "forms": ["연차 신청(동일 경로)"],
        "warn": ["연차 사용 강제 소진 절대 금지"],
        "target": "휴가 예정자", "next": "출산휴가 신청"
    },
    {
        "id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산/배우자", "color": "#E8556D",
        "guide": "배우자 출산휴가가 20일로 대폭 늘어났습니다. 미숙아 출산 시 휴가는 100일임을 잊지 마세요.",
        "check": ["배우자 출산휴가(20일/3회분할) 안내", "미숙아 출산 시 100일 적용", "유산·사산 휴가(11주 이내 10일) 안내"],
        "forms": ["출산휴가 신청서", "배우자 출산휴가 신청서"],
        "warn": ["배우자 휴가는 출산 후 120일 이내 사용"],
        "target": "출산 전후 임직원", "next": "육아기 지원 안내"
    },
    {
        "id": 6, "title": "육아기 지원 및 단축", "short": "육아 지원", "color": "#2980B9",
        "guide": "자녀 연령 만 12세(초6)까지 확대되었습니다. 육아휴직 미사용 기간의 2배를 가산하여 최대 3년까지 가능합니다.",
        "check": ["대상 자녀 연령(만 12세 이하) 확인", "단축 근무 기간(최대 3년) 안내", "최소 사용 기간 1개월로 단축"],
        "forms": ["육아기 단축신청서"],
        "warn": ["단축된 근로시간은 연차 산정 시 포함", "주 5~25시간 단축 가능"],
        "target": "육아기 임직원", "next": "복직 프로세스"
    },
    {
        "id": 7, "title": "육아휴직 및 복직", "short": "육아휴직", "color": "#27AE60",
        "guide": "부모 모두 3개월 사용 시 기간이 1년 6개월로 연장됩니다. 사후지급금 폐지로 전액 즉시 지급됨을 안내하세요.",
        "check": ["부모 동시/순차 사용 여부 확인", "육아휴직 급여(최대 250만원) 안내", "사후지급금 폐지 및 전액 지급 설명"],
        "forms": ["육아휴직 신청서", "복직원"],
        "warn": ["복직 후 14일 이내 사업주 서면 허용의사 표시 의무"],
        "target": "복직 예정자", "next": "사후 관리"
    }
]

# 4. 세션 관리
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

step = STEPS[st.session_state.active_step]

# 5. 화면 레이아웃 구성
# 상단 배너
st.markdown(
    f"""
    <div class="slim-header">
      <div style="font-size: 1.1rem; font-weight: 800;">👶 2025 KCIM 출산·육아 응대 매뉴얼 <span class="new-badge">2025 개정완료</span></div>
      <div style="font-size: 0.8rem; opacity: 0.9;">{datetime.date.today()} | 경영관리본부</div>
    </div>
    """, unsafe_allow_html=True
)

col_nav, col_main = st.columns([1, 4.4], gap="small")

with col_nav:
    st.markdown('<div class="section-title">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.75rem; color:#666;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

with col_main:
    # 핵심 정보 바
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; background:#fff; padding:0.4rem 1rem; border-radius:8px; border:1px solid var(--line);">
        <div style="font-weight:800; color:var(--navy); font-size:1rem;">{step['title']}</div>
        <div><span class="chip">👤 대상: {step['target']}</span> <span class="chip">➡️ 다음: {step['next']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 안내 문구
    st.markdown('<div class="section-title">💬 담당자 안내 핵심 문구</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="script-box">{step["guide"]}</div>', unsafe_allow_html=True)

    # 체크리스트 & 서류 (나란히 배치하여 공간 절약)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="compact-card" style="height:150px;"><div class="section-title">✅ 관리자 필수 체크</div>' + 
                    "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="compact-card" style="height:150px;"><div class="section-title">🧾 서류 및 주의사항</div>' + 
                    "".join([f'<div style="margin-bottom:3px;"><span class="chip">📄 {f}</span></div>' for f in step['forms']]) + 
                    f'<div style="margin-top:8px; font-size:0.8rem; color:#c53030; font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # FAQ
    with st.expander("❓ 자주 받는 질문 (FAQ)"):
        for q, a in step["faq"]:
            st.markdown(f"**Q. {q}**")
            st.info(a)

    # 챗봇 영역 (최하단 배치)
    st.markdown('<div class="section-title" style="margin-top:0.5rem;">🤖 AI 비서 상담</div>', unsafe_allow_html=True)
    chat_container = st.container(height=200)
    with chat_container:
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("이 단계에 대해 질문하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container: st.chat_message("user").write(prompt)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": f"너는 KCIM HR 챗봇이야. 2025 개정법안({step['title']})을 숙지하고 있어. 전문가답게 답변해."}, *st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except: st.error("상담 연결 실패")
