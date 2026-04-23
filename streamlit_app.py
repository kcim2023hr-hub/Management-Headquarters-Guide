import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정: 화면을 넓게 쓰고 여백을 최소화
st.set_page_config(
    page_title="KCIM 모성보호 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 디자인 레이아웃 복구 및 여백 제거 CSS
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 화면 여백 강제 제거 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --card: #ffffff; --line: #dbe4ee;
  --text: #1f2a35; --muted: #708191; --cyan: #11a8c7; --purple: #7d5fb2;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; }
.stApp { background: var(--bg); }

/* 상단 대형 히어로 배너 (복구됨) */
.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff; border-radius: 15px; padding: 1.5rem 2rem; margin-bottom: 1rem;
  box-shadow: 0 6px 20px rgba(23, 56, 75, 0.2);
}

.hero-title { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; }
.hero-desc { font-size: 1rem; opacity: 0.9; }

/* 메인 카드 디자인 */
.main-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 12px;
  padding: 1.2rem; margin-bottom: 0.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.main-title { font-size: 1.3rem; font-weight: 800; color: var(--text); margin-bottom: 0.3rem; }

/* 스크립트 박스 */
.script-box {
  background: #f4fbfe; border-left: 5px solid var(--cyan); padding: 0.8rem 1rem;
  border-radius: 8px; font-weight: 500; line-height: 1.6; color: #0e5a78; font-size: 1rem;
}

/* 리스트 스타일 */
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

# 3. 2025 개정 데이터 (전체 7단계 완결)
STEPS = [
    {"id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC", "guide": "“축하드립니다! 임신 소식은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 먼저 단축근무 제도부터 안내해 드릴까요?”", "check": ["공유 희망 범위 확인 (비밀유지)", "난임치료휴가(연 6일/유급2일) 안내", "플로우 내 신청서 경로 설명"], "forms": ["임신확인서", "난임휴가 신청서"], "warn": ["비밀유지 의무 준수 필수", "임신 이유 불이익 조치 금지"], "target": "임신 확인 직원", "next": "단축 조율"},
    {"id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A", "guide": "“이제 32주부터 단축 근무가 가능합니다. 하루 2시간을 원하시는 시간대에 맞춰 사용하실 수 있고, 급여는 그대로 보전됩니다.”", "check": ["임신 12주 이내 또는 32주 이후 확인", "단축 시간대(2시간) 협의", "팀 내 업무 조정 지원"], "forms": ["임신기 단축신청서"], "warn": ["개정: 36주 → 32주 확대", "고위험군은 전 기간 가능"], "target": "단축 희망 직원", "next": "검진 안내"},
    {"id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623", "guide": "“검진 시간은 유급으로 보장되는 권리입니다. 플로우 양식의 '건강진단 신청서'만 작성해 주시면 제가 팀장님께 공유해 드릴게요.”", "check": ["검진 주기별 시간 부여 확인", "유급 인정 및 증빙 안내", "신청 경로 가이드"], "forms": ["정기건강진단 신청서"], "warn": ["진료 영수증 등 사후 확인", "사용 불이익 금지"], "target": "검진 대상자", "next": "연차 조율"},
    {"id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6", "guide": "“출산휴가 전 남은 연차를 사용해 조금 더 일찍 휴식을 시작하실 수 있습니다. 인수인계 마무리 시점을 정해서 알려주세요.”", "check": ["잔여 연차 계산 및 소진 계획", "출산휴가 시작일 확정", "인수인계 리스트 작성"], "forms": ["연차 신청서"], "warn": ["연차 강제 소진 금지", "자율권 존중"], "target": "휴가 예정자", "next": "출산/배우자 휴가"},
    {"id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산 관련", "color": "#E8556D", "guide": "“출산휴가는 90일이며, 배우자분도 20일간 유급 휴가를 쓰실 수 있습니다. 미숙아 출산 시 휴가 기간은 100일로 적용됩니다.”", "check": ["배우자 출산휴가(20일) 안내", "미숙아 출산(100일) 적용 확인", "유산·사산 휴가(10일) 안내"], "forms": ["출산휴가 신청서", "배우자 휴가 신청서"], "warn": ["산후 45일 보장 필수", "배우자 휴가는 120일 내 사용"], "target": "출산 전후 직원", "next": "육아기 지원"},
    {"id": 6, "title": "육아기 근로시간 단축", "short": "육아 지원", "color": "#2980B9", "guide": "“자녀가 초등 6학년(만 12세)이 될 때까지 최대 3년 동안 단축 근무를 하실 수 있습니다. 필요하시면 언제든 말씀해주세요.”", "check": ["대상 자녀 연령(만 12세) 확인", "단축 기간 및 시간 협의", "최소 사용 기간 1개월 안내"], "forms": ["육아기 단축신청서"], "warn": ["단축 시간 연차 산정 포함", "주 5~25시간 단축"], "target": "육아기 부모", "next": "육아휴직/복직"},
    {"id": 7, "title": "육아휴직 및 복직 관리", "short": "복직 준비", "color": "#27AE60", "guide": "“육아휴직은 1년 6개월까지 가능해요. 복직 시 급여 전액을 받으시니 금전적 부담을 덜어보세요. 복직을 환영합니다!”", "check": ["육아휴직(1.5년) 연장 안내", "사후지급금 폐지(전액지급) 설명", "복직 면담 및 자리 세팅"], "forms": ["육아휴직 신청서", "복직원"], "warn": ["복직 전 14일 내 의사표시", "부당 처우 절대 금지"], "target": "복직 예정자", "next": "사후 관리"}
]

