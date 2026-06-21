"""
🇯🇵 일본 여행 쇼핑 & 1일 일본어 마스터 웹앱
중급자 대상 완전판 | 모바일(9:16) 최적화 | Streamlit 싱글 파일
실행: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import random

# ============================================================
# 1. 페이지 설정
# ============================================================
st.set_page_config(
    page_title="🇯🇵 일본어 1일 마스터",
    page_icon="🎌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 2. 세션 상태 초기화
# ============================================================
defaults = {
    "cart": [],
    "quiz_idx": 0,
    "quiz_score": 0,
    "quiz_total": 0,
    "quiz_answered": False,
    "quiz_correct": None,
    "quiz_pool": [],
    "vocab_category": "쇼핑",
    "flip_state": {},          # 플래시카드 뒤집기 상태
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# 3. 커스텀 CSS — 파스텔 아이보리 · 모바일 440px 최적화
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

/* ── 전체 ── */
.stApp {
    background: linear-gradient(160deg,#fffaf6 0%,#fef4e8 55%,#fde8d4 100%);
    font-family:'Noto Sans KR','Apple SD Gothic Neo',sans-serif;
}
.block-container {
    max-width:440px !important;
    margin:0 auto !important;
    padding:0.4rem 0.9rem 5rem !important;
}
#MainMenu,footer,header{visibility:hidden;}

/* ── 앱 헤더 ── */
.app-title{
    text-align:center;font-size:1.65rem;font-weight:900;
    background:linear-gradient(135deg,#e96c6c 0%,#f5a623 45%,#d35400 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;letter-spacing:-0.5px;padding:1rem 0 0.15rem;
}
.app-sub{text-align:center;color:#a08060;font-size:0.72rem;
    letter-spacing:0.8px;margin-bottom:0.7rem;}

/* ── BGM ── */
.bgm-box{
    background:linear-gradient(135deg,#fff0f8,#f0e8ff);
    border:1.5px solid #e2d0f0;border-radius:16px;
    padding:0.7rem 0.9rem 0.5rem;margin-bottom:0.8rem;
}
.bgm-label{font-size:0.7rem;font-weight:700;color:#8050a0;
    letter-spacing:0.3px;margin-bottom:0.35rem;}
audio{width:100%;height:34px;border-radius:8px;margin-top:0.2rem;}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"]{
    background:#fff8f2 !important;border-radius:14px !important;
    padding:4px !important;gap:2px !important;
    border:1.5px solid #f0d5bc !important;margin-bottom:0.4rem;
    flex-wrap:wrap !important;
}
.stTabs [data-baseweb="tab"]{
    border-radius:10px !important;font-size:0.72rem !important;
    font-weight:600 !important;color:#a08060 !important;
    padding:0.3rem 0.45rem !important;min-width:0 !important;
}
.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg,#ff8a65,#ffb74d) !important;
    color:white !important;font-weight:800 !important;
    box-shadow:0 2px 8px rgba(255,138,101,.4) !important;
}

/* ── 공통 드롭다운 ── */
.stSelectbox>div>div{
    background:white !important;border:2px solid #fad0c4 !important;
    border-radius:12px !important;font-size:0.88rem !important;font-weight:600 !important;
}
.stSelectbox label,.stRadio label{
    font-size:0.82rem !important;font-weight:700 !important;color:#5a3e2b !important;
}

/* ── 쇼핑 카드 ── */
.shop-card{
    background:#fff;border-radius:22px;
    padding:1.1rem 1rem 0.7rem;margin-bottom:0.3rem;
    box-shadow:0 4px 18px rgba(220,120,80,.12);
    border:1.5px solid #fef0e6;position:relative;overflow:hidden;
}
.shop-card::before{
    content:'';position:absolute;top:0;left:0;right:0;height:4px;
    background:linear-gradient(90deg,#ff8a65,#ffb74d,#ff8a65);
}
.item-emoji{font-size:2.6rem;display:block;margin-bottom:0.35rem;}
.item-name{font-size:1rem;font-weight:800;color:#3d2010;margin-bottom:0.2rem;}
.item-brand{font-size:0.68rem;font-weight:700;color:#e65100;background:#fff3e0;
    display:inline-block;padding:2px 9px;border-radius:20px;margin-bottom:0.5rem;}
.item-desc{font-size:0.78rem;color:#6d4c35;line-height:1.6;margin-bottom:0.3rem;}
.item-price{font-size:0.85rem;color:#c0392b;font-weight:700;margin-bottom:0.25rem;}
.item-where{font-size:0.73rem;color:#7d5c40;padding:3px 8px;
    background:#fdf6f0;border-radius:8px;margin-bottom:0.25rem;}
.item-tip{font-size:0.72rem;color:#b07840;padding:3px 8px;
    background:#fffde7;border-radius:8px;border-left:3px solid #ffd54f;}

/* ── 버튼 ── */
.stButton>button{
    background:linear-gradient(135deg,#ff8a65,#ffb74d) !important;
    color:white !important;border:none !important;border-radius:25px !important;
    font-weight:700 !important;font-size:0.82rem !important;
    padding:0.5rem 1.1rem !important;width:100% !important;
    box-shadow:0 3px 12px rgba(255,138,101,.35) !important;
    letter-spacing:0.2px !important;margin-top:0.5rem !important;
    margin-bottom:0.9rem !important;transition:all 0.2s !important;
}
.stButton>button:hover{
    background:linear-gradient(135deg,#e64a19,#f57c00) !important;
    box-shadow:0 5px 18px rgba(230,74,25,.45) !important;
}

/* ── 쇼핑 치트키 카드 ── */
.phrase-card{
    background:#fff;border-radius:18px;padding:1rem 1rem 0.85rem;
    margin-bottom:0.85rem;
    box-shadow:0 4px 14px rgba(80,80,200,.09);
    border-top:1.5px solid #e8e4ff;border-right:1.5px solid #e8e4ff;
    border-bottom:1.5px solid #e8e4ff;border-left:5px solid #7c4dff;
}
.phrase-sit{
    font-size:0.66rem;font-weight:800;color:#5c35c0;background:#ede7ff;
    display:inline-block;padding:2px 9px;border-radius:20px;
    margin-bottom:0.55rem;letter-spacing:0.4px;
}
.phrase-jp{font-size:1.18rem;font-weight:800;color:#1a1a2e;
    margin-bottom:0.3rem;line-height:1.5;}
.phrase-ko{font-size:0.8rem;color:#5a5a7a;margin-bottom:0.45rem;font-weight:500;}
.phrase-read{
    font-size:0.92rem;color:#bf360c;font-weight:700;
    background:linear-gradient(135deg,#fff3e0,#fce4ec);
    padding:4px 11px;border-radius:9px;display:inline-block;letter-spacing:0.4px;
}
.phrase-tip{font-size:0.7rem;color:#7c7c9a;margin-top:0.5rem;
    padding:3px 8px;background:#f8f8ff;border-radius:7px;border-left:3px solid #b39ddb;}

/* ── 어휘 플래시카드 ── */
.vocab-card{
    background:#fff;border-radius:20px;
    padding:1.1rem 1rem 0.9rem;margin-bottom:0.7rem;
    box-shadow:0 3px 14px rgba(0,150,136,.1);
    border:1.5px solid #e0f2f1;position:relative;
}
.vocab-jp{font-size:1.4rem;font-weight:900;color:#00695c;margin-bottom:0.2rem;}
.vocab-read{font-size:0.85rem;color:#e64a19;font-weight:700;
    background:#fff3e0;padding:2px 9px;border-radius:8px;
    display:inline-block;margin-bottom:0.4rem;}
.vocab-ko{font-size:0.88rem;font-weight:600;color:#37474f;margin-bottom:0.3rem;}
.vocab-ex{font-size:0.75rem;color:#607d8b;line-height:1.5;
    background:#f5f5f5;padding:5px 9px;border-radius:8px;font-style:italic;}
.vocab-badge{
    font-size:0.62rem;font-weight:700;color:#fff;
    background:linear-gradient(135deg,#26a69a,#00897b);
    padding:2px 8px;border-radius:12px;display:inline-block;margin-bottom:0.6rem;
}

/* ── 문법 패턴 카드 ── */
.grammar-card{
    background:#fff;border-radius:20px;
    padding:1.1rem 1rem 0.9rem;margin-bottom:0.8rem;
    box-shadow:0 3px 14px rgba(63,81,181,.1);
    border-left:5px solid #3f51b5;
    border-top:1.5px solid #e8eaf6;
    border-right:1.5px solid #e8eaf6;
    border-bottom:1.5px solid #e8eaf6;
}
.grammar-pattern{font-size:1.15rem;font-weight:900;color:#283593;margin-bottom:0.25rem;}
.grammar-meaning{font-size:0.8rem;color:#5c6bc0;font-weight:600;
    background:#e8eaf6;padding:2px 9px;border-radius:8px;
    display:inline-block;margin-bottom:0.55rem;}
.grammar-ex-jp{font-size:0.95rem;font-weight:700;color:#1a237e;margin-bottom:0.15rem;}
.grammar-ex-read{font-size:0.78rem;color:#e64a19;margin-bottom:0.15rem;font-weight:600;}
.grammar-ex-ko{font-size:0.78rem;color:#546e7a;margin-bottom:0.4rem;}
.grammar-tip{font-size:0.7rem;color:#7986cb;background:#f3f4ff;
    padding:4px 9px;border-radius:7px;line-height:1.5;}

/* ── 대화문 카드 ── */
.dialogue-wrap{
    background:#fff;border-radius:20px;padding:1rem;
    margin-bottom:1rem;box-shadow:0 3px 14px rgba(233,30,99,.09);
    border:1.5px solid #fce4ec;
}
.dialogue-title{
    font-size:0.8rem;font-weight:800;
    background:linear-gradient(135deg,#e91e63,#f06292);
    color:white;padding:4px 12px;border-radius:12px;
    display:inline-block;margin-bottom:0.8rem;
}
.dialogue-scene{
    font-size:0.7rem;color:#ad1457;background:#fce4ec;
    padding:3px 9px;border-radius:8px;margin-bottom:0.7rem;
    display:block;font-weight:600;
}
.d-row{display:flex;gap:0.5rem;margin-bottom:0.55rem;align-items:flex-start;}
.d-speaker-a{
    font-size:0.65rem;font-weight:800;color:#fff;
    background:#e91e63;padding:2px 7px;border-radius:10px;
    flex-shrink:0;margin-top:2px;white-space:nowrap;
}
.d-speaker-b{
    font-size:0.65rem;font-weight:800;color:#fff;
    background:#1976d2;padding:2px 7px;border-radius:10px;
    flex-shrink:0;margin-top:2px;white-space:nowrap;
}
.d-bubble-a{
    background:#fce4ec;border-radius:0 12px 12px 12px;
    padding:0.4rem 0.6rem;flex:1;
}
.d-bubble-b{
    background:#e3f2fd;border-radius:0 12px 12px 12px;
    padding:0.4rem 0.6rem;flex:1;
}
.d-jp{font-size:0.88rem;font-weight:700;color:#212121;margin-bottom:0.1rem;}
.d-read{font-size:0.72rem;color:#e64a19;font-weight:600;margin-bottom:0.1rem;}
.d-ko{font-size:0.72rem;color:#546e7a;}

/* ── 퀴즈 카드 ── */
.quiz-card{
    background:#fff;border-radius:22px;
    padding:1.3rem 1.1rem 1rem;margin-bottom:0.6rem;
    box-shadow:0 5px 20px rgba(156,39,176,.13);
    border:2px solid #f3e5f5;text-align:center;
}
.quiz-q-label{
    font-size:0.68rem;font-weight:700;color:#7b1fa2;
    background:#f3e5f5;padding:2px 10px;border-radius:12px;
    display:inline-block;margin-bottom:0.8rem;letter-spacing:0.4px;
}
.quiz-q-jp{font-size:1.5rem;font-weight:900;color:#1a1a2e;margin-bottom:0.3rem;}
.quiz-q-read{font-size:0.85rem;color:#e64a19;font-weight:700;margin-bottom:0.9rem;}
.quiz-score-box{
    background:linear-gradient(135deg,#9c27b0,#673ab7);
    color:white;border-radius:18px;padding:1rem 1.2rem;
    text-align:center;margin-bottom:0.8rem;
    box-shadow:0 4px 16px rgba(156,39,176,.35);
}
.quiz-opt-correct{background:#e8f5e9 !important;border:2px solid #43a047 !important;color:#1b5e20 !important;}
.quiz-opt-wrong{background:#ffebee !important;border:2px solid #e53935 !important;color:#b71c1c !important;}

/* ── 장바구니 ── */
.cart-card{
    background:#fff;border-radius:16px;padding:0.8rem 0.9rem;
    margin-bottom:0.65rem;box-shadow:0 2px 10px rgba(0,0,0,.06);
    border:1.5px solid #f5f5f5;display:flex;align-items:center;gap:0.7rem;
}
.cart-emoji{font-size:1.8rem;flex-shrink:0;}
.cart-info{flex:1;min-width:0;}
.cart-name{font-size:0.85rem;font-weight:700;color:#3d2010;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cart-rgn{font-size:0.65rem;color:#e65100;background:#fff3e0;
    padding:1px 6px;border-radius:8px;display:inline-block;
    margin:0.15rem 0;font-weight:600;}
.cart-price{font-size:0.72rem;color:#c0392b;font-weight:600;}
.cart-empty{text-align:center;padding:3rem 1rem 2rem;color:#c0a898;}
.cart-total{
    background:linear-gradient(135deg,#7c4dff,#e040fb);
    color:white;border-radius:18px;padding:1rem 1.1rem;
    text-align:center;margin-top:0.7rem;
    box-shadow:0 5px 18px rgba(124,77,255,.35);
}

/* ── 지역 배지 / 섹션 타이틀 ── */
.region-badge{
    background:linear-gradient(135deg,#e65100,#f57c00);
    color:white;padding:0.4rem 1rem;border-radius:20px;
    font-size:0.8rem;font-weight:700;display:inline-block;
    margin-bottom:0.9rem;box-shadow:0 3px 10px rgba(230,81,0,.3);
}
.sec-title{
    font-size:0.9rem;font-weight:800;color:#4a2e10;
    margin:0.9rem 0 0.55rem;display:flex;align-items:center;gap:0.35rem;
}
.level-badge{
    font-size:0.62rem;font-weight:700;
    background:linear-gradient(135deg,#ff7043,#ff5722);
    color:white;padding:2px 8px;border-radius:10px;
    display:inline-block;margin-left:0.3rem;vertical-align:middle;
}
hr{border:none !important;height:1px !important;
    background:linear-gradient(to right,transparent,#fad0c4 30%,#fad0c4 70%,transparent) !important;
    margin:0.8rem 0 !important;}

/* ── 삭제 버튼 작게 ── */
[data-testid="column"]:last-child .stButton>button{
    background:linear-gradient(135deg,#ef9a9a,#e57373) !important;
    font-size:0.9rem !important;padding:0.35rem 0.5rem !important;
    border-radius:50% !important;width:2.2rem !important;
    height:2.2rem !important;margin-top:0 !important;margin-bottom:0 !important;
    box-shadow:0 2px 6px rgba(229,115,115,.3) !important;
}

/* ── 카테고리 칩 ── */
.chip-row{display:flex;flex-wrap:wrap;gap:0.4rem;margin-bottom:0.8rem;}
.chip{
    font-size:0.72rem;font-weight:700;padding:4px 12px;
    border-radius:20px;cursor:pointer;border:2px solid transparent;
    display:inline-block;
}
.chip-active{
    background:linear-gradient(135deg,#26a69a,#00897b);
    color:white;border-color:#00897b;
}
.chip-inactive{background:#e0f2f1;color:#004d40;border-color:#b2dfdb;}

/* ── 진행 표시기 ── */
.progress-bar-wrap{
    background:#f5f5f5;border-radius:10px;height:8px;
    margin-bottom:0.6rem;overflow:hidden;
}
.progress-bar-fill{
    background:linear-gradient(90deg,#9c27b0,#e040fb);
    height:100%;border-radius:10px;transition:width .3s;
}

/* ── TTS 클릭 스타일 ── */
.speak-btn{cursor:pointer;transition:all 0.15s;display:inline-block;width:100%;}
.speak-btn:hover{opacity:0.75;transform:scale(0.985);}
.speak-btn:active{transform:scale(0.96);}
.tts-icon{
    font-size:0.72em;background:linear-gradient(135deg,#ff7043,#ff5722);
    color:white;padding:1px 6px;border-radius:8px;
    margin-left:6px;vertical-align:middle;opacity:0.9;
    font-style:normal;font-weight:700;letter-spacing:0.3px;
}
.tts-toast{
    position:fixed;bottom:80px;left:50%;transform:translateX(-50%);
    background:rgba(33,33,33,0.88);color:white;
    padding:6px 16px;border-radius:20px;font-size:0.75rem;
    z-index:9999;pointer-events:none;
    animation:fadeout 1.8s forwards;
}
@keyframes fadeout{0%{opacity:1;}70%{opacity:1;}100%{opacity:0;}}
</style>
""", unsafe_allow_html=True)

