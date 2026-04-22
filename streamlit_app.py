import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정: 화면 여백 최소화 및 와이드 모드
st.set_page_config(
    page_title="2025 KCIM 모성보호 파트너",
    page_icon="👶",
    layout="wide",
)

# 2. 고효율/제로스크롤 레이아웃 CSS
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 전체 컨테이너 여백 제거 및 스크롤 억제 */
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
    color: white; padding: 0.4rem 1rem; border-radius: 10px; margin-bottom: 0.5rem;
    display: flex; justify-content: space-between; align-items: center;
}

/* 카드 공통 스타일 (높이 고정으로 균형 유지) */
.compact-card {
    background: white; border: 1px solid var(--line); border-radius: 8px;
    padding: 0.6rem 0.8rem; margin-bottom: 0.3rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.section-title {
    font-weight: 800; color: var(--navy); font-size: 0.85rem; margin-bottom: 0.3rem;
    display: flex; align-items: center; gap: 4px;
}

/* 스크립트 박스 최적화 */
.script-box {
    background: #f0f9ff; border-left: 4px solid var(--cyan); padding: 0.5rem 0.8rem;
    border-radius: 6px; font-weight: 500; line-height: 1.4; color: #0e5a78; font-size: 0.92rem;
}

.item-row { display: flex; gap: 5px; padding: 0.15rem 0; border-bottom: 1px solid #f0f4f8; font-size: 0.82rem; }

.chip {
    background: #f1f5f9; color: var(--navy); padding: 0.1rem 0.5rem;
    border-radius: 4px; font-size: 0.75rem; font-weight: 700; border: 1px solid var(--line);
}

.new-badge {
    background: var(--purple); color: white; padding: 1px 4px; border-radius: 3px; font-size: 0.7rem; margin-left: 5px;
}

/* 챗봇 UI 밀착 */
.stChatInput { padding-bottom: 5px !important; }
</style>
""",
    unsafe_allow_html=True,
)

# 3. 2025 개정 데이터 반영 (7단계 완결)
STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC",
        "guide": "“축하드립니다! 임신 소식은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 2025년부터 난임치료휴가가 6일로 늘어났는데 관련 내용도 확인해 드릴까요?”",
        "check": ["임신 사실 공유 범위 확인 (비밀유지)", "난임치료휴가(6일/유급2일) 안내", "고위험 임신부 여부 확인(전 기간 단축 가능)"],
        "forms": ["임신확인서", "난임치료휴가 신청서"],
        "warn": ["비밀유지 의무 신설('24.10)", "임신 이유 불이익 조치 금지"],
        "target": "임신 확인 직원", "next": "단축근무 조율"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "guide": "“이제 32주부터 단축 근무가 가능합니다. 하루 2시간을 원하시는 시간대에 맞춰 사용하실 수 있고, 급여는 100% 보전되니 걱정 마세요.”",
        "check": ["임신 12주 이내 또는 32주 이후 확인", "단축 시간대(출퇴근 조율) 협의", "급여 100% 보전 안내"],
        "forms": ["임신기 단축신청서"],
        "warn": ["개정: 36주 → 32주로 확대", "고위험군은 주수 상관없이 상시 신청"],
        "target": "단축 희망 직원", "next": "정기검진 안내"
    },
    {
        "id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623",
        "guide": "“검진 시간은 유급으로 보장되는 당연한 권리에요. 검진일 전 플로우 양식의 '건강진단 신청서'만 작성해 주시면 팀장님께 미리 공유해 드릴게요.”",
        "check": ["검진 주기별 시간 부여 확인", "유급 인정 및 사후 증빙(영수증) 안내", "신청서 작성 경로 가이드"],
        "forms": ["정기건강진단 신청서"],
        "warn": ["진료 영수증 등 증빙 필수", "검진 시간 사용 불이익 금지"],
        "target": "검진 대상자", "next": "연차/휴가 조율"
    },
    {
        "id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6",
        "guide": "“출산휴가 전 남은 연차를 사용하실 수 있습니다. 인수인계 마무리 시점을 고려하여 가장 편한 날짜를 정해 알려주세요.”",
        "check": ["잔여 연차 계산", "출산휴가 전 연차 사용일 확정", "업무 인수인계 시점 조율"],
        "forms": ["연차 신청서"],
        "warn": ["연차 강제 소진 금지 (자율권 존중)"],
        "target": "휴가 예정자", "next": "출산/배우자 휴가"
    },
    {
        "id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산/배우자", "color": "#E8556D",
        "guide": "“배우자 출산휴가가 20일로 대폭 늘어났습니다. 3회에 나누어 쓰실 수 있고, 미숙아 출산 시 휴가 기간은 100일로 적용됩니다.”",
        "check": ["배우자 출산휴가(20일/3회분할) 안내", "미숙아 출산(100일) 적용 확인", "유산·사산 휴가(10일) 안내"],
        "forms": ["출산휴가 신청서", "배우자 휴가 신청서"],
        "warn": ["산후 45일 보장 필수", "배우자 휴가는 120일 내 사용"],
        "target": "출산 전후 직원", "next": "육아기 지원 안내"
    },
    {
        "id": 6, "title": "육아기 근로시간 단축", "short": "육아 지원", "color": "#2980B9",
        "guide": "“자녀가 만 12세(초6) 이하인 경우 최대 3년까지 단축 근무가 가능해요. 최소 1개월 단위로도 신청 가능하니 유연하게 활용해 보세요.”",
        "check": ["대상 자녀 연령(만 12세 이하) 확인", "단축 기간(최대 3년) 협의", "최소 사용 기간 1개월 단축 안내"],
        "forms": ["육아기 단축신청서"],
        "warn": ["단축 시간 연차 산정 시 포함 확인", "주 5~25시간 단축 가능"],
        "target": "육아기 부모", "next": "육아휴직/복직"
    },
    {
        "id": 7, "title": "육아휴직 및 복직 관리", "short": "복직 준비", "color": "#27AE60",
        "guide": "“육아휴직은 이제 1년 6개월까지 가능해요. 복직 후 사후지급금 폐지로 급여 전액을 받으시니 경제적 부담을 덜어보세요. 복직을 환영합니다!”",
        "check": ["육아휴직(1.5년) 연장 안내", "사후지급금 폐지(전액지급) 설명", "복직 면담 및 자리 세팅"],
        "forms": ["육아휴직 신청서", "복직원"],
        "warn": ["복직 후 14일 이내 허용의사 표시", "부당 처우 절대 금지"],
        "target": "복직 예정자", "next": "사후 관리"
    }
]

# 4. 세션 상태 관리
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

step = STEPS[st.session_state.active_step]

# 5. 메인 레이아웃 (한 페이지 최적화)

# 헤더
st.markdown(
    f"""
    <div class="slim-header">
        <div><b>👶 2026 KCIM 모성보호 파트너 <span class="new-badge">2025 개정완료</span></b></div>
        <div style="font-size:0.75rem;">{datetime.date.today()} | 경영관리본부 HR 매뉴얼</div>
    </div>
    """, unsafe_allow_html=True
)

col_nav, col_body = st.columns([1, 4.4], gap="small")

with col_nav:
    st.markdown('<div class="section-title">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.7rem; color:#666;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

with col_body:
    # 상단 요약 바
    st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem; background:#fff; padding:0.3rem 0.8rem; border-radius:6px; border:1px solid var(--line);"><div style="font-weight:800; color:var(--navy); font-size:0.9rem;">STEP {step['id']}. {step['title']}</div><div><span class="chip">👤 대상: {step['target']}</span> <span class="chip">➡️ 다음: {step['next']}</span></div></div>""", unsafe_allow_html=True)

    # 1. 안내 문구
    st.markdown('<div class="section-title">💬 담당자 핵심 안내 문구 (Script)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="script-box">{step["guide"]}</div>', unsafe_allow_html=True)

    # 2. 필수 체크 & 서류 (높이 고정하여 대칭 유지)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="compact-card" style="height:125px;"><div class="section-title">✅ 필수 체크리스트</div>' + "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="compact-card" style="height:125px;"><div class="section-title">🧾 서류 및 주의사항</div>' + "".join([f'<div style="margin-bottom:2px;"><span class="chip">📄 {f}</span></div>' for f in step['forms']]) + f'<div style="margin-top:5px; font-size:0.75rem; color:var(--red); font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # 3. 최하단 챗봇 (높이 조절하여 한 페이지 완성)
    st.markdown('<div class="section-title" style="margin-top:0.2rem; margin-bottom:0px;">🤖 HR 파트너 케이(K) 상담</div>', unsafe_allow_html=True)
    chat_container = st.container(height=300) 
    with chat_container:
        if not st.session_state.messages:
            st.write(f"<div style='font-size:0.8rem; color:#888;'>반가워요! 저는 KCIM의 HR 파트너 <b>케이(K)</b>입니다. <br>현재 <b>{step['short']}</b> 단계에 대해 더 궁금한 법규나 대응법이 있다면 물어봐주세요.</div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).markdown(f"<div style='font-size:0.85rem;'>{msg['content']}</div>", unsafe_allow_html=True)

    # 4. 케이(K) 페르소나 시스템 프롬프트 주입 및 API 호출
    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container: st.chat_message("user").write(prompt)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            system_prompt = f"""
            너의 이름은 'HR 파트너 케이(K)'야. KCIM 경영관리본부 담당자를 돕는 모성보호 전문 AI 비서야.
            [현재 상황] 사용자는 [{step['title']}] 단계를 처리 중이야.
            [답변 원칙]
            1. 모든 답변은 '2025년 개정 법안'을 최우선 반영한다. (임신기 단축 32주, 배우자 휴가 20일, 육아휴직 1.5년 등)
            2. 담당자가 임직원에게 즉시 말할 수 있는 '구어체 스크립트'를 항상 포함해줘.
            3. 법적 근거와 사내 양식 위치를 언급하며 전문성을 높인다.
            4. 말투는 친절하고 명확하며, 든든한 동료 느낌을 유지한다.
            [지식 요약]
            - 임신기 단축: 12주 이내, 32주 이후
            - 배우자 출산휴가: 20일 (분할 3회)
            - 육아기 단축: 자녀 만 12세 이하 (최대 3년)
            - 육아휴직: 부모 모두 3개월 사용 시 1.5년으로 연장, 사후지급금 폐지
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except:
            st.error("OpenAI API 연결 실패")
