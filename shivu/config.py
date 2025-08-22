class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6596417062"
    sudo_users = "7576729648", "6596417062"
    GROUP_ID = -1001992462505
    TOKEN = "8288304784:AAH-UOflloHLYkwU7ji32Q9tx_7o1JYeQLQ"
    mongo_url = "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot"
    PHOTO_URL = ["https://files.catbox.moe/n4sucx.jpg", "https://files.catbox.moe/n4sucx.jpg"]
    SUPPORT_CHAT = "strawberry_graveyard"
    UPDATE_CHAT = "Naruto_X_Waifu"
    BOT_USERNAME = "Nguess_Zangetsu_bot"
    CHARA_CHANNEL_ID = "-1002133191051"
    api_id = 21218274
    api_hash = "3474a18b61897c672d315fb330edb213"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
