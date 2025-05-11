import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import filters
import nest_asyncio
import asyncio

# Telegram API token'ınızı buraya yazın
TOKEN = '8137494195:AAF64rgBuINneNHdHWUa0jC7hu3WTCn8tag'

# Kanalın ID'si, kanalınıza ekleyin (örnek olarak)
CHANNEL_IDS = ['@boutiqueport', '@boutiqueportbags', '@boutiqueporttrainers''@boutiqueportwatches', '@boutiqueportreviews']

# Üye sayısını takip edeceğiz
max_members = 1000
current_members = 0

# Logging ayarları
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # INFO seviyesinde log tutuyoruz.

# Botu başlatmak için bir işlev
async def start(update: Update, context):
    logging.info(f"Bot başladığında gelen mesaj: {update.message.text}")  # Logla
    await update.message.reply_text("Bot aktif!")

# Yeni üyeler geldiğinde kontrol etme
async def new_member(update: Update, context):
    global current_members
    current_members += 1

    # 500 üyeyi geçti mi?
    if current_members > max_members:
        # Yeni katılanı at
        for member in update.message.new_chat_members:
            for channel in CHANNEL_IDS:
                logging.info(f"{member.full_name} 500 üye sınırını geçti ve {channel} kanalından atıldı.")  # Logla
                await context.bot.kick_chat_member(channel, member.id)
                await context.bot.send_message(channel, f"Üye {member.full_name} 500 sınırını geçtiği için atıldı.")
    
    # Geriye dönüp kanalı kontrol et
    logging.info(f"Güncel üye sayısı: {current_members}")  # Logla

# Botu sonlandırmak için bir işlev
async def stop(update: Update, context):
    logging.info(f"Bot kapanıyor...")  # Logla
    await update.message.reply_text("Bot kapanıyor...")
    await context.bot.stop()

# Bot başlatma
async def main():
    # Yeni sürümde Application kullanıyoruz
    application = Application.builder().token(TOKEN).build()

    # Mesaj geldiğinde yeni üyeleri kontrol et
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))  # /stop komutu ekledik

    # Botu çalıştır
    logging.info("Bot başlatıldı ve çalışıyor.")  # Bot başlatılınca logla
    await application.run_polling()

# Eğer event loop zaten çalışıyorsa, asyncio.run() kullanmak yerine doğrudan uygulamayı başlatıyoruz.
if __name__ == '__main__':
    nest_asyncio.apply()  # Bu satır mevcut event loop'u yeniden başlatmaya olanak tanır.
    asyncio.run(main())
