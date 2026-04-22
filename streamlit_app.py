import datetime
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)

# 2. 고효율 레이아웃을 위한 CSS (디자인 설정)
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #17384b; --bg: #f5f7fb; --card: #ffffff; --line: #dbe4ee;
  --text: #1f2a35; --muted: #708191; --cyan: #11a8c7; --purple: #7d5fb2;
}

html, body, [class*="css"] { font-family: 'Pretendard', sans-serif !important; }
.stApp { background: var(--bg); }

/* 여백 최소화 */
.block-container { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }

.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff; border-radius: 15px; padding: 1rem 1.5rem; margin-bottom: 1rem;
}

.main-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 15px;
  padding: 1.2rem; margin-bottom: 0.8rem; box-shadow: 0 4px 12px rgba(23, 43, 64, 0.05);
}

.main-title { font-size: 1.25rem; font-weight: 800; color: var(--text); }

.item-row {
  display: flex; align-items: flex-start; gap: 8px; padding: 0.4rem 0;
  border-bottom: 1px solid #f1f5f9; font-size: 0.88rem;
}

.form-chip {
  display: inline-flex; align-items: center; gap: 4px; border-radius: 6px;
  border: 1px solid var(--line); background: #f8fafc; padding: 0.3rem 0.6rem;
  font-size: 0.8rem; color: var(--navy); font-weight: 600;
}

.new-badge {
  background: var(--purple); color: white; padding: 1px 5px;
  border-radius: 4px; font-size: 0.7rem; font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)

