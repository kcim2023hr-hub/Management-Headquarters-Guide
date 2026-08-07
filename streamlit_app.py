import streamlit as st
from openai import OpenAI
import math
from datetime import date, timedelta
import pandas as pd

st.set_page_config(
    page_title="KCIM 출산·육아 응대 가이드",
    page_icon="👶",
    layout="wide",
)


# ──────────────────────────────────────────
# CSS
# ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

*, html, body, [class*="css"] {
  font-family: 'Pretendard', -apple-system, sans-serif !important;
  box-sizing: border-box;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #f0f4f8; }

/* ── 최상단 헤더 ── */
.top-header {
  background: linear-gradient(135deg, #0f2942 0%, #1a4a6e 60%, #1e6091 100%);
  padding: 0.9rem 2rem; display: flex; align-items: center;
  justify-content: space-between; box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}
.top-header-title { font-size: 1.25rem; font-weight: 800; color: #fff; letter-spacing: -0.3px; word-break: keep-all; }
.top-header-sub { font-size: 0.78rem; color: rgba(255,255,255,0.7); margin-top: 2px; word-break: keep-all; }
.badge-2025 {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white; padding: 3px 10px; border-radius: 20px;
  font-size: 0.7rem; font-weight: 700; margin-left: 10px; vertical-align: middle;
  white-space: nowrap;
}

/* ── 스텝 프로그레스 (클릭 가능한 버튼형 stepper) ── */
.st-key-stepper_wrap_box {
  background: #fff; border-bottom: 1px solid #e2e8f0;
  padding: 0.7rem 2rem;
}
.st-key-stepper_wrap_box div[data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; row-gap: 6px !important; }
.st-key-stepper_wrap_box button {
  border-radius: 20px !important; font-weight: 700 !important;
  font-size: 0.74rem !important; padding: 0.35rem 0.85rem !important;
  min-height: 2rem !important; white-space: nowrap !important;
  border: 1.5px solid #e2e8f0 !important; background: #f8fafc !important;
  color: #64748b !important; transition: all 0.15s !important;
}
.st-key-stepper_wrap_box div[class*="st-key-step_active_"] button {
  background: #3b82f6 !important; border-color: #3b82f6 !important;
  color: #fff !important; box-shadow: 0 0 0 4px rgba(59,130,246,0.18) !important;
}
.st-key-stepper_wrap_box div[class*="st-key-step_done_"] button {
  background: #ecfdf5 !important; border-color: #22c55e !important; color: #16a34a !important;
}
.st-key-stepper_wrap_box div[class*="st-key-step_todo_"] button:hover {
  border-color: #94a3b8 !important; color: #334155 !important;
}

/* ── 모바일 반응형 (640px 이하) ── */
@media (max-width: 640px) {
  .top-header { padding: 0.8rem 1rem; flex-wrap: wrap; }
  .top-header-title { font-size: 1.05rem; display: block; }
  .badge-2025 { display: inline-block; margin-left: 0; margin-top: 6px; }
  .top-header-sub { font-size: 0.7rem; }
  .st-key-stepper_wrap_box { padding: 0.6rem 0.8rem; }
  .st-key-stepper_wrap_box button { font-size: 0.68rem !important; padding: 0.3rem 0.65rem !important; min-height: 1.8rem !important; }
  .step-main-title { font-size: 1.15rem !important; }
  .step-header-card { padding: 1rem 1.1rem !important; }
  .step-header-card::after { font-size: 3.2rem !important; }
}

/* ── 왼쪽 패널 ── */
.nav-section-title {
  font-size: 0.65rem; font-weight: 700; color: #94a3b8;
  letter-spacing: 0.8px; text-transform: uppercase;
  padding: 0.3rem 0.5rem 0.2rem; margin-top: 0.5rem;
}
.law-item {
  padding: 0.4rem 0.6rem; border-radius: 6px; background: #f8fafc;
  border-left: 3px solid #e2e8f0; margin-bottom: 4px;
}
.law-item-title { font-size: 0.7rem; font-weight: 700; color: #374151; }
.law-item-desc { font-size: 0.65rem; color: #6b7280; margin-top: 1px; line-height: 1.4; }
.kpi-card {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid #bae6fd; border-radius: 8px;
  padding: 0.5rem 0.7rem; margin-bottom: 4px; text-align: center;
}
.kpi-value { font-size: 1.1rem; font-weight: 900; color: #0369a1; }
.kpi-label { font-size: 0.62rem; font-weight: 600; color: #0369a1; opacity: 0.8; }

/* ── 스텝 헤더 카드 ── */
.step-header-card {
  border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1rem;
  color: white; position: relative; overflow: hidden;
}
.step-header-card::after {
  content: attr(data-num); position: absolute; right: 1rem; top: 50%;
  transform: translateY(-50%); font-size: 5rem; font-weight: 900; opacity: 0.12; line-height: 1;
}
.step-num-badge {
  font-size: 0.72rem; font-weight: 700; background: rgba(255,255,255,0.25);
  border-radius: 20px; padding: 2px 10px; display: inline-block; margin-bottom: 5px;
}
.step-main-title { font-size: 1.4rem; font-weight: 900; letter-spacing: -0.5px; }
.step-meta { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.step-chip {
  background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3);
  border-radius: 20px; padding: 3px 10px; font-size: 0.72rem; font-weight: 600; color: white;
}

/* ── 스크립트 박스 ── */
.script-card {
  background: white; border-radius: 12px; border: 1px solid #e2e8f0;
  padding: 1rem 1.2rem; margin-bottom: 0.8rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.card-title {
  font-size: 0.8rem; font-weight: 800; color: #374151;
  margin-bottom: 0.6rem; display: flex; align-items: center; gap: 6px;
}
.script-content {
  background: #f0f9ff; border-left: 4px solid #3b82f6;
  border-radius: 0 8px 8px 0; padding: 0.8rem 1rem;
  font-size: 0.95rem; font-weight: 500; color: #1e40af; line-height: 1.7; font-style: italic;
}
.info-card {
  background: white; border-radius: 12px; border: 1px solid #e2e8f0;
  padding: 0.9rem 1rem; box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.form-chip2 {
  display: inline-flex; align-items: center; gap: 5px;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;
  padding: 4px 10px; font-size: 0.78rem; font-weight: 600; color: #334155;
  margin-bottom: 5px; width: 100%;
}
.warn-banner {
  background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px;
  padding: 0.5rem 0.8rem; font-size: 0.78rem; font-weight: 600;
  color: #dc2626; margin-top: 6px; line-height: 1.5;
}
.faq-card {
  background: white; border-radius: 12px; border: 1px solid #e2e8f0;
  padding: 0.9rem 1rem; margin-bottom: 0.8rem; box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.faq-item { padding: 0.4rem 0; border-bottom: 1px solid #f1f5f9; }
.faq-item:last-child { border-bottom: none; }
.faq-q { font-size: 0.8rem; font-weight: 700; color: #1d4ed8; margin-bottom: 2px; }
.faq-a { font-size: 0.78rem; color: #475569; line-height: 1.5; }

/* ── 챗봇 ── */
.chat-header {
  padding: 0.9rem 1rem; border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #1e3a5f, #1a5276);
  display: flex; align-items: center; gap: 10px;
}
.chat-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; flex-shrink: 0;
}
.chat-header-text .chat-name { font-size: 0.9rem; font-weight: 800; color: white; }
.chat-header-text .chat-desc { font-size: 0.65rem; color: rgba(255,255,255,0.65); }
.welcome-msg {
  background: linear-gradient(135deg, #eff6ff, #f0f9ff);
  border: 1px solid #bfdbfe; border-radius: 10px;
  padding: 0.8rem; font-size: 0.8rem; color: #1e40af; line-height: 1.6; text-align: center;
}

/* ── 계산기 ── */
.calc-header-card {
  background: linear-gradient(135deg, #1e3a5f, #1a5276);
  border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; color: white;
}
.period-bar {
  border-radius: 8px; padding: 0.65rem 1rem; margin-bottom: 6px;
  display: flex; justify-content: space-between; align-items: center;
}
.period-ok { background: #dcfce7; border: 1.5px solid #86efac; }
.period-na { background: #f1f5f9; border: 1.5px solid #cbd5e1; }
.period-label { font-size: 0.82rem; font-weight: 700; }
.period-date { font-size: 0.76rem; color: #475569; margin-top: 1px; }
.period-days { font-size: 1rem; font-weight: 800; }
.calc-note-box {
  background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px;
  padding: 0.75rem 1rem; margin-top: 0.8rem;
  font-size: 0.8rem; color: #0369a1; line-height: 1.8;
}
.result-metric {
  background: white; border: 1px solid #e2e8f0; border-radius: 10px;
  padding: 0.8rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.result-metric-val { font-size: 1.3rem; font-weight: 900; color: #0f172a; }
.result-metric-label { font-size: 0.68rem; font-weight: 600; color: #64748b; margin-top: 2px; }

/* ── Streamlit 요소 커스텀 ── */
div[data-testid="stChatInput"] {
  padding: 0.5rem 0.7rem 0.8rem !important;
  background: #f8faff !important;
  border-top: 2px solid #dbeafe !important;
  margin-top: 0 !important;
}
div[data-testid="stChatInput"] > div {
  border: 2px solid #3b82f6 !important;
  border-radius: 12px !important;
  background: white !important;
  box-shadow: 0 0 0 4px rgba(59,130,246,0.08) !important;
}
div[data-testid="stChatInput"] textarea { color: #1f2937 !important; font-size: 0.88rem !important; }
div[data-testid="stChatInput"] textarea::placeholder { color: #94a3b8 !important; font-size: 0.85rem !important; }
div[data-testid="stChatInput"] button {
  background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
  border-radius: 8px !important; color: white !important;
}
section[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* ── 플로팅 액션 버튼(FAB): 메뉴 토글 · AI 챗봇 ──
   화면 가장자리에 고정된 원형 버튼으로, 레이아웃 흐름(block-container)에
   전혀 영향을 주지 않아 본문이 한쪽으로 쏠리는 문제가 발생하지 않음.
   좌/우 하단에 분리 배치하여 PC·모바일 모두 엄지로 닿기 쉬운 위치 확보. */
.block-container { padding-bottom: 92px !important; }

.st-key-menu_toggle_btn, .st-key-chat_toggle_btn {
  position: fixed !important;
  bottom: max(20px, env(safe-area-inset-bottom)) !important;
  z-index: 999 !important;
  width: auto !important;
}
.st-key-menu_toggle_btn { left: 18px !important; }
.st-key-chat_toggle_btn { right: 18px !important; }

.st-key-menu_toggle_btn button, .st-key-chat_toggle_btn button {
  width: 54px !important; height: 54px !important;
  min-width: 54px !important; min-height: 54px !important;
  border-radius: 50% !important; border: none !important;
  padding: 0 !important; margin: 0 !important;
  font-size: 1.3rem !important; font-weight: 800 !important;
  line-height: 1 !important; color: white !important;
  display: flex !important; align-items: center !important; justify-content: center !important;
  box-shadow: 0 4px 14px rgba(0,0,0,0.28) !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
}
.st-key-menu_toggle_btn button {
  background: linear-gradient(135deg, #1a4a6e, #1e6091) !important;
}
.st-key-chat_toggle_btn button {
  background: linear-gradient(135deg, #f093fb, #f5576c) !important;
}
.st-key-menu_toggle_btn button:hover, .st-key-chat_toggle_btn button:hover {
  transform: translateY(-2px) scale(1.05) !important;
  box-shadow: 0 6px 18px rgba(0,0,0,0.32) !important;
}
.st-key-menu_toggle_btn button:active, .st-key-chat_toggle_btn button:active {
  transform: scale(0.94) !important;
}
@media (max-width: 640px) {
  .block-container { padding-bottom: 84px !important; }
  .st-key-menu_toggle_btn button, .st-key-chat_toggle_btn button {
    width: 48px !important; height: 48px !important;
    min-width: 48px !important; min-height: 48px !important;
    font-size: 1.15rem !important;
  }
}

/* ── 챗봇 다이얼로그 내부 ── */
div[data-testid="stDialog"] .chat-desc-caption { margin-top: -0.6rem; }

.stChatMessage { background: transparent !important; }
.stButton button { border-radius: 8px !important; font-weight: 700 !important; transition: all 0.15s !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# 데이터 정의 (2026-08 기준, 노무법인 인화 매뉴얼 2026.03 1판 참고)
# ──────────────────────────────────────────
STEPS = [
    {
        "id": 0, "short": "임신 확인", "title": "임신 확인 및 초기 응대",
        "color": "#3b82f6", "grad": "linear-gradient(135deg, #2563eb, #3b82f6)",
        "target": "임신 확인 직원", "next": "단축 조율",
        "guide": '"축하드립니다! 임신 소식은 본인이 원하는 범위 내에서만 공유될 예정이니 안심하세요. 먼저 단축근무 제도부터 안내해 드릴까요?"',
        "check": ["공유 희망 범위 확인 및 비밀유지 약속", "단축근무 신청 방법 및 서류 안내", "플로우 내 신청서 경로 설명"],
        "forms": ["임신확인서", "KCIM_임신·육아기 관련 지원 신청서"],
        "warn": ["비밀유지 의무 준수 필수 (무단 공유 금지)", "임신 이유로 불이익 주는 행위 금지"],
        "laws": [
            {"name": "근로기준법 제74조", "desc": "임신기 근로시간 단축 및 보호"},
            {"name": "남녀고용평등법 제14조", "desc": "직장 내 모성보호 불이익 금지"},
        ],
        "faq": [
            {"q": "직원이 임신 사실을 비밀로 해달라고 하면?", "a": "당연히 비밀 유지됩니다. 본인 동의 없이 어떠한 방식으로도 공유하지 않음을 먼저 안심시켜 주세요."},
            {"q": "임신 초기라 아직 단축 신청 안 하려 한다면?", "a": "괜찮습니다. 제도 존재만 안내하고, 필요할 때 언제든 신청 가능하다고 전달해주세요."},
            {"q": "임신 사실을 업무 배치에 반영해도 되나요?", "a": "본인의 동의와 요청이 있을 때만 가능합니다. 일방적인 배치 변경은 불이익으로 간주될 수 있습니다."},
        ],
        "kpi": [{"val": "즉시", "label": "비밀유지"}],
    },
    {
        "id": 1, "short": "임신기 단축", "title": "임신기 근로시간 단축 및 근무조정",
        "color": "#10b981", "grad": "linear-gradient(135deg, #059669, #10b981)",
        "target": "단축 희망 직원", "next": "검진 안내",
        "guide": '"임신 12주 이내(84일까지) 또는 32주 이후(246일 이후)에 하루 2시간 단축 근무가 가능합니다. 급여는 전액 유지되고, 출퇴근 시간 조정이나 쉬운 업무 전환도 함께 신청하실 수 있어요."',
        "check": ["임신 12주 이내 또는 32주 이후 여부 확인 (고위험 임산부는 전 기간)", "단축 개시 3일 전까지 신청서 접수", "출퇴근시간 변경·쉬운 근로 전환 희망 여부 확인"],
        "forms": ["KCIM_임신·육아기 관련 지원 신청서", "출퇴근시간 변경 신청서(해당 시)", "쉬운 근로 전환 신청서(해당 시)"],
        "warn": ["2025 개정: 32주 이후로 확대 적용", "고위험 임산부는 전 기간 단축 가능(진단서 필요)", "단축 개시 3일 전 신청 원칙 — 늦으면 접수일+3일부터 적용"],
        "laws": [
            {"name": "근로기준법 제74조의2", "desc": "임신기 근로시간 단축 (12주 이내/32주 이후, 1일 최대 2시간·6시간까지)"},
            {"name": "모자보건법 제10조", "desc": "고위험 임산부 추가 보호"},
        ],
        "faq": [
            {"q": "단축 중 급여는 어떻게 되나요?", "a": "단축 근무 기간에도 통상 급여 전액이 지급됩니다. 다만 포괄임금제로 연장근로수당이 포함돼 있었다면, 임신 중 연장근로가 금지되므로 해당 수당은 지급하지 않을 수 있습니다."},
            {"q": "12주~32주 사이에는 단축이 불가한가요?", "a": "일반적으로는 불가하나, 고위험 임산부 진단을 받은 경우 전 기간 가능합니다."},
            {"q": "단축 근무 기간의 연차휴가는 어떻게 계산되나요?", "a": "최근 행정해석에 따라 임신기 단축 근무자는 '단시간 근로자'가 아니라 '정상 근무'로 간주됩니다. 따라서 단축 전과 동일한 방식으로 연차가 발생·사용됩니다."},
        ],
        "kpi": [{"val": "2시간", "label": "일 단축(6시간까지)"}],
    },
    {
        "id": 2, "short": "건강진단", "title": "정기 건강진단 (태아검진)",
        "color": "#f59e0b", "grad": "linear-gradient(135deg, #d97706, #f59e0b)",
        "target": "검진 대상자", "next": "연차 안내",
        "guide": '"검진 시간은 이동·대기·진료시간을 모두 포함해 사실상 유급으로 보장됩니다. 신청서만 작성해 주시면 팀장님께 자동 공유됩니다."',
        "check": ["검진 주기별 허용 시간 확인 및 부여", "유급 인정 기준 및 증빙 방법 안내", "플로우 내 신청 경로 안내"],
        "forms": ["KCIM_임신·육아기 관련 지원 신청서"],
        "warn": ["사전 예약 문자 및 진료 영수증 등 증빙 필요", "검진 사용으로 인한 불이익 절대 금지", "상시 근로자 5인 미만 사업장은 법적 의무는 아님 (KCIM은 해당 없음)"],
        "laws": [
            {"name": "근로기준법 제74조의2 제3항 / 모자보건법 제10조", "desc": "정기 태아검진 시간 부여 (28주까지 4주마다, 29~36주 2주마다, 37주 이후 매주)"},
        ],
        "faq": [
            {"q": "검진 주기마다 몇 시간이나 주어지나요?", "a": "임신 28주까지는 4주에 1회, 29~36주는 2주에 1회, 37주 이후는 매주 1회 기준으로 이동·대기·진료 시간 전체가 부여됩니다."},
            {"q": "증빙을 잃어버렸다면?", "a": "병원에서 재발급이 가능합니다. 예약 확인 문자도 임시 증빙으로 활용 가능하나 원본 제출을 권장합니다."},
            {"q": "검진 결과를 회사에 제출해야 하나요?", "a": "아니요. 검진 사실 증빙(영수증, 예약문자)만 필요하며 검진 결과 자체는 제출 의무가 없습니다."},
        ],
        "kpi": [{"val": "유급", "label": "검진 시간(사실상)"}],
    },
    {
        "id": 3, "short": "연차 정리", "title": "연차 정리 및 인수인계",
        "color": "#8b5cf6", "grad": "linear-gradient(135deg, #7c3aed, #8b5cf6)",
        "target": "휴가 예정자", "next": "출산/배우자 휴가",
        "guide": '"출산휴가 전 남은 연차를 사용해 조금 더 일찍 쉬실 수 있어요. 인수인계 시점만 알려주시면 제가 도와드릴게요."',
        "check": ["잔여 연차 일수 계산 및 안내", "출산휴가 시작 예정일 확정", "인수인계 항목 리스트 작성 지원"],
        "forms": ["어울지기 내 신청"],
        "warn": ["연차 강제 소진 지시 금지 (자율 사용 원칙)", "직원의 자율권 존중"],
        "laws": [
            {"name": "근로기준법 제60조", "desc": "연차 유급휴가 자율 사용 원칙"},
        ],
        "faq": [
            {"q": "출산휴가 전 연차를 다 소진해야 하나요?", "a": "아닙니다. 연차는 직원이 원하는 시점에 자유롭게 사용합니다. 회사가 강제로 소진 지시하는 것은 불법입니다."},
            {"q": "인수인계 기간이 짧으면 어떻게 하나요?", "a": "핵심 업무 위주의 간소화된 인수인계를 진행하고, 나머지는 복직 후 인계하는 방식으로 조율할 수 있습니다."},
            {"q": "출산일이 예정보다 빨라졌다면?", "a": "출산 전후 휴가는 출산일 기준으로 재산정됩니다. 즉시 HR에 알려주세요."},
        ],
        "kpi": [{"val": "자율", "label": "연차 사용"}],
    },
    {
        "id": 4, "short": "출산 관련", "title": "출산 전후 및 배우자 출산(전후)휴가",
        "color": "#ef4444", "grad": "linear-gradient(135deg, #dc2626, #ef4444)",
        "target": "출산 전후 직원", "next": "육아기 지원",
        "guide": '"출산휴가는 90일(다태아 120일, 미숙아 100일), 배우자분은 근무일 기준 20일 유급 휴가가 보장되고 3회까지 나눠 쓸 수 있어요. 출산 후 45일은 반드시 쉬셔야 합니다."',
        "check": ["배우자 출산휴가(20일, 3분할) 신청 안내", "미숙아·다태아 출산 여부 확인 (100일/120일)", "유산·사산 휴가 해당 여부 및 임신주수 확인"],
        "forms": ["어울지기 내 신청", "출산전후휴가 확인서", "배우자출산휴가 확인서"],
        "warn": ["산후 45일 이상 반드시 보장 (위반 시 2년 이하 징역 또는 2천만원 이하 벌금)", "배우자 휴가는 출산 후 120일 이내 사용", "⚠️ 2026-09-18 시행 예정: 배우자출산휴가 → '배우자출산전후휴가'로 명칭 변경, 출산예정일 50일 전부터 사용 가능하도록 확대(20일·3분할 유지) — 시행 전이므로 현재는 종전 기준 적용"],
        "laws": [
            {"name": "근로기준법 제74조", "desc": "출산전후 휴가 90일(다태아 120일·미숙아 100일), 산후 반드시 45일 이상"},
            {"name": "남녀고용평등법 제18조의2", "desc": "배우자 출산휴가 20일(근무일 기준) 유급, 3회 분할 가능"},
        ],
        "faq": [
            {"q": "배우자 출산휴가 20일은 연속으로 써야 하나요?", "a": "아니요. 3회까지 나눠 총 4번에 걸쳐 사용 가능합니다. 단, 출산일로부터 120일 이내에 모두 사용해야 합니다."},
            {"q": "쌍둥이 출산 시 휴가 일수는?", "a": "다태아 출산은 120일(전후 최초 75일 유급), 미숙아는 100일(최초 60일 유급)이 부여됩니다."},
            {"q": "유산·사산했는데 휴가를 신청할 수 있나요?", "a": "네, 신청 시에만 부여됩니다(자동 부여 아님). 임신 15주 이내 10일, 16~21주 30일, 22~27주 60일, 28주 이상 90일이며, 유산·사산일부터 기산되므로 신청이 늦을수록 사용 가능일수가 줄어듭니다."},
        ],
        "kpi": [{"val": "90일", "label": "출산휴가"}],
    },
    {
        "id": 5, "short": "육아 지원", "title": "육아기 근로시간 단축 · 육아시간",
        "color": "#0ea5e9", "grad": "linear-gradient(135deg, #0284c7, #0ea5e9)",
        "target": "육아기 부모", "next": "육아휴직/복직",
        "guide": '"자녀가 만 12세 이하(초6 이하)라면 원칙적으로 1년, 육아휴직 미사용분을 전환하면 최대 3년까지 단축 근무가 가능합니다. 생후 1년 미만 자녀가 있으면 육아시간(수유시간)도 별도로 신청하실 수 있어요."',
        "check": ["대상 자녀 연령 확인 (만 12세 이하/초6 이하)", "단축 후 근로시간(주 15~35시간) 및 방법 협의", "육아휴직 미사용분 전환 여부 확인(1:2 비율)"],
        "forms": ["KCIM_임신·육아기 관련 지원 신청서"],
        "warn": ["단축 시작 30일 전 신청 원칙", "육아휴직 6개월 연장분(요건부 가산분)은 단축기간으로 전환 불가", "육아시간은 상시 5인 이상 사업장만 법적 의무"],
        "laws": [
            {"name": "남녀고용평등법 제19조의2", "desc": "육아기 근로시간 단축 (만 12세 이하, 원칙 1년+전환 시 최대 3년)"},
            {"name": "동법 제19조의7 (육아시간)", "desc": "생후 1년 미만 자녀, 1일 2회 각 30분(또는 1회 1시간) 유급"},
        ],
        "faq": [
            {"q": "육아휴직과 단축근무를 동시에 할 수 있나요?", "a": "동시 사용은 불가하나, 육아휴직 미사용 기간을 2배로 가산해 단축 기간으로 전환할 수 있습니다(예: 육아휴직 전혀 미사용 시 원칙 1년+전환 2년=최대 3년)."},
            {"q": "단축 근무 중 급여는 어떻게 계산되나요?", "a": "단축 시간에 비례해 회사가 임금을 지급하고, 고용보험에서 육아기 근로시간 단축 급여(첫 10시간분 100%·상한 250만원, 나머지 80%·상한 160만원)를 별도 지원합니다."},
            {"q": "회사가 단축을 거부할 수 있나요?", "a": "근속 6개월 미만, 자녀 연령 초과, 14일 이상 대체인력 채용 노력에도 실패, 업무 성격상 곤란한 경우 등에 한해 거부할 수 있습니다."},
        ],
        "kpi": [{"val": "최대 3년", "label": "단축(전환 시)"}],
    },
    {
        "id": 6, "short": "복직 준비", "title": "육아휴직 및 복직 관리",
        "color": "#22c55e", "grad": "linear-gradient(135deg, #16a34a, #22c55e)",
        "target": "복직 예정자", "next": "가족돌봄 지원",
        "guide": '"육아휴직은 기본 1년이며, 부모가 각각 3개월 이상 사용하시거나 한부모·중증장애아동 부모이신 경우 6개월이 추가돼 최대 1년 6개월까지 가능합니다. 사후지급금 없이 매월 급여 100%가 지급됩니다. 갑자기 며칠만 필요하시면 단기 육아휴직으로 1주나 2주만 쓰실 수도 있어요."',
        "check": ["육아휴직 기본 1년 + 조건부 연장 요건 확인", "사후지급금 폐지 사실 안내", "6+6 부모육아휴직제 해당 여부 확인 (자녀 생후 18개월 이내)", "단기 육아휴직(1주/2주) 필요 여부 확인 — 자녀 질병·휴원·방학 등", "복직 면담 일정 잡기 및 자리 세팅"],
        "forms": ["어울지기 내 신청 (휴직/복직)", "단기 육아휴직 신청서(해당 시)"],
        "warn": ["연장(1년6개월)은 조건부 — 무조건 안내 금지: 부모 각각 3개월+ 사용 또는 한부모/중증장애아동 부모만 해당", "복직 14일 전 의사표시 필요", "복직 후 부당 처우·차별 절대 금지", "⚠️ 2026-08-20 시행: 단기 육아휴직 신설(연 1회, 1주/2주 단위) — 정당한 사유 없이 거부 불가, 신청일로부터 7일 이내 승인·거부 통보", "⚠️ 2026-09-18 시행 예정: 배우자 유산·조산 위험 시 남성 근로자도 출산 전 육아휴직 사용 가능하도록 확대"],
        "laws": [
            {"name": "남녀고용평등법 제19조", "desc": "육아휴직 기본 1년, 조건부 +6개월(최대 1년 6개월), 사후지급금 폐지"},
            {"name": "동법 제19조 (단기 육아휴직, 2026-08-20 시행)", "desc": "만 8세 이하 자녀 단기 돌봄 시 연 1회 1주/2주 단위 사용, 전체 육아휴직 기간에서 차감(분할횟수 미포함)"},
            {"name": "동법 제19조의4", "desc": "복직 후 동일 또는 동등 업무 복귀 보장"},
        ],
        "faq": [
            {"q": "육아휴직 급여는 얼마나 받나요?", "a": "최초 3개월 통상임금 100%(상한 250만원, 한부모 300만원), 4~6개월 100%(상한 200만원), 7개월 이후 80%(상한 160만원)이며 하한은 70만원입니다. 사후지급금은 폐지되어 매월 전액 지급됩니다."},
            {"q": "배우자도 동시에 육아휴직이 가능한가요?", "a": "네, 가능합니다. 자녀 생후 18개월 이내에 부모가 동시 또는 순차로 사용하면 '6+6 부모육아휴직제'가 적용되어 첫 6개월 동안 통상임금 100%가 지급되고, 부모 합산 상한액이 1개월 250만원에서 6개월 450만원까지 계단식으로 올라갑니다. (첫 3개월이 아니라 첫 6개월입니다)"},
            {"q": "자녀가 갑자기 아파서 며칠만 쉬어야 하는데, 육아휴직은 30일 이상 써야 하지 않나요?", "a": "2026년 8월 20일부터는 '단기 육아휴직'으로 연 1회, 1주 또는 2주 단위로도 쓰실 수 있습니다. 자녀 질병·사고 입원, 소속 기관 휴원·휴교, 방학 등이 사유가 되고, 급여도 기존 육아휴직급여 기준으로 일할 계산되어 지급됩니다."},
            {"q": "단기 육아휴직을 쓰면 나중에 일반 육아휴직 쓸 수 있는 기간이 줄어드나요?", "a": "네, 사용한 만큼 전체 육아휴직 한도(최대 1년 6개월)에서 차감됩니다. 다만 육아휴직의 분할 사용 횟수(3회) 카운트에는 포함되지 않으니 이 부분은 구분해서 안내해 주세요."},
            {"q": "복직 후 기존 부서로 반드시 돌아가야 하나요?", "a": "동일하거나 동등한 수준의 업무로 복직해야 하며, 일방적인 부서 변경이나 직급 하락은 금지됩니다."},
        ],
        "kpi": [{"val": "최대 1.5년", "label": "육아휴직(조건부)"}, {"val": "1~2주", "label": "단기 육아휴직(연1회)"}],
    },
    {
        "id": 7, "short": "가족돌봄", "title": "가족돌봄휴직 및 휴가",
        "color": "#64748b", "grad": "linear-gradient(135deg, #475569, #64748b)",
        "target": "가족돌봄 필요 직원", "next": "난임치료 안내(참고)",
        "guide": '"조부모·부모·배우자·배우자의 부모·자녀·손자녀를 돌봐야 하는 경우 연간 최대 90일 휴직이 가능하고, 급하게 하루 이틀만 필요하면 그 안에서 연 10일은 휴가 형태로 쓰실 수 있어요."',
        "check": ["돌봄 대상 가족관계 확인", "휴직(30일 이상 단위) vs 휴가(1일 단위, 연 10일) 구분 안내", "감염병·휴원 등 특별사유 해당 여부 확인(+10일 가능)"],
        "forms": ["가족돌봄휴직·휴가 신청서", "가족관계 및 돌봄 필요성 입증서류"],
        "warn": ["전 기간 무급", "근속 6개월 미만, 대체 돌봄 가능자 존재, 14일 이상 대체인력 채용 실패, 업무상 중대 지장 시 거부 가능", "휴가(연 10일)는 휴직 연 90일 한도에 포함되는 것이지 별도 추가가 아님"],
        "laws": [
            {"name": "남녀고용평등법 제22조의2", "desc": "가족돌봄휴직 연 90일(분할 시 1회 30일 이상)"},
            {"name": "동법 제22조의3", "desc": "가족돌봄휴가 연 10일(1일 단위, 특별사유 시 +10일)"},
        ],
        "faq": [
            {"q": "휴직과 휴가의 차이는 뭔가요?", "a": "휴직은 1회 신청 시 30일 이상 단위로 사용하고, 휴가는 1일 단위로 급하게 쓸 수 있습니다. 둘을 합쳐 연 90일 한도 안에서 운용됩니다."},
            {"q": "휴가 신청도 사전 신청이 필요한가요?", "a": "휴직은 시작 30일 전 신청이 원칙이지만, 휴가는 긴급성을 인정해 당일 신청도 허용됩니다."},
            {"q": "연차휴가로 대체할 수 있나요?", "a": "아니요. 가족돌봄휴가는 연차와 별개의 무급휴가입니다. 다만 직원이 연차휴가를 신청하는 경우라면 그건 유급으로 처리하면 됩니다."},
        ],
        "kpi": [{"val": "90일", "label": "연간 (휴직+휴가 합산)"}],
    },
    {
        "id": 8, "short": "난임치료", "title": "난임치료휴가",
        "color": "#ec4899", "grad": "linear-gradient(135deg, #db2777, #ec4899)",
        "target": "난임치료 중인 직원", "next": "가이드 종료(참고 항목)",
        "guide": '"난임치료(인공수정·체외수정 등 시술 및 전후 준비·휴식기 포함)를 위한 휴가는 연 6일까지 가능하고, 최초 2일은 유급입니다. 신청기한이 따로 없으니 당일 신청도 가능해요."',
        "check": ["난임치료휴가 신청서 접수", "최초 2일 유급 처리 (정부 지원금 상한 84,210원/일 차감 안내)", "치료 관련 정보 비밀유지 서약"],
        "forms": ["난임치료휴가 신청서", "치료 사실 입증서류(선택)"],
        "warn": ["거부 시 500만원 이하 과태료", "신청 과정에서 알게 된 질환·치료 정보 무단 누설 금지", "1일 단위 분할 사용 가능"],
        "laws": [
            {"name": "남녀고용평등법 제18조의3", "desc": "난임치료휴가 연 6일, 최초 2일 유급"},
        ],
        "faq": [
            {"q": "난임치료휴가 급여는 회사가 다 부담하나요?", "a": "아닙니다. 근로자가 고용센터에 난임치료휴가급여를 신청해 받으면(1일 상한 84,210원), 회사는 통상임금에서 그 금액을 뺀 차액만 지급하면 됩니다."},
            {"q": "연차휴가에서 차감되나요?", "a": "아니요. 연차휴가와 별개로 부여되는 법정휴가라 연차에서 차감할 수 없습니다."},
            {"q": "증빙 서류가 꼭 필요한가요?", "a": "회사는 난임치료 사실을 확인할 수 있는 입증서류를 요청할 수 있습니다. 다만 신청서 제출 기한 자체는 별도로 없습니다."},
        ],
        "kpi": [{"val": "6일", "label": "연간 최대(2일 유급)"}],
    },
]

# ──────────────────────────────────────────
# 세션 초기화
# ──────────────────────────────────────────
if "active_step" not in st.session_state:
    st.session_state.active_step = 0
if "mode" not in st.session_state:
    st.session_state.mode = "steps"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "checks" not in st.session_state:
    st.session_state.checks = {i: [False] * len(STEPS[i]["check"]) for i in range(len(STEPS))}
if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = set()

active_idx = st.session_state.active_step
step = STEPS[active_idx]
is_calc = st.session_state.mode == "calc"

# ──────────────────────────────────────────
# 상단 헤더
# ──────────────────────────────────────────
right_label = "📊 계산기 도구" if is_calc else f"현재 단계: <strong style='color:white;'>STEP {step['id']}. {step['short']}</strong> (총 {len(STEPS)}단계)"
st.markdown(f"""
<div class="top-header">
  <div>
    <div class="top-header-title">👶 KCIM 출산·육아 응대 가이드
      <span class="badge-2025">2026-08 개정 반영</span>
    </div>
    <div class="top-header-sub">경영관리본부 담당자를 위한 단계별 업무 대응 워크스테이션</div>
  </div>
  <div style="color:rgba(255,255,255,0.6); font-size:0.75rem; text-align:right;">
    {right_label}
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# 스텝 프로그레스 (클릭 가능한 버튼형, 계산기 모드에서는 숨김)
# ──────────────────────────────────────────
if not is_calc:
    with st.container(key="stepper_wrap_box"):
        with st.container(horizontal=True, gap="small"):
            for i, s in enumerate(STEPS):
                is_done = i in st.session_state.completed_steps
                is_active = i == active_idx
                icon = "✓" if is_done else str(s["id"])
                key_state = "step_active" if is_active else ("step_done" if is_done else "step_todo")
                if st.button(
                    f"{icon}. {s['short']}",
                    key=f"{key_state}_{i}",
                    help=f"STEP {s['id']}. {s['short']}로 이동",
                ):
                    st.session_state.active_step = i
                    st.session_state.mode = "steps"
                    st.rerun()

# ──────────────────────────────────────────
# 메뉴 / 챗봇 상태 초기화
# ──────────────────────────────────────────
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False  # 모바일 기본값을 고려해 기본은 닫힘(본문 우선)
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# ──────────────────────────────────────────
# 플로팅 액션 버튼 (좌하단: 메뉴 토글 / 우하단: AI 챗봇 열기)
# 두 버튼 모두 CSS로 position:fixed 처리되어 레이아웃 흐름에서 완전히
# 벗어나므로, block-container에 어떤 강제 여백도 필요하지 않습니다.
# → 모바일에서 본문이 한쪽으로 쏠려 보이던 문제의 근본 원인을 제거.
# ──────────────────────────────────────────
menu_btn_label = "✕" if st.session_state.menu_open else "☰"
menu_btn_help = "메뉴 닫기" if st.session_state.menu_open else "메뉴 열기"
if st.button(menu_btn_label, key="menu_toggle_btn", help=menu_btn_help):
    st.session_state.menu_open = not st.session_state.menu_open
    st.rerun()

if st.button("💬", key="chat_toggle_btn", help="AI 챗봇 육아지원박사에게 질문하기"):
    st.session_state.chat_open = True
    st.rerun()

# ──────────────────────────────────────────
# 메인 레이아웃 (본문 중심 1~2단)
# 좌측 메뉴는 열렸을 때만 컬럼을 차지하고, 닫히면 본문이 전체 폭을 사용합니다.
# (기존 "가장자리 고정 탭 + block-container 좌측 여백 강제" 방식은 모바일에서
#  본문이 오른쪽으로 쏠려 보이는 비대칭 여백을 유발했기 때문에 완전히 제거했습니다.)
# ──────────────────────────────────────────
if st.session_state.menu_open:
    col_menu, col_center = st.columns([1, 3.6], gap="small")
else:
    col_menu = None
    col_center = st.container()

# ── 메뉴 패널 (계산 도구 / 법령 / KPI — 단계 이동은 상단 스텝바로 통합) ──
if col_menu is not None:
    with col_menu:
        # 계산기 버튼
        st.markdown('<div class="nav-section-title">🧮 계산 도구</div>', unsafe_allow_html=True)
        if st.button(
            "📊 계산기" + (" ✓" if is_calc else ""),
            key="btn_calc",
            use_container_width=True,
            type="primary" if is_calc else "secondary",
        ):
            st.session_state.mode = "steps" if is_calc else "calc"
            st.rerun()

        # 법령 & KPI (단계 모드에서만)
        if not is_calc:
            st.markdown('<div class="nav-section-title" style="margin-top:1rem;">⚖️ 관련 법령</div>', unsafe_allow_html=True)
            for law in step["laws"]:
                st.markdown(f"""
                <div class="law-item">
                  <div class="law-item-title">{law['name']}</div>
                  <div class="law-item-desc">{law['desc']}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="nav-section-title" style="margin-top:1rem;">🔢 핵심 수치</div>', unsafe_allow_html=True)
            for kpi in step["kpi"]:
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-value">{kpi['val']}</div>
                  <div class="kpi-label">{kpi['label']}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("""
            <div class="kpi-card"><div class="kpi-value">90일</div><div class="kpi-label">출산휴가</div></div>
            <div class="kpi-card"><div class="kpi-value">20일</div><div class="kpi-label">배우자휴가</div></div>
            <div class="kpi-card"><div class="kpi-value">2시간</div><div class="kpi-label">임신기단축/일</div></div>
            """, unsafe_allow_html=True)

# ── 중앙 패널 ──
with col_center:

    # ════════════════════════════════
    # 계산기 모드
    # ════════════════════════════════
    if is_calc:
        st.markdown("""
        <div class="calc-header-card">
          <div style="font-size:0.72rem;font-weight:700;background:rgba(255,255,255,0.2);
               border-radius:20px;padding:2px 10px;display:inline-block;margin-bottom:6px;">KCIM 계산 도구</div>
          <div style="font-size:1.4rem;font-weight:900;">📊 기간 계산기</div>
          <div style="font-size:0.8rem;opacity:0.75;margin-top:4px;">
            출산·육아 관련 법정 기간 및 연차를 자동으로 계산합니다
          </div>
        </div>""", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📐 임신기 단축 기간", "📅 출산·육아 일정", "📉 무급휴가 연차"])

        # ── Tab 1: 임신기 단축 대상기간 ──
        with tab1:
            st.markdown("#### 임신기 근로시간 단축 대상기간 계산기")
            st.caption("출산예정일을 입력하면 근로기준법 제74조의2에 따른 단축 가능 기간을 자동으로 계산합니다.")
            st.markdown("")

            col_in, col_hint = st.columns([1, 1])
            with col_in:
                due = st.date_input(
                    "출산예정일",
                    value=date.today() + timedelta(days=180),
                    min_value=date.today() - timedelta(days=30),
                    max_value=date.today() + timedelta(days=400),
                    key="calc_due",
                )
            with col_hint:
                st.markdown("""
                <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;
                     padding:0.7rem;font-size:0.78rem;color:#92400e;margin-top:1.7rem;">
                  💡 병원 분만예정일 확인서의 날짜를 입력하세요
                </div>""", unsafe_allow_html=True)

            if st.button("🔍 단축 기간 계산", key="calc_btn1", type="primary"):
                # 마지막생리시작일 = 출산예정일 - 279일 (40주 = 280일, 1일차 포함)
                lmp = due - timedelta(days=279)
                week12_end = lmp + timedelta(days=83)    # 84일째 (12주×7일)
                week32_start = lmp + timedelta(days=217)  # 218일째 (31주×7일 + 1일)

                days_early = (week12_end - lmp).days + 1
                days_mid = (week32_start - week12_end).days - 1
                days_late = (due - week32_start).days + 1
                total_ok = days_early + days_late

                st.markdown(f"""
                <div style="margin-top:1rem;">
                  <div class="period-bar period-ok">
                    <div>
                      <div class="period-label" style="color:#16a34a;">✅ 임신 12주 이내 (단축 가능)</div>
                      <div class="period-date">{lmp.strftime('%Y년 %m월 %d일')} ~ {week12_end.strftime('%Y년 %m월 %d일')}</div>
                    </div>
                    <div class="period-days" style="color:#16a34a;">{days_early}일</div>
                  </div>
                  <div class="period-bar period-na">
                    <div>
                      <div class="period-label" style="color:#94a3b8;">⏸ 13주 ~ 31주 (단축 불가)</div>
                      <div class="period-date">{(week12_end + timedelta(1)).strftime('%Y년 %m월 %d일')} ~ {(week32_start - timedelta(1)).strftime('%Y년 %m월 %d일')}</div>
                    </div>
                    <div class="period-days" style="color:#94a3b8;">{days_mid}일</div>
                  </div>
                  <div class="period-bar period-ok">
                    <div>
                      <div class="period-label" style="color:#16a34a;">✅ 임신 32주 이후 (단축 가능)</div>
                      <div class="period-date">{week32_start.strftime('%Y년 %m월 %d일')} ~ {due.strftime('%Y년 %m월 %d일')}</div>
                    </div>
                    <div class="period-days" style="color:#16a34a;">{days_late}일</div>
                  </div>
                </div>
                <div class="calc-note-box">
                  <strong>📌 요약</strong><br>
                  마지막 생리시작일(추정): <strong>{lmp.strftime('%Y.%m.%d')}</strong> &nbsp;|&nbsp;
                  단축 가능 총 기간: <strong>{total_ok}일</strong><br>
                  ※ 고위험 임산부(유산·조산 위험)는 전 임신 기간 단축 신청 가능 (의사 소견서 필요)<br>
                  ※ 단축 개시 3일 전까지 신청서 접수 필요 (근로기준법 제74조의2)<br>
                  ※ 2025년 개정 행정해석: 단축 근무 기간도 '정상 근무'로 간주되어 연차휴가 발생·사용에 불이익이 없습니다.
                </div>
                """, unsafe_allow_html=True)

        # ── Tab 2: 출산·육아 일정 계산기 ──
        with tab2:
            st.markdown("#### 출산·육아휴직 일정 계산기")
            st.caption("각 휴가 항목의 기간을 입력하면 합산 일수, 잔여 육아휴직을 자동으로 계산합니다.")

            emp_name = st.text_input("직원명", placeholder="예: 홍길동 책임", key="calc_emp")

            today = date.today()
            df_default = pd.DataFrame({
                "구분": ["연차", "출산휴가", "육아휴직"],
                "시작일": [today, today + timedelta(14), today + timedelta(104)],
                "종료일": [today + timedelta(13), today + timedelta(103), today + timedelta(468)],
                "주말_제외일수": [4, 0, 0],
            })

            st.markdown("**기간 입력** (행 추가: + 버튼, 삭제: 행 선택 후 Delete)")
            edited_df = st.data_editor(
                df_default,
                column_config={
                    "구분": st.column_config.SelectboxColumn(
                        "구분",
                        options=["연차", "출산휴가", "육아휴직", "산전육아휴직", "배우자출산휴가"],
                        required=True,
                        width="medium",
                    ),
                    "시작일": st.column_config.DateColumn("시작일", required=True),
                    "종료일": st.column_config.DateColumn("종료일", required=True),
                    "주말_제외일수": st.column_config.NumberColumn(
                        "주말 제외 (일)", min_value=0, max_value=100, step=1, width="small"
                    ),
                },
                num_rows="dynamic",
                use_container_width=True,
                key="calc_schedule_df",
            )

            if st.button("🔍 일정 계산", key="calc_btn2", type="primary"):
                rows_ok = []
                for _, row in edited_df.iterrows():
                    s_date = row["시작일"]
                    e_date = row["종료일"]
                    if s_date is None or e_date is None:
                        continue
                    if isinstance(s_date, str):
                        s_date = pd.to_datetime(s_date).date()
                    if isinstance(e_date, str):
                        e_date = pd.to_datetime(e_date).date()
                    if hasattr(s_date, "date"):
                        s_date = s_date.date()
                    if hasattr(e_date, "date"):
                        e_date = e_date.date()
                    total_days = (e_date - s_date).days + 1
                    excl = int(row["주말_제외일수"] or 0)
                    net = total_days - excl
                    rows_ok.append({
                        "구분": row["구분"],
                        "시작일": s_date.strftime("%Y.%m.%d"),
                        "종료일": e_date.strftime("%Y.%m.%d"),
                        "총 일수": total_days,
                        "주말 제외": excl,
                        "소계": net,
                    })

                if rows_ok:
                    res_df = pd.DataFrame(rows_ok)
                    st.dataframe(res_df, use_container_width=True, hide_index=True)

                    annual_total = res_df[res_df["구분"] == "연차"]["소계"].sum()
                    maternity_total = res_df[res_df["구분"] == "출산휴가"]["소계"].sum()
                    parental_total = res_df[res_df["구분"].isin(["육아휴직", "산전육아휴직"])]["소계"].sum()
                    remaining_parental = max(0, 365 - int(parental_total))

                    st.markdown("**📊 요약**")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.markdown(f"""<div class="result-metric">
                          <div class="result-metric-val">{int(annual_total)}일</div>
                          <div class="result-metric-label">연차 합계</div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""<div class="result-metric">
                          <div class="result-metric-val">{int(maternity_total)}일</div>
                          <div class="result-metric-label">출산휴가</div>
                        </div>""", unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"""<div class="result-metric">
                          <div class="result-metric-val">{int(parental_total)}일</div>
                          <div class="result-metric-label">육아휴직 사용</div>
                        </div>""", unsafe_allow_html=True)
                    with c4:
                        color = "#16a34a" if remaining_parental > 0 else "#dc2626"
                        st.markdown(f"""<div class="result-metric" style="border-color:{color};">
                          <div class="result-metric-val" style="color:{color};">{remaining_parental}일</div>
                          <div class="result-metric-label">잔여 육아휴직</div>
                        </div>""", unsafe_allow_html=True)

                    name_label = emp_name if emp_name else "해당 직원"
                    st.markdown(f"""
                    <div class="calc-note-box" style="margin-top:0.8rem;">
                      <strong>📌 {name_label} 요약</strong><br>
                      연차 {int(annual_total)}일 + 출산휴가 {int(maternity_total)}일 + 육아휴직 {int(parental_total)}일 사용<br>
                      잔여 육아휴직: <strong>{remaining_parental}일</strong> (원칙 365일 기준 / 부모 각각 3개월+ 사용 또는 한부모·중증장애아동 부모 요건 충족 시 최대 548일)
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("유효한 기간 데이터가 없습니다. 시작일·종료일을 확인해주세요.")

        # ── Tab 3: 무급휴가 연차 삭감 계산기 ──
        with tab3:
            st.markdown("#### 무급휴가 연차삭감 계산기")
            st.caption("연간 80% 미만 근무 시 연차가 삭감됩니다 (근로기준법 제60조 제2항). 무급휴가 기간을 입력하여 확인하세요.")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                annual_cnt = st.number_input("발생 연차 (일)", min_value=1, max_value=25, value=15, key="calc_annual_cnt")
            with col_b:
                base_days = st.number_input("연도 기준일수", min_value=365, max_value=366, value=365, key="calc_base_days",
                                             help="윤년은 366 입력")
            with col_c:
                st.markdown("")
                st.markdown("""<div style="background:#fef9c3;border:1px solid #fde047;border-radius:8px;
                     padding:0.5rem;font-size:0.75rem;color:#713f12;margin-top:0.5rem;">
                  ⚠️ 80% 기준: 73일 초과 무급 시 삭감
                </div>""", unsafe_allow_html=True)

            st.markdown("**무급휴가 기간 입력** (행 추가 가능)")
            df_leave_default = pd.DataFrame({
                "무급휴가 시작일": [date.today()],
                "무급휴가 종료일": [date.today() + timedelta(days=30)],
            })
            edited_leave = st.data_editor(
                df_leave_default,
                column_config={
                    "무급휴가 시작일": st.column_config.DateColumn("시작일", required=True),
                    "무급휴가 종료일": st.column_config.DateColumn("종료일", required=True),
                },
                num_rows="dynamic",
                use_container_width=True,
                key="calc_leave_df",
            )

            if st.button("🔍 연차삭감 계산", key="calc_btn3", type="primary"):
                total_leave = 0
                leave_rows = []
                for _, row in edited_leave.iterrows():
                    s = row["무급휴가 시작일"]
                    e = row["무급휴가 종료일"]
                    if s is None or e is None:
                        continue
                    if hasattr(s, "date"):
                        s = s.date()
                    if hasattr(e, "date"):
                        e = e.date()
                    days = (e - s).days + 1
                    total_leave += days
                    leave_rows.append({"시작일": s.strftime("%Y.%m.%d"), "종료일": e.strftime("%Y.%m.%d"), "일수": days})

                if leave_rows:
                    st.dataframe(pd.DataFrame(leave_rows), use_container_width=True, hide_index=True)

                work_ratio = (base_days - total_leave) / base_days
                # CEILING to 0.5 단위 (엑셀 CEILING 함수 동일)
                adjusted = math.ceil(annual_cnt * work_ratio * 2) / 2
                adjusted = max(0, adjusted)
                deducted = annual_cnt - adjusted
                threshold_days = base_days * 0.2  # 20% = 73일

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""<div class="result-metric">
                      <div class="result-metric-val">{total_leave}일</div>
                      <div class="result-metric-label">무급 총 일수</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    ratio_color = "#16a34a" if work_ratio >= 0.8 else "#dc2626"
                    st.markdown(f"""<div class="result-metric" style="border-color:{ratio_color};">
                      <div class="result-metric-val" style="color:{ratio_color};">{work_ratio*100:.1f}%</div>
                      <div class="result-metric-label">근무 비율</div>
                    </div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="result-metric">
                      <div class="result-metric-val">{adjusted}일</div>
                      <div class="result-metric-label">조정 후 연차</div>
                    </div>""", unsafe_allow_html=True)
                with c4:
                    ded_color = "#dc2626" if deducted > 0 else "#16a34a"
                    st.markdown(f"""<div class="result-metric" style="border-color:{ded_color};">
                      <div class="result-metric-val" style="color:{ded_color};">-{deducted}일</div>
                      <div class="result-metric-label">차감 연차</div>
                    </div>""", unsafe_allow_html=True)

                if work_ratio >= 0.8:
                    st.success(f"✅ 근무비율 {work_ratio*100:.1f}% ≥ 80% → 연차 삭감 없음 (발생 연차 {annual_cnt}일 전액 지급)")
                else:
                    st.warning(
                        f"⚠️ 근무비율 {work_ratio*100:.1f}% < 80% → 연차 {deducted}일 삭감 "
                        f"(원래 {annual_cnt}일 → 조정 후 {adjusted}일)\n"
                        f"무급 {total_leave}일 > 기준 {int(threshold_days)}일 초과"
                    )

                st.markdown(f"""
                <div class="calc-note-box">
                  <strong>📌 계산 기준</strong><br>
                  근무비율 = ({base_days}일 - {total_leave}일) ÷ {base_days}일 = {work_ratio*100:.2f}%<br>
                  조정연차 = {annual_cnt}일 × {work_ratio*100:.2f}% = {annual_cnt * work_ratio:.2f}일 → 0.5 단위 올림 → <strong>{adjusted}일</strong><br>
                  ※ 출산전후휴가·육아휴직 기간은 출근으로 간주되어 무급휴가 산정에서 제외됩니다 (근로기준법 제60조 제6항)
                </div>""", unsafe_allow_html=True)

    # ════════════════════════════════
    # 단계 가이드 모드
    # ════════════════════════════════
    else:
        st.markdown(f"""
        <div class="step-header-card" data-num="{step['id']}" style="background:{step['grad']};">
          <div class="step-num-badge">STEP {step['id']} / {len(STEPS)-1}</div>
          <div class="step-main-title">{step['title']}</div>
          <div class="step-meta">
            <span class="step-chip">👤 대상: {step['target']}</span>
            <span class="step-chip">➡️ 다음: {step['next']}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="script-card">
          <div class="card-title">💬 담당자 안내 핵심 스크립트</div>
          <div class="script-content">{step['guide']}</div>
        </div>""", unsafe_allow_html=True)

        col_copy, col_done = st.columns([2, 1])
        with col_copy:
            script_text = step["guide"].strip('"').strip('“').strip('”')
            st.code(script_text, language=None)
        with col_done:
            if st.button("✅ 이 단계 완료", key=f"done_{active_idx}", use_container_width=True):
                st.session_state.completed_steps.add(active_idx)
                if active_idx < len(STEPS) - 1:
                    st.session_state.active_step = active_idx + 1
                st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            check_count = sum(st.session_state.checks[active_idx])
            total_count = len(step["check"])
            pct = int(check_count / total_count * 100)
            st.markdown(f"""
            <div class="info-card">
              <div class="card-title">
                ✅ 관리자 필수 체크
                <span style="margin-left:auto;font-size:0.7rem;color:#6b7280;font-weight:600;">{check_count}/{total_count} 완료</span>
              </div>""", unsafe_allow_html=True)
            for ci, check_text in enumerate(step["check"]):
                checked = st.session_state.checks[active_idx][ci]
                if st.checkbox(check_text, value=checked, key=f"chk_{active_idx}_{ci}"):
                    st.session_state.checks[active_idx][ci] = True
                else:
                    st.session_state.checks[active_idx][ci] = False
            st.progress(pct / 100)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="info-card"><div class="card-title">🧾 필요 서류 및 주의사항</div>', unsafe_allow_html=True)
            for f in step["forms"]:
                st.markdown(f'<div class="form-chip2">📄 {f}</div>', unsafe_allow_html=True)
            for w in step["warn"]:
                st.markdown(f'<div class="warn-banner">⚠️ {w}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="faq-card">
          <div class="card-title">💡 자주 묻는 질문 (FAQ)</div>""", unsafe_allow_html=True)
        for faq in step["faq"]:
            st.markdown(f"""
          <div class="faq-item">
            <div class="faq-q">Q. {faq['q']}</div>
            <div class="faq-a">A. {faq['a']}</div>
          </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────
# AI 챗봇 (우하단 플로팅 버튼 → 모달 다이얼로그)
# PC/모바일 동일한 방식으로 동작하며, 평소에는 화면 공간을 전혀 차지하지
# 않아 본문 폭을 최대한 넓게 유지할 수 있습니다. (기존 3번째 컬럼 고정 배치
# 방식은 모바일에서 본문 폭을 지나치게 좁혀 가독성을 해쳤기 때문에 제거)
# ──────────────────────────────────────────
@st.dialog("🎓 육아지원박사", width="large")
def render_chatbot_dialog():
    chat_desc = "계산기 도구 대기 중" if is_calc else f"KCIM 모성보호 전문 AI · {step['short']} 단계 대기 중"
    st.markdown(f"""
    <div class="chat-header" style="border-radius:10px;margin:-1rem -1rem 0.8rem;">
      <div class="chat-avatar">🎓</div>
      <div class="chat-header-text">
        <div class="chat-name">육아지원박사</div>
        <div class="chat-desc">{chat_desc}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    chat_container = st.container(height=420)
    with chat_container:
        if not st.session_state.messages:
            st.markdown(f"""
            <div class="welcome-msg">
              안녕하세요! 저는 KCIM의 육아지원 전문 AI <strong>박사</strong>입니다.<br><br>
              현재 <strong>[{step['short']}]</strong> 단계에 대한 법령 해석, 대응 방법, 엣지케이스 등 무엇이든 질문하세요. 📚
            </div>""", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            avatar = "🙋" if msg["role"] == "user" else "🎓"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user", avatar="🙋"):
                st.markdown(prompt)

        try:
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("OPENAI_API_KEY가 secrets.toml에 없습니다.")
                st.stop()

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            system_prompt = f"""
너의 이름은 '육아지원박사'야. KCIM 경영관리본부 HR 담당자를 돕는 모성보호 전문 AI야.

[현재 상황]
- 담당자는 [{step['title']}] 단계를 처리 중이야.
- 현재 체크리스트: {step['check']}
- 관련 법령: {[l['name'] for l in step['laws']]}

[답변 원칙]
1. 최신 개정 반영: 임신기 단축 32주, 배우자출산휴가 20일(3분할), 육아휴직 기본 1년+조건부 6개월(최대 1.5년, 부모 각각 3개월+ 사용 또는 한부모·중증장애아동 부모만 해당), 사후지급금 폐지, 6+6 부모육아휴직제(자녀 생후 18개월 이내, 동시/순차 사용 시 첫 6개월 100% 지급), 난임치료휴가 연 6일(2일 유급), 가족돌봄휴직 연 90일(휴가 연 10일 포함), 단기 육아휴직(2026-08-20 시행, 만 8세 이하 자녀 단기 돌봄 시 연 1회 1주/2주 단위, 전체 육아휴직 기간에서 차감). 단, 2026-09-18 시행 예정 사항(배우자출산전후휴가 명칭변경 및 출산예정일 50일 전부터 사용 가능하도록 확대, 배우자 유산·사산휴가 신설, 배우자 유산·조산 위험 시 남성 육아휴직 확대)은 아직 시행 전이므로 시행일을 함께 안내할 것
2. 담당자가 직원에게 즉시 말할 수 있는 구어체 스크립트를 포함할 것
3. 법령 조항명을 정확히 인용할 것
4. 친절하고 명확하며, 든든한 동료 느낌 유지
5. 답변은 간결하게 (3~5문장 핵심 위주)
6. 확실하지 않은 세부 수치는 단정하지 말고 "노무사 확인 권장"으로 안내할 것
"""

            with chat_container:
                with st.chat_message("assistant", avatar="🎓"):
                    response_placeholder = st.empty()
                    full_response = ""

                    stream = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.messages,
                        ],
                        stream=True,
                    )

                    for chunk in stream:
                        delta = chunk.choices[0].delta.content or ""
                        full_response += delta
                        response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"챗봇 오류: {str(e)}")


if st.session_state.get("chat_open"):
    st.session_state.chat_open = False
    render_chatbot_dialog()

