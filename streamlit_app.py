import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(
    page_title="Kcim 출산·육아 여정 가이드",
    page_icon="👶",
    layout="wide"
)

# ══════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --navy:   #193D52;
  --cyan:   #00A8C0;
  --red:    #FF4B6B;
  --bg:     #EEF2F6;
  --card:   #FFFFFF;
  --border: #D8E2EC;
  --text:   #1E2D3D;
  --muted:  #64788A;

  --s1: #4FACCC;   /* 임신 확인 */
  --s2: #37B89A;   /* 임신기 단축 */
  --s3: #F5A623;   /* 정기건강진단 */
  --s4: #9B59B6;   /* 연차 소진 */
  --s5: #E8556D;   /* 출산휴가 */
  --s6: #2980B9;   /* 육아휴직 */
  --s7: #27AE60;   /* 복직·단축근무 */
}

* { font-family: 'Pretendard', sans-serif !important; box-sizing: border-box; }

.stApp { background: var(--bg) !important; }

/* 사이드바 */
[data-testid="stSidebar"] {
    background: var(--navy) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.2rem; }
[data-testid="stSidebar"] * { color: #E2EAF0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.1) !important; margin: 1rem 0; }

/* 메인 패딩 */
.block-container {
    padding: 2rem 2.5rem 5rem 2.5rem !important;
    max-width: 980px !important;
}

/* ── 헤더 ── */
.page-header {
    background: linear-gradient(130deg, #193D52 0%, #1a5a78 55%, #0e7fa0 100%);
    border-radius: 20px;
    padding: 2.2rem 2.6rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.4rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; right: -30px; top: -30px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(0,168,192,.15);
    pointer-events: none;
}
.ph-icon { font-size: 2.6rem; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(0,0,0,.3)); }
.ph-title { margin: 0 0 4px; font-size: 1.6rem; font-weight: 800; color: #fff; line-height: 1.2; }
.ph-sub   { margin: 0; font-size: 0.88rem; color: rgba(255,255,255,.68); }

/* ── 진행 바 ── */
.progress-bar-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    position: relative;
    padding: 0 4px;
}
.progress-bar-wrap::before {
    content: '';
    position: absolute;
    left: 28px; right: 28px; top: 22px;
    height: 3px;
    background: var(--border);
    z-index: 0;
}
.pb-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    z-index: 1;
    cursor: pointer;
    min-width: 60px;
}
.pb-circle {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    font-weight: 800;
    border: 3px solid var(--border);
    background: white;
    color: var(--muted);
    transition: all .25s;
    box-shadow: 0 2px 8px rgba(0,0,0,.07);
}
.pb-circle.active {
    border-color: var(--step-color, #00A8C0);
    background: var(--step-color, #00A8C0);
    color: white;
    box-shadow: 0 4px 16px rgba(0,168,192,.35);
    transform: scale(1.12);
}
.pb-circle.done {
    border-color: var(--step-color, #00A8C0);
    background: white;
    color: var(--step-color, #00A8C0);
}
.pb-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--muted);
    text-align: center;
    line-height: 1.3;
    white-space: nowrap;
}
.pb-label.active { color: var(--navy); font-weight: 800; }

/* ── 메인 카드 ── */
.step-card {
    background: white;
    border-radius: 20px;
    border: 1px solid var(--border);
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,.06);
    margin-bottom: 1.4rem;
}
.step-card-header {
    padding: 1.4rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 1px solid var(--border);
}
.step-num {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 800;
    color: white; flex-shrink: 0;
}
.step-card-title { margin: 0; font-size: 1.15rem; font-weight: 800; color: var(--navy); }
.step-card-period { margin: 2px 0 0; font-size: 0.8rem; color: var(--muted); font-weight: 500; }
.step-card-body { padding: 1.6rem 1.8rem; }

/* ── 섹션 내부 ── */
.inner-section { margin-bottom: 1.4rem; }
.inner-section:last-child { margin-bottom: 0; }
.inner-title {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.82rem; font-weight: 800;
    letter-spacing: .6px; text-transform: uppercase;
    color: var(--muted); margin-bottom: .7rem;
}
.inner-title::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

/* 체크리스트 */
.cl-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 7px 0;
    font-size: 0.9rem; color: var(--text); line-height: 1.6;
    border-bottom: 1px solid #F0F4F8;
}
.cl-item:last-child { border-bottom: none; }
.cl-dot {
    width: 7px; height: 7px; border-radius: 50%;
    flex-shrink: 0; margin-top: 7px;
}
.cl-warn { color: var(--red); font-weight: 700; }