# 3. 2025 개정안 데이터 (7단계)
STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 안내", "short": "임신 확인", "color": "#4FACCC",
        "summary": "임신 확인 직후 개인정보 보호와 2025 개정 제도를 안내하는 단계입니다.",
        "guide": "축하 인사와 함께 비밀유지 원칙을 안내하세요. 2025년부터 난임치료휴가가 연간 6일(유급 2일)로 늘어난 점을 함께 설명해 주세요.",
        "check": ["임신 사실 공유 범위 확인 (비밀유지)", "난임치료휴가(6일/유급2일) 안내", "플로우 내 신청서 경로 안내"],
        "forms": ["임신확인서", "난임치료휴가 신청서"],
        "warn": ["비밀유지 의무 신설('24.10.22)", "임신 이유 불이익 조치 엄격 금지"],
        "target": "임신 확인 직원", "next_step": "단축근무 조율"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "summary": "12주 이내 및 32주 이후 단축 근무를 설정하는 단계입니다.",
        "guide": "2025년부터 단축 가능 기간이 확대되었습니다(기존 36주→32주). 하루 2시간 단축 시에도 급여는 100% 보장됨을 강조해 주세요.",
        "check": ["임신 12주 이내 또는 32주 이후 확인", "단축 시간대(2시간) 조율", "고위험 임신부 상시 단축 가능 안내"],
        "forms": ["임신기 단축신청서"],
        "warn": ["32주 이후 확대 적용 여부 확인", "고위험군은 주수 상관없이 상시 신청 가능"],
        "target": "단축 희망 직원", "next_step": "건강진단 안내"
    },
    {
        "id": 3, "title": "임산부 정기건강진단", "short": "건강진단", "color": "#F5A623",
        "summary": "태아 검진을 위한 유급 시간을 보장하는 단계입니다.",
        "guide": "검진 시간은 유급입니다. 플로우에서 '정기건강진단 신청서'를 작성하도록 안내하고, 검진 당일 진료비 영수증 등을 확인하세요.",
        "check": ["검진 주기별 시간 부여 확인", "유급 인정 기준 설명", "신청서 작성 경로 안내"],
        "forms": ["정기건강진단 신청서"],
        "warn": ["검진 시간 사용에 대한 눈치 주기 금지"],
        "target": "검진 대상 직원", "next_step": "연차/휴가 조율"
    },
    {
        "id": 4, "title": "연차 정리 및 인수인계", "short": "연차 정리", "color": "#9B59B6",
        "summary": "출산휴가 전 남은 연차를 사용하도록 돕는 단계입니다.",
        "guide": "휴가 전 연차를 붙여 사용하면 더 일찍 휴식할 수 있습니다. 업무 인수인계가 완료되는 시점을 고려하여 일정을 확정해 보세요.",
        "check": ["잔여 연차 일수 계산", "출산휴가 전 연차 사용일 확정", "업무 인수인계 리스트 확인"],
        "forms": ["연차 신청서"],
        "warn": ["연차 사용 강제 소진 절대 금지 (자율 사용)"],
        "target": "휴가 예정자", "next_step": "출산휴가 신청"
    },
    {
        "id": 5, "title": "출산 전후 및 배우자 휴가", "short": "출산/배우자", "color": "#E8556D",
        "summary": "90일의 출산휴가와 20일로 늘어난 배우자 휴가를 안내합니다.",
        "guide": "배우자 출산휴가가 20일로 대폭 확대되었습니다(3회 분할). 미숙아 출산 시 휴가 기간은 100일로 늘어난 점도 참고하세요.",
        "check": ["배우자 휴가(20일) 안내", "미숙아 출산 시 100일 적용 확인", "산후 45일 보장 여부 체크"],
        "forms": ["출산휴가 신청서", "배우자 휴가 신청서"],
        "warn": ["배우자 휴가는 출산 후 120일 이내 사용", "산후 45일 의무 휴식"],
        "target": "출산 전후 직원", "next_step": "육아 지원 안내"
    },
    {
        "id": 6, "title": "육아기 지원 및 단축", "short": "육아 지원", "color": "#2980B9",
        "summary": "만 12세 이하 자녀 대상 최대 3년의 단축 근무를 지원합니다.",
        "guide": "자녀 연령이 만 12세(초6)까지 확대되었습니다. 육아휴직 미사용 기간을 가산해 최대 3년까지 단축 근무가 가능함을 안내하세요.",
        "check": ["자녀 연령(만 12세 이하) 확인", "단축 근무 기간(최대 3년) 안내", "최소 사용 기간 1개월 단축 안내"],
        "forms": ["육아기 단축신청서"],
        "warn": ["단축 시간 연차 산정 시 포함 확인", "주 5~25시간 단축 가능"],
        "target": "육아기 부모 직원", "next_step": "복직/연장 프로세스"
    },
    {
        "id": 7, "title": "육아휴직 및 복직 관리", "short": "복직 준비", "color": "#27AE60",
        "summary": "최대 1.5년으로 늘어난 육아휴직과 성공적 복직을 돕는 단계입니다.",
        "guide": "육아휴직은 부모 모두 3개월 사용 시 1.5년까지 가능합니다. 사후지급금 폐지로 복직 즉시 전액 지급되니 경제적 부담을 덜 수 있음을 알리세요.",
        "check": ["육아휴직(1.5년) 기간 확정", "사후지급금 폐지(전액지급) 설명", "복직 면담 및 자리 세팅"],
        "forms": ["육아휴직 신청서", "복직원"],
        "warn": ["복직 후 부당 처우 엄격 금지", "복직 전 14일 이내 허용의무 표시"],
        "target": "복직 예정자", "next_step": "사후 관리"
    }
]

# 4. 세션 상태 관리
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

active_idx = st.session_state.active_step
step = STEPS[active_idx]