# ── TTS 함수를 부모 윈도우에 주입 (components.html → iframe → window.parent) ──
# Streamlit은 st.markdown의 <script>를 제거함 → components.html 우회 필수
components.html("""
<script>
(function(){
  var P = window.parent;
  if(!P || !P.speechSynthesis){ return; }

  // 보이스 미리 로드
  P.speechSynthesis.getVoices();
  P.speechSynthesis.onvoiceschanged = function(){ P.speechSynthesis.getVoices(); };

  // 전역 speakJP 함수 → 부모 윈도우에 등록
  P.speakJP = function(txt){
    P.speechSynthesis.cancel();
    var u = new P.SpeechSynthesisUtterance(txt);
    u.lang  = 'ja-JP';
    u.rate  = 0.82;
    u.pitch = 1.05;
    var voices = P.speechSynthesis.getVoices();
    var jv = voices.find(function(v){ return v.lang && v.lang.startsWith('ja'); });
    if(jv) u.voice = jv;
    P.speechSynthesis.speak(u);

    // 하단 토스트 표시
    var old = P.document.getElementById('_tts_toast');
    if(old) old.remove();
    var el = P.document.createElement('div');
    el.id = '_tts_toast';
    el.style.cssText = [
      'position:fixed','bottom:76px','left:50%',
      'transform:translateX(-50%)',
      'background:rgba(30,30,30,0.9)','color:#fff',
      'padding:7px 18px','border-radius:22px',
      'font-size:0.78rem','font-weight:600',
      'z-index:99999','pointer-events:none',
      'box-shadow:0 4px 14px rgba(0,0,0,0.35)',
      'transition:opacity 0.4s'
    ].join(';');
    el.textContent = '🔊  ' + txt.slice(0,22) + (txt.length > 22 ? '…' : '');
    P.document.body.appendChild(el);
    setTimeout(function(){ el.style.opacity='0'; }, 1600);
    setTimeout(function(){ if(el.parentNode) el.remove(); }, 2100);
  };
})();
</script>
""", height=0)

