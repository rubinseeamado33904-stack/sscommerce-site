# -*- coding: utf-8 -*-
"""sscommerce.net 하위 페이지·sitemap·robots·llms.txt 생성기.

  python _build/build_pages.py            # 페이지 생성 (저장소 루트 기준)
  python _build/build_pages.py --ping     # 생성 후 IndexNow(빙·네이버 등)에 바뀐 URL 알림

규칙 (카톡 SEO 정리):
  - 제목은 검색어 먼저, 브랜드는 끝 ("피쉬그립 … | SS Commerce")
  - 한 키워드 = 한 페이지. 같은 키워드를 여러 페이지에 나눠 쓰지 않는다
  - 개인 연락처(휴대폰 등)는 어떤 페이지에도 넣지 않는다
  - 글을 추가하면 GUIDES에 넣고 다시 실행 → sitemap 자동 갱신
"""
import html, json, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sscommerce.net"
TODAY = "2026-10-27"
INDEXNOW_KEY = "8d34bba48157cc0fd7174460e3cc4f46"
BRAND = "SS Commerce"

NAVER = "https://smartstore.naver.com/ssmake100"
AUCTION = "https://stores.auction.co.kr/sscommerse"
GMARKET = "https://minishop.gmarket.co.kr/sscommerse"
au = lambda n: f"http://itempage3.auction.co.kr/DetailView.aspx?itemno={n}"
gm = lambda n: f"https://item.gmarket.co.kr/Item?goodsCode={n}"

PRODUCTS = {
    "passport": ("여권·카드지갑 일체형 케이스", "여행 · 가죽 소품", "/img/passport.jpg", "옥션", au("F689923813")),
    "passport-wallet": ("다기능 가죽 여권지갑", "항공권·카드 수납", "/img/passport-wallet.jpg", "옥션", au("F689916462")),
    "cardwallet": ("천연가죽 RFID 카드지갑", "스키밍 방지", "/img/cardwallet.jpg", "옥션", au("F689916302")),
    "slimcard": ("슬림 카드지갑 카드홀더", "카드 수십 장 한 번에", "/img/slimcard.jpg", "G마켓", gm("4882006198")),
    "balaclava": ("겨울 니트 발라클라바", "귀·목까지 따뜻하게", "/img/balaclava.jpg", "옥션", au("F689923747")),
    "beanie": ("니트 귀마개 비니", "땋은 끈 포인트", "/img/beanie.jpg", "옥션", au("F689923838")),
    "padding": ("여성 경량 롱패딩", "5가지 색상", "/img/padding.jpg", "G마켓", gm("4869649712")),
    "fishgrip": ("피쉬그립 물고기 집게", "무게 측정 · 360도 회전", "/img/fishgrip.jpg", "옥션", au("F657289106")),
    "tacklebox": ("에기케이스 70구 태클박스", "낚시 · 수납", "/img/tacklebox.jpg", "옥션", au("F657294089")),
    "hookcap": ("에기 훅캡 세트", "바늘 보호 · 릴홀더", "/img/hookcap.jpg", "G마켓", gm("4849481178")),
    "xmas": ("크리스마스 뜨개 펜던트 DIY 키트", "트리 · 리스 장식", "/img/xmas.jpg", "옥션", au("F689886065")),
}

