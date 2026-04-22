import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정: 화면 여백을 최소화하여 스크롤 발생 억제
st.set_page_config(
    page_title="KCIM 출산 육아 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 고효율 레이아웃을 위한 CSS (텍스트 가독성 및 공간 최적화)
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 전체 스크롤 억제 및 폰트 크기 조정 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    max-height: 100vh;
}

:root {
  --navy: #17384b; --bg: #f5f7fb; --line: #dbe4ee; --cyan: #11a8c7;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; font-size: 14px; }

/* 상단 슬림 배너 */
.slim-header {
    background: linear-gradient(90deg, #17384b 0%, #156a8d 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin-bottom: 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 컴팩트 카드 및 섹션 제목 */
.compact-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.section-title {
    font-weight: 800; color: var(--navy); font-size: 0.9rem; margin-bottom: 0.4rem;
}

/* 핵심 스크립트 박스 */
.script-box {
    background: #f0f9ff; border-left: 4px solid var(--cyan); padding: 0.7rem; border-radius: 8px; font-weight: 500; line-height: 1.5; color: #0e5a78; font-size: 0.95rem;
}

.item-row { display: flex; gap: 8px; padding: 0.25rem 0; border-bottom: 1px solid #f0f4f8; font-size: 0.85rem; }

.chip {
    background: #f1f5f9; color: var(--navy); padding: 0.1rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; border: 1px solid var(--line);
}
</style>
""",
    unsafe_allow_html=True,
)

# 3. 정제된 7단계 핵심 데이터
STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 응대", "short": "임신 확인", "color": "#4FACCC",
        "guide": "“정말 축하드립니다! 기쁜 소식이네요. 이 사실은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 우선 단축근무 제도부터 안내해 드릴까요?”",
        "check": ["임신 사실 공유 범위 확인 (비밀 유지)", "임신기 근로시간 단축 제도 안내", "플로우 내 신청서 경로 안내"],
        "forms": ["임신기 단축신청서"],
        "warn": ["비밀 엄수 필수", "임신 이유로 한 업무 배제 금지"],
        "target": "임신 확인 직원", "next": "단축근무 조율"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "guide": "“초기(12주 이내)와 말기(36주 이후)에는 하루 2시간 단축 근무가 가능합니다. 급여 삭감은 없으니, 원하시는 출퇴근 시간대를 말씀해 주세요.”",
        "check": ["임신 주수 확인 (증빙 수령)", "단축 시간대 협의 및 팀 공유", "플로우 신청서 작성 확인"],
        "forms": ["임신기 단축신청서"],
        "warn": ["주수 경과 시 변경 신청 필요"],
        "target": "단축근무 희망자", "next": "검진 시간 안내"
    },
    {
        "id": 3, "title": "정기 건강진단 (태아검진)", "short": "건강진단", "color": "#F5A623",
        "guide": "“검진 시간은 당연히 유급으로 보장됩니다. 검진일 전 플로우 양식의 '건강진단 신청서'를 통해 팀장님께 미리 공유해 주시면 됩니다.”",
        "check": ["검진 주기별 시간 부여 (4주/2주/1주)", "유급 인정 및 사후 증빙 안내", "신청 경로 가이드"],
        "forms": ["정기건강진단 신청서"],
        "warn": ["당일 진료 영수증 등 확인"],
        "target": "검진 대상 직원", "next": "연차/일정 조율"
    },
    {
        "id": 4, "title": "휴가 전 연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6",
        "guide": "“출산휴가 시작 전 남은 연차를 사용하실 수 있습니다. 팀 업무 인수인계 마무리 시점을 고려하여 가장 편한 날짜를 정해 알려주세요.”",
        "check": ["잔여 연차 일수 계산", "출산휴가 시작일 확정", "인수인계 리스트 점검"],
        "forms": ["연차 신청(표준 양식)"],
        "warn": ["연차 사용은 직원 자율 (강제 금지)"],
        "target": "휴가 예정자", "next": "출산휴가 등록"
    },
    {
        "id": 5, "title": "출산 전후 휴가 등록", "short": "출산 관련", "color": "#E8556D",
        "guide": "“출산휴가는 총 90일입니다. 출산 후 반드시 45일 이상이 확보되어야 하니 시작일을 잘 조정해 보아요. 정부 지원금 신청법도 메일로 보내드릴게요.”",
        "check": ["휴가 기간(90일) 등록", "출산 후 45일 보장 여부 확인", "급여 지원금 신청 안내"],
        "forms": ["출산휴가 신청서"],
        "warn": ["다태아의 경우 120일 보장"],
        "target": "출산 전후 직원", "next": "육아기 제도 안내"
    },
    {
        "id": 6, "title": "육아기 근로시간 단축 안내", "short": "육아 지원", "color": "#2980B9",
        "guide": "“복직 후 아이와 시간을 더 보내고 싶으시다면 육아기 단축 근무가 가능합니다. 육아휴직과 별개로 사용하실 수 있으니 계획을 세워볼까요?”",
        "check": ["단축 시간대 협의 (주 15~35시간)", "단축에 따른 급여 지원금 안내", "변경 신청 프로세스 설명"],
        "forms": ["육아기 단축신청서"],
        "warn": ["단축 기간 중 연장근로 원칙적 제한"],
        "target": "육아기 부모 직원", "next": "복직 프로세스"
    },
    {
        "id": 7, "title": "복직 준비 및 최종 확인", "short": "복직 준비", "color": "#27AE60",
        "guide": "“오랜만에 뵙네요! 복직을 진심으로 환영합니다. 자리는 미리 세팅해 두었습니다. 업무 적응을 위해 첫 주에는 가벼운 면담부터 시작해 볼까요?”",
        "check": ["복직일 재확정 및 공지", "자리/PC/권한 세팅 완료 확인", "복직 면담 및 업무 업데이트"],
        "forms": ["복직원 (사내 양식)"],
        "warn": ["복직 후 부당한 처우 절대 금지"],
        "target": "복직 예정자", "next": "사후 관리"
    }
]

# 4. 상태 관리
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

step = STEPS[st.session_state.active_step]

# 5. 메인 레이아웃 (한 페이지 최적화)

# 1열 상단 슬림 헤더
st.markdown(
    f"""
    <div class="slim-header">
      <div style="font-size: 1.1rem; font-weight: 800;">👶 KCIM 출산 육아 응대 가이드</div>
      <div style="font-size: 0.8rem; opacity: 0.9;">경영관리본부 HR 매뉴얼 | {datetime.date.today()}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2열 구성 (메뉴 | 본문)
col_left, col_right = st.columns([1, 4.3], gap="small")

with col_left:
    st.markdown('<div class="section-title">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"s_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    
    with st.expander("📂 양식 위치 정보"):
        st.markdown("<div style='font-size:0.75rem; color:#666;'>플로우 > [KCIM] 전체 공지 > 주요 양식 안내 > 2. 휴가 및 휴직</div>", unsafe_allow_html=True)

with col_right:
    # 단계 제목 및 정보 요약 바
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem; background:#fff; padding:0.5rem 1rem; border-radius:10px; border:1px solid var(--line);">
            <div style="font-size:1rem; font-weight:800; color:var(--navy);">STEP {step['id']}. {step['title']}</div>
            <div>
                <span class="chip">👤 대상: {step['target']}</span>
                <span class="chip">➡️ 다음: {step['next']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # 안내 스크립트 박스
    st.markdown('<div class="section-title">💬 담당자 핵심 안내 문구 (Script Tip)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="script-box">{step["guide"]}</div>', unsafe_allow_html=True)

    # 체크리스트와 서류 정보 (나란히 배치)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(
            f"""
            <div class="compact-card" style="height:150px;">
                <div class="section-title">✅ 관리자 필수 체크</div>
                {"".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']])}
            </div>
            """, unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="compact-card" style="height:150px;">
                <div class="section-title">🧾 필요 서류 / 주의사항</div>
                {"".join([f'<div style="margin-bottom:3px;"><span class="chip">📄 {f}</span></div>' for f in step['forms']])}
                <div style="margin-top:8px; font-size:0.8rem; color:#c53030; font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>
            </div>
            """, unsafe_allow_html=True
        )

    # 6. 하단 챗봇 (높이 고정하여 스크롤 최소화)
    st.markdown('<div class="section-title" style="margin-top:0.3rem; margin-bottom:0px;">🤖 AI 비서 상담 (실시간 사내 규정 문의)</div>', unsafe_allow_html=True)
    chat_container = st.container(height=180) 
    with chat_container:
        if not st.session_state.messages:
            st.write(f"<div style='font-size:0.8rem; color:#777;'>현재 <b>{step['short']}</b> 단계와 관련해 무엇이든 물어보세요.</div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            chat_container.chat_message(msg["role"]).markdown(f"<div style='font-size:0.85rem;'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("이 단계에 대해 질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": f"너는 KCIM HR 담당자 가이드봇이야. 현재 단계는 {step['title']}이고, 대상은 {step['target']}이야. 사내 규정에 따라 짧고 전문적으로 대답해줘."}, *st.session_state.messages],
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except:
            st.error("OpenAI API 연결을 확인해주세요.")
