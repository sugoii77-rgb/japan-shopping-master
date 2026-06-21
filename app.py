"""
🇯🇵 일본 여행 쇼핑 & 1일 일본어 마스터 웹앱
중급자 대상 완전판 | 모바일 최적화 | Streamlit 싱글 파일
TTS: Web Speech API (브라우저 내장, 무료)
실행: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="🇯🇵 일본어 1일 마스터",
    page_icon="🎌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 세션 상태 ──────────────────────────────────────────────
for k, v in {
    "cart": [], "quiz_idx": 0, "quiz_score": 0,
    "quiz_total": 0, "quiz_answered": False,
    "quiz_correct": None, "quiz_pool": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# CSS — 메인 페이지 (Streamlit 버튼/탭/드롭다운 스타일)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
.stApp{background:linear-gradient(160deg,#fffaf6 0%,#fef4e8 55%,#fde8d4 100%);
    font-family:'Noto Sans KR',sans-serif;}
.block-container{max-width:440px!important;margin:0 auto!important;
    padding:0.4rem 0.9rem 5rem!important;}
#MainMenu,footer,header{visibility:hidden;}
.app-title{text-align:center;font-size:1.65rem;font-weight:900;padding:1rem 0 .15rem;
    background:linear-gradient(135deg,#e96c6c,#f5a623 45%,#d35400);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.app-sub{text-align:center;color:#a08060;font-size:.72rem;letter-spacing:.8px;margin-bottom:.7rem;}
.bgm-box{background:linear-gradient(135deg,#fff0f8,#f0e8ff);border:1.5px solid #e2d0f0;
    border-radius:16px;padding:.7rem .9rem .5rem;margin-bottom:.8rem;}
.bgm-label{font-size:.7rem;font-weight:700;color:#8050a0;letter-spacing:.3px;margin-bottom:.35rem;}
.stTabs [data-baseweb="tab-list"]{background:#fff8f2!important;border-radius:14px!important;
    padding:4px!important;gap:2px!important;border:1.5px solid #f0d5bc!important;margin-bottom:.4rem;flex-wrap:wrap!important;}
.stTabs [data-baseweb="tab"]{border-radius:10px!important;font-size:.72rem!important;
    font-weight:600!important;color:#a08060!important;padding:.3rem .45rem!important;min-width:0!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#ff8a65,#ffb74d)!important;
    color:white!important;font-weight:800!important;box-shadow:0 2px 8px rgba(255,138,101,.4)!important;}
.stSelectbox>div>div{background:white!important;border:2px solid #fad0c4!important;
    border-radius:12px!important;font-size:.88rem!important;font-weight:600!important;}
.stSelectbox label,.stRadio label{font-size:.82rem!important;font-weight:700!important;color:#5a3e2b!important;}
.stButton>button{background:linear-gradient(135deg,#ff8a65,#ffb74d)!important;color:white!important;
    border:none!important;border-radius:25px!important;font-weight:700!important;
    font-size:.82rem!important;width:100%!important;box-shadow:0 3px 12px rgba(255,138,101,.35)!important;
    margin-top:.5rem!important;margin-bottom:.9rem!important;}
.region-badge{background:linear-gradient(135deg,#e65100,#f57c00);color:white;
    padding:.4rem 1rem;border-radius:20px;font-size:.8rem;font-weight:700;
    display:inline-block;margin-bottom:.9rem;box-shadow:0 3px 10px rgba(230,81,0,.3);}
.sec-title{font-size:.9rem;font-weight:800;color:#4a2e10;margin:.9rem 0 .55rem;}
hr{border:none!important;height:1px!important;
    background:linear-gradient(to right,transparent,#fad0c4 30%,#fad0c4 70%,transparent)!important;
    margin:.8rem 0!important;}
.cart-card{background:#fff;border-radius:16px;padding:.8rem .9rem;margin-bottom:.65rem;
    box-shadow:0 2px 10px rgba(0,0,0,.06);border:1.5px solid #f5f5f5;
    display:flex;align-items:center;gap:.7rem;}
.cart-total{background:linear-gradient(135deg,#7c4dff,#e040fb);color:white;
    border-radius:18px;padding:1rem 1.1rem;text-align:center;margin-top:.7rem;
    box-shadow:0 5px 18px rgba(124,77,255,.35);}
.quiz-score-box{background:linear-gradient(135deg,#9c27b0,#673ab7);color:white;
    border-radius:18px;padding:1rem 1.2rem;text-align:center;margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(156,39,176,.35);}
.progress-bar-wrap{background:#f5f5f5;border-radius:10px;height:8px;
    margin-bottom:.6rem;overflow:hidden;}
.progress-bar-fill{background:linear-gradient(90deg,#9c27b0,#e040fb);
    height:100%;border-radius:10px;}
[data-testid="column"]:last-child .stButton>button{
    background:linear-gradient(135deg,#ef9a9a,#e57373)!important;
    border-radius:50%!important;width:2.2rem!important;height:2.2rem!important;
    margin-top:0!important;margin-bottom:0!important;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 공유 TTS + 카드 CSS (components.html 내부 iframe용)
# JS와 HTML이 같은 iframe → onclick이 정상 동작
# ============================================================
_HEAD = """
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:transparent;padding:4px 2px 10px;}

/* ── 공통 카드 ── */
.card{background:#fff;border-radius:20px;padding:1.1rem 1rem .85rem;
    margin-bottom:.8rem;position:relative;overflow:hidden;}

