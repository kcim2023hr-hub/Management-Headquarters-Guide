import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 대응 시스템",
    page_icon="⚖️",
    layout="wide"
)

# [Kcim 브랜드 컬러 팔레트]
KCIM_DARK = "#193D52"    # 메인 네이비 (사이드바, 헤더)
KCIM_MEDIUM = "#00A8C0"  # 포인트 사이언 (하이라이트)
KCIM_LIGHT = "#8CCEE7"   # 라이트 블루 (태그, 강조 배경)

# 2. 실무 가독성 최적화 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    .stApp {{ background-color: #F8FAFC; }}
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {{ background-color: {KCIM_DARK}; color: white; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* 헤더 배너 */
    .header-banner {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
        padding: 2.5rem;
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
        border-left: 6px solid {KCIM_MEDIUM};
        padding-left: 15px;
        margin-bottom: 1.5rem;
    }}

    /* 실무 응대 카드 */
    .manual-card {{
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }}
    .category-tag {{
        background: {KCIM_LIGHT};
        color: {KCIM_DARK} !important;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 800;
        margin-bottom: 1rem;
        display: inline-block;
    }}
    .manual-q {{ font-size: 1.15rem; font-weight: 700; color: {KCIM_DARK}; margin-bottom: 0.8rem; display: block; }}
    .manual-a {{ font-size: 1rem; color: #334155; line-height: 1.8; }}
    .point {{ color: {KCIM_MEDIUM}; font-weight: 800; text-decoration: underline; }}

    /* 하단 검색창(상담창) 영역 */
    .search-area {{
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid {KCIM_DARK};
        margin-top: 4rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (실무 카테고리 네비게이션)
with st.sidebar:
    st.markdown("## 📂 실무 응대 카테고리")
    st.caption("확인할 제도를 선택하세요")
    category = st.radio(
        "",
        ["전체 보기", "🤰 임신기 단축근무", "👨‍🍼 배우자 출산휴가", "🤱 육아휴직 및 단축", "💰 급여 및 복직 가이드"]
    )
    st.divider()
    st.markdown("### 📞 실무진 헬프데스크")
    st.write("• 인사지원팀: 내선 102")
    st.write("• IT 시스템: 내선 105")

# 4. 메인 화면 헤더
st.markdown(f"""
    <div class="header-banner">
        <h1 style="margin:0;">⚖️ 2025 육아지원 실무 대응 대시보드</h1>
        <p style="opacity:0.9; margin-top:0.8rem; font-size:1.1rem;">Kcim 경영관리본부 전용 | {category} 실전 응대 매뉴얼</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 콘텐츠: 카테고리별 즉시 응대 FAQ
st.markdown(f'<p class="section-title">📍 {category} 주요 지침</p>', unsafe_allow_html=True)

# FAQ 데이터 정의 (고용노동부 및 사내 주의사항 반영)
faq_pool = [
    {
        "cat": "🤰 임신기 단축근무", 
        "q": "임신 초기 직원이 단축근무를 요청할 때 필수 확인사항은?", 
        "a": "임신 후 <span class='point'>12주 이내</span> 또는 <span class='point'>32주 이후</span>인지 확인하십시오. 임금 삭감 없이 하루 2시간 단축이 가능하며, 고위험 임신부는 전 기간 사용 가능함을 안내해야 합니다."
    },
    {
        "cat": "👨‍🍼 배우자 출산휴가", 
        "q": "배우자 출산휴가 기간과 분할 사용에 대해 묻는다면?", 
        "a": "25.2.23. 이후 <span class='point'>유급 20일</span>로 확대되었습니다. 출산일로부터 120일 내에 사용 완료해야 하며, <span class='point'>총 4회(분할 3회)</span>까지 나누어 쓸 수 있어 유연한 육아 참여가 가능합니다."
    },
    {
        "cat": "🤱 육아휴직 및 단축", 
        "q": "초등 고학년 자녀를 둔 직원의 단축근무가 가능한가요?", 
        "a": "<b>네, 가능합니다.</b> 대상 자녀 연령이 <span class='point'>만 12세 또는 초등 6학년 이하</span>로 확대되었습니다. 육아휴직 미사용분 포함 시 최대 3년까지 사용 가능함을 안내하십시오."
    },
    {
        "cat": "💰 급여 및 복직 가이드", 
        "q": "복직 예정자가 사후지급금(25%) 수령 시점을 문의한다면?", 
        "a": "2025년 1월 1일 이후 사용분부터 <span class='point'>사후지급금 제도가 폐지</span>되었습니다. 이제 복직 후 6개월 대기 없이 휴직 중에 급여 100%를 즉시 수령하게 됨을 안내하여 경제적 안정을 강조하십시오."
    }
]

# 필터링 로직
display_data = faq_pool if category == "전체 보기" else [d for d in faq_pool if d['cat'] == category]

col1, col2 = st.columns(2)
for i, item in enumerate(display_data):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
            <div class="manual-card">
                <span class="category-tag">{item['cat']}</span>
                <span class="manual-q">Q. {item['q']}</span>
                <p class="manual-a">A. {item['a']}</p>
            </div>
        """, unsafe_allow_html=True)

# 6. 최하단 통합 검색 및 AI 상담창
st.markdown('<div class="search-area">', unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:{KCIM_DARK};'>🤖 전문 노무사 실시간 자문 (검색)</h3>", unsafe_allow_html=True)
st.caption("위 매뉴얼 외에 상세한 법률 해석이나 복잡한 급여 계산이 필요한 경우 아래에 입력하세요.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 이력 컨테이너 (가독성을 위해 높이 제한)
chat_placeholder = st.container(height=250)
with chat_placeholder:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 가로형 검색바 스타일의 채팅 입력
if prompt := st.chat_input("노무사에게 상세 내용을 문의하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "너는 Kcim 전문 노무사야. 2025년 육아지원법 개정안(초6 자녀연령, 급여 250만 상한 등)을 바탕으로 경영관리본부 실무자에게 정확한 법률 조언을 제공해."}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API 연동 상태를 확인해 주세요.")

st.markdown('</div>', unsafe_allow_html=True)

# 7. 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:0.8rem;'>© 2025 Kcim Management Support Division | HR Practical Dashboard</center>", unsafe_allow_html=True)
