import subprocess

# Установка необходимых библиотек
subprocess.check_call(["pip", "install", "python-telegram-bot==20.0"])
subprocess.check_call(["pip", "install", "nest_asyncio"])

# Убедитесь, что все необходимые библиотеки установлены через терминал:
# pip install telethon
# pip install python-telegram-bot==20.0

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# Your bot token
TOKEN = "8155499355:AAGm42KV9sfLhqNTEu6onJwURcMx5pUY81A"

# Define main menu buttons with emojis
menu_buttons = {
    "ru": [
        ["💼 Кошелек", "👥 Партнеры"],
        ["ℹ️ Инфо", "💬 Отзывы"],
        ["👨‍💼 Админ", "⚙️ Настройки"]
    ],
    "uz": [
        ["💼 Hamyon", "👥 Hamkorlar"],
        ["ℹ️ Ma'lumot", "💬 Sharhlar"],
        ["👨‍💼 Admin", "⚙️ Sozlamalar"]
    ]
}

# Dictionary to store referral information and track registered users
user_referrals = {}
registered_users = set()  # Set to track unique users who have registered
user_languages = {}  # Dictionary to store user language preferences

# Welcome message and display buttons
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the user followed a referral link
    args = context.args
    if args:
        referrer_id = int(args[0])
        if user_id not in registered_users:
            registered_users.add(user_id)
            if referrer_id in user_referrals:
                user_referrals[referrer_id]["referrals_count"] += 1
            else:
                user_referrals[referrer_id] = {"referral_link": f"https://t.me/jbinvest_bot?start={referrer_id}", "referrals_count": 1}

            await context.bot.send_message(
                chat_id=referrer_id,
                text=f"По вашей реферальной ссылке зарегистрировался новый пользователь! Общее количество рефералов: {user_referrals[referrer_id]['referrals_count']}"
            )

    # Check if the user has already selected a language
    if user_id not in user_languages:
        # Ask for language selection
        language_buttons = [
            [InlineKeyboardButton("Русский", callback_data='lang_ru')],
            [InlineKeyboardButton("O'zbek", callback_data='lang_uz')]
        ]
        reply_markup = InlineKeyboardMarkup(language_buttons)
        await update.message.reply_text(
            "Пожалуйста, выберите язык / Iltimos, tilni tanlang:",
            reply_markup=reply_markup
        )
    else:
        # Display the main menu
        language = user_languages[user_id]
        await update.message.reply_text(
            "Добро пожаловать! Пожалуйста, выберите опцию из меню ниже:" if language == 'ru' else "Xush kelibsiz! Iltimos, quyidagi menyudan variantni tanlang:",
            reply_markup=ReplyKeyboardMarkup(menu_buttons[language], resize_keyboard=True)
        )

# Handle language selection
async def language_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    language = query.data.split('_')[1]
    user_languages[user_id] = language

    await query.answer()
    await query.edit_message_text(
        text="Язык выбран! / Til tanlandi!"
    )

    # Display the main menu
    await query.message.reply_text(
        "Добро пожаловать! Пожалуйста, выберите опцию из меню ниже:" if language == 'ru' else "Xush kelibsiz! Iltimos, quyidagi menyudan variantni tanlang:",
        reply_markup=ReplyKeyboardMarkup(menu_buttons[language], resize_keyboard=True)
    )