/* 포인트 박스 */
.point-box {
    background: #F0F8FF;
    border-radius: 12px;
    border-left: 4px solid var(--cyan);
    padding: .9rem 1.1rem;
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.75;
    margin-bottom: .7rem;
}
.point-box:last-child { margin-bottom: 0; }
.hl { font-weight: 700; }

/* 구분 뱃지 (단태아/다태아) */
.twin-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: .7rem; }
.twin-card {
    border-radius: 12px; padding: .9rem 1rem;
    border: 1px solid var(--border);
    text-align: center;
}
.twin-card .tc-label { font-size: 0.75rem; font-weight: 700; color: var(--muted); margin-bottom: 4px; }
.twin-card .tc-days { font-size: 1.5rem; font-weight: 900; line-height: 1; }
.twin-card .tc-note { font-size: 0.72rem; color: var(--muted); margin-top: 4px; }

/* 태그 pill */
.pill {
    display: inline-block;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 700;
    margin-right: 5px; margin-bottom: 3px;
}

/* 네비 버튼 */
.nav-row {
    display: flex; gap: 12px; margin-top: 1.2rem;
    justify-content: space-between;
}

/* Streamlit 버튼 */
.stButton > button {
    background: linear-gradient(135deg, var(--navy), #1e5470);
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Pretendard', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px 22px !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .85 !important; }

/* 채팅 */
[data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 데이터 정의
# ══════════════════════════════════════════════════════
STEPS = [
    {
        "id": 1, "color": "#4FACCC", "icon": "🤰", "emoji": "1",
        "title": "임신 확인 & 신고",
        "period": "임신 확인 즉시",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("임신 사실 구두/서면 확인 후 축하 인사 전달", False),
                    ("임신기 근로시간 단축 신청 안내 (즉시 가능)", False),
                    ("임산부 보호 규정 안내 (야근·위험업무 제한)", False),
                    ("인사시스템 '임신' 상태 등록", False),
                ],
                "type": "checklist"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("임신을 이유로 한 업무 배제·불이익 처우 금지 (법 위반)", True),
                    ("임신 사실 무단 공개 금지 — 당사자 동의 필요", True),
                ],
                "type": "warn"
            },
            {
                "title": "💡 안내 포인트",
                "content": [
                    "임신기 근로시간 단축은 <span class='hl'>임신 확인 즉시</span> 신청 가능합니다. 신청서 제출 전에도 구두 협의로 먼저 시작할 수 있습니다.",
                ],
                "type": "point"
            }
        ]
    },
    {
        "id": 2, "color": "#37B89A", "icon": "⏰", "emoji": "2",
        "title": "임신기 근로시간 단축",
        "period": "12주 이내 · 32주 이후 (하루 2시간)",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("임신기/육아기 근로시간 단축 신청서 접수", False),
                    ("12주 이내 또는 32주 이후 해당 여부 확인", False),
                    ("결재라인 상신 처리 (팀장 → HR → 완료)", False),
                    ("급여 변동 없음 확인 (임금 삭감 불가)", False),
                    ("단축 시간대 팀 내 공유 (업무 공백 조율)", False),
                ],
                "type": "checklist"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("13주~31주 구간은 단축 대상 아님 — 정기건강진단 시간만 허용", True),
                    ("단축 거부 또는 임금 삭감 시 500만 원 이하 과태료", True),
                ],
                "type": "warn"
            },
            {
                "title": "💡 안내 포인트",
                "content": [
                    "<span class='hl'>12주 이내</span>: 하루 2시간 단축, 급여 100% 유지",
                    "<span class='hl'>32주 이후</span>: 하루 2시간 단축, 급여 100% 유지 (2025년 법 개정 반영)",
                ],
                "type": "point"
            },
            {
                "title": "📎 관련 서식",
                "content": ["임신기/육아기 근로시간 단축 신청서 (Kcim 양식)"],
                "type": "form"
            }
        ]
    },
    {
        "id": 3, "color": "#F5A623", "icon": "🏥", "emoji": "3",
        "title": "임산부 정기건강진단",
        "period": "임신 주수별 (임신 기간 전반)",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("임산부 정기건강진단 신청서 접수 (주수 기재 확인)", False),
                    ("검진 시간 허용 (유급 처리)", False),
                    ("검진 예약 확인서 및 진료 확인서 사후 수령", False),
                ],
                "type": "checklist"
            },
            {
                "title": "📅 주수별 허용 시간",
                "schedule": [
                    ("임신 28주까지", "2시간", "#4FACCC"),
                    ("임신 29~36주", "4시간", "#F5A623"),
                    ("임신 37주 이후", "4시간", "#E8556D"),
                ],
                "type": "schedule"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("검진 시간은 근로시간으로 인정 — 무급 처리 불가", True),
                    ("신청서 없이 구두 처리 시 추후 분쟁 소지 있음", True),
                ],
                "type": "warn"
            },
            {
                "title": "📎 관련 서식",
                "content": ["임산부 정기건강진단 신청서 (Kcim 양식)"],
                "type": "form"
            }
        ]
    },
    {
        "id": 4, "color": "#9B59B6", "icon": "📅", "emoji": "4",
        "title": "잔여 연차 선 소진",
        "period": "출산휴가 시작 전",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("당해 연도 잔여 연차 일수 확인", False),
                    ("차수 연차(다음 해 발생분) 선사용 여부 협의", False),
                    ("연차 소진 후 출산휴가 시작일 확정", False),
                    ("연차-출산휴가-육아휴직 연속 일정표 작성", False),
                ],
                "type": "checklist"
            },
            {
                "title": "💡 안내 포인트",
                "content": [
                    "잔여 연차를 출산휴가 <span class='hl'>직전에 소진</span>하면 실질적인 유급 휴가 기간이 늘어납니다.",
                    "차수 연차(익년도 발생 예정분) <span class='hl'>선사용 가능 여부</span>는 취업규칙 확인 후 진행하세요.",
                ],
                "type": "point"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("연차 강제 소진 지시 불가 — 직원 자발적 신청이어야 함", True),
                    ("출산휴가 시작일과 연차 종료일이 중복되지 않도록 주의", True),
                ],
                "type": "warn"
            }
        ]
    },
    {
        "id": 5, "color": "#E8556D", "icon": "🍼", "emoji": "5",
        "title": "출산휴가",
        "period": "단태아 90일 · 다태아 120일",
        "sections": [
            {
                "title": "⏱ 휴가 기간",
                "type": "twin",
                "twins": [
                    {"label": "단태아 (1명)", "days": "90일", "color": "#E8556D", "note": "출산 후 최소 45일 의무"},
                    {"label": "다태아 (쌍둥이↑)", "days": "120일", "color": "#9B59B6", "note": "출산 후 최소 45일 의무"},
                ]
            },
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("출산휴가 신청서 + 의사진단서(예정일) 접수", False),
                    ("결재라인 처리 (HR팀 승인 고정)", False),
                    ("급여팀 통상임금 100% 처리 (최초 60일)", False),
                    ("고용보험 출산전후휴가급여 신청 (이후 30일)", False),
                    ("대체인력 필요 시 '대체인력지원금' 신청 검토", False),
                    ("실제 출산일과 신청일 상이 시 서류 사후 정정", False),
                ],
                "type": "checklist"
            },
            {
                "title": "💰 급여 처리",
                "content": [
                    "최초 <span class='hl'>60일</span>: 회사 부담 — 통상임금 100%",
                    "이후 <span class='hl'>30일(다태아 60일)</span>: 고용보험 부담 — 상한액 적용",
                ],
                "type": "point"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("출산 후 최소 45일 이상 반드시 사용 (법 위반 시 제재)", True),
                    ("출산예정일 변경 시 신청서 수정 및 결재 재승인 필요", True),
                ],
                "type": "warn"
            }
        ]
    },
    {
        "id": 6, "color": "#2980B9", "icon": "🤱", "emoji": "6",
        "title": "육아휴직",
        "period": "최대 1년 (부모 각각)",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("육아휴직 신청서 + 가족관계증명서 접수 (시작 30일 전)", False),
                    ("결재 처리 후 급여 중지 / 4대보험 변동 신고", False),
                    ("고용보험 육아휴직급여 신청 대행 여부 안내", False),
                    ("대체인력 투입 여부 확인 및 인수인계 일정 수립", False),
                    ("복직 예정일 1개월 전 사전 안내 발송", False),
                    ("복직 시 동일·동등 직위 보장 확인", False),
                ],
                "type": "checklist"
            },
            {
                "title": "💰 급여 (2025년 기준)",
                "content": [
                    "첫 <span class='hl'>3개월</span>: 통상임금의 80% (상한 <span class='hl'>월 250만 원</span>)",
                    "이후 <span class='hl'>9개월</span>: 통상임금의 50% (상한 월 120만 원)",
                    "사후지급금 제도 폐지 → <span class='hl'>휴직 중 100% 지급</span>",
                ],
                "type": "point"
            },
            {
                "title": "🔄 활용 옵션",
                "content": [
                    "부부 <span class='hl'>동시 사용</span> 가능 (동일 자녀 기준)",
                    "<span class='hl'>분할 3회</span>까지 가능 (사유 명시 필요)",
                    "복직 직전 <span class='hl'>단축근무 연계</span> 운영 가능 (예외적 HR 승인 필요)",
                ],
                "type": "point"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("만 8세 이하 또는 초등학교 2학년 이하 자녀만 해당", True),
                    ("동일 자녀 부부 동시 사용은 가능하나, 동시 육아휴직급여 중복 수령 제한", True),
                ],
                "type": "warn"
            }
        ]
    },
    {
        "id": 7, "color": "#27AE60", "icon": "🏢", "emoji": "7",
        "title": "복직 & 육아기 단축근무",
        "period": "복직 후 최대 3년 (만 12세까지)",
        "sections": [
            {
                "title": "📋 HR 담당자 체크",
                "items": [
                    ("복직일 1개월 전 복직 의사 확인 및 인사발령 준비", False),
                    ("육아기 근로시간 단축 신청서 접수 (원하는 경우)", False),
                    ("단축 시간 및 업무 범위 팀 내 조율", False),
                    ("급여 단축 비례 처리 + 고용보험 단축급여 신청 안내", False),
                    ("복직자 적응 지원 프로그램 안내", False),
                ],
                "type": "checklist"
            },
            {
                "title": "⏱ 단축근무 조건",
                "content": [
                    "대상: 만 <span class='hl'>12세 이하</span> (초등학교 6학년) 자녀",
                    "기간: 최대 <span class='hl'>3년</span> (육아휴직 미사용 기간 가산 가능)",
                    "시간: 주 <span class='hl'>15~35시간</span> 범위 내 협의",
                ],
                "type": "point"
            },
            {
                "title": "⚠️ 주의사항",
                "items": [
                    ("복직 후 6개월 이내 해고 금지 (부당해고 해당)", True),
                    ("단축 거부 시 500만 원 이하 과태료 — 업무 사정상 거부 불가", True),
                    ("단축 기간 중 초과근무 강요 금지", True),
                ],
                "type": "warn"
            }
        ]
    },
]