# ============================================================
# 4. 데이터 — 쇼핑 핫템
# ============================================================
SHOPPING_DATA = {
    "🗼 도쿄 (Tokyo)": [
        {"emoji":"🍮","name":"넘버슈가 카라멜","brand":"NUMBER SUGAR",
         "desc":"소금·말차·홍차 등 12가지 수제 캐러멜. 고급 박스 패키징. 1개씩 낱개 시식 가능.",
         "price":"약 ¥1,620 (10개입)","where":"📍 이세탄 신주쿠 B1 · 다카시마야 시부야",
         "tip":"💡 소금·캬라멜 맛 오픈 즉시 매진. 주말 정오 전 방문!"},
        {"emoji":"🍌","name":"도쿄 바나나","brand":"TOKYO BANANA",
         "desc":"바나나 크림을 채운 스펀지 케이크. 기간 한정 콜라보 버전도 상시 출시.",
         "price":"약 ¥980 (8개입)","where":"📍 도쿄역 그란스타 · 하네다·나리타 공항",
         "tip":"💡 유통기한 5일. 귀국 직전 공항 구매가 가장 신선!"},
        {"emoji":"🧴","name":"SK-II 페이셜 트리트먼트 에센스","brand":"SK-II",
         "desc":"피테라 성분 명품 화장수. 일본 면세가 한국 정가보다 20~30% 저렴.",
         "price":"약 ¥16,000 (230ml 면세가)","where":"📍 긴자·신주쿠·시부야 면세점",
         "tip":"💡 ¥5,500 이상 구매 시 소비세(10%) 환급. 여권 원본 필수!"},
        {"emoji":"🎌","name":"유니클로 한정판 UT","brand":"UNIQLO Japan",
         "desc":"일본 현지 한정 아티스트 컬래버 티셔츠. 한국 미출시 디자인 다수.",
         "price":"약 ¥1,500~2,500","where":"📍 긴자 유니클로 글로벌 플래그십 12층",
         "tip":"💡 일본 사이즈 한국보다 1단계 작음. XL이면 XXL 권장."},
        {"emoji":"🍜","name":"닛신 한정판 컵라멘 세트","brand":"日清食品",
         "desc":"요코하마 컵누들 뮤지엄 한정 패키지 & 지역 限定 맛. DIY 컵 제작 체험 가능.",
         "price":"약 ¥500~2,500","where":"📍 돈키호테 · 이온몰 · 요코하마 컵누들 뮤지엄",
         "tip":"💡 봉지면 버전으로 여러 맛 사는 게 가성비 최고!"},
    ],
    "🏯 오사카 (Osaka)": [
        {"emoji":"🥟","name":"551 호라이 찐만두","brand":"551 蓬莱",
         "desc":"오사카 소울 푸드. 돼지고기+파 가득한 점보 찐만두. 60년 전통 명가.",
         "price":"약 ¥670 (6개입)","where":"📍 신사이바시 · 난바 · 우메다 · 오사카 공항",
         "tip":"💡 냉동 제품도 판매. 공항 매장에서 아이스팩과 함께 구매 가능!"},
        {"emoji":"🏷️","name":"한큐백화점 한정 손수건","brand":"阪急百貨店",
         "desc":"마리메꼬·호레이 등 컬래버 한정 디자인. 가볍고 포장 예뻐 선물 최적.",
         "price":"약 ¥1,000~3,500","where":"📍 한큐 우메다 본점 1F 손수건 코너",
         "tip":"💡 5장 이상 구매 시 선물 세트 박스 무료 제공!"},
        {"emoji":"🍪","name":"오사카 버터 밀크 쿠키","brand":"大阪土産菓子",
         "desc":"오사카 한정 바삭 버터 쿠키. 소량~대용량 선물 세트 다양.",
         "price":"약 ¥1,200~3,000","where":"📍 신사이바시스지 상점가 · 나카자키초",
         "tip":"💡 유통기한 30일, 상온 보관 가능해 대량 구매 추천."},
        {"emoji":"🧴","name":"마츠키요 가성비 화장품","brand":"DHC / Canmake / KOSE",
         "desc":"DHC 클렌징오일·캔메이크 쿠션·KOSE 마스크팩. 한국보다 20~40% 저렴.",
         "price":"약 ¥500~3,000","where":"📍 마츠모토 키요시 · 코코카라파인 · 돈키호테",
         "tip":"💡 포인트 카드 발급 + 외국인 면세 카운터 적극 활용!"},
        {"emoji":"🐙","name":"타코야키 홈 메이커 세트","brand":"イワタニ",
         "desc":"이와타니 타코야키 전용 기계+믹스 가루 세트. 집에서 정통 오사카 타코야키 재현.",
         "price":"약 ¥2,500~5,500","where":"📍 도구야스지 상점가 · 빅카메라 난바점",
         "tip":"💡 이와타니 가스 타입은 전압 무관. 일반 전기식은 변압기 확인!"},
    ],
    "🌊 후쿠오카 (Fukuoka)": [
        {"emoji":"🐟","name":"후쿠사야 명란 마요네즈","brand":"ふくさや",
         "desc":"후쿠오카 발 명란 마요네즈. 주먹밥·파스타에 뿌리면 감동. 냉장 보관 필수.",
         "price":"약 ¥750~1,200","where":"📍 후쿠오카 공항 면세점 · 캐널시티 · 하카타역",
         "tip":"💡 아이스팩 요청 가능. 귀국 당일 아침 구매가 포인트!"},
        {"emoji":"🐣","name":"히요코 병아리 과자","brand":"ひよ子本舗吉野堂",
         "desc":"병아리 모양 콩소 앙금 화과자. 1927년 창업 후쿠오카 원조 명과.",
         "price":"약 ¥1,000~2,500","where":"📍 하카타역 · 후쿠오카 공항 · 캐널시티 B1",
         "tip":"💡 도쿄에서도 팔지만 후쿠오카가 원조. 패키지 디자인도 달라요!"},
        {"emoji":"🍜","name":"이치란 라멘 테이크아웃 세트","brand":"一蘭",
         "desc":"이치란 오리지널 소스+면 세트. 집에서 하카타 돈코츠 풍미 완벽 재현.",
         "price":"약 ¥1,800~3,500","where":"📍 이치란 나카스점 기념품 카운터 · 하카타역",
         "tip":"💡 매장 내 카운터에서만 구매 가능. 온라인·해외 배송 불가!"},
        {"emoji":"👘","name":"하카타 전통 공예 기념품","brand":"博多人形 / 博多織",
         "desc":"하카타 직물 소품·하카타 인형. 후쿠오카 700년 전통 공예.",
         "price":"약 ¥1,500~15,000","where":"📍 하카타 마찌야 후루사토관 · 캐널시티 공예관",
         "tip":"💡 윗사람 선물로 품격 최고. 포장도 정성스러움."},
        {"emoji":"🥩","name":"모츠나베 곱창 재료 세트","brand":"楽天地 / やま中",
         "desc":"모츠나베 전용 牛 곱창+된장·간장 국물 소스 세트. 집에서 나베 파티 가능.",
         "price":"약 ¥2,000~4,500","where":"📍 야마야 슈퍼 · 암즈 백화점 B1",
         "tip":"💡 드라이아이스 포장 요청 가능. 24시간 이내 소비 권장."},
    ],
}

