import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 전문 대시보드",
    page_icon="⚖️",
    layout="wide"
)

# Kcim 브랜드 컬러
KCIM_DARK = "#193D52"
KCIM_MEDIUM = "#00A8C0"
KCIM_LIGHT = "#8CCEE7"
WHITE = "#FFFFFF"

# 2. 대시보드 전용 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    .stApp {{ background-color: #F8FAFC; }}
    
    /* 헤더 */
    .header-box {{
        background: {KCIM_DARK};
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* 섹션 타이틀 */
    .section-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {KCIM_DARK};
        margin-bottom: 1rem;
        border-left: 5px solid {KCIM_MEDIUM};
        padding-left: 12px;
    }}
    
    /* FAQ 카드 스타일 */
    .faq-card {{
        background: {WHITE};
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .faq-q {{ font-weight: 700; color: {KCIM_MEDIUM}; margin-bottom: 0.5rem; display: block; }}
    .faq-a {{ font-size: 0.95rem; color: #334155; line-height: 1.6; }}
    
    /* 핵심 수치 하이라이트 */
    .highlight-box {{
        background: #F1F5F9;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px dashed {KCIM_MEDIUM};
    }}
    .highlight-val {{ font-size: 1.5rem; font-weight: 800; color: {KCIM_DARK}; }}
    </style>
    """, unsafe_allow_html=True)

# 3. 상단 헤더
st.markdown(f"""
    <div class="header-box">
        <h2 style="margin:0;">⚖️ 2025 육아지원제도 전문 노무 대시보드</h2>
        <p style="opacity:0.8; margin:5px 0 0 0;">Kcim 경영관리본부 | 가장 많이 묻는 질문과 핵심 개정안</p>
    </div>
    """, unsafe_allow_html=True)

# 4. 메인 레이아웃 (L: FAQ 및 핵심요약, R: AI 상담)
col_left, col_right = st.columns([0.65, 0.35], gap="large")

with col_left:
    # --- 핵심 변경 수치 퀵뷰 ---
    st.markdown('<p class="section-title">🚀 2025 핵심 변경 사항 (한눈에 보기)</p>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown(f'<div class="highlight-box"><small>육아기 단축연령</small><br><span class="highlight-val">초등 6학년</span></div>', unsafe_allow_html=True)
    with q2:
        st.markdown(f'<div class="highlight-box"><small>육아휴직 급여상한</small><br><span class="highlight-val">최대 250만원</span></div>', unsafe_allow_html=True)
    with q3:
        st.markdown(f'<div class="highlight-box"><small>배우자 출산휴가</small><br><span class="highlight-val">20일 (유급)</span></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- FAQ 섹션 (자주 묻는 질문) ---
    st.markdown('<p class="section-title">❓ 임직원 자주 묻는 질문 (FAQ)</p>', unsafe_allow_html=True)
    
    faqs = [
        {
            "q": "이미 육아휴직 중인데, 2025년에 인상된 급여를 받을 수 있나요?",
            "a": "<b>네, 가능합니다.</b> 2025년 1월 1일 이후 사용한 기간에 대해서는 개정된 급여 기준(1~3개월 250만 원 등)이 적용됩니다."
        },
        {
            "q": "육아기 근로시간 단축을 사용할 수 있는 자녀 연령이 어떻게 바뀌었나요?",
            "a": "기존 만 8세(초2) 이하에서 <b>만 12세 또는 초등학교 6학년 이하</b>로 대폭 확대되었습니다."
        },
        {
            "q": "육아휴직 1년 6개월 연장 조건이 궁금합니다.",
            "a": "부모가 각각 육아휴직을 <b>3개월 이상 사용한 경우</b>에만 각각 6개월씩 연장되어 총 1년 6개월 사용이 가능합니다."
        },
        {
            "q": "배우자 출산휴가는 언제까지, 몇 번이나 나눠 쓸 수 있나요?",
            "a": "출산일로부터 120일 이내에 사용해야 하며, <b>총 3회까지 분할(4번 사용)</b> 가능하도록 확대되었습니다."
        },
        {
            "q": "사후지급금 제도가 정말 폐지되었나요?",
            "a": "네, 2025년 1월 1일 이후 육아휴직 기간에 대해서는 복직 후 지급되던 25%를 <b>휴직 중에 전액 합산하여 지급</b>합니다."
        }
    ]

    for item in faqs:
        st.markdown(f"""
            <div class="faq-card">
                <span class="faq-q">Q. {item['q']}</span>
                <span class="faq-a">A. {item['a']}</span>
            </div>
        """, unsafe_allow_html=True)

with col_right:
    # --- AI 상담 섹션 ---
    st.markdown('<p class="section-title">🤖 실시간 노무 상담</p>', unsafe_allow_html=True)
    
    with st.container(border=True, height=650):
        st.info("개정 법령에 대해 구체적인 계산이나 사례가 궁금하시면 아래에 입력해 주세요.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "너는 Kcim 경영관리본부의 전문 노무사야. 2025년 개정된 육아지원법 내용을 바탕으로 상담해줘. 자녀연령 초6 확대, 급여 250만 상한, 배우자 휴가 20일 등 핵심 수치를 정확히 답변해."}
            ]

        # 대화 표시
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # 입력창
        if prompt := st.chat_input("문의 내용을 입력하세요..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("API Key를 확인해주세요.")

# 5. 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:0.8rem;'>Kcim Management Support Division | Professional Labor Guide 2025</center>", unsafe_allow_html=True)