# 5. 헤더
st.markdown(
    f"""
    <div class="hero">
      <div style="font-size: 1.5rem; font-weight: 800;">👶 2026 KCIM 출산·육아 응대 매뉴얼 <span class="new-badge">2025 개정완료</span></div>
      <div style="font-size: 0.9rem; opacity: 0.9;">임신 확인부터 복직까지, HR 담당자를 위한 단계별 핵심 가이드라인입니다.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. 레이아웃
left_col, main_col = st.columns([1, 4.3], gap="small")

with left_col:
    st.markdown('<div style="font-size:1rem; font-weight:800; color:var(--navy); margin-bottom:0.8rem;">📍 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == active_idx else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"btn_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    with st.expander("📂 양식 위치 정보"):
        st.markdown("<div style='font-size:0.75rem;'>플로우 > 전체 공지사항 > 상단고정 > [공지] 사내 주요 양식 안내 > 2. 휴가 및 휴직</div>", unsafe_allow_html=True)

with main_col:
    tab_guide, tab_chat = st.tabs(["📖 단계별 가이드", "🤖 AI 파트너 케이(K) 상담"])

    with tab_guide:
        # 가이드 요약 카드 (들여쓰기 제거로 SyntaxError 방지)
        st.markdown(f"""
<div class="main-card" style="border-left: 6px solid {step['color']};">
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div>
<div style="color:var(--muted); font-size:0.85rem; font-weight:700;">STEP {step['id']}</div>
<div class="main-title">{step['title']}</div>
<div style="color:var(--muted); font-size:0.9rem; margin-top:3px;">{step['summary']}</div>
</div>
<div style="text-align:right;">
<span class="form-chip">👤 {step['target']}</span><br>
<span class="form-chip" style="margin-top:5px;">➡️ {step['next_step']}</span>
</div>
</div>
<div style="margin-top:1.2rem;">
<div style="font-size:0.9rem;font-weight:800;color:var(--navy);margin-bottom:0.4rem;">🗣️ 담당자 안내 스크립트</div>
<div style="background:#f4fbfe; border:1px solid #d0ecf8; border-radius:10px; padding:1rem; font-size:0.95rem; line-height:1.6; font-weight:500; color:#0e5a78;">
{step['guide']}
</div>
</div>
</div>
""", unsafe_allow_html=True)

        # 체크리스트 및 서류 (2단 구성)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
<div class="main-card" style="height:160px;">
<div style="font-size:0.9rem; font-weight:800; color:var(--navy); margin-bottom:0.6rem;">✅ 관리자 체크리스트</div>
{"".join([f'<div class="item-row">✔ {i}</div>' for i in step['check']])}
</div>
""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
<div class="main-card" style="height:160px;">
<div style="font-size:0.9rem; font-weight:800; color:var(--navy); margin-bottom:0.5rem;">🧾 필요 서류 / 주의사항</div>
{"".join([f'<div style="margin-bottom:4px;"><span class="form-chip">📄 {f}</span></div>' for f in step['forms']])}
<div style="margin-top:8px; font-size:0.8rem; color:#c53030; font-weight:700;">⚠️ 주의: {" / ".join(step["warn"])}</div>
</div>
""", unsafe_allow_html=True)

    with tab_chat:
        st.markdown(f"""
<div style="background:#eaf5fa; border-radius:12px; padding:1rem; margin-bottom:1rem;">
<div style="font-size:1rem; font-weight:800; color:var(--navy); margin-bottom:0.3rem;">🤖 HR 파트너 케이(K) 상담</div>
<div style="font-size:0.85rem; color:#4a5d6e;">현재 선택된 <b>[{step['title']}]</b> 단계의 개정 수치나 구체적인 대응법을 알려드려요.</div>
</div>
""", unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("질문을 입력하세요..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                # 케이(K) 페르소나 시스템 프롬프트 주입
                system_prompt = f"""
너의 이름은 'HR 파트너 케이(K)'야. KCIM 경영관리본부 담당자를 돕는 모성보호 전문 AI 비서야.
[현재 상황] 사용자는 지금 [{step['title']}] 단계를 처리 중이야.
[답변 원칙]
1. 모든 답변은 '2025년 개정 법안'을 최우선으로 반영한다. (배우자 휴가 20일, 육아휴직 1.5년 등)
2. 담당자가 임직원에게 즉시 말할 수 있는 '구어체 스크립트'를 포함해줘.
3. 말투는 친절하고 명확하며, 든든한 동료 느낌을 유지한다.
[지식 요약]
- 임신기 단축: 12주 이내, 32주 이후
- 배우자 휴가: 20일 (분할 3회)
- 육아기 단축: 만 12세 이하 (초6)
- 육아휴직: 부모 모두 3개월 사용 시 1.5년
"""
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, *st.session_state.chat_messages],
                )
                answer = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.write(answer)
                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("OpenAI API 연결에 오류가 발생했습니다.")
