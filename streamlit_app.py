import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="KCIM 모성보호 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 디자인 레이아웃 CSS
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --card: #ffffff; --line: #dbe4ee;
  --text: #1f2a35; --muted: #708191; --cyan: #11a8c7; --purple: #7d5fb2; --red: #e74c3c;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; }
.stApp { background: var(--bg); }

.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff; border-radius: 15px; padding: 1.5rem 2rem; margin-bottom: 1rem;
  box-shadow: 0 6px 20px rgba(23, 56, 75, 0.2);
}

.hero-title { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; }
.hero-desc { font-size: 1rem; opacity: 0.9; }

.main-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 12px;
  padding: 1.2rem; margin-bottom: 0.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.main-title { font-size: 1.3rem; font-weight: 800; color: var(--text); margin-bottom: 0.3rem; }

.script-box {
  background: #f4fbfe; border-left: 5px solid var(--cyan); padding: 0.8rem 1rem;
  border-radius: 8px; font-weight: 500; line-height: 1.6; color: #0e5a78; font-size: 1rem;
}

.item-row { display: flex; gap: 8px; padding: 0.3rem 0; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.item-row:last-child { border-bottom: 0; }

.form-chip {
  display: inline-flex; align-items: center; gap: 4px; border-radius: 6px;
  border: 1px solid var(--line); background: #f8fafc; padding: 0.3rem 0.6rem;
  font-size: 0.8rem; color: var(--navy); font-weight: 700;
}

.new-badge { background: var(--purple); color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; margin-left: 10px; }
</style>
""",
    unsafe_allow_html=True,
)

# 3. 데이터 정의
STEPS = [
    {"id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC", "guide": "“축하드립니다! 임신 소식은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 먼저 단축근무 제도부터 안내해 드릴까요?”", "check": ["공유 희망 범위 확인 (비밀유지)", "단축근무 신청 방법 및 서류 안내", "플로우 내 신청서 경로 설명"], "forms": ["임신확인서", "KCIM_임신▪육아기 관련 지원 신청서"], "warn": ["비밀유지 의무 준수 필수", "임신 이유 불이익 금지"], "target": "임신 확인 직원", "next": "단축 조율"},
    {"id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A", "guide": "“이제 임신 후 12주 이내 / 32주 이후 단축 근무가 가능합니다. 하루 2시간을 자유롭게 사용하실 수 있습니다.”", "check": ["임신 12주 이내 또는 32주 이후 확인", "단축 시간대 협의", "팀 내 업무 조정 지원"], "forms": ["KCIM_임신▪육아기 관련 지원 신청서"], "warn": ["개정: 32주 확대 적용", <b>"고위험군은 전 기간 가능"</b>], "target": "단축 희망 직원", "next": "검진 안내"},
    {"id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623", "guide": "“검진 시간은 유급으로 보장됩니다. 플로우 양식 신청서만 작성해 주시면 팀장님께 공유해 드릴게요.”", "check": ["검진 주기별 시간 부여", "유급 인정 및 증빙 안내", "신청 경로 가이드"], "forms": ["KCIM_임신▪육아기 관련 지원 신청서"], "warn": ["사전 예약 문자 및 진료 영수증 등 증빙 확인", "사용 불이익 금지"], "target": "검진 대상자", "next": "연차 조율"},
    {"id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6", "guide": "“출산휴가 전 남은 연차를 사용해 일찍 휴식을 시작하실 수 있습니다. 인수인계 시점을 알려주세요.”", "check": ["잔여 연차 계산", "출산휴가 시작일 확정", "인수인계 리스트 작성"], "forms": ["어울지기 내 신청"], "warn": ["연차 강제 소진 금지", "자율권 존중"], "target": "휴가 예정자", "next": "출산/배우자 휴가"},
    {"id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산 관련", "color": "#E8556D", "guide": "“출산휴가는 90일, 배우자분은 20일 유급 휴가가 가능합니다. 미숙아 출산 시 100일이 적용됩니다.”", "check": ["배우자 휴가(20일) 안내", "미숙아 출산(100일) 확인", "유산·사산 휴가 안내"], "forms": ["어울지기 내 신청"], "warn": [<b>"산후 45일 보장 필수"</b>, "배우자 휴가 120일 내 사용"], "target": "출산 전후 직원", "next": "육아기 지원"},
    {"id": 6, "title": "육아기 근로시간 단축", "short": "육아 지원", "color": "#2980B9", "guide": "“자녀가 만 12세 이하인 경우 최대 3년 동안 단축 근무를 하실 수 있습니다. 언제든 말씀해주세요.”", "check": ["대상 자녀 연령 확인", "단축 기간 협의", "최소 1개월 사용 안내"], "forms": ["육아기 단축신청서"], "warn": ["단축 시간 연차 산정 포함", "주 5~25시간 단축"], "target": "육아기 부모", "next": "육아휴직/복직"},
    {"id": 7, "title": "육아휴직 및 복직 관리", "short": "복직 준비", "color": "#27AE60", "guide": "“육아휴직은 1년 6개월까지 가능하며 사후지급금 없이 전액 지급됩니다. 복직을 환영합니다!”", "check": ["육아휴직(1.5년) 안내", "사후지급금 폐지 설명", "복직 면담 및 자리 세팅"], "forms": ["육아휴직 신청서", "복직원"], "warn": ["복직 전 14일 내 의사표시", "부당 처우 절대 금지"], "target": "복직 예정자", "next": "사후 관리"}
]

# 4. 세션 초기화
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

active_idx = st.session_state.active_step
step = STEPS[active_idx]

# 5. UI 렌더링
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">👶 KCIM 출산 육아 응대 가이드 <span class="new-badge">2025 개정 반영</span></div>
        <div class="hero-desc">임신 확인부터 복직까지, 경영관리본부 담당자를 위한 단계별 핵심 가이드라인입니다.</div>
    </div>
    """, unsafe_allow_html=True
)

