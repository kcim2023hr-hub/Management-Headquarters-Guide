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

# 2. 대시보드 전용 CSS (가로형 채팅 및 대시보드 최적화)
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    .stApp {{ background-color: #F8FAFC; }}
    
    /* 헤더 */
    .header-box {{
        background: {KCIM_DARK};
        padding: 1.5rem;
        border-radius: 12px 12px 0 0;
        color: white;
        text-align: center;
    }}
    
    /* 가로형 상담창 구역 */
    .chat-section {{
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 0 0 12px 12px;
        border: 1px solid #E2E8F0;
        border-top: none;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
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
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border-top: 4px solid {KCIM_MEDIUM};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .highlight-val {{ font-size: 1.8rem; font-weight: 800; color: {KCIM_DARK}; display: block; margin-top: 5px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. 상단 헤더 및 실시간 상담 (가로 배치)
st.markdown(f"""
    <div class="header-box">
        <h2 style="margin:0;">⚖️ 2025 육아지원제도 전문 노무 대시보드</h2>
        <p style="opacity:0.8; margin:5px 0 0 0;">Kcim 경영관리본부 | 실시간 전문 노무 상담 어시스턴트</p>
    </div>
    """, unsafe_allow_html=True)

# 실시간 상담 입력창 (타이틀 바로 아래 가로 형태)
with st.container():
    st.markdown('<div class="chat-section">', unsafe_allow_html=True)
    
    # 세션 메시지 관리
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 Kcim 경영관리본부의 전문 노무사야. 2025년 개정된 육아지원법(자녀연령 초6, 급여 250만, 배우자 휴가 20일 등)을 바탕으로 전문적이고 명확하게 상담해줘."}
        ]

    # 채팅 입력창과 최근 답변을 가로로 배치하거나 상단에 노출
    col_input, col_status = st.columns([0.7, 0.3])
    with col_input:
        prompt = st.chat_input("궁금한 제도를 입력하면 노무사가 즉시 답변해 드립니다 (예: 육아휴직 급여 소급 적용되나요?)")
    with col_status:
        st.markdown(f"<div style='padding-top:10px; color:{KCIM_MEDIUM}; font-weight:bold; text-align:right;'>● 전문 노무사 온라인</div>", unsafe_allow_html=True)

    # 채팅 내용 표시 영역
    chat_container = st.container(height=300)
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            res = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("API 연결 실패. 설정된 OpenAI API Key를 확인하세요.")

    with chat_container:
        for message in reversed(st.session_state.messages): # 최신 답변이 위로 오게 하거나 순차 표시
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# 4. 하단 대시보드 내용 (지표 + FAQ)
col_stat, col_faq = st.columns([0.3, 0.7], gap="large")

with col_stat:
    st.markdown('<p class="section-title">🚀 3대 핵심 요약</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="highlight-box"><small>육아기 단축 자녀연령</small><span class="highlight-val">초등 6학년</span></div><br>
        <div class="highlight-box"><small>육아휴직 급여상한</small><span class="highlight-val">최대 250만원</span></div><br>
        <div class="highlight-box"><small>배우자 출산휴가</small><span class="highlight-val">20일 (유급)</span></div>
    """, unsafe_allow_html=True)

with col_faq:
    st.markdown('<p class="section-title">❓ 자주 묻는 질문 (FAQ)</p>', unsafe_allow_html=True)
    
    faqs = [
        {"q": "이미 육아휴직 중인데 250만 원 급여를 받을 수 있나요?", "a": "네, 2025년 1월 1일 이후 사용한 기간에 대해서는 인상된 상한액이 적용됩니다."},
        {"q": "사후지급금 제도가 폐지되었다는데 사실인가요?", "a": "네, 2025년부터는 복직 후 지급되던 25%의 적립금 없이 휴직 기간 중 전액(100%)을 지급합니다."},
        {"q": "육아휴직 1.5년 연장 조건은 무엇인가요?", "a": "부모가 각각 육아휴직을 3개월 이상 사용한 경우에 한해 최대 1년 6개월까지 가능합니다."},
        {"q": "배우자 출산휴가는 분할이 가능한가요?", "a": "네, 출산일로부터 120일 이내에 총 3회까지 분할하여(총 4번 사용) 사용할 수 있습니다."}
    ]

    for item in faqs:
        st.markdown(f"""
            <div class="faq-card">
                <span class="faq-q">Q. {item['q']}</span>
                <span class="faq-a">A. {item['a']}</span>
            </div>
        """, unsafe_allow_html=True)

# 5. 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:0.8rem;'>Kcim Management Support Division | Professional Labor Guide 2025</center>", unsafe_allow_html=True)