/* ── 어휘 ── */
.vocab-card{box-shadow:0 3px 14px rgba(0,150,136,.1);border:1.5px solid #e0f2f1;}
.vocab-badge{font-size:.62rem;font-weight:700;color:#fff;
    background:linear-gradient(135deg,#26a69a,#00897b);
    padding:2px 8px;border-radius:12px;display:inline-block;margin-bottom:.55rem;}
.vocab-jp{font-size:1.5rem;font-weight:900;color:#00695c;margin-bottom:.2rem;
    cursor:pointer;display:inline-block;}
.vocab-read{font-size:.85rem;color:#e64a19;font-weight:700;background:#fff3e0;
    padding:2px 9px;border-radius:8px;display:inline-block;margin-bottom:.4rem;}
.vocab-ko{font-size:.88rem;font-weight:600;color:#37474f;margin-bottom:.3rem;}
.vocab-ex{font-size:.75rem;color:#607d8b;line-height:1.5;background:#f5f5f5;
    padding:5px 9px;border-radius:8px;cursor:pointer;}

/* ── 문법 ── */
.grammar-card{box-shadow:0 3px 14px rgba(63,81,181,.1);
    border-left:5px solid #3f51b5;border:1.5px solid #e8eaf6;border-left:5px solid #3f51b5;}
.grammar-pattern{font-size:1.1rem;font-weight:900;color:#283593;cursor:pointer;display:inline-block;}
.grammar-level{font-size:.6rem;font-weight:700;color:#fff;background:#ff7043;
    padding:1px 7px;border-radius:10px;margin-left:6px;vertical-align:middle;}
.grammar-meaning{font-size:.78rem;color:#5c6bc0;font-weight:600;background:#e8eaf6;
    padding:2px 9px;border-radius:8px;display:inline-block;margin:.3rem 0 .5rem;}
.grammar-ex-jp{font-size:.95rem;font-weight:700;color:#1a237e;margin-bottom:.15rem;
    cursor:pointer;display:inline-block;}
.grammar-ex-read{font-size:.78rem;color:#e64a19;margin-bottom:.15rem;font-weight:600;}
.grammar-ex-ko{font-size:.78rem;color:#546e7a;margin-bottom:.35rem;}
.grammar-tip{font-size:.7rem;color:#7986cb;background:#f3f4ff;
    padding:4px 9px;border-radius:7px;line-height:1.5;}

/* ── 대화문 ── */
.dialogue-wrap{background:#fff;border-radius:20px;padding:1rem;
    margin-bottom:1rem;box-shadow:0 3px 14px rgba(233,30,99,.09);border:1.5px solid #fce4ec;}
.dialogue-title{font-size:.8rem;font-weight:800;
    background:linear-gradient(135deg,#e91e63,#f06292);color:white;
    padding:4px 12px;border-radius:12px;display:inline-block;margin-bottom:.7rem;}
.dialogue-scene{font-size:.7rem;color:#ad1457;background:#fce4ec;
    padding:3px 9px;border-radius:8px;margin-bottom:.65rem;
    display:block;font-weight:600;}
.d-row{display:flex;gap:.5rem;margin-bottom:.55rem;align-items:flex-start;}
.d-spk-a{font-size:.65rem;font-weight:800;color:#fff;background:#e91e63;
    padding:2px 7px;border-radius:10px;flex-shrink:0;margin-top:2px;}
.d-spk-b{font-size:.65rem;font-weight:800;color:#fff;background:#1976d2;
    padding:2px 7px;border-radius:10px;flex-shrink:0;margin-top:2px;}
.d-bub-a{background:#fce4ec;border-radius:0 12px 12px 12px;padding:.4rem .6rem;flex:1;}
.d-bub-b{background:#e3f2fd;border-radius:0 12px 12px 12px;padding:.4rem .6rem;flex:1;}
.d-jp{font-size:.88rem;font-weight:700;color:#212121;margin-bottom:.1rem;cursor:pointer;}
.d-read{font-size:.72rem;color:#e64a19;font-weight:600;margin-bottom:.1rem;cursor:pointer;}
.d-ko{font-size:.72rem;color:#546e7a;}

/* ── 치트키 ── */
.phrase-card{background:#fff;border-radius:18px;padding:1rem 1rem .85rem;
    margin-bottom:.85rem;box-shadow:0 4px 14px rgba(80,80,200,.09);
    border-top:1.5px solid #e8e4ff;border-right:1.5px solid #e8e4ff;
    border-bottom:1.5px solid #e8e4ff;border-left:5px solid #7c4dff;}
.phrase-sit{font-size:.66rem;font-weight:800;color:#5c35c0;background:#ede7ff;
    display:inline-block;padding:2px 9px;border-radius:20px;margin-bottom:.55rem;}
.phrase-jp{font-size:1.18rem;font-weight:800;color:#1a1a2e;
    margin-bottom:.3rem;line-height:1.5;cursor:pointer;display:block;}
.phrase-ko{font-size:.8rem;color:#5a5a7a;margin-bottom:.45rem;font-weight:500;}
.phrase-read{font-size:.92rem;color:#bf360c;font-weight:700;
    background:linear-gradient(135deg,#fff3e0,#fce4ec);
    padding:4px 11px;border-radius:9px;display:inline-block;cursor:pointer;}
.phrase-tip{font-size:.7rem;color:#7c7c9a;margin-top:.5rem;padding:3px 8px;
    background:#f8f8ff;border-radius:7px;border-left:3px solid #b39ddb;}

/* ── 쇼핑 카드 ── */
.shop-card{background:#fff;border-radius:22px;padding:1.1rem 1rem .7rem;
    margin-bottom:.8rem;box-shadow:0 4px 18px rgba(220,120,80,.12);
    border:1.5px solid #fef0e6;position:relative;overflow:hidden;}
.shop-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;
    background:linear-gradient(90deg,#ff8a65,#ffb74d,#ff8a65);}
.item-emoji{font-size:2.5rem;display:block;margin-bottom:.35rem;}
.item-name{font-size:1rem;font-weight:800;color:#3d2010;margin-bottom:.2rem;}
.item-brand{font-size:.68rem;font-weight:700;color:#e65100;background:#fff3e0;
    display:inline-block;padding:2px 9px;border-radius:20px;margin-bottom:.5rem;}
.item-desc{font-size:.78rem;color:#6d4c35;line-height:1.6;margin-bottom:.3rem;}
.item-price{font-size:.85rem;color:#c0392b;font-weight:700;margin-bottom:.25rem;}
.item-where{font-size:.73rem;color:#7d5c40;padding:3px 8px;
    background:#fdf6f0;border-radius:8px;margin-bottom:.25rem;}
.item-tip{font-size:.72rem;color:#b07840;padding:3px 8px;
    background:#fffde7;border-radius:8px;border-left:3px solid #ffd54f;}

/* ── TTS 뱃지 ── */
.tts{font-size:.62em;background:linear-gradient(135deg,#ff7043,#ff5722);
    color:#fff;padding:1px 6px;border-radius:8px;margin-left:5px;
    vertical-align:middle;font-weight:700;font-style:normal;}
[onclick]{cursor:pointer;}
[onclick]:hover{opacity:.75;}
[onclick]:active{opacity:.55;}

/* ── 퀴즈 ── */
.quiz-card{background:#fff;border-radius:22px;padding:1.3rem 1.1rem 1rem;
    box-shadow:0 5px 20px rgba(156,39,176,.13);border:2px solid #f3e5f5;text-align:center;}
.quiz-q-label{font-size:.68rem;font-weight:700;color:#7b1fa2;background:#f3e5f5;
    padding:2px 10px;border-radius:12px;display:inline-block;margin-bottom:.8rem;}
.quiz-q-jp{font-size:1.5rem;font-weight:900;color:#1a1a2e;margin-bottom:.3rem;cursor:pointer;}
.quiz-q-read{font-size:.85rem;color:#e64a19;font-weight:700;margin-bottom:.5rem;cursor:pointer;}
</style>
<script>
(function(){
  /* ── Web Speech API TTS ── */
  var synth = window.speechSynthesis;
  if(!synth) return;

  // 보이스 미리 로드
  synth.getVoices();
  synth.onvoiceschanged = function(){ synth.getVoices(); };

  window.speakJP = function(txt){
    synth.cancel();
    var u = new SpeechSynthesisUtterance(txt);
    u.lang  = 'ja-JP';
    u.rate  = 0.82;
    u.pitch = 1.05;
    var voices = synth.getVoices();
    var jv = voices.find(function(v){ return v.lang && v.lang.startsWith('ja'); });
    if(jv) u.voice = jv;
    synth.speak(u);

    /* 토스트 */
    var old = document.getElementById('_t');
    if(old) old.remove();
    var el = document.createElement('div');
    el.id = '_t';
    el.style.cssText='position:fixed;bottom:14px;left:50%;transform:translateX(-50%);'
      +'background:rgba(20,20,20,.92);color:#fff;padding:8px 20px;border-radius:24px;'
      +'font-size:.78rem;font-weight:600;z-index:9999;pointer-events:none;'
      +'white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.4);';
    el.textContent='🔊  '+txt.slice(0,26)+(txt.length>26?'…':'');
    document.body.appendChild(el);
    setTimeout(function(){el.style.transition='opacity .5s';el.style.opacity='0';},1600);
    setTimeout(function(){if(el.parentNode)el.remove();},2200);
  };

  /* ── Streamlit iframe 높이 자동 맞춤 ── */
  function resize(){
    var h = document.documentElement.scrollHeight+20;
    window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
  }
  window.addEventListener('load', resize);
  setTimeout(resize, 400);
  if(window.ResizeObserver) new ResizeObserver(resize).observe(document.body);
})();
</script>
"""

# ============================================================
# 데이터 — 쇼핑 핫템
# ============================================================
SHOPPING_DATA = {
    "🗼 도쿄 (Tokyo)": [
        {"emoji":"🍮","name":"넘버슈가 카라멜","brand":"NUMBER SUGAR",
         "desc":"소금·말차·홍차 등 12가지 수제 캐러멜. 고급 박스 패키징.",
         "price":"약 ¥1,620 (10개입)","where":"📍 이세탄 신주쿠 B1 · 다카시마야 시부야",
         "tip":"💡 소금·캬라멜 맛 오픈 즉시 매진. 주말 정오 전 방문!"},
        {"emoji":"🍌","name":"도쿄 바나나","brand":"TOKYO BANANA",
         "desc":"바나나 크림을 채운 스펀지 케이크. 기간 한정 콜라보 버전도 상시 출시.",
         "price":"약 ¥980 (8개입)","where":"📍 도쿄역 그란스타 · 하네다·나리타 공항",
         "tip":"💡 유통기한 5일. 귀국 직전 공항 구매가 가장 신선!"},
        {"emoji":"🧴","name":"SK-II 페이셜 에센스","brand":"SK-II",
         "desc":"피테라 성분 명품 화장수. 일본 면세가 한국보다 20~30% 저렴.",
         "price":"약 ¥16,000 (230ml 면세가)","where":"📍 긴자·신주쿠 면세점",
         "tip":"💡 ¥5,500 이상 구매 시 소비세 환급. 여권 필수!"},
        {"emoji":"🎌","name":"유니클로 한정판 UT","brand":"UNIQLO Japan",
         "desc":"일본 현지 한정 아티스트 컬래버 티셔츠. 한국 미출시 다수.",
         "price":"약 ¥1,500~2,500","where":"📍 긴자 유니클로 글로벌 플래그십 12층",
         "tip":"💡 일본 사이즈 한국보다 1단계 작음. XL이면 XXL 권장."},
        {"emoji":"🍜","name":"닛신 한정판 컵라멘 세트","brand":"日清食品",
         "desc":"요코하마 컵누들 뮤지엄 한정 & 지역限定 맛. DIY 컵 제작 체험 가능.",
         "price":"약 ¥500~2,500","where":"📍 돈키호테 · 이온몰",
         "tip":"💡 봉지면 여러 맛 사는 게 가성비 최고!"},
    ],
    "🏯 오사카 (Osaka)": [
        {"emoji":"🥟","name":"551 호라이 찐만두","brand":"551 蓬莱",
         "desc":"오사카 소울 푸드. 돼지고기+파 가득한 점보 찐만두. 60년 전통.",
         "price":"약 ¥670 (6개입)","where":"📍 신사이바시 · 난바 · 우메다 · 공항",
         "tip":"💡 냉동 제품 판매! 공항에서 아이스팩과 함께 구매 가능."},
        {"emoji":"🏷️","name":"한큐백화점 한정 손수건","brand":"阪急百貨店",
         "desc":"마리메꼬·호레이 컬래버 한정 디자인. 선물 최적.",
         "price":"약 ¥1,000~3,500","where":"📍 한큐 우메다 본점 1F",
         "tip":"💡 5장 이상 구매 시 선물 세트 박스 무료!"},
        {"emoji":"🍪","name":"오사카 버터 밀크 쿠키","brand":"大阪土産菓子",
         "desc":"오사카 한정 바삭 버터 쿠키. 상온 보관 가능.",
         "price":"약 ¥1,200~3,000","where":"📍 신사이바시스지 상점가",
         "tip":"💡 유통기한 30일. 대량 구매 추천."},
        {"emoji":"🧴","name":"마츠키요 가성비 화장품","brand":"DHC / Canmake",
         "desc":"DHC 클렌징오일·캔메이크 쿠션. 한국보다 20~40% 저렴.",
         "price":"약 ¥500~3,000","where":"📍 마츠모토 키요시 · 돈키호테",
         "tip":"💡 포인트 카드 + 면세 카운터 적극 활용!"},
        {"emoji":"🐙","name":"타코야키 홈 메이커 세트","brand":"イワタニ",
         "desc":"이와타니 타코야키 기계+믹스 가루. 집에서 오사카 타코야키 재현.",
         "price":"약 ¥2,500~5,500","where":"📍 도구야스지 상점가 · 빅카메라",
         "tip":"💡 이와타니 가스 타입은 전압 무관."},
    ],
    "🌊 후쿠오카 (Fukuoka)": [
        {"emoji":"🐟","name":"후쿠사야 명란 마요네즈","brand":"ふくさや",
         "desc":"후쿠오카 명란 마요네즈. 주먹밥·파스타에 뿌리면 감동.",
         "price":"약 ¥750~1,200","where":"📍 후쿠오카 공항 · 캐널시티 · 하카타역",
         "tip":"💡 아이스팩 요청 가능. 귀국 당일 아침 구매!"},
        {"emoji":"🐣","name":"히요코 병아리 과자","brand":"ひよ子本舗吉野堂",
         "desc":"병아리 모양 콩소 앙금 화과자. 1927년 창업 원조 명과.",
         "price":"약 ¥1,000~2,500","where":"📍 하카타역 · 후쿠오카 공항",
         "tip":"💡 도쿄에서도 팔지만 후쿠오카가 원조!"},
        {"emoji":"🍜","name":"이치란 라멘 테이크아웃 세트","brand":"一蘭",
         "desc":"이치란 오리지널 소스+면 세트. 집에서 하카타 돈코츠 재현.",
         "price":"약 ¥1,800~3,500","where":"📍 이치란 나카스점 기념품 카운터",
         "tip":"💡 매장 카운터에서만 구매. 온라인 불가!"},
        {"emoji":"👘","name":"하카타 전통 공예 기념품","brand":"博多人形 / 博多織",
         "desc":"하카타 직물 소품·인형. 후쿠오카 700년 전통 공예.",
         "price":"약 ¥1,500~15,000","where":"📍 하카타 마찌야 후루사토관",
         "tip":"💡 윗사람 선물로 품격 최고!"},
        {"emoji":"🥩","name":"모츠나베 곱창 재료 세트","brand":"楽天地 / やま中",
         "desc":"모츠나베 전용 곱창+국물 소스 세트. 집에서 나베 파티 가능.",
         "price":"약 ¥2,000~4,500","where":"📍 야마야 슈퍼 · 암즈 백화점 B1",
         "tip":"💡 드라이아이스 포장 요청 가능."},
    ],
}

# ============================================================
# 데이터 — 쇼핑 치트키
# ============================================================
PHRASES = [
    {"situation":"💳 카드 결제","japanese":"カードで払えますか？",
     "reading":"카도데 하라에마스카？","korean":"카드로 결제할 수 있나요?",
     "tip":"소규모 점포는 현금만 가능하기도 함. 미리 확인!"},
    {"situation":"🛍️ 봉투 요청","japanese":"袋をいただけますか？",
     "reading":"후쿠로오 이타다케마스카？","korean":"봉투를 주실 수 있나요?",
     "tip":"일본은 봉투 유료(¥3~5). 에코백 챙기면 절약!"},
    {"situation":"🎁 선물 포장","japanese":"ギフト包装をお願いします",
     "reading":"기후토 호소오오 오네가이시마스","korean":"선물 포장 부탁드립니다",
     "tip":"백화점은 대부분 무료. 리본 색도 선택 가능."},
    {"situation":"🚫 면세 신청","japanese":"免税手続きをお願いします",
     "reading":"멘제이 테츠즈키오 오네가이시마스","korean":"면세 처리 부탁드립니다",
     "tip":"¥5,500 이상 구매 시 가능. 여권 원본 필수!"},
    {"situation":"💰 가격 문의","japanese":"これはいくらですか？",
     "reading":"코레와 이쿠라데스카？","korean":"이것은 얼마인가요?",
     "tip":"못 알아들으면 계산기 보여달라고: 「電卓を見せてください」"},
    {"situation":"🔍 재고 확인","japanese":"在庫はありますか？",
     "reading":"자이코와 아리마스카？","korean":"재고가 있나요?",
     "tip":"사이즈 다를 때: 「Sサイズはありますか？」"},
    {"situation":"🔄 교환 요청","japanese":"交換できますか？",
     "reading":"코칸 데키마스카？","korean":"교환 가능한가요?",
     "tip":"영수증(領収書) 필수. 교환 기간 내에만 가능."},
    {"situation":"📦 호텔 배송","japanese":"ホテルに配送できますか？",
     "reading":"호테루니 하이소오 데키마스카？","korean":"호텔로 배송 가능한가요?",
     "tip":"야마토 택배(クロネコヤマト) 활용하면 짐이 훨씬 가벼워짐!"},
    {"situation":"🤏 가격 흥정","japanese":"もう少し安くなりますか？",
     "reading":"모오 스코시 야스쿠 나리마스카？","korean":"조금 더 싸게 해주실 수 있나요?",
     "tip":"백화점·편의점은 정가제. 상점가에서만 시도 가능."},
    {"situation":"🏃 급할 때","japanese":"急いでいます",
     "reading":"이소이데 이마스","korean":"저 급합니다",
     "tip":"공항 이동 직전 계산 서두를 때 유용."},
    {"situation":"🙏 마무리 인사","japanese":"ありがとうございました！",
     "reading":"아리가토오 고자이마시타！","korean":"감사했습니다!",
     "tip":"계산 후 꼭 한마디! 일본 점원이 정말 좋아함 ☺"},
]

# ============================================================
# 데이터 — 어휘 (N3~N4)
# ============================================================
VOCAB = {
    "쇼핑": [
        {"jp":"割引","read":"わりびき (와리비키)","ko":"할인","ex":"割引はありますか？"},
        {"jp":"領収書","read":"りょうしゅうしょ (료슈쇼)","ko":"영수증","ex":"領収書をください。"},
        {"jp":"試着","read":"しちゃく (시챠쿠)","ko":"시착/피팅","ex":"試着してもいいですか？"},
        {"jp":"売り切れ","read":"うりきれ (우리키레)","ko":"품절","ex":"もう売り切れです。"},
        {"jp":"限定品","read":"げんていひん (겐테이힌)","ko":"한정품","ex":"これは限定品ですか？"},
        {"jp":"免税","read":"めんぜい (멘제이)","ko":"면세","ex":"免税できますか？"},
        {"jp":"ポイントカード","read":"포인토 카도","ko":"포인트카드","ex":"ポイントカードはお持ちですか？"},
        {"jp":"送料","read":"そうりょう (소료)","ko":"배송비","ex":"送料はいくらですか？"},
    ],
    "식당": [
        {"jp":"おすすめ","read":"오스스메","ko":"추천","ex":"おすすめは何ですか？"},
        {"jp":"辛い","read":"からい (카라이)","ko":"맵다","ex":"辛くしないでください。"},
        {"jp":"アレルギー","read":"아레루기","ko":"알레르기","ex":"えびアレルギーがあります。"},
        {"jp":"お会計","read":"おかいけい (오카이케이)","ko":"계산서","ex":"お会計をお願いします。"},
        {"jp":"禁煙席","read":"きんえんせき (킨엔세키)","ko":"금연석","ex":"禁煙席をお願いします。"},
        {"jp":"持ち帰り","read":"もちかえり (모치카에리)","ko":"포장/테이크아웃","ex":"持ち帰りでお願いします。"},
        {"jp":"定食","read":"ていしょく (테이쇼쿠)","ko":"정식/세트","ex":"Aランチ定食をください。"},
        {"jp":"おかわり","read":"오카와리","ko":"리필","ex":"おかわりできますか？"},
    ],
    "교통": [
        {"jp":"乗り換え","read":"のりかえ (노리카에)","ko":"환승","ex":"どこで乗り換えますか？"},
        {"jp":"終電","read":"しゅうでん (슈덴)","ko":"막차","ex":"終電は何時ですか？"},
        {"jp":"ICカード","read":"아이씨 카도","ko":"교통카드","ex":"ICカードで乗れますか？"},
        {"jp":"特急","read":"とっきゅう (토큐)","ko":"특급 열차","ex":"特急券が必要ですか？"},
        {"jp":"渋滞","read":"じゅうたい (주타이)","ko":"교통 체증","ex":"渋滞で遅れています。"},
        {"jp":"タクシー乗り場","read":"타쿠시 노리바","ko":"택시 승강장","ex":"タクシー乗り場はどこですか？"},
        {"jp":"運賃","read":"うんちん (운친)","ko":"운임/요금","ex":"運賃はいくらですか？"},
        {"jp":"回数券","read":"かいすうけん (카이스우켄)","ko":"회수권","ex":"回数券はありますか？"},
    ],
    "숙박": [
        {"jp":"チェックイン","read":"체쿠인","ko":"체크인","ex":"チェックインをお願いします。"},
        {"jp":"禁煙ルーム","read":"킨엔 루무","ko":"금연 객실","ex":"禁煙ルームを予約しました。"},
        {"jp":"アメニティ","read":"아메니티","ko":"어메니티","ex":"アメニティをもらえますか？"},
        {"jp":"連泊","read":"れんぱく (렌파쿠)","ko":"연박","ex":"連泊したいのですが。"},
        {"jp":"布団","read":"ふとん (후톤)","ko":"이불/요","ex":"布団を追加してください。"},
        {"jp":"フロント","read":"후론토","ko":"프런트","ex":"フロントに電話してください。"},
        {"jp":"部屋のカギ","read":"헤야노 카기","ko":"방 열쇠","ex":"カギをなくしてしまいました。"},
        {"jp":"モーニングコール","read":"모닝구 코루","ko":"모닝콜","ex":"7時にモーニングコールをお願いします。"},
    ],
    "긴급": [
        {"jp":"助けてください","read":"타스케테 쿠다사이","ko":"도와주세요!","ex":"誰か助けてください！"},
        {"jp":"救急車","read":"きゅうきゅうしゃ (큐큐샤)","ko":"구급차","ex":"救急車を呼んでください！"},
        {"jp":"警察","read":"けいさつ (케이사츠)","ko":"경찰","ex":"警察を呼んでください。"},
        {"jp":"財布を盗まれました","read":"사이후오 누스마레마시타","ko":"지갑 도둑맞음","ex":"財布を盗まれました！"},
        {"jp":"迷子","read":"まいご (마이고)","ko":"길을 잃음","ex":"迷子になりました。"},
        {"jp":"病院","read":"びょういん (뵤인)","ko":"병원","ex":"近くに病院はありますか？"},
        {"jp":"薬局","read":"やっきょく (약쿄쿠)","ko":"약국","ex":"薬局はどこですか？"},
        {"jp":"アレルギー反応","read":"아레루기 한노","ko":"알레르기 반응","ex":"アレルギー反応が出ています。"},
    ],
}

# ============================================================
# 데이터 — 문법 패턴
# ============================================================
GRAMMAR = [
    {"pattern":"〜てみる","meaning":"(한번) 해보다","level":"N4",
     "ex_jp":"このお菓子を食べてみてください。","ex_read":"코노 오카시오 타베테 미테 쿠다사이。",
     "ex_ko":"이 과자를 먹어보세요.","tip":"시도·경험을 권할 때 가장 자주 쓰는 패턴."},
    {"pattern":"〜てもいいですか","meaning":"~해도 되나요?","level":"N4",
     "ex_jp":"写真を撮ってもいいですか？","ex_read":"샤신오 톳테모 이이데스카？",
     "ex_ko":"사진 찍어도 되나요?","tip":"試着(시착), 触る(만지기) 앞에 붙여 사용."},
    {"pattern":"〜なければなりません","meaning":"~해야 합니다","level":"N4",
     "ex_jp":"パスポートを見せなければなりません。","ex_read":"파스포오토오 미세나케레바 나리마센。",
     "ex_ko":"여권을 보여줘야 합니다.","tip":"면세 처리 시 자주 쓰임."},
    {"pattern":"〜ことができる","meaning":"~할 수 있다","level":"N4",
     "ex_jp":"日本語を話すことができます。","ex_read":"니혼고오 하나스 코토가 데키마스。",
     "ex_ko":"일본어를 말할 수 있습니다.","tip":"できる 단독보다 격식 있는 표현."},
    {"pattern":"〜たことがある","meaning":"~한 적이 있다","level":"N4",
     "ex_jp":"一蘭に行ったことがありますか？","ex_read":"이치란니 잇타 코토가 아리마스카？",
     "ex_ko":"이치란에 간 적이 있나요?","tip":"여행 중 현지인과 경험 대화할 때."},
    {"pattern":"〜ながら","meaning":"~하면서","level":"N4",
     "ex_jp":"音楽を聴きながら歩きます。","ex_read":"온가쿠오 키키나가라 아루키마스。",
     "ex_ko":"음악을 들으면서 걷습니다.","tip":"ショッピングしながら 자주 쓰임."},
    {"pattern":"〜てしまう","meaning":"~해버리다","level":"N3",
     "ex_jp":"つい買いすぎてしまいました。","ex_read":"츠이 카이스기테 시마이마시타。",
     "ex_ko":"그만 너무 많이 사버렸어요.","tip":"충동구매 후 한마디로 딱!"},
    {"pattern":"〜らしい","meaning":"~인 것 같다","level":"N3",
     "ex_jp":"このブランドは人気らしいですよ。","ex_read":"코노 부란도와 닌키 라시이데스요。",
     "ex_ko":"이 브랜드는 인기 있는 것 같아요.","tip":"들은 소문을 전달할 때."},
    {"pattern":"〜はずだ","meaning":"~일 것이다","level":"N3",
     "ex_jp":"ここに売っているはずです。","ex_read":"코코니 우텟테 이루 하즈데스。",
     "ex_ko":"여기에 팔고 있을 텐데요.","tip":"사전 조사 기반의 확신 표현."},
    {"pattern":"〜ために","meaning":"~을 위해","level":"N3",
     "ex_jp":"お土産のために買いました。","ex_read":"오미야게노 타메니 카이마시타。",
     "ex_ko":"기념품을 위해 샀습니다.","tip":"면세 창구에서 '선물용(プレゼントのために)'으로!"},
    {"pattern":"〜ば〜ほど","meaning":"~하면 할수록","level":"N3",
     "ex_jp":"食べれば食べるほど美味しい！","ex_read":"타베레바 타베루 호도 오이시이！",
     "ex_ko":"먹으면 먹을수록 맛있어요!","tip":"일본 음식 칭찬할 때 찰떡 패턴!"},
    {"pattern":"〜かもしれない","meaning":"~일지도 모른다","level":"N3",
     "ex_jp":"売り切れかもしれません。","ex_read":"우리키레 카모 시레마센。",
     "ex_ko":"품절일지도 모릅니다.","tip":"불확실한 정보를 부드럽게 전달할 때."},
]

# ============================================================
# 데이터 — 여행 대화문
# ============================================================
DIALOGUES = [
    {"title":"🏨 호텔 체크인","scene":"📍 호텔 프런트 | A=나(여행자) B=직원","lines":[
        {"spk":"A","jp":"チェックインをお願いします。山田の名前で予約しています。",
         "read":"체쿠인오 오네가이시마스。야마다노 나마에데 요야쿠시테 이마스。",
         "ko":"체크인 부탁드립니다. 야마다 이름으로 예약했습니다."},
        {"spk":"B","jp":"パスポートをお見せいただけますか？","read":"파스포오토오 오미세 이타다케마스카？",
         "ko":"여권을 보여주실 수 있나요?"},
        {"spk":"A","jp":"はい、どうぞ。朝食は付いていますか？","read":"하이, 도조。쵸쇼쿠와 츠이테 이마스카？",
         "ko":"네, 여기요. 조식은 포함되어 있나요?"},
        {"spk":"B","jp":"はい、7時から10時まで1階のレストランでお召し上がりいただけます。",
         "read":"하이, 시치지카라 주지마데 잇카이노 레스토란데 오메시아가리 이타다케마스。",
         "ko":"네, 7시부터 10시까지 1층 레스토랑에서 드실 수 있습니다."},
        {"spk":"A","jp":"Wi-Fiのパスワードも教えていただけますか？",
         "read":"와이파이노 파스와도모 오시에테 이타다케마스카？",
         "ko":"와이파이 비밀번호도 알려주실 수 있나요?"},
    ]},
    {"title":"🍜 레스토랑 주문","scene":"📍 이자카야 | A=나 B=점원","lines":[
        {"spk":"B","jp":"いらっしゃいませ！何名様ですか？","read":"이랏샤이마세！난메이사마데스카？",
         "ko":"어서오세요! 몇 분이세요?"},
        {"spk":"A","jp":"2名です。禁煙席をお願いしたいのですが。","read":"니메이데스。킨엔세키오 오네가이시타이노데스가。",
         "ko":"2명입니다. 금연석으로 부탁드리고 싶은데요."},
        {"spk":"A","jp":"おすすめは何ですか？辛いものは苦手なんですが。",
         "read":"오스스메와 난데스카？카라이 모노와 니가테난데스가。",
         "ko":"추천은 뭔가요? 매운 것을 잘 못하는데요."},
        {"spk":"B","jp":"塩ラーメンはいかがですか？あっさりしていて人気ですよ。",
         "read":"시오 라멘와 이카가데스카？앗사리 시테이테 닌키데스요。",
         "ko":"소금 라멘은 어떠세요? 담백하고 인기 있어요."},
        {"spk":"A","jp":"それにします！お会計はカードで払えますか？",
         "read":"소레니 시마스！오카이케이와 카도데 하라에마스카？",
         "ko":"그걸로 할게요! 계산은 카드로 가능한가요?"},
    ]},
    {"title":"🛍️ 백화점 면세 쇼핑","scene":"📍 백화점 화장품 코너 | A=나 B=점원","lines":[
        {"spk":"A","jp":"このファンデーションのサンプルを試してもいいですか？",
         "read":"코노 판데이션노 산푸루오 타메시테모 이이데스카？",
         "ko":"이 파운데이션 샘플을 시험해봐도 되나요?"},
        {"spk":"A","jp":"これを2つください。免税手続きもお願いしたいのですが。",
         "read":"코레오 후타츠 쿠다사이。멘제이 테츠즈키모 오네가이시타이노데스가。",
         "ko":"이것 2개 주세요. 면세 처리도 부탁드리고 싶은데요."},
        {"spk":"B","jp":"パスポートをお見せいただけますか？5,500円以上で免税になります。",
         "read":"파스포오토오 오미세 이타다케마스카？고센 고햐쿠엔 이조데 멘제이니 나리마스。",
         "ko":"여권을 보여주실 수 있나요? 5,500엔 이상 구매 시 면세가 됩니다."},
        {"spk":"A","jp":"ギフト包装もお願いできますか？","read":"기후토 호소오모 오네가이 데키마스카？",
         "ko":"선물 포장도 부탁드릴 수 있나요?"},
        {"spk":"B","jp":"承知しました！少々お時間をいただきます。",
         "read":"쇼치 시마시타！쇼쇼 오지칸오 이타다키마스。",
         "ko":"알겠습니다! 잠시 시간이 걸립니다."},
    ]},
    {"title":"🚉 길 찾기·교통","scene":"📍 지하철역 | A=나 B=역무원","lines":[
        {"spk":"A","jp":"新宿駅に行きたいのですが、どの電車に乗ればいいですか？",
         "read":"신주쿠에키니 이키타이노데스가, 도노 덴샤니 노레바 이이데스카？",
         "ko":"신주쿠역에 가고 싶은데, 어떤 전철을 타면 되나요?"},
        {"spk":"B","jp":"山手線に乗って、新宿で降りてください。3番線です。",
         "read":"야마노테센니 놋테, 신주쿠데 오리테 쿠다사이。산반센데스。",
         "ko":"야마노테선을 타고 신주쿠에서 내리세요. 3번 승강장입니다."},
        {"spk":"A","jp":"ICカードで乗れますか？","read":"아이씨카도데 노레마스카？",
         "ko":"IC카드로 탈 수 있나요?"},
        {"spk":"B","jp":"はい、タッチして改札を通ってください。","read":"하이, 탓치시테 카이사츠오 토오테 쿠다사이。",
         "ko":"네, 터치하고 개찰구를 통과하세요."},
    ]},
    {"title":"🏥 긴급 상황","scene":"📍 응급 상황 | A=나 B=행인","lines":[
        {"spk":"A","jp":"助けてください！財布を盗まれてしまいました！",
         "read":"타스케테 쿠다사이！사이후오 누스마레테 시마이마시타！",
         "ko":"도와주세요! 지갑을 도둑맞아버렸어요!"},
        {"spk":"B","jp":"大丈夫ですか？すぐに警察を呼びましょう。",
         "read":"다이죠부데스카？스구니 케이사츠오 요비마쇼。",
         "ko":"괜찮으세요? 바로 경찰을 부릅시다."},
        {"spk":"A","jp":"日本語がまだうまくないので、英語で話せますか？",
         "read":"니혼고가 마다 우마쿠나이노데, 에이고데 하나세마스카？",
         "ko":"일본어를 아직 잘 못해서요, 영어로 말할 수 있나요?"},
        {"spk":"B","jp":"近くの交番に一緒に行きましょう。",
         "read":"치카쿠노 코반니 잇쇼니 이키마쇼。","ko":"근처 파출소에 같이 갑시다."},
        {"spk":"A","jp":"本当にありがとうございます。助かりました。",
         "read":"혼토니 아리가토오 고자이마스。타스카리마시타。","ko":"정말 감사합니다. 살았습니다."},
    ]},
]

# ============================================================
# 퀴즈 문제 풀 생성
# ============================================================
def build_quiz_pool():
    all_v = []
    for cat, ws in VOCAB.items():
        for w in ws:
            all_v.append({"cat": cat, **w})
    pool = []
    for i, item in enumerate(all_v):
        wrong_pool = [w["ko"] for j, w in enumerate(all_v) if j != i]
        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        opts = wrongs + [item["ko"]]
        random.shuffle(opts)
        pool.append({"q_jp": item["jp"], "q_read": item["read"],
                     "answer": item["ko"], "options": opts,
                     "category": item["cat"], "example": item["ex"]})
    random.shuffle(pool)
    return pool

if not st.session_state.quiz_pool:
    st.session_state.quiz_pool = build_quiz_pool()

# ============================================================
# BGM
# ============================================================
BGM_OPTIONS = {
    "🌸 잔잔한 Lo-fi":      "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🎋 감성 앰비언트":     "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    "🍜 경쾌한 팝 리듬":   "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "🎐 여유로운 어쿠스틱": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
}

# ============================================================
# UI
# ============================================================
st.markdown('<div class="app-title">🇯🇵 일본어 1일 마스터</div>', unsafe_allow_html=True)
st.markdown('<div class="app-sub">Japan Shopping &amp; 일본어 완전정복 — 중급자 맞춤판</div>', unsafe_allow_html=True)

# BGM 플레이어
st.markdown('<div class="bgm-box"><div class="bgm-label">🎵 여행 BGM — 선택 후 ▶ 클릭!</div>', unsafe_allow_html=True)
bgm_sel = st.selectbox("BGM", list(BGM_OPTIONS.keys()), label_visibility="collapsed")
_bu = BGM_OPTIONS[bgm_sel]
components.html(f"""
<style>
  body{{margin:0;padding:0;background:transparent;}}
  .bp{{display:flex;align-items:center;gap:10px;
    background:linear-gradient(135deg,#f3e5f5,#e8eaf6);
    border-radius:14px;padding:8px 14px;border:1.5px solid #d1c4e9;}}
  .bb{{background:linear-gradient(135deg,#9c27b0,#673ab7);color:white;
    border:none;border-radius:50%;width:40px;height:40px;
    font-size:1.1rem;cursor:pointer;flex-shrink:0;
    box-shadow:0 3px 10px rgba(156,39,176,.4);}}
  .bt{{font-size:.78rem;font-weight:700;color:#4a148c;flex:1;}}
  .bs{{font-size:.68rem;color:#7986cb;margin-top:2px;}}
  input[type=range]{{width:100%;accent-color:#9c27b0;margin-top:4px;}}
</style>
<div class="bp">
  <button class="bb" id="btn" onclick="toggle()">▶</button>
  <div style="flex:1;min-width:0;">
    <div class="bt">{bgm_sel}</div>
    <div class="bs" id="st">▶ 버튼을 눌러 재생하세요</div>
    <input type="range" id="sk" value="0" step="1">
  </div>
  <span style="font-size:.7rem;color:#7986cb;" id="tm">0:00</span>
</div>
<audio id="au" loop preload="auto"><source src="{_bu}" type="audio/mpeg"></audio>
<script>
var a=document.getElementById('au'),btn=document.getElementById('btn'),
    sk=document.getElementById('sk'),st=document.getElementById('st'),
    tm=document.getElementById('tm');
function fmt(s){{var m=Math.floor(s/60),sc=Math.floor(s%60);return m+':'+(sc<10?'0':'')+sc;}}
function toggle(){{
  if(a.paused){{a.play().then(function(){{btn.textContent='⏸';st.textContent='재생 중 🎵';}}).catch(function(e){{st.textContent='오류:'+e.message;}});}}
  else{{a.pause();btn.textContent='▶';st.textContent='일시정지';}}
}}
a.addEventListener('timeupdate',function(){{
  if(a.duration){{sk.max=Math.floor(a.duration);sk.value=Math.floor(a.currentTime);
    tm.textContent=fmt(a.currentTime)+'/'+fmt(a.duration);}}
}});
sk.addEventListener('input',function(){{a.currentTime=sk.value;}});
window.parent.postMessage({{type:'streamlit:setFrameHeight',height:72}},'*');
</script>
""", height=72)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# 탭
tab_shop, tab_vocab, tab_grammar, tab_dial, tab_quiz, tab_phrase, tab_cart = st.tabs([
    "🛍️ 쇼핑핫템", "📖 어휘", "📚 문법", "💬 대화문",
    "🧠 퀴즈", "🗣️ 치트키", f"🧺 장바구니({len(st.session_state.cart)})",
])

# ── TAB 1: 쇼핑 핫템 ────────────────────────────────────────
with tab_shop:
    st.markdown('<div class="sec-title">📍 여행 지역 선택</div>', unsafe_allow_html=True)
    region = st.selectbox("지역", list(SHOPPING_DATA.keys()), label_visibility="collapsed")
    items  = SHOPPING_DATA[region]
    st.markdown(f'<div class="region-badge">✈️ {region} — 필수 쇼핑 Best {len(items)}</div>', unsafe_allow_html=True)
    for i, item in enumerate(items):
        # 쇼핑 카드는 components.html (TTS 포함)
        components.html(_HEAD + f"""
<div class="shop-card">
  <span class="item-emoji">{item['emoji']}</span>
  <div class="item-name">{item['name']}</div>
  <div class="item-brand">{item['brand']}</div>
  <div class="item-desc">{item['desc']}</div>
  <div class="item-price">💴 {item['price']}</div>
  <div class="item-where">{item['where']}</div>
  <div class="item-tip">{item['tip']}</div>
</div>
""", height=230)
        if st.button(f"🛒 장바구니 담기 — {item['name']}", key=f"add_{region}_{i}"):
            st.session_state.cart.append({"emoji":item["emoji"],"name":item["name"],
                "brand":item["brand"],"price":item["price"],"region":region})
            st.toast(f"✅ '{item['name']}' 담았어요!", icon="🛒")

# ── TAB 2: 어휘 마스터 ──────────────────────────────────────
with tab_vocab:
    st.markdown('<div class="sec-title">📖 여행 필수 어휘 (N3~N4) — 단어/예문 탭하면 🔊</div>', unsafe_allow_html=True)
    cats   = list(VOCAB.keys())
    cat_sel = st.radio("카테고리", cats, horizontal=True, label_visibility="collapsed")
    words  = VOCAB[cat_sel]

    # 해당 카테고리 모든 카드를 하나의 iframe에
    cards_html = ""
    for w in words:
        ex_speak = w['ex'].split('(')[0].strip()
        cards_html += f"""
<div class="card vocab-card">
  <span class="vocab-badge">{cat_sel}</span><br>
  <span class="vocab-jp" onclick="speakJP('{w['jp']}')">{w['jp']} <span class="tts">🔊</span></span><br>
  <span class="vocab-read">{w['read']}</span><br>
  <div class="vocab-ko">🇰🇷 {w['ko']}</div>
  <div class="vocab-ex" onclick="speakJP('{ex_speak}')">✏️ {w['ex']} <span class="tts">🔊</span></div>
</div>"""

    components.html(_HEAD + cards_html, height=len(words) * 185 + 20, scrolling=False)

# ── TAB 3: 문법 패턴 ────────────────────────────────────────
with tab_grammar:
    st.markdown('<div class="sec-title">📚 중급 문법 패턴 (N3~N4) — 탭하면 🔊</div>', unsafe_allow_html=True)
    g_html = ""
    for g in GRAMMAR:
        g_html += f"""
<div class="card grammar-card">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;flex-wrap:wrap;">
    <span class="grammar-pattern" onclick="speakJP('{g['ex_jp']}')">{g['pattern']} <span class="tts">🔊</span></span>
    <span class="grammar-level">{g['level']}</span>
  </div>
  <span class="grammar-meaning">{g['meaning']}</span>
  <div style="margin-top:6px;">
    <div class="grammar-ex-jp" onclick="speakJP('{g['ex_jp']}')">{g['ex_jp']} <span class="tts">🔊</span></div>
    <div class="grammar-ex-read">{g['ex_read']}</div>
    <div class="grammar-ex-ko">🇰🇷 {g['ex_ko']}</div>
  </div>
  <div class="grammar-tip">💡 {g['tip']}</div>
</div>"""
    components.html(_HEAD + g_html, height=len(GRAMMAR) * 195 + 20, scrolling=False)

# ── TAB 4: 여행 대화문 ──────────────────────────────────────
with tab_dial:
    st.markdown('<div class="sec-title">💬 여행 완성 대화문 — 탭하면 🔊</div>', unsafe_allow_html=True)
    d_html = ""
    for dial in DIALOGUES:
        rows = ""
        for line in dial["lines"]:
            spk_cls = "d-spk-a" if line["spk"] == "A" else "d-spk-b"
            bub_cls = "d-bub-a" if line["spk"] == "A" else "d-bub-b"
            rows += f"""
<div class="d-row">
  <span class="{spk_cls}">{line['spk']}</span>
  <div class="{bub_cls}">
    <div class="d-jp" onclick="speakJP('{line['jp']}')">{line['jp']} <span class="tts">🔊</span></div>
    <div class="d-read" onclick="speakJP('{line['jp']}')">{line['read']}</div>
    <div class="d-ko">🇰🇷 {line['ko']}</div>
  </div>
</div>"""
        d_html += f"""
<div class="dialogue-wrap">
  <div class="dialogue-title">{dial['title']}</div>
  <span class="dialogue-scene">{dial['scene']}</span>
  {rows}
</div>"""
    total_lines = sum(len(d["lines"]) for d in DIALOGUES)
    components.html(_HEAD + d_html, height=len(DIALOGUES)*100 + total_lines*110 + 30, scrolling=False)

# ── TAB 5: 퀴즈 ─────────────────────────────────────────────
with tab_quiz:
    st.markdown('<div class="sec-title">🧠 어휘 퀴즈</div>', unsafe_allow_html=True)
    pool  = st.session_state.quiz_pool
    total = len(pool)
    idx   = st.session_state.quiz_idx

    st.markdown(f"""
<div class="quiz-score-box">
  <div style="font-size:.72rem;opacity:.85;font-weight:600;">현재 점수</div>
  <div style="font-size:2rem;font-weight:900;line-height:1.1;">
    {st.session_state.quiz_score}
    <span style="font-size:1rem;opacity:.7;">/ {st.session_state.quiz_total}</span>
  </div>
  <div style="font-size:.68rem;opacity:.8;">문제 {min(idx+1,total)} / {total}</div>
</div>
<div class="progress-bar-wrap">
  <div class="progress-bar-fill" style="width:{int(idx/total*100) if total else 0}%"></div>
</div>""", unsafe_allow_html=True)

    if idx >= total:
        acc = int(st.session_state.quiz_score / st.session_state.quiz_total * 100) if st.session_state.quiz_total else 0
        grade = "🏆 완벽!" if acc>=90 else "🌸 우수!" if acc>=70 else "💪 분발!"
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#9c27b0,#673ab7);color:white;
  border-radius:22px;padding:1.5rem 1rem;text-align:center;
  box-shadow:0 6px 20px rgba(156,39,176,.4);">
  <div style="font-size:2.5rem;">{grade}</div>
  <div style="font-size:1.5rem;font-weight:900;">{acc}점</div>
  <div style="font-size:.8rem;opacity:.85;margin-top:.3rem;">
    {st.session_state.quiz_total}문제 중 {st.session_state.quiz_score}개 정답
  </div>
</div>""", unsafe_allow_html=True)
        if st.button("🔄 퀴즈 다시 시작"):
            for k in ["quiz_idx","quiz_score","quiz_total","quiz_answered","quiz_correct"]:
                st.session_state[k] = 0 if "score" in k or "idx" in k or "total" in k else False
            st.session_state.quiz_correct = None
            st.session_state.quiz_pool = build_quiz_pool()
            st.rerun()
    else:
        q = pool[idx]
        # 문제 표시 (TTS 포함 — components.html)
        components.html(_HEAD + f"""
<div class="quiz-card">
  <span class="quiz-q-label">📂 {q['category']} | Q{idx+1}</span>
  <div class="quiz-q-jp" onclick="speakJP('{q['q_jp']}')">{q['q_jp']} <span class="tts">🔊</span></div>
  <div class="quiz-q-read" onclick="speakJP('{q['q_jp']}')">{q['q_read']}</div>
  <div style="font-size:.72rem;color:#9e9e9e;">아래에서 한국어 뜻을 고르세요</div>
</div>""", height=165)

        if not st.session_state.quiz_answered:
            for opt in q["options"]:
                if st.button(opt, key=f"opt_{idx}_{opt}"):
                    st.session_state.quiz_answered = True
                    st.session_state.quiz_total   += 1
                    if opt == q["answer"]:
                        st.session_state.quiz_correct = True
                        st.session_state.quiz_score  += 1
                        st.toast("🎉 정답!", icon="✅")
                    else:
                        st.session_state.quiz_correct = False
                        st.toast(f"😅 오답! 정답: {q['answer']}", icon="❌")
                    st.rerun()
        else:
            ok   = st.session_state.quiz_correct
            col  = "#43a047" if ok else "#e53935"
            bg   = "#e8f5e9" if ok else "#ffebee"
            icon = "✅ 정답!" if ok else "❌ 오답!"
            st.markdown(f"""
<div style="background:{bg};border:2px solid {col};border-radius:14px;
  padding:.8rem 1rem;text-align:center;margin-bottom:.5rem;">
  <div style="font-size:1.1rem;font-weight:800;color:{col};">{icon}</div>
  <div style="font-size:.85rem;font-weight:700;color:#333;margin-top:.2rem;">정답: {q['answer']}</div>
  <div style="font-size:.72rem;color:#546e7a;margin-top:.3rem;">✏️ {q['example']}</div>
</div>""", unsafe_allow_html=True)
            if st.button("다음 문제 ➡️", key=f"next_{idx}"):
                st.session_state.quiz_idx      += 1
                st.session_state.quiz_answered  = False
                st.session_state.quiz_correct   = None
                st.rerun()

# ── TAB 6: 치트키 ───────────────────────────────────────────
with tab_phrase:
    st.markdown('<div class="sec-title">🗣️ 쇼핑 치트키 — 탭하면 🔊</div>', unsafe_allow_html=True)
    ph_html = ""
    for p in PHRASES:
        ph_html += f"""
<div class="phrase-card">
  <span class="phrase-sit">{p['situation']}</span>
  <span class="phrase-jp" onclick="speakJP('{p['japanese']}')">{p['japanese']} <span class="tts">🔊</span></span>
  <div class="phrase-ko">🇰🇷 {p['korean']}</div>
  <span class="phrase-read" onclick="speakJP('{p['japanese']}')">{p['reading']}</span>
  <div class="phrase-tip">💡 {p['tip']}</div>
</div>"""
    components.html(_HEAD + ph_html, height=len(PHRASES)*165+20, scrolling=False)

# ── TAB 7: 장바구니 ─────────────────────────────────────────
with tab_cart:
    st.markdown('<div class="sec-title">🧺 내 쇼핑 위시리스트</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.markdown("""
<div style="text-align:center;padding:3rem 1rem 2rem;color:#c0a898;">
  <div style="font-size:3rem;">🛒</div>
  <div style="font-size:.92rem;font-weight:700;color:#a08070;margin:.5rem 0 .2rem;">
    장바구니가 비어있어요</div>
  <div style="font-size:.75rem;">쇼핑핫템 탭에서 아이템을 담아보세요!</div>
</div>""", unsafe_allow_html=True)
    else:
        to_remove = None
        for i, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
<div class="cart-card">
  <span style="font-size:1.8rem;flex-shrink:0;">{item['emoji']}</span>
  <div style="flex:1;min-width:0;">
    <div style="font-size:.85rem;font-weight:700;color:#3d2010;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item['name']}</div>
    <span style="font-size:.65rem;color:#e65100;background:#fff3e0;
      padding:1px 6px;border-radius:8px;font-weight:600;">{item['region']}</span>
    <div style="font-size:.72rem;color:#c0392b;font-weight:600;margin-top:2px;">{item['price']}</div>
  </div>
</div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{i}"):
                    to_remove = i
        if to_remove is not None:
            removed = st.session_state.cart.pop(to_remove)
            st.toast(f"🗑️ '{removed['name']}' 삭제됨", icon="🗑️")
            st.rerun()
        count = len(st.session_state.cart)
        st.markdown(f"""
<div class="cart-total">
  <div style="font-size:.72rem;opacity:.85;font-weight:600;">총 위시리스트</div>
  <div style="font-size:1.9rem;font-weight:900;line-height:1.1;">{count}개 아이템</div>
  <div style="font-size:.68rem;opacity:.8;margin-top:.2rem;">✈️ 스크린샷으로 저장해두세요!</div>
</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ 전체 비우기"):
            st.session_state.cart.clear()
            st.toast("장바구니를 비웠어요!", icon="✨")
            st.rerun()

st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:.68rem;color:#b09878;
  padding-bottom:1.5rem;line-height:1.8;">
  🇯🇵 즐거운 일본 여행 되세요! | Made with ❤️ &amp; Streamlit<br>
  BGM: SoundHelix Royalty-Free · 어휘 기준: JLPT N3~N4 · TTS: Web Speech API
</div>
""", unsafe_allow_html=True)