# ============================================================
# 5. 데이터 — 쇼핑 치트키 문장
# ============================================================
PHRASES = [
    {"situation":"💳 카드 결제","japanese":"カードで払えますか？",
     "reading":"카도데 하라에마스카？","korean":"카드로 결제할 수 있나요?",
     "tip":"소규모 점포·포장마차는 현금만 가능하기도 함. 미리 확인 필수!"},
    {"situation":"🛍️ 봉투 요청","japanese":"袋をいただけますか？",
     "reading":"후쿠로오 이타다케마스카？","korean":"봉투를 주실 수 있나요?",
     "tip":"일본은 봉투 유료(¥3~5). 에코백 챙기면 절약!"},
    {"situation":"🎁 선물 포장","japanese":"ギフト包装をお願いします",
     "reading":"기후토 호소오오 오네가이시마스","korean":"선물 포장 부탁드립니다",
     "tip":"백화점은 대부분 무료. 리본 색·한지 패턴도 선택 가능."},
    {"situation":"🚫 면세 신청","japanese":"免税手続きをお願いします",
     "reading":"멘제이 테츠즈키오 오네가이시마스","korean":"면세 처리 부탁드립니다",
     "tip":"¥5,500 이상(소비세 포함) 구매 시 가능. 여권 원본 필수!"},
    {"situation":"💰 가격 문의","japanese":"これはいくらですか？",
     "reading":"코레와 이쿠라데스카？","korean":"이것은 얼마인가요?",
     "tip":"못 알아들으면: 「電卓を見せてください」(덴타쿠오 미세테 쿠다사이) = 계산기 보여주세요"},
    {"situation":"🔍 재고 확인","japanese":"在庫はありますか？",
     "reading":"자이코와 아리마스카？","korean":"재고가 있나요?",
     "tip":"사이즈 다를 때: 「Sサイズはありますか？」(S 사이즈와 아리마스카？)"},
    {"situation":"🔄 교환 요청","japanese":"交換できますか？",
     "reading":"코칸 데키마스카？","korean":"교환 가능한가요?",
     "tip":"영수증(領収書 레시우쇼) 필수. 교환 기간 내에만 가능."},
    {"situation":"📦 호텔 배송","japanese":"ホテルに配送できますか？",
     "reading":"호테루니 하이소오 데키마스카？","korean":"호텔로 배송 가능한가요?",
     "tip":"야마토 택배(クロネコヤマト) 활용하면 짐이 훨씬 가벼워짐!"},
    {"situation":"🤏 가격 흥정","japanese":"もう少し安くなりますか？",
     "reading":"모오 스코시 야스쿠 나리마스카？","korean":"조금 더 싸게 해주실 수 있나요?",
     "tip":"백화점·편의점은 정가제. 상점가·개인 가게에서만 시도 가능."},
    {"situation":"🏃 급할 때","japanese":"急いでいます",
     "reading":"이소이데 이마스","korean":"저 급합니다",
     "tip":"공항 이동 직전 계산 서두를 때 유용. 점원이 우선 처리해줌."},
    {"situation":"🙏 마무리 인사","japanese":"ありがとうございました！",
     "reading":"아리가토오 고자이마시타！","korean":"감사했습니다!",
     "tip":"계산 후 꼭 한마디! 일본인 점원이 정말 좋아함 ☺"},
]

# ============================================================
# 6. 데이터 — 어휘 (중급자 N3~N4 여행 필수 단어)
# ============================================================
VOCAB = {
    "쇼핑": [
        {"jp":"割引","read":"わりびき (와리비키)","ko":"할인","ex":"割引はありますか？ (할인 있나요?)"},
        {"jp":"領収書","read":"りょうしゅうしょ (료슈쇼)","ko":"영수증","ex":"領収書をください。 (영수증 주세요.)"},
        {"jp":"試着","read":"しちゃく (시챠쿠)","ko":"시착/피팅","ex":"試着してもいいですか？ (입어봐도 되나요?)"},
        {"jp":"売り切れ","read":"うりきれ (우리키레)","ko":"품절/매진","ex":"もう売り切れです。 (이미 품절입니다.)"},
        {"jp":"限定品","read":"げんていひん (겐테이힌)","ko":"한정품","ex":"これは限定品ですか？ (이건 한정품인가요?)"},
        {"jp":"送料","read":"そうりょう (소료)","ko":"배송비","ex":"送料はいくらですか？ (배송비는 얼마예요?)"},
        {"jp":"ポイントカード","read":"포인토카도","ko":"포인트카드","ex":"ポイントカードはお持ちですか？ (포인트카드 있으세요?)"},
        {"jp":"免税","read":"めんぜい (멘제이)","ko":"면세","ex":"免税できますか？ (면세 되나요?)"},
    ],
    "식당": [
        {"jp":"おすすめ","read":"오스스메","ko":"추천 메뉴","ex":"おすすめは何ですか？ (추천은 뭔가요?)"},
        {"jp":"辛い","read":"からい (카라이)","ko":"맵다","ex":"辛くしないでください。 (맵지 않게 해주세요.)"},
        {"jp":"アレルギー","read":"아레루기","ko":"알레르기","ex":"えびアレルギーがあります。 (새우 알레르기가 있어요.)"},
        {"jp":"お会計","read":"おかいけい (오카이케이)","ko":"계산서","ex":"お会計をお願いします。 (계산 부탁드립니다.)"},
        {"jp":"禁煙席","read":"きんえんせき (킨엔세키)","ko":"금연석","ex":"禁煙席をお願いします。 (금연석 부탁드립니다.)"},
        {"jp":"持ち帰り","read":"もちかえり (모치카에리)","ko":"포장/테이크아웃","ex":"持ち帰りでお願いします。 (포장으로 부탁드립니다.)"},
        {"jp":"定食","read":"ていしょく (테이쇼쿠)","ko":"정식/세트 메뉴","ex":"Aランチ定食をください。 (A런치 정식 주세요.)"},
        {"jp":"おかわり","read":"오카와리","ko":"리필/추가","ex":"おかわりできますか？ (리필 가능한가요?)"},
    ],
    "교통": [
        {"jp":"乗り換え","read":"のりかえ (노리카에)","ko":"환승","ex":"どこで乗り換えますか？ (어디서 환승하나요?)"},
        {"jp":"終電","read":"しゅうでん (슈덴)","ko":"막차","ex":"終電は何時ですか？ (막차는 몇 시예요?)"},
        {"jp":"ICカード","read":"아이씨카도","ko":"교통카드(스이카 등)","ex":"ICカードで乗れますか？ (교통카드로 탈 수 있나요?)"},
        {"jp":"回数券","read":"かいすうけん (카이스우켄)","ko":"회수권","ex":"回数券はありますか？ (회수권 있나요?)"},
        {"jp":"渋滞","read":"じゅうたい (주타이)","ko":"교통 체증","ex":"渋滞で遅れています。 (교통 체증으로 늦고 있어요.)"},
        {"jp":"タクシー乗り場","read":"타쿠시 노리바","ko":"택시 승강장","ex":"タクシー乗り場はどこですか？ (택시 승강장 어딘가요?)"},
        {"jp":"特急","read":"とっきゅう (토큐)","ko":"특급 열차","ex":"特急券が必要ですか？ (특급권이 필요한가요?)"},
        {"jp":"運賃","read":"うんちん (운친)","ko":"운임/요금","ex":"運賃はいくらですか？ (요금은 얼마예요?)"},
    ],
    "숙박": [
        {"jp":"チェックイン","read":"체쿠인","ko":"체크인","ex":"チェックインをお願いします。 (체크인 부탁드립니다.)"},
        {"jp":"禁煙ルーム","read":"킨엔 루무","ko":"금연 객실","ex":"禁煙ルームを予約しました。 (금연 객실 예약했습니다.)"},
        {"jp":"アメニティ","read":"아메니티","ko":"어메니티","ex":"アメニティをもらえますか？ (어메니티 받을 수 있나요?)"},
        {"jp":"連泊","read":"れんぱく (렌파쿠)","ko":"연박","ex":"連泊したいのですが。 (연박하고 싶은데요.)"},
        {"jp":"布団","read":"ふとん (후톤)","ko":"이불/요","ex":"布団を追加してください。 (이불 추가해 주세요.)"},
        {"jp":"フロント","read":"후론토","ko":"프런트/리셉션","ex":"フロントに電話してください。 (프런트에 전화해 주세요.)"},
        {"jp":"部屋のカギ","read":"헤야노 카기","ko":"방 열쇠","ex":"カギをなくしてしまいました。 (열쇠를 잃어버렸습니다.)"},
        {"jp":"モーニングコール","read":"모닝구 코루","ko":"모닝콜","ex":"7時にモーニングコールをお願いします。 (7시에 모닝콜 부탁드립니다.)"},
    ],
    "긴급": [
        {"jp":"助けてください","read":"たすけてください (타스케테 쿠다사이)","ko":"도와주세요!","ex":"誰か助けてください！ (누구 좀 도와주세요!)"},
        {"jp":"救急車","read":"きゅうきゅうしゃ (큐큐샤)","ko":"구급차","ex":"救急車を呼んでください！ (구급차 불러주세요!)"},
        {"jp":"警察","read":"けいさつ (케이사츠)","ko":"경찰","ex":"警察を呼んでください。 (경찰 불러주세요.)"},
        {"jp":"財布を盗まれました","read":"사이후오 누스마레마시타","ko":"지갑을 도둑맞았습니다","ex":"財布を盗まれました！ (지갑을 도둑맞았어요!)"},
        {"jp":"迷子","read":"まいご (마이고)","ko":"미아/길을 잃음","ex":"迷子になりました。 (길을 잃었어요.)"},
        {"jp":"病院","read":"びょういん (뵤인)","ko":"병원","ex":"近くに病院はありますか？ (근처에 병원 있나요?)"},
        {"jp":"薬局","read":"やっきょく (약쿄쿠)","ko":"약국","ex":"薬局はどこですか？ (약국은 어디인가요?)"},
        {"jp":"アレルギー反応","read":"아레루기 한노","ko":"알레르기 반응","ex":"アレルギー反応が出ています。 (알레르기 반응이 나타나고 있어요.)"},
    ],
}