# ---------- 카테고리 페이지: 키워드 하나씩 ----------
CATEGORIES = [
    dict(slug="passport-wallet", kw="여권지갑",
         title="가죽 여권지갑 추천 – 여권·항공권·카드 한 번에 | SS Commerce",
         desc="해외여행 갈 때 여권, 항공권, 카드를 한 번에 넣는 가죽 여권지갑. 여권·카드지갑 일체형과 다기능 여권지갑을 옥션·스마트스토어에서 만나보세요.",
         h1="가죽 여권지갑", lead="출국장에서 여권과 항공권, 카드를 따로 찾지 않도록 한 지갑에 모았습니다.",
         items=["passport", "passport-wallet"], search="여권지갑",
         body=[("여권지갑, 이런 분께 필요합니다", "공항에서는 여권·탑승권·결제 카드를 여러 번 꺼내게 됩니다. 여권지갑은 이 세 가지를 한곳에 두어 잃어버릴 걱정을 줄이고, 여권 표지가 구겨지거나 젖는 것을 막아 줍니다."),
               ("고를 때 볼 것", "① 여권이 너무 빡빡하지 않게 들어가는지 ② 탑승권을 접지 않고 넣을 칸이 있는지 ③ 카드·현금 칸이 몇 개인지 ④ 목에 걸거나 손목에 거는 끈이 필요한지. 상품마다 칸 구성이 다르니 상세페이지의 사진을 꼭 확인하세요.")],
         faq=[("여권지갑에 넣으면 전자여권 칩이 손상되나요?", "일반 가죽 여권지갑은 칩에 영향을 주지 않습니다. 오히려 접힘과 습기를 막아 여권 보호에 도움이 됩니다."),
              ("여권 크기는 다 같나요?", "한국 여권은 국제 규격(약 125×88mm)이라 일반 여권지갑에 맞습니다. 두꺼운 여권 커버를 씌운 채로는 들어가지 않을 수 있습니다.")],
         related=["card-wallet", "guide/rfid-wallet"]),
    dict(slug="card-wallet", kw="RFID 카드지갑",
         title="RFID 차단 카드지갑 – 스키밍 방지 슬림 카드홀더 | SS Commerce",
         desc="카드 정보를 무단으로 읽는 스키밍을 막는 RFID 차단 카드지갑과 카드 여러 장을 얇게 넣는 슬림 카드홀더. 천연가죽 카드지갑을 옥션·G마켓에서.",
         h1="RFID 차단 카드지갑", lead="얇게 들고 다니면서, 카드 정보는 지갑 안에서 지킵니다.",
         items=["cardwallet", "slimcard"], search="카드지갑",
         body=[("RFID 차단 카드지갑이란", "교통카드와 비접촉 결제 카드는 가까이 대면 무선(RFID·NFC)으로 정보를 주고받습니다. RFID 차단 지갑은 금속 차폐층으로 이 신호를 막아, 지갑 안에 있는 동안에는 외부 기기가 카드를 읽지 못하게 합니다."),
               ("슬림 카드홀더를 고르는 기준", "자주 쓰는 카드가 3~5장이면 슬림형, 멤버십 카드까지 10장 이상이면 아코디언식 카드홀더가 편합니다. 지폐를 같이 넣을지도 미리 정해 두세요.")],
         faq=[("RFID 차단 지갑에 교통카드를 넣으면 찍히나요?", "차단 기능이 있는 칸에서는 찍히지 않습니다. 교통카드는 차단층 바깥 칸에 두거나 꺼내서 사용하세요."),
              ("스키밍 피해가 실제로 많나요?", "국내 실제 피해 사례는 드문 편입니다. 다만 해외여행이나 사람이 붐비는 곳에서 안심하고 싶다면 차단 지갑이 간단한 대비책입니다.")],
         related=["passport-wallet", "guide/rfid-wallet"]),
    dict(slug="balaclava", kw="발라클라바",
         title="겨울 니트 발라클라바·귀마개 비니 – 방한 모자 | SS Commerce",
         desc="귀와 목까지 한 번에 덮는 겨울 니트 발라클라바, 귀마개 달린 니트 비니, 여성 경량 롱패딩. 출퇴근·캠핑·라이딩용 방한 아이템을 옥션·G마켓에서.",
         h1="겨울 니트 발라클라바", lead="모자, 귀마개, 넥워머를 하나로. 칼바람 부는 날 가장 먼저 꺼내게 되는 방한 아이템입니다.",
         items=["balaclava", "beanie", "padding"], search="발라클라바",
         body=[("발라클라바가 좋은 이유", "발라클라바는 머리·귀·목을 이어서 감싸는 방한 모자입니다. 목도리처럼 풀리지 않고, 모자와 넥워머를 따로 챙길 필요가 없어 자전거·오토바이·캠핑처럼 바람을 정면으로 맞는 활동에 특히 편합니다."),
               ("니트와 기모, 무엇을 고를까", "도심 출퇴근에는 스타일이 사는 니트형, 영하 10도 아래 야외 활동에는 안감 기모형이 낫습니다. 얼굴이 답답한 분은 귀만 덮는 귀마개 비니도 좋은 선택입니다.")],
         faq=[("발라클라바 사이즈는 어떻게 고르나요?", "대부분 신축성 있는 프리사이즈입니다. 머리둘레가 큰 편이면 상세페이지의 실측(머리둘레·길이)을 확인하세요."),
              ("세탁은 어떻게 하나요?", "니트 제품은 미지근한 물에 중성세제로 손세탁하고 눕혀서 말리면 늘어남을 줄일 수 있습니다.")],
         related=["guide/overseas-purchase-agency"]),
    dict(slug="fish-grip", kw="피쉬그립",
         title="피쉬그립 물고기 집게 – 무게 측정 립그립·에기케이스 | SS Commerce",
         desc="물고기를 안전하게 잡고 무게까지 재는 피쉬그립(립그립), 에기 70개를 정리하는 에기케이스 태클박스, 바늘을 보호하는 에기 훅캡. 에깅·루어 낚시용품.",
         h1="피쉬그립 물고기 집게", lead="손 다칠 걱정 없이 고기를 잡고, 그 자리에서 무게까지. 에깅 낚시 소품도 함께 모았습니다.",
         items=["fishgrip", "tacklebox", "hookcap"], search="피쉬그립",
         body=[("피쉬그립을 쓰는 이유", "물고기 입을 집게로 물어 고정하는 도구라 지느러미 가시나 이빨에 손을 다치지 않고, 고기를 놓치는 일도 줄어듭니다. 저울이 달린 제품은 바로 무게를 재고 놓아줄 수 있습니다."),
               ("에깅 낚시 소품 정리", "에기(무늬오징어·갑오징어용 루어)는 바늘이 많아 서로 엉키기 쉽습니다. 칸이 나뉜 에기케이스에 세워 보관하고, 이동할 때는 훅캡을 씌우면 바늘과 가방을 함께 보호할 수 있습니다.")],
         faq=[("피쉬그립과 립그립은 같은 건가요?", "네, 같은 도구를 부르는 이름입니다. 고기 입술(립)을 잡는다고 해서 립그립이라고도 합니다."),
              ("바닷물에 써도 되나요?", "사용 후 민물로 헹구고 말려 두면 녹을 줄일 수 있습니다. 회전 부위는 가끔 기름칠을 해 주세요.")],
         related=["guide/overseas-purchase-agency"]),
    dict(slug="christmas-diy-kit", kw="크리스마스 DIY 키트",
         title="크리스마스 뜨개 DIY 키트 – 트리·리스 펜던트 만들기 | SS Commerce",
         desc="실과 재료가 다 들어 있어 처음 해도 완성하는 크리스마스 뜨개 펜던트 DIY 키트. 트리·리스 장식, 아이와 함께하는 연말 만들기.",
         h1="크리스마스 뜨개 DIY 키트", lead="재료를 따로 사지 않아도 됩니다. 상자를 열고 바로 연말 장식을 만들어 보세요.",
         items=["xmas"], search="크리스마스 DIY",
         body=[("이런 분께 추천합니다", "뜨개는 처음이지만 손으로 만든 장식을 걸고 싶은 분, 아이와 함께 연말 시간을 보내고 싶은 가족, 모임 선물을 직접 만들고 싶은 분께 맞습니다."),
               ("주문 시기", "해외 구매대행 상품은 받기까지 보통 1~2주가 걸립니다. 크리스마스에 쓰려면 12월 초까지는 주문해 두는 것이 안전합니다.")],
         faq=[("완전 초보도 만들 수 있나요?", "기본 재료가 들어 있는 키트라 처음 하는 분도 시도할 수 있습니다. 난이도와 구성은 상세페이지에서 확인하세요."),
              ("언제 주문해야 크리스마스 전에 받나요?", "해외 배송 기간을 생각하면 12월 초, 늦어도 12월 둘째 주 전 주문을 권합니다.")],
         related=["guide/overseas-purchase-agency"]),
]

