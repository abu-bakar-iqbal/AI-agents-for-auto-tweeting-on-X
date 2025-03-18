import tweepy
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials from .env file
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Authenticate using Tweepy Client (API v2)
client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

# Authenticate using API v1.1 (needed for media upload)
auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# ✅ List of different tweets
tweets_list = [
    "Who is ready for our next NFT giveaway??\n\n" "You can mint here:\n" "https://kaspa.com/nft/collections/KROAKCLUB…\n\n" "https://astroart.club/kspr721/KROAKCLUB… \n" "And @KsprBot",
    "55% minted—$75K+ in rewards still up, including the $10K GOLDEN KROAK!\n\n"" Mint here:\n" "https://kaspa.com/nft/collections/KROAKCLUB\n\n" "https://astroart.club/kspr721/KROAKCLUB",
    "The GOLDEN KROAK which comes with a reward of $10,000 - is still at large!! \n""Mint here: \n""https://kaspa.com/nft/collections/KROAKCLUB\n\n""https://astroart.club/kspr721/KROAKCLUB\n""And @KsprBot\n",
    "Everyday you put off minting a $KROAK NFT is another day your life stays the same 🤕\n""You can mint here:\n""https://kaspa.com/nft/collections/KROAKCLUB\n\n""https://astroart.club/kspr721/KROAKCLUB",
    "Let the FOMO set in!! There is less than 50% remaining in Phase 1 of our NFT collection\n""Mint here:\n""kaspa.com/nft/collections/KROAKCLUB\n\n""astroart.club/kspr721/KROAKCLUB\n",
    "We will be giving away NFTs for the next 7 DAYS until @binance lists $KAS or until the GOLDEN KROAK is minted!! \n""You can mint here:\n""kaspa.com/nft/collections/KROAKCLUB\n\n",
    "#KRC20 Projects are fair launched and built on the BEST layer 1 with BEST technology.\n\n""ENOUGH IS ENOUGH! $KAS\n""This is for you 🐸\n""@stoolpresidente\n""@kanyewest\n""@solana\n""@barkmeta"
    
    ]

# ✅ List of 10 influencers (Twitter handles without '@')
influencers = [
     "DamianProsa", "MarcellxMarcell", "OfficialTravlad", "graildoteth",
    "elonmusk", "naval", "garyvee", "pmarca", "lexfridman", "sundarpichai","Lilly_crypto_","SergejK19","ZenRacc00n","RomeoTrades","RuggedWojak","AltcoinMiyagi","CryptoCPriest","RvCrypto","wauwda","CryptoMocro_","degen_z","GoonBoyCrypto","pumpolinsky","Jahncrypto","Tutushik5","MrCryptoJapan","CryptoMeme_Ita","SachiCrypto","DrSolanaNF","@chinapumprocket","Sarah_GreenOk","BNBCHAIN","Zubairey0","casperdefi","nichxbt","WisdomMatic","BelieveInLuce","0xdetweiler","cheatcoiner","DopeOxide","itsCryptoWolf","NFTsAreNice","Ga__ke","DiaryofaMadeMan","solana","cryptosymbiiote","Landshareio","Crypt0_Andrew","Rafi_0x","a1lon9","SoulzBTC","jpeggler","SuiNetwork","robinhood_degen","cryptojack","cryptoworld202","naiivememe","MartiniGuyYT","Chris_Hutch7","CoffeeNCrypto","BenArmstrongsX","intocryptoverse","Cryptoholic_boy","APompliano","LayahHeilpern","ErikVoorhees","EricTrump","defi_darling","cdixon","AgencyLaser","rogerkver","balajis","pmarca"
]

# ✅ Path to the folder containing images/videos
media_folder = "C:/Users/khalid.shahzad/Desktop/AI Agents -Shah/Media_Files"

# ✅ Ensure media folder exists
if not os.path.exists(media_folder):
    os.makedirs(media_folder)
    print("📂 'Media_Files' folder created. Add media files and rerun the script.")
    exit()

# ✅ Get list of media files
media_files = [f for f in os.listdir(media_folder) if f.endswith(('.jpg', '.png', '.mp4', '.mov'))]

# ✅ Ensure there are at least 4 media files
if len(media_files) < 4:
    print("⚠️ ERROR: Please add at least 10 media files to 'Media_Files' before running the script.")
    exit()

# ✅ Loop to post 4 tweets
while True:        #added
  for i in range(7):
    try:
        # Select tweet and media file based on the index
        tweet_content = tweets_list[i]  # Select corresponding tweet
        media_path = os.path.join(media_folder, media_files[i])  # Select corresponding media file

        # Select all 10 influencers and format as mentions
        start_index = (i * 10) % len(influencers)  # Start index, loops if exceeding length
        end_index = start_index + 10  # End index
        selected_influencers = influencers[start_index:end_index]
        if len(selected_influencers) < 10:
          selected_influencers += influencers[:(10 - len(selected_influencers))]
        influencer_tags = " ".join([f"@{user}" for user in selected_influencers])

        # Ensure total tweet length does not exceed 280 characters
        final_tweet = f"{tweet_content}\n\n{influencer_tags}"
        if len(final_tweet) > 280:
            final_tweet = f"{tweet_content[:260]}...\n{influencer_tags}"  # Truncate tweet if needed

        # Upload media
        media = api.media_upload(media_path)

        # Post tweet with media and tags
        response = client.create_tweet(text=final_tweet, media_ids=[media.media_id])
        
        print(f"✅ Tweet {i+1}/7 posted: {final_tweet}")
        print(f"🔗 Tweet Link: https://twitter.com/user/status/{response.data['id']}")

    except tweepy.TweepyException as e:
        print(f"❌ Tweeting error: {e}")

    # Wait 1 minute before posting the next tweet
    if i < 3:  # No need to wait after the last tweet
        print("⏳ Waiting for 30 minute before the next tweet...")
        time.sleep(1800)

  print("🎉 All 4 tweets posted! The script has stopped. Run again after 2 hours.")
  wait_time = random.randint(1800, 3600)  # Wait between 1 to 2 hours before restarting
  print(f"🔄 Restarting tweet cycle in {wait_time // 60} minutes...")
  time.sleep(wait_time)