# ============================================================
# 7. 데이터 — 중급 문법 패턴 (N4~N3)
# ============================================================
GRAMMAR = [
    {"pattern":"〜てみる","meaning":"(한번) 해보다","level":"N4",
     "ex_jp":"このお菓子を食べてみてください。","ex_read":"코노 오카시오 타베테 미테 쿠다사이。",
     "ex_ko":"이 과자를 먹어보세요.","tip":"시도·경험을 권할 때 가장 자주 쓰는 패턴. 쇼핑몰 시식대에서 꼭 쓰임."},
    {"pattern":"〜てもいいですか","meaning":"~해도 되나요?","level":"N4",
     "ex_jp":"写真を撮ってもいいですか？","ex_read":"샤신오 톳테모 이이데스카？",
     "ex_ko":"사진 찍어도 되나요?","tip":"허가를 구할 때 핵심 패턴. 試着(시착), 触る(만지기) 앞에 붙여 사용."},
    {"pattern":"〜なければなりません","meaning":"~해야 합니다 (의무)","level":"N4",
     "ex_jp":"パスポートを見せなければなりません。","ex_read":"파스포오토오 미세나케레바 나리마센。",
     "ex_ko":"여권을 보여줘야 합니다.","tip":"면세 처리 시 자주 쓰임. 회화에서는 〜ないといけない가 더 자연스러움."},
    {"pattern":"〜ことができる","meaning":"~할 수 있다 (능력/가능)","level":"N4",
     "ex_jp":"日本語を話すことができます。","ex_read":"니혼고오 하나스 코토가 데키마스。",
     "ex_ko":"일본어를 말할 수 있습니다.","tip":"중급자라면 できる 단독보다 이 패턴으로 격식 있게 표현해 보세요."},
    {"pattern":"〜たことがある","meaning":"~한 적이 있다 (경험)","level":"N4",
     "ex_jp":"一蘭に行ったことがありますか？","ex_read":"이치란니 잇타 코토가 아리마스카？",
     "ex_ko":"이치란에 간 적이 있나요?","tip":"여행 중 현지인과 경험 대화할 때 자연스러운 패턴."},
    {"pattern":"〜ながら","meaning":"~하면서 (동시 동작)","level":"N4",
     "ex_jp":"音楽を聴きながら歩きます。","ex_read":"온가쿠오 키키나가라 아루키마스。",
     "ex_ko":"음악을 들으면서 걷습니다.","tip":"쇼핑하면서(ショッピングしながら) 자주 쓰임."},
    {"pattern":"〜てしまう","meaning":"~해버리다 (완료/후회)","level":"N3",
     "ex_jp":"つい買いすぎてしまいました。","ex_read":"츠이 카이스기테 시마이마시타。",
     "ex_ko":"그만 너무 많이 사버렸어요.","tip":"충동구매 후 한마디로 딱! 일본인들이 공감하며 웃어줌."},
    {"pattern":"〜らしい","meaning":"~인 것 같다 (추측·소문)","level":"N3",
     "ex_jp":"このブランドは人気らしいですよ。","ex_read":"코노 부란도와 닌키 라시이데스요。",
     "ex_ko":"이 브랜드는 인기 있는 것 같아요.","tip":"정보를 전달하거나 들은 소문을 말할 때. 〜そうだ보다 확신이 낮음."},
    {"pattern":"〜はずだ","meaning":"~일 것이다 (확신 있는 추측)","level":"N3",
     "ex_jp":"ここに売っているはずです。","ex_read":"코코니 우텟테 이루 하즈데스。",
     "ex_ko":"여기에 팔고 있을 텐데요.","tip":"사전 조사 기반의 확신 표현. 길 찾거나 매장 찾을 때 자주 씀."},
    {"pattern":"〜ために","meaning":"~을 위해 / ~하기 위해","level":"N3",
     "ex_jp":"お土産のために買いました。","ex_read":"오미야게노 타메니 카이마시타。",
     "ex_ko":"기념품을 위해 샀습니다.","tip":"목적을 명확히 말할 때. 면세 창구에서 '선물용(プレゼントのために)'으로 활용!"},
    {"pattern":"〜ば〜ほど","meaning":"~하면 할수록","level":"N3",
     "ex_jp":"食べれば食べるほど美味しい！","ex_read":"타베레바 타베루 호도 오이시이！",
     "ex_ko":"먹으면 먹을수록 맛있어요!","tip":"일본 음식 칭찬할 때 찰떡 패턴. 현지인들이 정말 좋아함."},
    {"pattern":"〜かもしれない","meaning":"~일지도 모른다 (불확실 추측)","level":"N3",
     "ex_jp":"売り切れかもしれません。","ex_read":"우리키레 카모 시레마센。",
     "ex_ko":"품절일지도 모릅니다.","tip":"불확실한 정보를 부드럽게 전달할 때. 정중한 불확실성 표현."},
]