# ---------- 가이드(정보 글): AI가 답으로 인용하기 좋은 문답형 ----------
GUIDES = [
    dict(slug="overseas-purchase-agency", kw="해외구매대행",
         title="해외구매대행이란? 주문 전 알아둘 5가지 – 배송기간·관세·반품 | SS Commerce",
         desc="해외구매대행이 무엇인지, 직구와 무엇이 다른지, 배송은 얼마나 걸리고 관세는 언제 내는지, 반품할 때 무엇을 조심해야 하는지 정리했습니다.",
         h1="해외구매대행이란? 주문 전 알아둘 5가지",
         lead="해외 쇼핑몰에서 직접 사기 번거로운 상품을, 국내 판매자가 대신 사서 보내 주는 방식입니다.",
         sections=[
             ("해외구매대행이란", "해외구매대행은 국내 판매자가 해외 쇼핑몰의 상품을 소개하고, 고객이 주문하면 판매자가 현지에서 대신 구매해 고객 주소로 보내 주는 방식입니다. 고객은 한국어로 된 상품 정보를 보고, 원화로 결제하고, 국내 쇼핑몰(스마트스토어·옥션·G마켓 등)의 고객센터로 문의할 수 있습니다."),
             ("해외직구와 다른 점", "해외직구는 고객이 해외 사이트에서 직접 결제하고 배송대행지를 거쳐 받는 방식입니다. 구매대행은 판매자가 구매·배송·통관 안내를 맡기 때문에 외국어 사이트를 다룰 필요가 없고, 문제가 생기면 국내 판매자에게 연락하면 됩니다."),
             ("① 배송 기간", "현지 구매 → 국제 배송 → 통관 → 국내 택배 순서로 진행되어 보통 1~2주가 걸립니다. 명절, 연말, 현지 쇼핑 행사 기간에는 더 늦어질 수 있습니다."),
             ("② 개인통관고유부호", "해외에서 들어오는 물건을 개인이 받으려면 주문할 때 개인통관고유부호(P로 시작하는 13자리)를 입력해야 합니다. 이름과 휴대폰 번호가 부호에 등록된 정보와 같아야 통관이 늦어지지 않습니다. 발급 방법은 아래 가이드를 참고하세요."),
             ("③ 관세와 부가세", "개인이 쓰려고 사는 물건은 물품 가격이 미화 150달러(미국에서 오는 일부 물품은 200달러) 이하면 대개 관세·부가세가 면제됩니다. 같은 날 여러 건이 한꺼번에 들어오면 합산해서 과세될 수 있으니 큰 금액을 나눠 주문할 때는 주의하세요."),
             ("④ 반품과 교환", "해외에서 온 상품은 반품할 때 국제 반송비가 들 수 있습니다. 단순 변심 반품 조건과 비용은 상품마다 다르니 주문 전에 상세페이지의 반품 안내를 확인하세요. 불량·오배송은 판매자가 책임지고 처리합니다."),
             ("⑤ 정품과 판매자 확인", "구매대행 판매자는 사업자 정보(상호·사업자등록번호)를 공개해야 합니다. 사업자 정보가 분명하고, 현지 판매자를 어떻게 고르는지 밝히는 곳에서 사는 것이 안전합니다. SS Commerce는 해외 판매자의 신뢰도와 상품 상태를 확인한 뒤 등록합니다."),
         ],
         faq=[("해외구매대행 배송은 얼마나 걸리나요?", "보통 주문 후 1~2주입니다. 연말·명절과 현지 쇼핑 행사 기간에는 더 걸릴 수 있습니다."),
              ("해외구매대행 상품도 관세를 내나요?", "개인 사용 목적이고 물품 가격이 미화 150달러(미국발 일부 200달러) 이하면 대부분 면세입니다. 넘으면 관세와 부가세가 붙을 수 있습니다."),
              ("해외구매대행과 해외직구 중 무엇이 나은가요?", "외국어 사이트 결제와 배송대행지 이용이 번거롭다면 구매대행이 편하고, 직접 비교하며 사는 데 익숙하다면 직구가 조금 저렴할 수 있습니다.")],
         related=["guide/personal-customs-code"]),
    dict(slug="personal-customs-code", kw="개인통관고유부호",
         title="개인통관고유부호 발급 방법 – 구매대행 주문할 때 왜 필요할까 | SS Commerce",
         desc="해외구매대행·직구 주문에 필요한 개인통관고유부호를 관세청 유니패스에서 발급하는 방법, 입력할 때 자주 틀리는 부분, 분실했을 때 확인하는 방법.",
         h1="개인통관고유부호 발급 방법",
         lead="해외에서 오는 물건을 받을 때 주민등록번호 대신 쓰는 통관용 번호입니다. 한 번 발급하면 계속 쓸 수 있습니다.",
         sections=[
             ("개인통관고유부호란", "관세청이 개인에게 부여하는 통관용 고유번호로, P로 시작하는 13자리입니다. 해외구매대행이나 해외직구로 물건을 받을 때 주민등록번호를 노출하지 않고 통관할 수 있게 해 줍니다."),
             ("발급 방법", "관세청 유니패스 누리집(unipass.customs.go.kr)이나 모바일 앱에 들어가 ‘개인통관고유부호 발급’을 선택하고, 휴대폰이나 공동인증서로 본인 인증을 하면 바로 발급됩니다. 비용은 들지 않습니다."),
             ("입력할 때 자주 틀리는 것", "주문할 때 적은 받는 사람 이름과 휴대폰 번호가 부호에 등록된 정보와 다르면 통관이 멈출 수 있습니다. 가족 이름으로 주문하면서 내 부호를 넣는 경우가 가장 흔한 실수입니다. 휴대폰 번호를 바꿨다면 유니패스에서 정보도 함께 바꿔 주세요."),
             ("부호를 잊어버렸다면", "같은 유니패스 메뉴에서 본인 인증을 하면 다시 조회할 수 있습니다. 쇼핑몰 주문서에 저장해 두면 다음 주문부터 자동으로 들어갑니다."),
         ],
         faq=[("개인통관고유부호는 어디서 발급하나요?", "관세청 유니패스(unipass.customs.go.kr) 웹사이트나 앱에서 본인 인증 후 무료로 바로 발급됩니다."),
              ("개인통관고유부호가 틀리면 어떻게 되나요?", "이름·휴대폰 번호가 등록 정보와 다르면 통관이 보류되어 배송이 늦어집니다. 판매자에게 올바른 정보를 알려 주면 수정할 수 있습니다.")],
         related=["guide/overseas-purchase-agency"]),
    dict(slug="rfid-wallet", kw="RFID 차단 지갑",
         title="RFID 차단 지갑, 정말 필요할까? 스키밍 원리와 고르는 법 | SS Commerce",
         desc="RFID 차단 지갑이 무엇을 막는지, 카드 스키밍은 어떻게 일어나는지, 교통카드를 쓸 때 불편한 점은 없는지, 차단 지갑을 고르는 기준을 정리했습니다.",
         h1="RFID 차단 지갑, 정말 필요할까?",
         lead="결론부터: 꼭 필요한 물건은 아니지만, 해외여행이 잦거나 카드를 많이 들고 다닌다면 값싼 안심 장치입니다.",
         sections=[
             ("RFID 차단 지갑이 막는 것", "교통카드, 비접촉(컨택리스) 결제 카드, 전자여권에는 무선으로 정보를 주고받는 칩이 들어 있습니다. RFID 차단 지갑은 얇은 금속 차폐층으로 감싸, 지갑 안에 든 카드를 바깥 기기가 읽지 못하게 합니다."),
             ("스키밍은 어떻게 일어나나", "무선 스키밍은 휴대용 리더기를 가방이나 주머니 가까이 대서 카드 번호 같은 정보를 몰래 읽는 수법입니다. 최근 카드는 결제할 때마다 바뀌는 일회용 값을 써서 읽혀도 바로 결제에 쓰기 어렵고, 국내 실제 피해 사례도 드문 편입니다."),
             ("그래도 쓰는 이유", "사람이 붐비는 해외 관광지에서 마음 놓고 다니고 싶을 때, 여권과 카드를 한곳에 모아 두고 싶을 때 유용합니다. 지갑 하나에 교통카드 여러 장을 넣었을 때 생기는 ‘카드 충돌’을 막으려고 쓰는 사람도 있습니다."),
             ("불편한 점", "차단 칸에 넣은 교통카드는 단말기에 대도 찍히지 않습니다. 자주 쓰는 교통카드는 차단층 바깥 칸에 두는 구조인지 확인하세요."),
             ("고르는 기준", "① 차단층이 지갑 전체인지 일부 칸인지 ② 자주 쓰는 카드가 몇 장인지(슬림형 vs 카드홀더) ③ 여권도 함께 넣을지(여권지갑 일체형). 가죽 소재는 오래 쓸수록 손에 길드는 맛이 있습니다."),
         ],
         faq=[("RFID 차단 지갑은 효과가 있나요?", "네, 차폐층이 있는 칸에 든 비접촉 카드는 외부 리더기가 읽지 못합니다. 다만 국내 실제 스키밍 피해는 드물어 필수품이라기보다 안심용입니다."),
              ("RFID 지갑에 넣으면 교통카드가 안 찍히나요?", "차단 칸 안에서는 찍히지 않습니다. 교통카드는 바깥 칸에 두거나 꺼내서 쓰세요.")],
         related=["card-wallet", "passport-wallet"]),
]

