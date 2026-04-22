import datetime
import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="KCIM 출산 육아 응대 가이드",
    page_icon="👶",
    layout="wide", # 가이드와 챗봇을 한눈에 보기 위한 와이드 모드
)

# ================================================
# 🎨 맞춤형 CSS 디자인
# ================================================
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy: #17384b;
  --bg: #f5f7fb;
  --card: #ffffff;
  --line: #dbe4ee;
  --text: #1f2a35;
  --muted: #708191;
  --cyan: #11a8c7;
}

html, body, [class*="css"] {
  font-family: 'Pretendard', sans-serif !important;
}

.stApp { background: var(--bg); }

/* Hero Header */
.hero {
  background: linear-gradient(135deg, #17384b 0%, #156a8d 100%);
  color: #fff;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px rgba(23, 56, 75, 0.2);
}

/* Card Style */
.main-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.5rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.item-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 0.6rem 0;
  border-bottom: 1px solid #f0f4f8;
  font-size: 0.92rem;
}

.item-row:last-child { border-bottom: 0; }

.form-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: #f8fafc;
  padding: 0.4rem 0.8rem;
  font-size: 0.82rem;
  color: var(--navy);
  font-weight: 600;
}

/* Chat Section */
.chat-header {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ================================================
# 📊 가이드 데이터 (1~7단계 완결)
# ================================================
COMMON_FORM_GUIDE = {
    "location": "플로우 내 [KCIM] 전체 공지사항 > 상단고정 > [공지] 사내 주요 양식 안내 > 2. 휴가 및 휴직",
    "form_name": "KCIM_임신•육아기 관련 지원 신청서",
    "tabs": ["임신기/육아기 단축신청서", "정기건강진단 신청서", "유산/사산 휴가 신청서", "단축 변경신청서"]
}

STEPS = [
    {
        "id": 1, "title": "임신 확인 및 초기 안내", "short": "임신 확인", "color": "#4FACCC",
        "summary": "임신 사실 확인 직후 개인정보 보호와 지원 제도를 안내하는 단계입니다.",
        "guide": "먼저 진심 어린 축하 인사를 전해주세요! 그 후 임신 사실 공유 범위를 확인하고, 플로우 상단고정의 신청서 위치를 안내하는 것이 핵심입니다.",
        "check": ["임신 사실 공유 범위 확인", "임신기 근로시간 단축 가능 여부 안내", "플로우 내 신청서 위치 및 작성법 설명"],
        "forms": ["임신기/육아기 근로시간 단축신청서"],
        "warn": ["임신 이유로 한 불이익 조치 금지", "당사자 동의 없는 임신 사실 공유 주의"],
        "faq": [("처음 문의 시 무엇부터 할까요?", "축하 인사와 함께 개인정보 보호 원칙을 확인하고 신청서 위치를 알려주세요.")],
        "target": "임신 확인 임직원", "next": "단축근무 여부 확인"
    },
    {
        "id": 2, "title": "임신기 근로시간 단축", "short": "임신기 단축", "color": "#37B89A",
        "summary": "주수 확인 후 실제 단축 근무 시간을 조율하고 신청하는 단계입니다.",
        "guide": "직원의 현재 임신 주수를 먼저 확인하세요. 법정 단축 시기에 해당하는지 보고, 업무 공백이 생기지 않도록 팀 내 조율을 지원합니다.",
        "check": ["현재 임신 주수 확인 (12주 이내 또는 36주 이후)", "단축 시간대 및 업무 조율", "최초 신청/변경 신청 구분"],
        "forms": ["임신기/육아기 근로시간 단축신청서"],
        "warn": ["시기가 바뀌면 변경신청서를 다시 작성해야 함을 안내하세요."],
        "faq": [("주수 계산은 어떻게 하나요?", "병원이 발행한 진단서나 임신확인서상의 주수를 기준으로 합니다.")],
        "target": "단축근무 희망자", "next": "정기건강진단 안내"
    },
    {
        "id": 3, "title": "임산부 정기건강진단", "short": "건강진단", "color": "#F5A623",
        "summary": "정기 검진 시 유급 휴가(시간)를 보장하고 신청하는 단계입니다.",
        "guide": "검진 일정은 미리 공유받는 것이 좋습니다. 유급으로 인정되는 시간임을 안내하고, 신청서 탭에서 '정기건강진단'을 선택하게 하세요.",
        "check": ["검진 예정일 확인", "근로시간 인정 기준 설명", "신청서 작성 위치 안내"],
        "forms": ["임산부 정기건강진단 신청서"],
        "warn": ["검진 시간 사용에 대해 눈치를 주는 분위기가 형성되지 않도록 관리합니다."],
        "faq": [("반복되는 검진마다 써야 하나요?", "네, 내부 기록과 근태 관리를 위해 매번 작성하는 것이 원칙입니다.")],
        "target": "정기 검진 대상자", "next": "연차 일정 점검"
    },
    {
        "id": 4, "title": "잔여 연차 및 일정 정리", "short": "연차 정리", "color": "#9B59B6",
        "summary": "출산휴가 전 남은 연차를 효율적으로 사용할 수 있게 돕는 단계입니다.",
        "guide": "출산휴가 시작 전 잔여 연차를 소진할지 여부를 확인하세요. 강제 사항은 아니지만, 휴가 일정을 미리 확정하면 팀 인수인계가 수월해집니다.",
        "check": ["잔여 연차 일수 확인", "연차 사용 희망 일정 조율", "인수인계 시점 확인"],
        "forms": ["별도 양식 없음 (일정 조율 중심)"],
        "warn": ["연차 강제 소진으로 느껴지지 않도록 부드럽게 권유하세요."],
        "faq": [("연차를 꼭 다 써야 하나요?", "아니요, 근로자의 권리이므로 본인의 의사를 존중해야 합니다.")],
        "target": "출산휴가 앞둔 임직원", "next": "출산휴가 신청"
    },
    {
        "id": 5, "title": "출산 전후 관련 신청", "short": "출산 관련", "color": "#E8556D",
        "summary": "본격적인 출산휴가 및 혹시 모를 유산/사산 상황에 대응하는 단계입니다.",
        "guide": "가장 중요한 시기입니다. 출산휴가 기간(90일)과 급여 신청 방법을 안내하세요. 유산/사산 시에도 법적 보호를 받을 수 있음을 미리 인지하고 계시면 좋습니다.",
        "check": ["출산 예정일 및 휴가 시작일 확정", "유산/사산 휴가 신청 양식 안내", "정부 지원금 신청법 안내"],
        "forms": ["유산/사산 휴가 신청서", "출산전후휴가 신청서(내부규정확인)"],
        "warn": ["출산 전후 90일(다태아 120일)의 기간을 정확히 준수해야 합니다."],
        "faq": [("휴가는 언제부터 쓸 수 있나요?", "출산일 전후를 합쳐 90일이며, 출산 후에 반드시 45일 이상이 확보되어야 합니다.")],
        "target": "출산 전후 임직원", "next": "육아기 지원 안내"
    },
    {
        "id": 6, "title": "육아기 지원 및 변경", "short": "육아기 지원", "color": "#2980B9",
        "summary": "복직 전후 육아를 위해 근로시간을 단축하거나 지원 제도를 이용하는 단계입니다.",
        "guide": "육아기 근로시간 단축 제도를 안내하세요. 복직 후에도 일과 육아를 병행할 수 있도록 유연한 근무 환경을 지원하는 것이 목적입니다.",
        "check": ["육아기 단축 근무 시간 확정", "변경 필요 시 변경신청서 안내", "육아휴직과의 차이점 설명"],
        "forms": ["임신기/육아기 근로시간 단축신청서", "단축 변경신청서"],
        "warn": ["단축 기간 중 연장 근로는 원칙적으로 제한됩니다."],
        "faq": [("육아휴직 대신 단축근무가 가능한가요?", "네, 만 8세 이하 자녀가 있다면 육아기 근로시간 단축 신청이 가능합니다.")],
        "target": "육아기 임직원", "next": "복직 준비 점검"
    },
    {
        "id": 7, "title": "복직 및 최종 일정 확인", "short": "복직 준비", "color": "#27AE60",
        "summary": "긴 휴가를 마치고 돌아오는 직원의 연착륙을 돕는 마지막 단계입니다.",
        "guide": "복직을 진심으로 환영해 주세요! 복직 전 면담을 통해 근무 형태 변경 여부를 최종 확인하고, 변화된 사내 규정이나 시스템이 있다면 미리 안내합니다.",
        "check": ["정확한 복직일 재확인", "부서 및 업무 배치 적절성 검토", "복직 후 초기 적응 면담"],
        "forms": ["복직원(내부규정확인)", "단축 변경신청서(필요시)"],
        "warn": ["복직 후 업무 배제나 차별이 발생하지 않도록 팀 분위기를 관리합니다."],
        "faq": [("복직 시기를 앞당길 수 있나요?", "부서와 협의가 완료된다면 조기 복직도 가능합니다.")],
        "target": "복직 예정 임직원", "next": "사후 관리"
    }
]

# ================================================
# ⚙️ 세션 상태 관리
# ================================================
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

step = STEPS[st.session_state.active_step]

# ================================================
# 🏠 메인 레이아웃 (3단 구성)
# ================================================
# 상단 배너
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-title">👶 KCIM 출산 육아 응대 가이드</div>
      <div class="hero-desc">임신 확인부터 복직까지, 가이드를 보며 AI 비서와 실시간으로 상담하세요.</div>
      <div class="chip-container">
        <div class="chip">📌 단계별 빠른 응대</div>
        <div class="chip">🧾 필요 서류 즉시 확인</div>
        <div class="date-chip">기준일: {datetime.date.today()}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 좌측(1) : 중앙(2.5) : 우측(1.5) 컬럼 배치
col_menu, col_main, col_chat = st.columns([1, 2.5, 1.5], gap="medium")

# --- 1단: 좌측 메뉴 (단계 선택) ---
with col_menu:
    st.markdown('<div style="font-weight: 800; color:var(--navy); margin-bottom: 15px;">🏁 단계 선택</div>', unsafe_allow_html=True)
    for idx, s in enumerate(STEPS):
        btn_type = "primary" if idx == st.session_state.active_step else "secondary"
        if st.button(f"STEP {s['id']}. {s['short']}", key=f"step_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_step = idx
            st.rerun()

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    with st.expander("📂 공통 양식 위치 안내"):
        st.markdown(
            f"""
            <div style="font-size:0.85rem; line-height:1.6;">
            <b>📍 위치:</b><br>{COMMON_FORM_GUIDE['location']}<br><br>
            <b>📄 양식명:</b><br>{COMMON_FORM_GUIDE['form_name']}
            </div>
            """, unsafe_allow_html=True
        )

# --- 2단: 중앙 콘텐츠 (가이드 본문) ---
with col_main:
    # 제목 및 요약 카드
    st.markdown(
f"""
<div class="main-card" style="border-left: 6px solid {step['color']};">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-weight:700; color:var(--muted); font-size:0.9rem;">STEP {step['id']}</span>
        <div>
            <span class="form-chip">👤 대상: {step['target']}</span>
            <span class="form-chip">➡️ 다음: {step['next']}</span>
        </div>
    </div>
    <div class="main-title" style="margin-top:0.5rem; margin-bottom:0.5rem;">{step['title']}</div>
    <div style="color:var(--muted); font-size:0.95rem; margin-bottom:1.5rem;">{step['summary']}</div>
    <div style="font-weight:800; font-size:0.9rem; color:var(--navy); margin-bottom:0.6rem;">🗣️ 담당자 안내 스크립트 (Tip)</div>
    <div style="background:#f4fbfe; border:1px solid #d0ecf8; border-radius:12px; padding:1.2rem; font-size:1rem; line-height:1.7; color:#0e5a78;">
        {step['guide']}
    </div>
</div>
""", unsafe_allow_html=True)

    # 체크리스트 & 서류/주의사항 (2단 구성)
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown(
            f"""
            <div class="main-card" style="height: 100%;">
                <div style="font-weight:800; color:var(--navy); margin-bottom:1rem;">✅ HR 담당자 체크리스트</div>
                {''.join([f'<div class="item-row"><b>✔</b> {i}</div>' for i in step['check']])}
            </div>
            """, unsafe_allow_html=True
        )
    with c_right:
        st.markdown(
            f"""
            <div class="main-card" style="height: 100%;">
                <div style="font-weight:800; color:var(--navy); margin-bottom:0.8rem;">🧾 필요 서류 및 주의사항</div>
                <div style="margin-bottom:1rem;">
                    {''.join([f'<span class="form-chip" style="margin-bottom:5px;">📄 {f}</span>' for f in step['forms']])}
                </div>
                <hr style="border:none; border-top:1px solid #eee;">
                <div style="font-size:0.85rem; color:#9a2948; line-height:1.5;">
                    <b>⚠️ 주의:</b><br>
                    {'<br>'.join(['• ' + w for w in step['warn']])}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    # FAQ 영역
    with st.expander("❓ 자주 받는 질문 (FAQ)"):
        for q, a in step["faq"]:
            st.markdown(f"**Q. {q}**")
            st.info(a)

# --- 3단: 우측 콘텐츠 (AI 상담 챗봇) ---
with col_chat:
    st.markdown('<div class="chat-header">🤖 AI 비서 상담</div>', unsafe_allow_html=True)
    st.caption(f"현재 [STEP {step['id']}] 내용을 바탕으로 답변합니다.")

    # 채팅창 영역 (스크롤 가능하도록 높이 고정)
    chat_box = st.container(height=550)
    with chat_box:
        if not st.session_state.chat_messages:
            st.write("안녕하세오! 궁금한 점이 있으신가요? 가이드를 보며 자유롭게 물어봐주세요. 😉")
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # 입력창
    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.write(prompt)

        try:
            # OpenAI 클라이언트 (st.secrets에 API 키가 설정되어 있어야 함)
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            # 단계별 컨텍스트를 시스템 프롬프트에 제공
            system_msg = f"""너는 KCIM 경영관리본부의 친절하고 스마트한 HR 상담사야. 
            현재 사용자는 '{step['title']}' 단계를 처리 중이야. 
            내용 요약: {step['summary']} / 가이드: {step['guide']}
            이 맥락을 바탕으로 담당자가 임직원에게 답변하기 좋게 친절하고 위트 있게 답변해줘."""
            
            with st.chat_message("assistant"):
                with st.spinner("생각 중..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": system_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages],
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            st.rerun() # 대화 내용 갱신을 위해 리런
        except Exception as e:
            st.error(f"상담 연결에 실패했습니다. (API 키 확인 필요)")

    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

# --- 하단 저작권 표기 ---
st.markdown(
    """
    <hr style="margin-top: 3rem; border:none; border-top:1px solid #ddd;">
    <div style="text-align:center; color: #999; font-size: 0.8rem; padding-bottom: 2rem;">
      © 2026 KCIM Management Headquarters. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True
)
