import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 대시보드",
    page_icon="⚖️",
    layout="wide"
)

# Kcim 브랜드 컬러
KCIM_DARK = "#193D52"
KCIM_MEDIUM = "#00A8C0"
KCIM_LIGHT = "#8CCEE7"
WHITE = "#FFFFFF"

# 2. 실무 최적화 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    .stApp {{ background-color: #F8FAFC; }}
    
    /* 헤더 */
    .header-box {{
        background: {KCIM_DARK};
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* 실무 섹션 타이틀 */
    .section-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {KCIM_DARK};
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border-left: 6px solid {KCIM_MEDIUM};
        padding-left: 15px;
    }}

    /* 응대 매뉴얼 카드 스타일 */
    .manual-card {{
        background: {WHITE};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }}
    .category-tag {{
        background: {KCIM_LIGHT};
        color: {KCIM_DARK};
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        display: inline-block;
    }}
    .manual-q {{ font-size: 1.1rem; font-weight: 700; color: {KCIM_DARK}; margin-bottom: 0.7rem; display: block; }}
    .manual-a {{ font-size: 0.95rem; color: #334155; line-height: 1.7; }}
    .point {{ color: {KCIM_MEDIUM}; font-weight: bold; }}

    /* 하단 가로형 상담창 디자인 */
    .footer-chat-container {{
        background: {KCIM_DARK};
        padding: 2.5rem;
        border-radius: 20px;
        margin-top: 4rem;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 상단 헤더
st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0;">⚖️ 2025 육아지원 실무 대응 대시보드</h1>
        <p style="opacity:0.9; margin-top:0.5rem;">Kcim 경영관리본부 전용 | 임직원 문의 즉시 응대 매뉴얼</p>
    </div>
    """, unsafe_allow_html=True)

# 4. 메인 콘텐츠: 실무진 필독 FAQ (응대 시나리오 별 배치)
st.markdown('<p class="section-title">📂 실무진 즉시 응대 FAQ (임신·육아·복직)</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    # 임신기/출산기 응대
    st.markdown(f"""
        <div class="manual-card">
            <span class="category-tag">임신·출산기</span>
            <span class="manual-q">Q. 임신 초기 직원이 근로시간 단축을 요청할 때 확인사항은?</span>
            <span class="manual-a">
                <b>임신 후 12주 이내</b> 또는 <b>32주 이후</b>(개정)인지 확인하십시오. <br>
                임금 삭감 없이 <span class="point">1일 2시간 단축</span>이 가능하며, 32주 이전이라도 고위험 임신부라면 전 기간 사용 가능함을 안내하십시오.
            </span>
        </div>
        <div class="manual-card">
            <span class="category-tag">임신·출산기</span>
            <span class="manual-q">Q. 배우자 출산휴가 신청 시 일수와 분할 사용 안내는?</span>
            <span class="manual-a">
                25.2.23. 이후부터는 <span class="point">유급 20일</span>로 확대되었습니다. <br>
                출산일로부터 120일 이내에 사용해야 하며, <span class="point">총 4회(분할 3회)</span>까지 나누어 쓸 수 있어 유연한 육아 참여가 가능함을 안내하십시오.
            </span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # 육아기/복직 응대
    st.markdown(f"""
        <div class="manual-card">
            <span class="category-tag">육아기·복직</span>
            <span class="manual-q">Q. 초등학교 4학년 자녀를 둔 직원의 단축근무가 가능한가요?</span>
            <span class="manual-a">
                <b>네, 가능합니다.</b> 2025년 개정으로 대상 자녀 연령이 <span class="point">만 12세 또는 초등 6학년 이하</span>로 확대되었습니다. <br>
                육아휴직 미사용분 포함 최대 3년까지 사용 가능함을 안내하십시오.
            </span>
        </div>
        <div class="manual-card">
            <span class="category-tag">육아기·복직</span>
            <span class="manual-q">Q. 복직 예정자가 사후지급금(25%)에 대해 문의한다면?</span>
            <span class="manual-a">
                2025년 1월 1일 이후 육아휴직 사용분부터 <span class="point">사후지급금 제도가 폐지</span>되었습니다. <br>
                이제 복직 후 6개월을 기다릴 필요 없이 휴직 중에 급여 전액(100%)을 수령하게 됨을 안내하여 경제적 불안감을 해소해주십시오.
            </span>
        </div>
    """, unsafe_allow_html=True)

# 5. 급여 체계 실무 참고 (표 형태)
with st.expander("💰 [실무참고] 2025 육아휴직 급여 지급액 기준 (상한액)", expanded=False):
    st.markdown("""
    | 기간 | 상한액 (통상임금 100~80%) | 비고 |
    | :--- | :--- | :--- |
    | **1~3개월** | **250만원** | 사후지급금 없음 |
    | **4~6개월** | **200만원** | 사후지급금 없음 |
    | **7~12개월** | **160만원** | 사후지급금 없음 |
    """)

# 6. 최하단 가로형 실시간 상담창 (디자인 변경)
st.markdown('<div class="footer-chat-container">', unsafe_allow_html=True)
st.markdown(f'<h3 style="color:white; text-align:center;">🤖 ' + "전문 노무사 실시간 자문" + '</h3>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; opacity:0.8;">위 FAQ 외에 복잡한 계산이나 법률 해석이 필요한 경우 질문해 주세요.</p>', unsafe_allow_html=True)

# 세션 메시지 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 가로형 배치를 위한 컬럼
c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    # 채팅 출력부
    chat_box = st.container(height=250)
    with chat_box:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    # 입력창
    if prompt := st.chat_input("노무사에게 상담할 내용을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "너는 Kcim 경영관리본부의 전문 노무사야. 2025년 개정된 육아지원법(자녀연령 초6, 급여 250만, 배우자 휴가 20일 등)을 바탕으로 실무진에게 법률적 근거를 제공해줘."}
                        ] + st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("API Key를 확인해 주세요.")

st.markdown('</div>', unsafe_allow_html=True)

# 7. 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:0.8rem;'>© 2025 Kcim Management Support Division | HR Legal Dashboard</center>", unsafe_allow_html=True)