NAV_LABEL = {c["slug"]: c["h1"] for c in CATEGORIES} | {"guide/" + g["slug"]: g["h1"] for g in GUIDES}

# ---------- 공통 조각 ----------
e = html.escape

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def head(title, desc, path, extra_ld=()):
    url = SITE + path
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SS Commerce 에스에스커머스">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FDF9F4">
<link rel="icon" href="/character.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="/assets/sub.css">
{"".join(ld(x) for x in extra_ld)}
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<header class="top">
  <a class="logo" href="/" aria-label="SS Commerce 홈"><img src="/character.svg" alt="">SS <b>Commerce</b></a>
  <nav aria-label="주요 메뉴">
    <a href="/#goods">상품</a>
    <a href="/guide/">구매 가이드</a>
    <a href="/#stores">쇼핑몰</a>
  </nav>
</header>
"""

def crumbs(trail):
    items = [("홈", "/")] + trail
    vis = " <span aria-hidden=\"true\">›</span> ".join(
        f'<a href="{u}">{e(n)}</a>' if i < len(items) - 1 else f'<span aria-current="page">{e(n)}</span>'
        for i, (n, u) in enumerate(items))
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="현재 위치">{vis}</nav>', data

def faq_block(faq):
    rows = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return f'<section class="faq"><h2>자주 묻는 질문</h2>{rows}</section>', data

def related_block(slugs):
    links = "".join(f'<a href="/{s}/">{e(NAV_LABEL[s])}<span aria-hidden="true">→</span></a>' for s in slugs)
    return f'<section class="related"><h2>함께 보면 좋은 글</h2><div>{links}</div></section>'

def card(key):
    name, note, img, where, url = PRODUCTS[key]
    cls = "au" if where == "옥션" else "gm"
    return (f'<a class="card {cls}" href="{url}" target="_blank" rel="noopener">'
            f'<figure><img src="{img}" alt="{e(name)}" loading="lazy" width="800" height="1000"><span class="where">{where}</span></figure>'
            f'<span class="nm">{e(name)}</span><span class="note">{e(note)}</span></a>')

FOOT = f"""<footer>
  <div class="wrap">
    <p class="f-brand"><b>SS Commerce</b> 에스에스 커머스 · 해외구매대행 · 해외수출</p>
    <p>상호 에스에스 커머스 · 사업자등록번호 866-06-03336 · 서울특별시 송파구 · <a href="mailto:contact@sscommerce.net">contact@sscommerce.net</a></p>
    <p class="f-links"><a href="/">홈</a><a href="/guide/">구매 가이드</a><a href="{NAVER}" target="_blank" rel="noopener">스마트스토어</a><a href="{AUCTION}" target="_blank" rel="noopener">옥션</a><a href="{GMARKET}" target="_blank" rel="noopener">G마켓</a></p>
  </div>