# Function to handle the "Кошелек" button
async def wallet(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    balance = 0
    keyboard = [
        [InlineKeyboardButton("Пополнить" if language == 'ru' else "To'ldirish", callback_data='recharge')],
        [InlineKeyboardButton("Вывести" if language == 'ru' else "Chiqarmoq", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Ваш баланс: {balance} USD" if language == 'ru' else f"Balansingiz: {balance} USD", reply_markup=reply_markup
    )

# Function to handle the "Пополнить" button
# Функция для обработки кнопки "Пополнить"
async def recharge(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    language = user_languages.get(user_id, 'ru')

    # Ссылка на бот для пополнения
    link = "https://t.me/jb_investpulbot"
    
    # В зависимости от языка выводим соответствующее сообщение
    await update.callback_query.answer(
        "Перейдите по ссылке для пополнения баланса: " + link if language == 'ru' 
        else "Balansni to'ldirish uchun quyidagi havolaga o'ting: " + link
    )

    # Создаем кнопку с URL для перехода
    keyboard = [
        [InlineKeyboardButton("Перейти к боту для пополнения" if language == 'ru' else "Botga o'tish", url=link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.callback_query.message.reply_text(
        "Для пополнения баланса перейдите по ссылке:" if language == 'ru' 
        else "Balansni to'ldirish uchun quyidagi havolaga o'ting:", reply_markup=reply_markup
    )

# Функция для обработки кнопки "Вывести"
async def withdraw(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    language = user_languages.get(user_id, 'ru')

    # Ссылка на бот для вывода средств
    link = "https://t.me/jb_investpulbot"
    
    # В зависимости от языка выводим соответствующее сообщение
    await update.callback_query.answer(
        "Перейдите по ссылке для вывода средств: " + link if language == 'ru' 
        else "Mablag'ni chiqarish uchun quyidagi havolaga o'ting: " + link
    )

    # Создаем кнопку с URL для перехода
    keyboard = [
        [InlineKeyboardButton("Перейти к боту для вывода" if language == 'ru' else "Botga o'tish", url=link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.callback_query.message.reply_text(
        "Для вывода средств перейдите по ссылке:" if language == 'ru' 
        else "Mablag'ni chiqarish uchun quyidagi havolaga o'ting:", reply_markup=reply_markup
    )

# Function to handle the "Партнеры" button with referral link generation and referral count display
async def partners(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')

    if user_id not in user_referrals:
        referral_link = f"https://t.me/jbinvest_bot?start={user_id}"
        user_referrals[user_id] = {
            "referral_link": referral_link,
            "referrals_count": 0
        }
    else:
        referral_link = user_referrals[user_id]["referral_link"]

    referrals_count = user_referrals[user_id]["referrals_count"]

    keyboard = [
        [InlineKeyboardButton("Пригласить друзей" if language == 'ru' else "Do'stlarni taklif qilish", url=referral_link)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Ваша реферальная ссылка: {referral_link}\n"
        f"Количество приглашенных друзей: {referrals_count}\n"
        f"Пригласите 5 друзей по этой ссылке, чтобы получить бонус!" if language == 'ru' else
        f"Sizning referal havolangiz: {referral_link}\n"
        f"Taklif qilingan do'stlar soni: {referrals_count}\n"
        f"Bonus olish uchun ushbu havola orqali 5 do'stni taklif qiling!",
        reply_markup=reply_markup
    )

# Function to handle the "Админ" button
async def admin(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    await update.message.reply_text(
        "Связаться с администратором:" if language == 'ru' else "Admin bilan bog'lanish:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💼 Написать админу" if language == 'ru' else "👨‍💼 Admin bilan bog'lanish", url="https://t.me/RasulovJasur")]
        ])
    )

# Function to handle the "ℹ️ Инфо" button
async def info(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    await update.message.reply_text(
        "Мы – команда экспертов по инвестициям, готовая помочь вам увеличить ваши деньги. "
        "Присоединяйтесь к нам и начнем совместное путешествие к финансовой независимости! 💰" if language == 'ru' else
        "Biz – sarmoya bo'yicha mutaxassislar jamoasi, sizning pulingizni ko'paytirishga yordam berishga tayyormiz. "
        "Bizga qo'shiling va moliyaviy mustaqillikka birgalikda sayohatni boshlaymiz! 💰"
    )

# Function to handle the "Отзывы" button
async def reviews(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    await update.message.reply_text(
        "Читайте отзывы наших клиентов по ссылке ниже:" if language == 'ru' else "Mijozlarimizning sharhlarini quyidagi havola orqali o'qing:",
        reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("💬 Перейти к отзывам" if language == 'ru' else "💬 Sharhlarga o'tish", url="https://t.me/+bUndeuZTKPg2M2Uy")]
    )
    )

async def reviews(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    await update.message.reply_text(
        "Читайте отзывы наших клиентов по ссылке ниже:" if language == 'ru' else "Mijozlarimizning sharhlarini quyidagi havola orqali o'qing:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Перейти к отзывам" if language == 'ru' else "💬 Sharhlarga o'tish", url="https://t.me/+bUndeuZTKPg2M2Uy")]
        ])
    )


# Function to handle other menu buttons
async def menu_response(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')
    user_choice = update.message.text

    if user_choice == ("💼 Кошелек" if language == 'ru' else "💼 Hamyon"):
        await wallet(update, context)
    elif user_choice == ("👥 Партнеры" if language == 'ru' else "👥 Hamkorlar"):
        await partners(update, context)
    elif user_choice == ("ℹ️ Инфо" if language == 'ru' else "ℹ️ Ma'lumot"):
        await info(update, context)
    elif user_choice == ("💬 Отзывы" if language == 'ru' else "💬 Sharhlar"):
        await reviews(update, context)
    elif user_choice == ("👨‍💼 Админ" if language == 'ru' else "👨‍💼 Admin"):
        await admin(update, context)
    elif user_choice == ("⚙️ Настройки" if language == 'ru' else "⚙️ Sozlamalar"):
        await settings(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите опцию из меню." if language == 'ru' else "Iltimos, menyudan variantni tanlang.")


# Function to handle the "Настройки" button
async def settings(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'ru')

    # Ask for language selection
    language_buttons = [
        [InlineKeyboardButton("Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("O'zbek", callback_data='lang_uz')]
    ]
    reply_markup = InlineKeyboardMarkup(language_buttons)
    await update.message.reply_text(
        "Пожалуйста, выберите язык / Iltimos, tilni tanlang:",
        reply_markup=reply_markup
    )

# Setting up the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_response))
    application.add_handler(CallbackQueryHandler(recharge, pattern='recharge'))
    application.add_handler(CallbackQueryHandler(withdraw, pattern='withdraw'))

    await application.run_polling()

import nest_asyncio
nest_asyncio.apply()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