# ============================================================
# 8. 데이터 — 여행 대화문 시나리오
# ============================================================
DIALOGUES = [
    {
        "title":"🏨 호텔 체크인","scene":"📍 호텔 프런트 | A = 나(여행자), B = 직원",
        "lines":[
            {"spk":"A","jp":"チェックインをお願いします。山田の名前で予約しています。",
             "read":"체쿠인오 오네가이시마스。야마다노 나마에데 요야쿠시테 이마스。",
             "ko":"체크인 부탁드립니다. 야마다 이름으로 예약했습니다."},
            {"spk":"B","jp":"はい、少々お待ちください。パスポートをお見せいただけますか？",
             "read":"하이, 쇼쇼 오마치 쿠다사이。파스포오토오 오미세 이타다케마스카？",
             "ko":"네, 잠시만 기다려 주세요. 여권을 보여주실 수 있나요?"},
            {"spk":"A","jp":"はい、どうぞ。朝食は付いていますか？",
             "read":"하이, 도조。쵸쇼쿠와 츠이테 이마스카？",
             "ko":"네, 여기요. 조식은 포함되어 있나요?"},
            {"spk":"B","jp":"はい、7時から10時まで1階のレストランでお召し上がりいただけます。",
             "read":"하이, 시치지카라 주지마데 잇카이노 레스토란데 오메시아가리 이타다케마스。",
             "ko":"네, 7시부터 10시까지 1층 레스토랑에서 드실 수 있습니다."},
            {"spk":"A","jp":"ありがとうございます。Wi-Fiのパスワードも教えていただけますか？",
             "read":"아리가토오 고자이마스。와이파이노 파스와도모 오시에테 이타다케마스카？",
             "ko":"감사합니다. 와이파이 비밀번호도 알려주실 수 있나요?"},
        ]
    },
    {
        "title":"🍜 레스토랑 주문","scene":"📍 이자카야·라멘 가게 | A = 나, B = 점원",
        "lines":[
            {"spk":"B","jp":"いらっしゃいませ！何名様ですか？",
             "read":"이랏샤이마세！난메이사마데스카？",
             "ko":"어서오세요! 몇 분이세요?"},
            {"spk":"A","jp":"2名です。禁煙席をお願いしたいのですが。",
             "read":"니메이데스。킨엔세키오 오네가이시타이노데스가。",
             "ko":"2명입니다. 금연석으로 부탁드리고 싶은데요."},
            {"spk":"B","jp":"かしこまりました。こちらへどうぞ。ご注文はお決まりですか？",
             "read":"카시코마리마시타。코치라에 도조。고추문와 오키마리데스카？",
             "ko":"알겠습니다. 이쪽으로 오세요. 주문은 결정하셨나요?"},
            {"spk":"A","jp":"おすすめは何ですか？辛いものは苦手なんですが。",
             "read":"오스스메와 난데스카？카라이 모노와 니가테난데스가。",
             "ko":"추천은 뭔가요? 매운 것을 잘 못하는데요."},
            {"spk":"B","jp":"では、塩ラーメンはいかがですか？あっさりしていて人気ですよ。",
             "read":"데와, 시오 라멘와 이카가데스카？앗사리 시테이테 닌키데스요。",
             "ko":"그러면 소금 라멘은 어떠세요? 담백하고 인기 있어요."},
            {"spk":"A","jp":"それにします！あと、餃子も一つ。お会計はカードで払えますか？",
             "read":"소레니 시마스！앗토, 교자모 히토츠。오카이케이와 카도데 하라에마스카？",
             "ko":"그걸로 할게요! 그리고 교자도 하나. 계산은 카드로 가능한가요?"},
        ]
    },
    {
        "title":"🛍️ 백화점 쇼핑·면세","scene":"📍 백화점 화장품 코너 | A = 나, B = 점원",
        "lines":[
            {"spk":"A","jp":"すみません、このファンデーションのサンプルを試してもいいですか？",
             "read":"스미마센, 코노 판데이션노 산푸루오 타메시테모 이이데스카？",
             "ko":"저기요, 이 파운데이션 샘플을 시험해봐도 되나요?"},
            {"spk":"B","jp":"もちろんです！こちらのお色はいかがですか？",
             "read":"모치론데스！코치라노 오이로와 이카가데스카？",
             "ko":"물론이죠! 이 색상은 어떠세요?"},
            {"spk":"A","jp":"いいですね。これを2つください。免税手続きもお願いしたいのですが。",
             "read":"이이데스네。코레오 후타츠 쿠다사이。멘제이 테츠즈키모 오네가이시타이노데스가。",
             "ko":"좋네요. 이것 2개 주세요. 면세 처리도 부탁드리고 싶은데요."},
            {"spk":"B","jp":"はい！パスポートをお見せいただけますか？5,500円以上のお買い上げで免税になります。",
             "read":"하이！파스포오토오 오미세 이타다케마스카？고센 고햐쿠엔 이조노 오카이아게데 멘제이니 나리마스。",
             "ko":"네! 여권을 보여주실 수 있나요? 5,500엔 이상 구매 시 면세가 됩니다."},
            {"spk":"A","jp":"はい、どうぞ。あと、ギフト包装もお願いできますか？",
             "read":"하이, 도조。앗토, 기후토 호소오모 오네가이 데키마스카？",
             "ko":"네, 여기요. 그리고 선물 포장도 부탁드릴 수 있나요?"},
            {"spk":"B","jp":"承知しました！少々お時間をいただきます。",
             "read":"쇼치 시마시타！쇼쇼 오지칸오 이타다키마스。",
             "ko":"알겠습니다! 잠시 시간이 걸립니다."},
        ]
    },
    {
        "title":"🚉 길 찾기·교통","scene":"📍 지하철역 | A = 나, B = 역무원",
        "lines":[
            {"spk":"A","jp":"すみません、新宿駅に行きたいのですが、どの電車に乗ればいいですか？",
             "read":"스미마센, 신주쿠에키니 이키타이노데스가, 도노 덴샤니 노레바 이이데스카？",
             "ko":"저기요, 신주쿠역에 가고 싶은데, 어떤 전철을 타면 되나요?"},
            {"spk":"B","jp":"山手線に乗って、新宿で降りてください。3番線です。",
             "read":"야마노테센니 놋테, 신주쿠데 오리테 쿠다사이。산반센데스。",
             "ko":"야마노테선을 타고 신주쿠에서 내리세요. 3번 승강장입니다."},
            {"spk":"A","jp":"乗り換えは必要ですか？",
             "read":"노리카에와 히츠요데스카？",
             "ko":"환승은 필요한가요?"},
            {"spk":"B","jp":"いいえ、直通です。約15分かかります。",
             "read":"이이에, 쵸쯔데스。야쿠 주고훈 카카리마스。",
             "ko":"아니요, 직통입니다. 약 15분 걸립니다."},
            {"spk":"A","jp":"ICカードで乗れますか？",
             "read":"아이씨카도데 노레마스카？",
             "ko":"교통카드(IC카드)로 탈 수 있나요?"},
            {"spk":"B","jp":"はい、もちろんです。ICカードをタッチして改札を通ってください。",
             "read":"하이, 모치론데스。아이씨카도오 탓치시테 카이사츠오 토오테 쿠다사이。",
             "ko":"네, 물론이죠. IC카드를 터치하고 개찰구를 통과하세요."},
        ]
    },
    {
        "title":"🏥 긴급 상황","scene":"📍 응급 상황 | A = 나, B = 행인/직원",
        "lines":[
            {"spk":"A","jp":"すみません！助けてください！財布を盗まれてしまいました！",
             "read":"스미마센！타스케테 쿠다사이！사이후오 누스마레테 시마이마시타！",
             "ko":"저기요! 도와주세요! 지갑을 도둑맞아버렸어요!"},
            {"spk":"B","jp":"大丈夫ですか？すぐに警察を呼びましょう。",
             "read":"다이죠부데스카？스구니 케이사츠오 요비마쇼。",
             "ko":"괜찮으세요? 바로 경찰을 부릅시다."},
            {"spk":"A","jp":"ありがとうございます。日本語がまだうまくないので、英語で話せますか？",
             "read":"아리가토오 고자이마스。니혼고가 마다 우마쿠나이노데, 에이고데 하나세마스카？",
             "ko":"감사합니다. 일본어를 아직 잘 못해서요, 영어로 말할 수 있나요?"},
            {"spk":"B","jp":"少しだけ。近くの交番に一緒に行きましょう。",
             "read":"스코시다케。치카쿠노 코반니 잇쇼니 이키마쇼。",
             "ko":"조금만요. 근처 파출소에 같이 갑시다."},
            {"spk":"A","jp":"本当にありがとうございます。助かりました。",
             "read":"혼토니 아리가토오 고자이마스。타스카리마시타。",
             "ko":"정말 감사합니다. 살았습니다."},
        ]
    },
]

# ============================================================
# 9. 데이터 — 퀴즈 문제 풀 (어휘 기반)
# ============================================================
def build_quiz_pool():
    """모든 카테고리 어휘에서 퀴즈 문제 생성"""
    pool = []
    all_vocab = []
    for cat, words in VOCAB.items():
        for w in words:
            all_vocab.append({"cat": cat, **w})

    for i, item in enumerate(all_vocab):
        # 오답 보기 3개 뽑기 (같은 단어가 아닌 것)
        wrong_pool = [w["ko"] for j, w in enumerate(all_vocab) if j != i]
        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = wrongs + [item["ko"]]
        random.shuffle(options)
        pool.append({
            "q_jp": item["jp"],
            "q_read": item["read"],
            "answer": item["ko"],
            "options": options,
            "category": item["cat"],
            "example": item["ex"],
        })
    random.shuffle(pool)
    return pool

if not st.session_state.quiz_pool:
    st.session_state.quiz_pool = build_quiz_pool()

# ============================================================
# 10. BGM 옵션
# ============================================================
BGM_OPTIONS = {
    "🌸 잔잔한 Lo-fi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🎋 감성 앰비언트": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    "🍜 경쾌한 팝 리듬": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "🎐 여유로운 어쿠스틱": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
}

# ============================================================
# 11. UI 렌더링 시작
# ============================================================

# ── 헤더 ────────────────────────────────────────────────────
st.markdown("""
<div class="app-title">🇯🇵 일본어 1일 마스터</div>
<div class="app-sub">Japan Shopping &amp; 일본어 완전정복 — 중급자 맞춤판</div>
""", unsafe_allow_html=True)

