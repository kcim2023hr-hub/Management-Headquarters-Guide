import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정 (와이드 모드 및 스크롤 억제)
st.set_page_config(
    page_title="2026 KCIM 모성보호 파트너",
    page_icon="👶",
    layout="wide",
)

# 2. 제로 마진 및 전문가용 UI 디자인 (CSS)
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 전체 컨테이너 여백 및 스크롤 제어 */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0rem !important;
    max-height: 100vh;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --line: #dbe4ee; --cyan: #11a8c7; --red: #c53030; --purple: #7d5fb2;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; font-size: 14px; }

/* 상단 슬림 배너 */
.slim-header {
    background: linear-gradient(90deg, #17384b 0%, #156a8d 100%);
    color: white; padding: 0.4rem 1rem; border-radius: 8px; margin-bottom: 0.5rem;
    display: flex; justify-content: space-between; align-items: center;
}

/* 카드 높이 고정 및 대칭화 */
.compact-card {
    background: white; border: 1px solid var(--line); border-radius: 8px;
    padding: 0.6rem 0.8rem; margin-bottom: 0.3rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    height: 140px; /* 좌우 박스 높이 일치 */
}

.section-title {
    font-weight: 800; color: var(--navy); font-size: 0.85rem; margin-bottom: 0.3rem;
    display: flex; align-items: center; gap: 4px;
}

/* 스크립트 박스 (구어체 강조) */
.script-box {
    background: #f0f9ff; border-left: 4px solid var(--cyan); padding: 0.5rem 0.8rem;
    border-radius: 6px; font-weight: 500; line-height: 1.5; color: #0e5a78; font-size: 0.92rem;
}

.item-row { display: flex; gap: 5px; padding: 0.15rem 0; border-bottom: 1px solid #f0f4f8; font-size: 0.82rem; }

.chip {
    background: #f1f5f9; color: var(--navy); padding: 0.1rem 0.5rem;
    border-radius: 4px; font-size: 0.72rem; font-weight: 700; border: 1px solid var(--line);
}

.new-badge { background: var(--purple); color: white; padding: 1px 4px; border-radius: 3px; font-size: 0.7rem; margin-left: 5px; }

/* 챗봇 UI 최적화 */
.stChatInput { padding-bottom: 10px !important; }
</style>
""",
    unsafe_allow_html=True,
)

# 3. 2025 개정 지식 베이스가 반영된 단계별 데이터
STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 대응", "short": "임신 확인", "color": "#4FACCC",
        "guide": "“정말 축하드려요! 임신 소식은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 2025년부터 난임치료휴가가 6일로 늘어났는데, 관련 내용도 확인해 드릴까요?”",
        "check": ["공유 희망 범위 확인 (비밀유지 의무)", "난임치료휴가(6일/유급2일) 안내", "고위험 임신부(19대 질환) 여부 확인"],
        "forms": ["임신확인서", "난임치료휴가 신청서"],
        "warn": ["비밀유지 의무 신설('24.10)", "고위험군은 전 기간 단축 가능"],
        "target": "임신 확인 직원", "next": "단축근무 조율"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "guide": "“이제 32주부터 단축 근무가 가능해졌습니다. 하루 2시간을 원하시는 시간대에 맞춰 사용하실 수 있고, 급여는 그대로 보전되니 걱정 마세요.”",
        "check": ["임신 12주 이내 또는 32주 이후 확인", "단축 시간대(출근 지연/조기 퇴근) 협의", "팀 내 업무 조정 서포트"],
        "forms": ["임신기 단축신청서"],
        "warn": ["개정: 36주 → 32주로 확대", "고위험군은 주수 상관없음"],
        "target": "임신기 직원", "next": "검진 시간 안내"
    },
    {
        "id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623",
        "guide": "“검진 시간은 당연히 유급으로 보장되는 권리입니다. 플로우 양식의 '건강진단 신청서'만 미리 작성해 주시면 제가 팀장님께 공유해 드릴게요.”",
        "check": ["검진 주기별 부여 시간 확인", "유급 인정 및 사후 증빙(영수증) 안내", "신청서 작성 경로 가이드"],
        "forms": ["정기건강진단 신청서"],
        "warn": ["진료 영수증 등 증빙 수령 필수", "검진 시간 사용 불이익 금지"],
        "target": "검진 대상 직원", "next": "휴가 전 일정 조율"
    },
    {
        "id": 4, "title": "휴가 전 연차 및 인수인계", "short": "연차 정리", "color": "#9B59B6",
        "guide": "“출산휴가 시작 전 남은 연차를 붙여서 조금 더 일찍 쉬실 수 있게 도와드릴게요. 인수인계 마무리 시점만 정해서 알려주세요.”",
        "check": ["잔여 연차 일수 및 소진 계획 확인", "출산휴가 시작일 확정", "업무 인수인계 리스트 작성 지원"],
        "forms": ["연차 신청서"],
        "warn": ["연차 사용은 직원 자율권 존중", "강제 소진 지양"],
        "target": "휴가 앞둔 직원", "next": "출산/배우자 휴가"
    },
    {
        "id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산/배우자", "color": "#E8556D",
        "guide": "“출산휴가는 90일이고, 배우자분도 20일간 유급 휴가를 쓰실 수 있습니다. 미숙아 출산 시 휴가 기간이 100일로 늘어난 점도 참고해 주세요.”",
        "check": ["배우자 출산휴가(20일/3회 분할) 안내", "미숙아 출산(100일) 적용 확인", "유산·사산 휴가(10일) 안내"],
        "forms": ["출산휴가 신청서", "배우자 휴가 신청서"],
        "warn": ["산후 45일 보장 엄수", "다태아 120일 보장"],
        "target": "출산 전후 직원", "next": "육아기 지원 안내"
    },
    {
        "id": 6, "title": "육아기 근로시간 단축", "short": "육아 지원", "color": "#2980B9",
        "guide": "“자녀가 초등 6학년(만 12세)이 될 때까지 최대 3년 동안 단축 근무를 하실 수 있습니다. 최소 1개월 단위로도 신청 가능하니 유연하게 활용하세요.”",
        "check": ["자녀 연령(만 12세 이하) 확인", "단축 근무 기간 및 시간 협의", "최소 사용 기간(1개월) 단축 안내"],
        "forms": ["육아기 단축신청서"],
        "warn": ["단축 시간 연차 산정 시 포함", "주 5~25시간 단축 가능"],
        "target": "육아기 부모 직원", "next": "복직 및 휴직 연장"
    },
    {
        "id": 7, "title": "육아휴직 및 복직 관리", "short": "복직 준비", "color": "#27AE60",
        "guide": "“육아휴직은 이제 1년 6개월까지 가능해졌어요. 복직 후에 급여가 늦게 나오는 불편함이 없도록 전액 즉시 지급 방식으로 바뀌었으니 걱정 마세요.”",
        "check": ["육아휴직(1.5년) 기간 확정", "사후지급금 폐지(전액 지급) 안내", "복직 면담 및 자리/PC 세팅"],
        "forms": ["육아휴직 신청서", "복직원"],
        "warn": ["복직 후 14일 내 사업주 의사 표시", "부당 처우 절대 금지"],
        "target": "복직 예정자", "next": "사후 관리"
    }
]

# 4. 세션 관리
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

active_idx = st.session_state.active_step
step = STEPS[active_idx]

# 5. 메인 레이아웃 (한 화면 압축)

# 헤더
st.markdown(
    f"""
    <div class="slim-header">
        <div><b>👶 2026 KCIM 모성보호 파트너 <span class="new-badge">2025 개정완료</span></b></div>
        <div style="font-size:0.75rem;">{datetime.date.today()} | 경영관리본부 HR 매뉴얼</div>
    </div>
    """, unsafe_allow_html=True
)

col_nav, col_body = st.columns([1, 4.5], gap="small")

with col_nav:
    st.markdown('<div class="section-title">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == active_idx else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.7rem; color:#666;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

with col_body:
    # 상단 요약 바
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem; background:#fff; padding:0.4rem 0.8rem; border-radius:6px; border:1px solid var(--line);">
            <div style="font-weight:800; color:var(--navy); font-size:0.9rem;">STEP {step['id']}. {step['title']}</div>
            <div><span class="chip">👤 대상: {step['target']}</span> <span class="chip">➡️ 다음: {step['next']}</span></div>
        </div>
        """, unsafe_allow_html=True
    )

    # 1. 안내 문구
    st.markdown('<div class="section-title">💬 담당자 안내 핵심 문구 (Script)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="script-box">{step["guide"]}</div>', unsafe_allow_html=True)

    # 2. 필수 체크 & 서류 (높이 고정하여 하단 라인 일치)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="compact-card"><div class="section-title">✅ 필수 체크리스트</div>' + "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="compact-card"><div class="section-title">🧾 서류 및 주의사항</div>' + "".join([f'<div style="margin-bottom:2px;"><span class="chip">📄 {f}</span></div>' for f in step['forms']]) + f'<div style="margin-top:5px; font-size:0.75rem; color:var(--red); font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # 3. 최하단 챗봇 (높이 조절하여 한 페이지 완성)
    st.markdown('<div class="section-title" style="margin-top:0.2rem; margin-bottom:0px;">🤖 HR 파트너 케이(K) 상담</div>', unsafe_allow_html=True)
    chat_container = st.container(height=260) 
    with chat_container:
        if not st.session_state.messages:
            st.write(f"<div style='font-size:0.8rem; color:#888;'>반가워요! 저는 KCIM의 HR 파트너 <b>케이(K)</b>입니다. <br>현재 사용자가 보고 계신 <b>{step['short']}</b> 단계에 대해 더 궁금한 법규나 대응법이 있다면 물어봐주세요.</div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).markdown(f"<div style='font-size:0.85rem;'>{msg['content']}</div>", unsafe_allow_html=True)

    # 4. 챗봇 페르소나 및 API 로직
    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container: st.chat_message("user").write(prompt)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            # 전문 페르소나 주입
            system_prompt = f"""
            너의 이름은 'HR 파트너 케이(K)'야. KCIM 경영관리본부 담당자를 돕는 모성보호 전문 AI 비서야.
            [현재 상황] 사용자는 지금 [{step['title']}] 단계를 처리 중이야.
            [답변 원칙]
            1. 모든 답변은 '2025년 개정 법안'을 최우선으로 반영한다.
            2. 담당자가 임직원에게 즉시 말할 수 있는 '구어체 스크립트'를 항상 포함해줘.
            3. 법적 근거와 사내 양식 위치를 언급하며 전문성을 높인다.
            4. 말투는 친절하고 명확하며, 담당자를 서포트하는 든든한 동료의 느낌을 유지한다.
            [지식 베이스]
            - 임신기 단축: 12주 이내, 32주 이후 / 배우자 출산휴가: 20일 / 육아기 단축: 만 12세 이하 / 육아휴직: 1.5년
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except:
            st.error("OpenAI API 키를 확인해주세요.")
