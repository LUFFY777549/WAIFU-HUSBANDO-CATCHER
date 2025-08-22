import urllib.request
from pymongo import ReturnDocument

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

WRONG_FORMAT_TEXT = """Wrong ❌️ format...  eg. Reply to an image with:

/upload character-name anime-name rarity-number

use rarity number accordingly rarity Map"""

RARITY_MAP = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟡 Legendary",
    4: "🟢 Medium",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "💸 Premium Edition",
    8: "🌤 Summer",
    9: "🎐 Celestial",
    10: "❄️ Winter",
    11: "💝 Valentine",
    12: "🎃 Halloween",
    13: "🎄 Christmas Special",
    14: "🪐 𝙊𝙢𝙣𝙞𝙫𝙚𝙧𝙨𝙖𝙡 🪐",
    15: "🎭 Cosplay Master 🎭",
    16: "🎗️ 𝘼𝙈𝙑 𝙀𝙙𝙞𝙩𝙞𝙤𝙣",
    17: "🧧 𝙀𝙫𝙚𝙣𝙩𝙨",
    18: "🍑 Echhi",
}

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text("❌ Reply to an image with:\n/upload character-name anime-name rarity-number")
            return

        args = context.args
        if len(args) != 3:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        character_name = args[0].replace('-', ' ').title()
        anime = args[1].replace('-', ' ').title()

        try:
            rarity = RARITY_MAP[int(args[2])]
        except KeyError:
            await update.message.reply_text(f'Invalid rarity. Please use numbers 1–{len(RARITY_MAP)}.')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        # get file_id from replied photo
        photo = update.message.reply_to_message.photo[-1].file_id
        file = await context.bot.get_file(photo)
        img_url = file.file_path  # Telegram CDN direct path

        character = {
            'img_url': img_url,
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=photo,
                caption=f'<b>Character Name:</b> {character_name}\n<b>Anime Name:</b> {anime}\n<b>Rarity:</b> {rarity}\n<b>ID:</b> {id}\nAdded by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('CHARACTER ADDED ✅')
        except:
            await collection.insert_one(character)
            await update.message.reply_text("Character Added but no Database Channel Found, Consider adding one.")

    except Exception as e:
        await update.message.reply_text(f'Character Upload Unsuccessful. Error: {str(e)}\nIf you think this is a source error, forward to: {SUPPORT_CHAT}')


UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
application.add_handler(UPLOAD_HANDLER)