# ── BGM ─────────────────────────────────────────────────────
st.markdown('<div class="bgm-box"><div class="bgm-label">🎵 여행 BGM — 선택 후 ▶ 클릭!</div>', unsafe_allow_html=True)
bgm_sel = st.selectbox("BGM", list(BGM_OPTIONS.keys()), label_visibility="collapsed")
_bgm_url = BGM_OPTIONS[bgm_sel]
components.html(f"""
<style>
  .bgm-player {{
    display:flex;align-items:center;gap:10px;
    background:linear-gradient(135deg,#f3e5f5,#e8eaf6);
    border-radius:14px;padding:8px 14px;margin-top:6px;
    border:1.5px solid #d1c4e9;
  }}
  .bgm-btn {{
    background:linear-gradient(135deg,#9c27b0,#673ab7);
    color:white;border:none;border-radius:50%;
    width:40px;height:40px;font-size:1.1rem;
    cursor:pointer;flex-shrink:0;
    box-shadow:0 3px 10px rgba(156,39,176,.4);
    display:flex;align-items:center;justify-content:center;
  }}
  .bgm-btn:hover{{background:linear-gradient(135deg,#7b1fa2,#512da8);}}
  .bgm-title {{
    font-size:0.8rem;font-weight:700;color:#4a148c;
    font-family:'Noto Sans KR',sans-serif;flex:1;
  }}
  .bgm-status {{font-size:0.68rem;color:#7986cb;margin-top:2px;}}
  input[type=range]{{width:100%;accent-color:#9c27b0;}}
</style>
<div class="bgm-player">
  <button class="bgm-btn" onclick="togglePlay()" id="btn">▶</button>
  <div style="flex:1;min-width:0;">
    <div class="bgm-title">{bgm_sel}</div>
    <div class="bgm-status" id="status">재생 버튼을 눌러주세요</div>
    <input type="range" id="seek" value="0" step="1" style="margin-top:4px;">
  </div>
  <span style="font-size:0.72rem;color:#7986cb;" id="time">0:00</span>
</div>
<audio id="audio" loop preload="auto">
  <source src="{_bgm_url}" type="audio/mpeg">
</audio>
<script>
  var audio = document.getElementById('audio');
  var btn   = document.getElementById('btn');
  var seek  = document.getElementById('seek');
  var status= document.getElementById('status');
  var timeEl= document.getElementById('time');

  function fmt(s){{
    var m=Math.floor(s/60),sec=Math.floor(s%60);
    return m+':'+(sec<10?'0':'')+sec;
  }}

  function togglePlay(){{
    if(audio.paused){{
      audio.play().then(function(){{
        btn.textContent='⏸';
        status.textContent='재생 중 🎵';
      }}).catch(function(e){{
        status.textContent='재생 실패: '+e.message;
      }});
    }}else{{
      audio.pause();
      btn.textContent='▶';
      status.textContent='일시정지';
    }}
  }}

  audio.addEventListener('timeupdate',function(){{
    if(audio.duration){{
      seek.max=Math.floor(audio.duration);
      seek.value=Math.floor(audio.currentTime);
      timeEl.textContent=fmt(audio.currentTime)+' / '+fmt(audio.duration);
    }}
  }});

  seek.addEventListener('input',function(){{
    audio.currentTime=seek.value;
  }});
</script>
""", height=100)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ── 탭 (5개) ─────────────────────────────────────────────────
tab_shop, tab_vocab, tab_grammar, tab_dial, tab_quiz, tab_phrase, tab_cart = st.tabs([
    "🛍️ 쇼핑핫템",
    "📖 어휘마스터",
    "📚 문법패턴",
    "💬 대화문",
    "🧠 퀴즈",
    "🗣️ 치트키",
    f"🧺 장바구니({len(st.session_state.cart)})",
])

# ============================================================
# TAB 1 — 지역별 쇼핑 핫템
# ============================================================
with tab_shop:
    st.markdown('<div class="sec-title">📍 여행 지역 선택</div>', unsafe_allow_html=True)
    region = st.selectbox("지역", list(SHOPPING_DATA.keys()), label_visibility="collapsed")
    items = SHOPPING_DATA[region]
    st.markdown(f'<div class="region-badge">✈️ {region} — 필수 쇼핑 Best {len(items)}</div>', unsafe_allow_html=True)

    for i, item in enumerate(items):
        st.markdown(f"""
<div class="shop-card">
    <span class="item-emoji">{item['emoji']}</span>
    <div class="item-name">{item['name']}</div>
    <div class="item-brand">{item['brand']}</div>
    <div class="item-desc">{item['desc']}</div>
    <div class="item-price">💴 {item['price']}</div>
    <div class="item-where">{item['where']}</div>
    <div class="item-tip">{item['tip']}</div>
</div>
""", unsafe_allow_html=True)
        if st.button(f"🛒 장바구니 담기 — {item['name']}", key=f"add_{region}_{i}"):
            st.session_state.cart.append({
                "emoji": item["emoji"], "name": item["name"],
                "brand": item["brand"], "price": item["price"], "region": region,
            })
            st.toast(f"✅ '{item['name']}' 담았어요!", icon="🛒")