</footer>
</body>
</html>
"""

def write(path, text):
    p = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("  ", path)

# ---------- 페이지 생성 ----------
def build_category(c):
    path = f"/{c['slug']}/"
    cr, cr_ld = crumbs([("상품", "/#goods"), (c["h1"], path)])
    fq, fq_ld = faq_block(c["faq"])
    items_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": c["h1"],
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": PRODUCTS[k][0], "url": PRODUCTS[k][4]}
                                    for i, k in enumerate(c["items"])]}
    body = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in c["body"])
    search = f"{NAVER}/search?q={urllib.request.quote(c['search'])}"
    out = head(c["title"], c["desc"], path, [cr_ld, items_ld, fq_ld]) + f"""<main id="main" class="wrap">
{cr}
<section class="intro">
  <p class="eyebrow">SS COMMERCE · {e(c['kw'])}</p>
  <h1>{e(c['h1'])}</h1>
  <p class="lead">{e(c['lead'])}</p>
</section>
<section class="cards">{''.join(card(k) for k in c['items'])}</section>
<p class="more"><a class="btn" href="{search}" target="_blank" rel="noopener">스마트스토어에서 ‘{e(c['search'])}’ 더 보기 →</a></p>
<article class="prose">{body}</article>
{fq}
{related_block(c['related'])}
</main>
""" + FOOT
    write(path, out)

def build_guide(g):
    path = f"/guide/{g['slug']}/"
    cr, cr_ld = crumbs([("구매 가이드", "/guide/"), (g["h1"], path)])
    fq, fq_ld = faq_block(g["faq"])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"],
           "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ko",
           "author": {"@type": "Organization", "name": "SS Commerce", "url": SITE},
           "publisher": {"@type": "Organization", "name": "SS Commerce", "logo": {"@type": "ImageObject", "url": SITE + "/character.svg"}},
           "mainEntityOfPage": SITE + path}
    toc = "".join(f'<li><a href="#s{i}">{e(h)}</a></li>' for i, (h, _) in enumerate(g["sections"]))
    body = "".join(f'<h2 id="s{i}">{e(h)}</h2><p>{e(t)}</p>' for i, (h, t) in enumerate(g["sections"]))
    out = head(g["title"], g["desc"], path, [cr_ld, art, fq_ld]) + f"""<main id="main" class="wrap narrow">
{cr}
<article class="prose">
  <p class="eyebrow">구매 가이드 · {e(g['kw'])}</p>
  <h1>{e(g['h1'])}</h1>
  <p class="meta">SS Commerce · <time datetime="{TODAY}">{TODAY.replace('-', '.')}</time></p>
  <p class="answer">{e(g['lead'])}</p>
  <nav class="toc" aria-label="목차"><b>목차</b><ul>{toc}</ul></nav>
  {body}