# 4. 세션 관리
if "active_step" not in st.session_state: st.session_state.active_step = 0
if "messages" not in st.session_state: st.session_state.messages = []

active_idx = st.session_state.active_step
step = STEPS[active_idx]

# 5. 메인 화면 레이아웃 (한 화면 압축)

# 상단 헤더 배너 (복구)
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">👶 KCIM 출산 육아 응대 가이드 <span class="new-badge">2025 개정 반영</span></div>
        <div class="hero-desc">임신 확인부터 복직까지, 경영관리본부 담당자를 위한 단계별 핵심 가이드라인입니다.</div>
    </div>
    """, unsafe_allow_html=True
)

col_nav, col_body = st.columns([1, 4.4], gap="small")

# --- 좌측 내비게이션 ---
with col_nav:
    st.markdown('<div style="font-weight: 800; color:var(--navy); font-size:0.9rem; margin-bottom:0.5rem;">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == active_idx else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    with st.expander("📂 양식 위치", expanded=False):
        st.markdown("<div style='font-size:0.75rem; color:#666;'>플로우 > 전체공지 > 주요양식 > 2.휴가/휴직</div>", unsafe_allow_html=True)

# --- 우측 메인 본문 ---
with col_body:
    # 1. 상단 요약 카드 (제목 + 뱃지)
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

    # 2. 세부 내용 (체크리스트 & 서류)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="main-card" style="height:145px;"><div style="font-weight:800; font-size:0.9rem; margin-bottom:0.5rem;">✅ 관리자 필수 체크</div>' + 
                    "".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']]) + '</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="main-card" style="height:145px;"><div style="font-weight:800; font-size:0.9rem; margin-bottom:0.5rem;">🧾 서류 및 주의사항</div>' + 
                    "".join([f'<div style="margin-bottom:3px;"><span class="form-chip">📄 {f}</span></div>' for f in step['forms']]) + 
                    f'<div style="margin-top:6px; font-size:0.8rem; color:var(--red); font-weight:700; line-height:1.3;">⚠️ 주의: {" / ".join(step["warn"])}</div>' + '</div>', unsafe_allow_html=True)

    # 3. 최하단 챗봇 (높이 조절 및 페르소나 적용)
    st.markdown('<div style="font-weight: 800; color:var(--navy); font-size:0.9rem; margin-top:0.3rem; margin-bottom:0.2rem;">🤖 HR 파트너 케이(K) 상담</div>', unsafe_allow_html=True)
    chat_container = st.container(height=260) 
    with chat_container:
        if not st.session_state.messages:
            st.write(f"<div style='font-size:0.85rem; color:#888;'>반가워요! 저는 KCIM의 HR 파트너 <b>케이(K)</b>입니다. {step['short']} 단계의 구체적인 법규나 대응법이 궁금하시면 말씀해주세요.</div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).markdown(f"<div style='font-size:0.9rem;'>{msg['content']}</div>", unsafe_allow_html=True)

    # 4. 챗봇 API 로직
    if prompt := st.chat_input("이 단계의 대응법을 물어보세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container: st.chat_message("user").write(prompt)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            system_prompt = f"""
            너의 이름은 '육아지원박사'야. KCIM 경영관리본부 담당자를 돕는 모성보호 전문 AI 비서야.
            [현재 상황] 사용자는 지금 [{step['title']}] 단계를 처리 중이야.
            [답변 원칙]
            1. 모든 답변은 '2025년 개정 법안'을 최우선 반영한다. (임신기 단축 32주, 배우자 휴가 20일, 육아휴직 1.5년 등)
            2. 담당자가 임직원에게 즉시 말할 수 있는 '구어체 스크립트'를 항상 포함해줘.
            3. 법적 근거와 사내 양식 위치를 언급하며 전문성을 높인다.
            4. 말투는 친절하고 명확하며, 담당자를 서포트하는 '든든한 동료'의 느낌을 유지한다.
            5. 질문의 의도를 정확하게 파악하고, 거짓없이 사실만을 답변한다.
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