# ============================================================
# TAB 2 — 어휘 마스터 (카테고리별 플래시카드)
# ============================================================
with tab_vocab:
    st.markdown('<div class="sec-title">📖 여행 필수 어휘 <span class="level-badge">N3~N4</span></div>', unsafe_allow_html=True)

    cats = list(VOCAB.keys())
    cat_sel = st.radio("카테고리", cats, horizontal=True, label_visibility="collapsed")

    words = VOCAB[cat_sel]
    st.markdown(f'<div class="region-badge">📂 {cat_sel} — {len(words)}개 단어</div>', unsafe_allow_html=True)

    for w in words:
        st.markdown(f"""
<div class="vocab-card">
    <span class="vocab-badge">{cat_sel}</span>
    <div class="vocab-jp speak-btn" onclick="speakJP('{w['jp']}')">{w['jp']}<span class="tts-icon">🔊 탭</span></div>
    <div class="vocab-read">{w['read']}</div>
    <div class="vocab-ko">🇰🇷 {w['ko']}</div>
    <div class="vocab-ex speak-btn" onclick="speakJP('{w['ex'].split('(')[0].strip()}')" style="cursor:pointer;">✏️ {w['ex']}<span class="tts-icon">🔊</span></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:#fff;border-radius:16px;padding:0.9rem 1rem;
    border:1.5px solid #e0f2f1;box-shadow:0 2px 10px rgba(0,150,136,.08);">
<div style="font-size:0.82rem;font-weight:800;color:#00695c;margin-bottom:0.5rem;">
    💡 중급자 학습 팁</div>
<div style="font-size:0.75rem;color:#546e7a;line-height:1.7;">
    • 단어는 <b>예문(ex)</b>과 함께 외워야 실제 사용 가능<br>
    • 히라가나 읽기보다 <b>발음(한글 발음)</b>을 먼저 익혀 실전 활용<br>
    • 🧠 퀴즈 탭에서 바로 테스트해보세요!
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TAB 3 — 문법 패턴
# ============================================================
with tab_grammar:
    st.markdown('<div class="sec-title">📚 중급 문법 패턴 <span class="level-badge">N3~N4</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.73rem;color:#7986cb;margin-bottom:0.8rem;">패턴 → 예문 → 실전 팁 순으로 학습하세요</p>', unsafe_allow_html=True)

    for g in GRAMMAR:
        st.markdown(f"""
<div class="grammar-card">
    <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.2rem;">
        <div class="grammar-pattern speak-btn" onclick="speakJP('{g['ex_jp']}')" style="font-size:1.05rem;">{g['pattern']}<span class="tts-icon">🔊 탭</span></div>
        <span style="font-size:0.6rem;font-weight:700;color:#fff;
            background:#ff7043;padding:1px 7px;border-radius:10px;">{g['level']}</span>
    </div>
    <div class="grammar-meaning">{g['meaning']}</div>
    <div class="grammar-ex-jp speak-btn" onclick="speakJP('{g['ex_jp']}')">{g['ex_jp']}<span class="tts-icon">🔊</span></div>
    <div class="grammar-ex-read">{g['ex_read']}</div>
    <div class="grammar-ex-ko">🇰🇷 {g['ex_ko']}</div>
    <div class="grammar-tip">💡 {g['tip']}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TAB 4 — 여행 대화문 시나리오
# ============================================================
with tab_dial:
    st.markdown('<div class="sec-title">💬 여행 완성 대화문</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.73rem;color:#ad1457;margin-bottom:0.8rem;">실제 여행 현장 시나리오 — 소리 내어 읽어보세요 🗣️</p>', unsafe_allow_html=True)

    for dial in DIALOGUES:
        lines_html = ""
        for line in dial["lines"]:
            spk_class = "d-speaker-a" if line["spk"] == "A" else "d-speaker-b"
            bubble_class = "d-bubble-a" if line["spk"] == "A" else "d-bubble-b"
            lines_html += f"""
<div class="d-row">
    <span class="{spk_class}">{line['spk']}</span>
    <div class="{bubble_class}">
        <div class="d-jp speak-btn" onclick="speakJP('{line['jp']}')">{line['jp']}<span class="tts-icon">🔊</span></div>
        <div class="d-read" style="cursor:pointer;" onclick="speakJP('{line['jp']}')">🔊 {line['read']}</div>
        <div class="d-ko">🇰🇷 {line['ko']}</div>
    </div>
</div>"""

        st.markdown(f"""
<div class="dialogue-wrap">
    <div class="dialogue-title">{dial['title']}</div>
    <span class="dialogue-scene">{dial['scene']}</span>
    {lines_html}
</div>
""", unsafe_allow_html=True)

# ============================================================
# TAB 5 — 퀴즈
# ============================================================
with tab_quiz:
    st.markdown('<div class="sec-title">🧠 어휘 퀴즈</div>', unsafe_allow_html=True)

    pool = st.session_state.quiz_pool
    total_q = len(pool)
    idx = st.session_state.quiz_idx

    # 점수 박스
    st.markdown(f"""
<div class="quiz-score-box">
    <div style="font-size:0.72rem;opacity:.85;font-weight:600;">현재 점수</div>
    <div style="font-size:2rem;font-weight:900;line-height:1.1;">
        {st.session_state.quiz_score} <span style="font-size:1rem;opacity:.7;">/ {st.session_state.quiz_total}</span>
    </div>
    <div style="font-size:0.68rem;opacity:.8;">문제 {min(idx+1, total_q)} / {total_q}</div>
</div>
""", unsafe_allow_html=True)

    # 진행 바
    pct = int((idx / total_q) * 100) if total_q > 0 else 0
    st.markdown(f"""
<div class="progress-bar-wrap">
    <div class="progress-bar-fill" style="width:{pct}%"></div>
</div>
""", unsafe_allow_html=True)

    if idx >= total_q:
        # 모든 문제 완료
        acc = int((st.session_state.quiz_score / st.session_state.quiz_total) * 100) if st.session_state.quiz_total else 0
        grade = "🏆 완벽!" if acc >= 90 else "🌸 우수!" if acc >= 70 else "💪 분발하세요!"
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#9c27b0,#673ab7);color:white;
    border-radius:22px;padding:1.5rem 1rem;text-align:center;
    box-shadow:0 6px 20px rgba(156,39,176,.4);">
    <div style="font-size:2.5rem;margin-bottom:0.4rem;">{grade}</div>
    <div style="font-size:1.5rem;font-weight:900;">{acc}점</div>
    <div style="font-size:0.8rem;opacity:.85;margin-top:0.3rem;">
        {st.session_state.quiz_total}문제 중 {st.session_state.quiz_score}개 정답
    </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 퀴즈 다시 시작", key="restart_quiz"):
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_pool = build_quiz_pool()
            st.rerun()
    else:
        q = pool[idx]

        st.markdown(f"""
<div class="quiz-card">
    <span class="quiz-q-label">📂 {q['category']} | Q{idx+1}</span>
    <div class="quiz-q-jp speak-btn" onclick="speakJP('{q['q_jp']}')">{q['q_jp']}<span class="tts-icon">🔊 탭</span></div>
    <div class="quiz-q-read speak-btn" onclick="speakJP('{q['q_jp']}')" style="cursor:pointer;">🔊 {q['q_read']}</div>
    <div style="font-size:0.72rem;color:#9e9e9e;">아래에서 한국어 뜻을 고르세요</div>
</div>
""", unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            # 보기 버튼
            for opt in q["options"]:
                if st.button(opt, key=f"opt_{idx}_{opt}"):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_total += 1
                    if opt == q["answer"]:
                        st.session_state.quiz_correct = True
                        st.session_state.quiz_score += 1
                        st.toast("🎉 정답!", icon="✅")
                    else:
                        st.session_state.quiz_correct = False
                        st.toast(f"😅 오답! 정답: {q['answer']}", icon="❌")
                    st.rerun()
        else:
            # 결과 표시
            is_correct = st.session_state.quiz_correct
            result_icon = "✅ 정답!" if is_correct else "❌ 오답!"
            result_color = "#43a047" if is_correct else "#e53935"
            result_bg = "#e8f5e9" if is_correct else "#ffebee"

            st.markdown(f"""
<div style="background:{result_bg};border:2px solid {result_color};
    border-radius:14px;padding:0.8rem 1rem;text-align:center;margin-bottom:0.5rem;">
    <div style="font-size:1.1rem;font-weight:800;color:{result_color};">{result_icon}</div>
    <div style="font-size:0.85rem;font-weight:700;color:#333;margin-top:0.2rem;">
        정답: {q['answer']}</div>
    <div style="font-size:0.72rem;color:#546e7a;margin-top:0.3rem;">
        ✏️ {q['example']}</div>
</div>
""", unsafe_allow_html=True)

            if st.button("다음 문제 ➡️", key=f"next_{idx}"):
                st.session_state.quiz_idx += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_correct = None
                st.rerun()

# ============================================================
# TAB 6 — 쇼핑 치트키
# ============================================================
with tab_phrase:
    st.markdown('<div class="sec-title">🗣️ 상황별 쇼핑 치트키</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.73rem;color:#9a7a60;margin-bottom:0.8rem;">점원에게 화면 보여주거나, 소리 내어 읽어보세요 📱</p>', unsafe_allow_html=True)

    for phrase in PHRASES:
        st.markdown(f"""
<div class="phrase-card">
    <span class="phrase-sit">{phrase['situation']}</span>
    <div class="phrase-jp speak-btn" onclick="speakJP('{phrase['japanese']}')">{phrase['japanese']}<span class="tts-icon">🔊 탭</span></div>
    <div class="phrase-ko">🇰🇷 {phrase['korean']}</div>
    <div class="phrase-read speak-btn" onclick="speakJP('{phrase['japanese']}')" style="cursor:pointer;">🔊 {phrase['reading']}</div>
    <div class="phrase-tip">💡 {phrase['tip']}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TAB 7 — 장바구니
# ============================================================
with tab_cart:
    st.markdown('<div class="sec-title">🧺 내 쇼핑 위시리스트</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown("""
<div class="cart-empty">
    <div style="font-size:3rem;">🛒</div>
    <div style="font-size:0.92rem;font-weight:700;color:#a08070;margin:0.5rem 0 0.2rem;">
        장바구니가 비어있어요</div>
    <div style="font-size:0.75rem;">쇼핑핫템 탭에서 아이템을 담아보세요!</div>
</div>
""", unsafe_allow_html=True)
    else:
        to_remove = None
        for i, item in enumerate(st.session_state.cart):
            col_c, col_d = st.columns([5, 1])
            with col_c:
                st.markdown(f"""
<div class="cart-card">
    <span class="cart-emoji">{item['emoji']}</span>
    <div class="cart-info">
        <div class="cart-name">{item['name']}</div>
        <span class="cart-rgn">{item['region']}</span>
        <div class="cart-price">{item['price']}</div>
    </div>
</div>
""", unsafe_allow_html=True)
            with col_d:
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{i}"):
                    to_remove = i

        if to_remove is not None:
            removed = st.session_state.cart.pop(to_remove)
            st.toast(f"🗑️ '{removed['name']}' 삭제됨", icon="🗑️")
            st.rerun()

        count = len(st.session_state.cart)
        st.markdown(f"""
<div class="cart-total">
    <div style="font-size:0.72rem;opacity:.85;font-weight:600;">총 위시리스트</div>
    <div style="font-size:1.9rem;font-weight:900;line-height:1.1;">{count}개 아이템</div>
    <div style="font-size:0.68rem;opacity:.8;margin-top:0.2rem;">
        ✈️ 여행 전 스크린샷으로 저장해두세요!</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ 전체 비우기", key="clear_all"):
            st.session_state.cart.clear()
            st.toast("장바구니를 모두 비웠어요!", icon="✨")
            st.rerun()

# ── 하단 푸터 ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:0.68rem;color:#b09878;
    padding-bottom:1.5rem;line-height:1.8;">
    🇯🇵 즐거운 일본 여행 되세요! | Made with ❤️ &amp; Streamlit<br>
    BGM: SoundHelix Royalty-Free · 어휘 기준: JLPT N3~N4
</div>
""", unsafe_allow_html=True)