</article>
{fq}
{related_block(g['related'])}
<p class="more"><a class="btn" href="/#goods">SS Commerce 상품 보러 가기 →</a></p>
</main>
""" + FOOT
    write(path, out)

def build_guide_index():
    path = "/guide/"
    cr, cr_ld = crumbs([("구매 가이드", path)])
    cards = "".join(f'<a class="g-card" href="/guide/{g["slug"]}/"><span class="kw">{e(g["kw"])}</span><b>{e(g["h1"])}</b><p>{e(g["desc"])}</p></a>' for g in GUIDES)
    cats = "".join(f'<a class="g-card" href="/{c["slug"]}/"><span class="kw">상품</span><b>{e(c["h1"])}</b><p>{e(c["lead"])}</p></a>' for c in CATEGORIES)
    out = head("해외구매대행 구매 가이드 – 배송·통관·상품 고르는 법 | SS Commerce",
               "해외구매대행으로 살 때 궁금한 배송기간, 관세, 개인통관고유부호, 상품 고르는 법을 SS Commerce가 쉽게 정리합니다.",
               path, [cr_ld]) + f"""<main id="main" class="wrap">
{cr}
<section class="intro">
  <p class="eyebrow">BUYING GUIDE</p>
  <h1>해외구매대행 구매 가이드</h1>
  <p class="lead">주문 전에 궁금한 것들을 문답으로 정리했습니다. 새 글은 꾸준히 추가됩니다.</p>