STEP_COLORS = [s["color"] for s in STEPS]

# ══════════════════════════════════════════════════════
# 세션 초기화
# ══════════════════════════════════════════════════════
if "active_step" not in st.session_state:
    st.session_state.active_step = 0   # 0-indexed
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ══════════════════════════════════════════════════════
# 사이드바
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 👶 Kcim 육아 여정")
    st.caption("출산부터 복직까지 단계별 안내")
    st.divider()

    for i, s in enumerate(STEPS):
        label = f"{s['icon']} STEP {s['id']}  {s['title']}"
        if st.button(label, key=f"sb_{i}", use_container_width=True):
            st.session_state.active_step = i

    st.divider()
    st.markdown("**💡 실무 Tip**")
    st.info("각 단계에서 서류를 빠짐없이 챙기는 것이 나중에 분쟁을 예방합니다.")
    st.caption(f"📅 기준일: {datetime.date.today()}")
    st.caption("⚖️ 근로기준법·남녀고용평등법 2025년 기준")

# ══════════════════════════════════════════════════════
# 헤더
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <div class="ph-icon">👶</div>
    <div>
        <p class="ph-title">Kcim 출산·육아 여정 단계별 가이드</p>
        <p class="ph-sub">임신 확인부터 복직 후 단축근무까지 · 2025년 법령 최신 반영 · 경영관리본부</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 진행 바 (클릭 가능 버튼으로 구현)