col_nav, col_body = st.columns([1, 4.4], gap="small")

with col_nav:
    st.markdown('<div style="font-weight: 800; color:var(--navy); font-size:0.9rem; margin-bottom:0.5rem;">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == active_idx else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.75rem; color:#666;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

with col_body:
    st.markdown(f"""
    <div class="main-card" style="border-left: 6px solid {step['color']};">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.8rem;">
            <div>
                <div style="color:var(--muted); font-size:0.85rem; font-weight:700;">STEP {step['id']}</div>
                <div class="main-title">{step['title']}</div>
            </div>
            <div style="text-align:right;">
                <span class="form-chip">👤 대상: {step['target']}</span>
                <span class="form-chip">➡️ 다음: {step['next']}</span>
            </div>
        </div>
        <div style="font-weight:800; color:var(--navy); font-size:0.9rem; margin-bottom:0.4rem;">💬 담당자 안내 핵심 문구 (Script)</div>
        <div class="script-box">{step['guide']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="main-card" style="height:150px;"><div style="font-weight:800; font-size:0.9rem; margin-bottom:0.5rem;">✅ 관리자 필수 체크</div>' + 
                    "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="main-card" style="height:150px;"><div style="font-weight:800; font-size:0.9rem; margin-bottom:0.5rem;">🧾 서류 및 주의사항</div>' + 
                    "".join([f'<div style="margin-bottom:3px;"><span class="form-chip">📄 {f}</span></div>' for f in step['forms']]) + 
                    f'<div style="margin-top:6px; font-size:0.8rem; color:var(--red); font-weight:700; line-height:1.3;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # 챗봇 영역
    st.markdown('<div style="font-weight: 800; color:var(--navy); font-size:0.9rem; margin-top:0.3rem; margin-bottom:0.2rem;">🤖 육아지원박사 상담</div>', unsafe_allow_html=True)
    
    chat_container = st.container(height=300)
    with chat_container:
        if not st.session_state.messages:
            st.info(f"반가워요! 저는 KCIM의 육아지원 파트너 **박사**입니다. {step['short']} 단계의 법규나 대응법에 대해 무엇이든 물어보세요.")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 입력창
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 1. 사용자 메시지 추가 및 화면 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # 2. API 호출
        try:
            # API 키 존재 여부 확인
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("오류: .streamlit/secrets.toml 파일에 OPENAI_API_KEY가 설정되지 않았습니다.")
                st.stop()

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            system_prompt = f"""
            너의 이름은 '육아지원박사'야. KCIM 경영관리본부 담당자를 돕는 모성보호 전문 AI 비서야.
            [현재 상황] 사용자는 지금 [{step['title']}] 단계를 처리 중이야.
            [답변 원칙]
            1. 모든 답변은 '2025년 개정 법안'을 최우선 반영한다. (임신기 단축 32주, 배우자 휴가 20일, 육아휴직 1.5년 등)
            2. 담당자가 임직원에게 즉시 말할 수 있는 '구어체 스크립트'를 포함한다.
            3. 말투는 친절하고 명확하며, 든든한 동료의 느낌을 유지한다.
            """
            
            with st.spinner("박사가 답변을 생각하고 있어요..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
                )
                answer = response.choices[0].message.content
                
                # 3. 답변 저장 및 화면 갱신
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

        except Exception as e:
            st.error(f"챗봇 통신 중 에러가 발생했습니다: {str(e)}")