</section>
<h2 class="sec">구매대행 기초</h2>
<div class="g-grid">{cards}</div>
<h2 class="sec">상품별 안내</h2>
<div class="g-grid">{cats}</div>
</main>
""" + FOOT
    write(path, out)

def all_urls():
    return (["/"] + [f"/{c['slug']}/" for c in CATEGORIES] + ["/guide/"] + [f"/guide/{g['slug']}/" for g in GUIDES])

def build_meta():
    urls = all_urls()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "# 검색엔진·AI 검색 모두 허용\n"
        "User-agent: *\nAllow: /\nDisallow: /_build/\n\n"
        "User-agent: Yeti\nAllow: /\n\nUser-agent: Googlebot\nAllow: /\n\nUser-agent: Bingbot\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    lines = ["# SS Commerce (에스에스 커머스)", "",
             "> 해외구매대행과 해외수출을 하는 한국의 크로스보더 이커머스 사업자. 네이버 스마트스토어·옥션·G마켓에서 760여 개 상품을 판매한다.", "",
             "- 상호: 에스에스 커머스 (SS Commerce), 사업자등록번호 866-06-03336, 서울특별시 송파구",
             "- 문의: contact@sscommerce.net",
             f"- 스마트스토어: {NAVER}", f"- 옥션: {AUCTION}", f"- G마켓: {GMARKET}", "",
             "## 상품 카테고리"]
    lines += [f"- [{c['h1']}]({SITE}/{c['slug']}/): {c['desc']}" for c in CATEGORIES]
    lines += ["", "## 구매 가이드"]
    lines += [f"- [{g['h1']}]({SITE}/guide/{g['slug']}/): {g['desc']}" for g in GUIDES]
    (ROOT / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    print("   sitemap.xml · robots.txt · llms.txt · IndexNow 키")

def ping():
    body = json.dumps({"host": "sscommerce.net", "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
                       "urlList": [SITE + u for u in all_urls()]}).encode()
    for ep in ["https://api.indexnow.org/indexnow", "https://searchadvisor.naver.com/indexnow"]:
        req = urllib.request.Request(ep, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                print("   IndexNow", ep, r.status)
        except Exception as ex:
            print("   IndexNow", ep, "실패:", ex)

if __name__ == "__main__":
    print("생성:")
    for c in CATEGORIES: build_category(c)
    build_guide_index()
    for g in GUIDES: build_guide(g)
    build_meta()
    if "--ping" in sys.argv: ping()
