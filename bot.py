from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "7920112620:AAE3G2Mr_mT2ZveuK4YJvxe0cMWTp04spfE"
GROUP_CHAT_ID = 1002870878498
ADMIN_USER_ID = 5710665661
GROUP_JOIN_LINK = "https://t.me/+apFgfuyT0qhjZTQ8"

AUTO_REPLIES = {
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته يا قمر 🌷✨",
    "السلام عليكم ورحمة الله": "وعليكم السلام ورحمة الله وبركاته يا قمر 🌷✨",
    "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام ورحمة الله وبركاته يا قمر 🌷✨",
    "كيف حالك؟": "أنا بخير، شكرًا لسؤالك 💖 كيف أساعدك؟",
    "ازيك": "أنا بخير، شكرًا لسؤالك 💖 كيف أساعدك؟",
    "شكراً": "العفو بركوز حلو 💖",
    "شكرا": "العفو بركوز حلو 💖",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسلي لي أي رسالة، وسأساعدك في نشرها أو إبقائها خاصة.")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lowered = text.lower()

    for key in AUTO_REPLIES:
        if key.lower() == lowered:
            await update.message.reply_text(AUTO_REPLIES[key])
            return

    keyboard = [[
        InlineKeyboardButton("✅ شاركيني سرّك الجميل", callback_data="publish"),
        InlineKeyboardButton("❌ لا، خليها بس بينّا", callback_data="discard"),
    ],
    [
        InlineKeyboardButton("🔗 انضمي لمجموعتنا الحلوة", url=GROUP_JOIN_LINK)
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["pending_message"] = text
    await update.message.reply_text(
        "يا عسل، وصلتني رسالتك الحلوة يا نجمتي! 🌙💖\nحابّه تشاركيها مع البنات الطيبات؟ 🤗🌸",
        reply_markup=reply_markup,
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = context.user_data

    if "pending_message" not in user_data:
        await query.edit_message_text(text="لا توجد رسالة للنشر حالياً.")
        return

    if query.data == "publish":
        msg = user_data["pending_message"]
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"تقول إحداهن:\n_{msg}_",
            parse_mode="Markdown",
        )
        await query.edit_message_text(text="تمّ النشر بنجاح يا قمر، قلبنا معاك دايمًا! 💕")

    elif query.data == "discard":
        msg = user_data["pending_message"]
        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=f"وصلت رسالة سرّية من بوت البنات (من غير ما نعرف مين):\n\n{msg}"
        )
        await query.edit_message_text(text="لا عليكِ يا غالية، سرك في بير ❤️✨")

    user_data.pop("pending_message", None)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, auto_reply))
    app.add_handler(CallbackQueryHandler(button))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
