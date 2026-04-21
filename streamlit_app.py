import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 초기화
st.set_page_config(
    page_title="Kcim 육아지원 법률 대시보드",
    page_icon="⚖️",
    layout="wide"
)

# Kcim 브랜드 컬러
KCIM_DARK = "#193D52"    # 신뢰감 있는 네이비
KCIM_MEDIUM = "#00A8C0"  # 포인트 사이언
KCIM_LIGHT = "#8CCEE7"   # 소프트 블루
WHITE = "#FFFFFF"

# 2. 고도화된 대시보드용 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    
    .stApp {{ background-color: #F0F4F8; }}
    
    /* 대시보드 헤더 */
    .header-container {{
        background: {KCIM_DARK};
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* 섹션 타이틀 */
    .section-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {KCIM_DARK};
        margin-bottom: 1rem;
        padding-left: 10px;
        border-left: 5px solid {KCIM_MEDIUM};
    }}
    
    /* 대시보드 카드 */
    .card {{
        background: {WHITE};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
    }}
    
    /* 강조 지표 */
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {KCIM_MEDIUM};
    }}
    
    /* 법령 근거 텍스트 */
    .law-source {{
        font-size: 0.8rem;
        color: #718096;
        margin-top: 0.5rem;
    }}
    
    /* 챗봇 컨테이너 조정 */
    .stChatMessage {{ background-color: white !important; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. 메인 상단 헤더
st.markdown(f"""
    <div class="header-container">
        <h1 style="margin:0;">⚖️ 2025 육아지원제도 전문 노무 대시보드</h1>
        <p style="opacity:0.8; margin-top:0.5rem;">고용노동부 최신 지침 반영 | Kcim 경영관리본부 전용</p>
    </div>
    """, unsafe_allow_html=True)

# 4. 메인 대시보드 레이아웃 (상단 지표 + 중앙 상세 + 우측 챗봇)
col_left, col_right = st.columns([0.65, 0.35], gap="large")

with col_left:
    # --- 섹션 1: 핵심 개정 지표 (Metric Cards) ---
    st.markdown('<p class="section-title">📍 실무 핵심 개정 요약</p>', unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f"""<div class="card"><p>육아기 단축 자녀연령</p><p class="metric-value">만 12세</p><p class="law-source">(기존 만 8세)</p></div>""", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""<div class="card"><p>배우자 출산휴가</p><p class="metric-value">20일</p><p class="law-source">(기존 10일 / 4회 분할)</p></div>""", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""<div class="card"><p>육아휴직 급여상한</p><p class="metric-value">250만원</p><p class="law-source">(1~3개월 기준)</p></div>""", unsafe_allow_html=True)

    # --- 섹션 2: 상세 법령 가이드 ---
    st.markdown('<p class="section-title">📑 상세 제도 가이드</p>', unsafe_allow_html=True)
    with st.expander("🤰 임신기 및 출산기 (25.02.23 시행)", expanded=True):
        st.markdown("""
        - **임신기 근로시간 단축:** 기존 '36주 이후'에서 **'32주 이후'**로 확대
        - **난임치료휴가:** 연간 6일(유급 2일) 확대, 중소기업 급여지원 신설
        - **미숙아 출산:** 출산전후휴가 **100일**로 확대 (기존 90일)
        """)
    
    with st.expander("🤱 육아기 및 육아휴직 (25.01.01 / 2.23 시행)", expanded=True):
        st.markdown("""
        - **육아휴직 기간:** 부모 모두 3개월 이상 사용 시 **최대 1.5년**으로 연장
        - **육아기 단축 기간:** 휴직 미사용분 포함 **최대 3년** 가능
        - **사후지급금 폐지:** 25년 1월 이후 사용분부터 휴직 중 **100% 지급**
        """)

    # --- 섹션 3: 급여 체계 테이블 ---
    st.markdown('<p class="section-title">💰 2025 육아휴직 급여 체계</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card">
            <table style="width:100%; text-align:center; border-collapse:collapse;">
                <tr style="background:{KCIM_DARK}; color:white;">
                    <th style="padding:10px;">구분</th><th style="padding:10px;">상한액</th><th style="padding:10px;">비율</th>
                </tr>
                <tr style="border-bottom:1px solid #eee;"><td>1~3개월</td><td><b>250만원</b></td><td>통상임금 100%</td></tr>
                <tr style="border-bottom:1px solid #eee;"><td>4~6개월</td><td><b>200만원</b></td><td>통상임금 100%</td></tr>
                <tr><td>7~12개월</td><td><b>160만원</b></td><td>통상임금 80%</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # --- 섹션 4: AI 전문 노무 상담실 ---
    st.markdown('<p class="section-title">🤖 AI 전문 노무 상담</p>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.caption("고용노동부 최신 지침을 기반으로 노무사가 답변해 드립니다.")
        
        # 세션 메시지 관리
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "너는 Kcim 경영관리본부의 전문 노무사야. 2025년 개정된 육아지원법(자녀연령 만12세, 급여상한 250만, 사후지급금 폐지 등)을 완벽히 숙지하고 있어. 법률적 근거를 바탕으로 전문적이고 친절하게 답변해줘."}
            ]

        # 대화 내용 표시 (높이 제한을 위해 scrollable 공간 권장하나 기본 기능 활용)
        chat_placeholder = st.container(height=500)
        with chat_placeholder:
            for message in st.session_state.messages:
                if message["role"] != "system":
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

        # 채팅 입력
        if prompt := st.chat_input("노무사에게 문의하기"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_placeholder:
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    try:
                        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=st.session_state.messages
                        )
                        full_response = response.choices[0].message.content
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    except:
                        st.error("API 연결 실패. Settings에서 API Key를 확인하세요.")

# 5. 하단 푸터
st.divider()
st.markdown(f"<center style='color:gray; font-size:0.8rem;'>© 2025 Kcim Management Support Division. Professional Labor Relations Guide.</center>", unsafe_allow_html=True)
