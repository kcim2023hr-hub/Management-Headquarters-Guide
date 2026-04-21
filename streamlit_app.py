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
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {{
        background-color: {KCIM_DARK};
        color: white;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* 헤더 */
    .header-box {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
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
        margin-bottom: 1.2rem;
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
        background: {KCIM_MEDIUM};
        color: white !important;
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
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid {KCIM_DARK};
        margin-top: 3rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성 (카테고리 선택)
with st.sidebar:
    st.image("https://www.kcim.co.kr/img/common/logo_w.png", width=150) # 예시 로고
    st.markdown("### 📂 실무 응대 카테고리")
    category = st.radio(
        "확인할 제도를 선택하세요",
        ["전체 보기", "임신기 근로시간 단축", "배우자 출산휴가", "육아기 단축/휴직", "급여 및 복직"]
    )
    st.divider()
    st.markdown("#### 📞 실무진 지원\n- 인사팀: 내선 102\n- IT지원: 내선 105")

# 4. 메인 헤더
st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0;">⚖️ 2025 육아지원 실무 대응 대시보드</h1>
        <p style="opacity:0.9; margin-top:0.5rem;">Kcim 경영관리본부 전용 | {category} 매뉴얼</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 콘텐츠 (선택된 카테고리에 따라 FAQ 출력)
st.markdown(f'<p class="section-title">📍 {category} 주요 대응 지침</p>', unsafe_allow_html=True)

def show_faq(cat, q, a):
    st.markdown(f"""
        <div class="manual-card">
            <span class="category-tag">{cat}</span>
            <span class="manual-q">Q. {q}</span>
            <span class="manual-a">{a}</span>
        </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

# 데이터 정의
faq_data = [
    {"cat": "임신기 근로시간 단축", "q": "임신 초기 직원의 단축 요청 시 확인사항은?", "a": "<b>12주 이내</b> 또는 <b>32주 이후</b>인지 확인하십시오. 임금 삭감 없이 <span class='point'>1일 2시간</span> 단축이 가능합니다."},
    {"cat": "배우자 출산휴가", "q": "배우자 출산휴가 기간과 분할 사용은?", "a": "25.2.23. 이후 <span class='point'>유급 20일</span>로 확대되었습니다. 출산일로부터 120일 내 <span class='point'>4회(분할 3회)</span> 사용 가능합니다."},
    {"cat": "육아기 단축/휴직", "q": "초등 4학년 자녀를 둔 직원의 단축근무가 가능한가요?", "a": "<b>네, 가능합니다.</b> 2025년 개정으로 대상 자녀 연령이 <span class='point'>만 12세 또는 초등 6학년 이하</span>로 확대되었습니다."},
    {"cat": "급여 및 복직", "q": "사후지급금(25%)에 대해 문의한다면?", "a": "2025년 1월 1일 사용분부터 <span class='point'>사후지급금 제도가 폐지</span>되었습니다. 휴직 중 급여 100% 수령 가능함을 안내하십시오."}
]

# 필터링 및 출력
filtered_data = faq_data if category == "전체 보기" else [d for d in faq_data if d['cat'] == category]

for i, item in enumerate(filtered_data):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        show_faq(item['cat'], item['q'], item['a'])

# 6. 최하단 디자인된 실시간 상담창 (디자인 개선)
st.markdown('<div class="footer-chat-container">', unsafe_allow_html=True)
st.markdown(f'<h3 style="color:{KCIM_DARK}; text-align:center;">🤖 전문 노무사 실시간 자문 (검색)</h3>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅창 높이 조절
chat_placeholder = st.container(height=200)
with chat_placeholder:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
                    messages=[{"role": "system", "content": "너는 Kcim 전문 노무사야. 2025년 육아지원법 개정안(초6 자녀연령, 급여 250만 상한 등)을 바탕으로 답변해줘."}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API 연결을 확인하세요.")

st.markdown('</div>', unsafe_allow_html=True)