# ══════════════════════════════════════════════════════
pb_cols = st.columns(len(STEPS))
for i, (col, s) in enumerate(zip(pb_cols, STEPS)):
    with col:
        active = (i == st.session_state.active_step)
        border_style = f"border: 3px solid {s['color']}; background: {s['color']}; color: white;" if active else f"border: 2px solid #D8E2EC; background: white; color: #64788A;"
        label_style  = f"color: {s['color']}; font-weight: 800;" if active else "color: #64788A;"

        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:5px;">
            <div style="width:42px;height:42px;border-radius:50%;display:flex;align-items:center;
                        justify-content:center;font-size:1rem;{border_style}
                        box-shadow:{'0 4px 14px ' + s['color'] + '55' if active else 'none'};
                        transition:all .25s;">
                {s['icon'] if active else str(s['id'])}
            </div>
            <div style="font-size:0.65rem;font-weight:{'800' if active else '500'};
                        text-align:center;line-height:1.3;{label_style}">
                {s['title'].replace(' ', '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("", key=f"pb_{i}", help=s['title'], use_container_width=True):
            st.session_state.active_step = i
            st.rerun()

st.markdown("<div style='margin-bottom:1.4rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 스텝 카드 렌더링 함수
# ══════════════════════════════════════════════════════
def render_step(step):
    c = step["color"]
    st.markdown(f"""
    <div class="step-card">
        <div class="step-card-header">
            <div class="step-num" style="background:{c}">STEP<br>{step['id']}</div>
            <div>
                <p class="step-card-title">{step['icon']} {step['title']}</p>
                <p class="step-card-period">📅 {step['period']}</p>
            </div>
        </div>
        <div class="step-card-body">
    """, unsafe_allow_html=True)

    for sec in step["sections"]:
        st.markdown(f'<div class="inner-section"><div class="inner-title">{sec["title"]}</div>', unsafe_allow_html=True)

        if sec["type"] == "checklist":
            for text, is_warn in sec["items"]:
                cls = "cl-warn" if is_warn else ""
                dot_color = "#FF4B6B" if is_warn else c
                icon = "⛔" if is_warn else "✅"
                st.markdown(f"""
                <div class="cl-item">
                    <span style="font-size:1rem;flex-shrink:0;margin-top:1px">{icon}</span>
                    <span class="{cls}">{text}</span>
                </div>""", unsafe_allow_html=True)

        elif sec["type"] == "warn":
            for text, _ in sec["items"]:
                st.markdown(f"""
                <div class="cl-item">
                    <span style="font-size:1rem;flex-shrink:0;margin-top:1px">⛔</span>
                    <span class="cl-warn">{text}</span>
                </div>""", unsafe_allow_html=True)

        elif sec["type"] == "point":
            for line in sec["content"]:
                st.markdown(f'<div class="point-box" style="border-left-color:{c}">{line}</div>', unsafe_allow_html=True)

        elif sec["type"] == "form":
            for line in sec["content"]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                    background:#F7FAFC;border-radius:8px;border:1px solid #D8E2EC;
                    font-size:0.88rem;color:#193D52;font-weight:600;">
                    📎 {line}
                </div>""", unsafe_allow_html=True)

        elif sec["type"] == "twin":
            st.markdown('<div class="twin-grid">', unsafe_allow_html=True)
            for tw in sec["twins"]:
                st.markdown(f"""
                <div class="twin-card" style="border-top:4px solid {tw['color']}">
                    <div class="tc-label">{tw['label']}</div>
                    <div class="tc-days" style="color:{tw['color']}">{tw['days']}</div>
                    <div class="tc-note">{tw['note']}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif sec["type"] == "schedule":
            for period, hours, color in sec["schedule"]:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:9px 12px;border-radius:8px;margin-bottom:6px;
                    background:#F7FAFC;border:1px solid #E2EAF0;font-size:0.88rem;">
                    <span style="color:#1E2D3D;font-weight:600">{period}</span>
                    <span style="background:{color};color:white;padding:3px 12px;
                        border-radius:20px;font-weight:800;font-size:0.85rem">{hours}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # inner-section

    st.markdown('</div></div>', unsafe_allow_html=True)  # body + card

# ══════════════════════════════════════════════════════
# 전체 보기 or 단계 보기
# ══════════════════════════════════════════════════════
view_all = st.toggle("📋 전체 단계 펼쳐보기", value=False)

if view_all:
    for step in STEPS:
        render_step(step)
else:
    render_step(STEPS[st.session_state.active_step])

    # 이전/다음 버튼
    col_prev, col_idx, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.active_step > 0:
            if st.button("← 이전 단계", use_container_width=True):
                st.session_state.active_step -= 1
                st.rerun()
    with col_idx:
        st.markdown(
            f"<div style='text-align:center;font-size:0.85rem;color:#64788A;padding-top:10px;font-weight:600'>"
            f"STEP {st.session_state.active_step + 1} / {len(STEPS)}</div>",
            unsafe_allow_html=True
        )
    with col_next:
        if st.session_state.active_step < len(STEPS) - 1:
            if st.button("다음 단계 →", use_container_width=True):
                st.session_state.active_step += 1
                st.rerun()

# ══════════════════════════════════════════════════════
# AI 챗봇
# ══════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:white;border:1px solid #D8E2EC;border-radius:16px;
    padding:1.2rem 1.6rem .6rem;box-shadow:0 2px 8px rgba(0,0,0,.04)">
    <div style="font-size:0.82rem;font-weight:800;color:#00A8C0;margin-bottom:.6rem">
        🤖 AI 노무사 상담 — 현재 단계 관련 질문을 바로 물어보세요
    </div>
""", unsafe_allow_html=True)

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

current_step_name = STEPS[st.session_state.active_step]["title"]
if prompt := st.chat_input(f"예: {current_step_name} 관련 궁금한 점을 입력하세요..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        context = f"현재 사용자가 보고 있는 단계: STEP {st.session_state.active_step + 1} — {current_step_name}"
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": (
                            f"너는 Kcim 경영관리본부 전담 노무사야. {context}. "
                            "2025년 최신 근로기준법·남녀고용평등법·고용보험법 기준으로 "
                            "실무 중심으로 간결하고 정확하게 한국어로 답변해줘."
                        )}
                    ] + st.session_state.chat_messages,
                )
            ans = res.choices[0].message.content
        st.session_state.chat_messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
    except Exception:
        with st.chat_message("assistant"):
            st.warning("💡 API 설정 후 AI 상담이 가능합니다. 위 카드의 체크리스트를 먼저 참고해 주세요.")

st.markdown("</div>", unsafe_allow_html=True)
