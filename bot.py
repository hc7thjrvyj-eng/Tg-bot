import requests
import time
import hashlib
import re

#———————————————NS————————————————
BOT_TOKEN = "8580993278:AAHwoTITKEeeAXs07iojugI4y2uPBoXqHk8"   # তোমার বট টোকেন
CHAT_ID   = "-6381012703"                                      # তোমার চ্যানেল/গ্রপ আইডি
LAST_UPDATE_ID = None
API_URL   = "http://51.77.216.195/crapi/dgroup/viewstats"
TOKEN     = "RVJURTRSQnJjgG9UZmRvVnKBbkqChIhhfJJQWFlyT3VzX1VgYlJn="   # তোমার API টোকেন
#————————————————NS———————————————

# শুধু আফগানিস্তান রাখা হয়েছে
COUNTRY_MAP = {
    "93": ("AF", "🇦🇫"),  # শুধু আফগানিস্তান
}

# Service short name → Full name
SERVICE_MAP = {
    # Messaging
    "TG": "TELEGRAM",
    "WS": "WHATSAPP",
    "FB": "FACEBOOK",
    "IG": "INSTAGRAM",
    "SG": "SIGNAL",
    "VB": "VIBER",
    "LN": "LINE",
    "WC": "WECHAT",
    "SC": "SNAPCHAT",
    "DC": "DISCORD",

    # Google / Microsoft / Apple
    "GG": "GOOGLE",
    "YT": "YOUTUBE",
    "MS": "MICROSOFT",
    "AP": "APPLE",

    # Social Media
    "TW": "TWITTER",
    "TT": "TIKTOK",
    "IN": "LINKEDIN",
    "RD": "REDDIT",
    "PT": "PINTEREST",

    # Finance / Payment
    "PP": "PAYPAL",
    "PY": "PAYONEER",
    "ST": "STRIPE",
    "CA": "CASHAPP",
    "VM": "VENMO",
    "ZL": "ZELLE",
    "WI": "WISE",
    "SK": "SKRILL",
    "NT": "NETELLER",

    # Crypto
    "BN": "BINANCE",
    "CB": "COINBASE",
    "OK": "OKX",
    "BB": "BYBIT",
    "KC": "KUCOIN",
    "MM": "METAMASK",
    "TW": "TRUSTWALLET",

    # Shopping / Services
    "AM": "AMAZON",
    "EB": "EBAY",
    "AE": "ALIEXPRESS",
    "SP": "SHOPEE",
    "LZ": "LAZADA",

    # Ride / Delivery
    "UB": "UBER",
    "BT": "BOLT",
    "CR": "CAREEM",
    "FP": "FOODPANDA",
    "GB": "GRAB",

    # Streaming / Tools
    "NF": "NETFLIX",
    "SF": "SPOTIFY",
    "ZM": "ZOOM",

    # Default / Other
    "OT": "OTHER"
}

SERVICE_SHORT_MAP = {
    # Messaging
    "WhatsApp": "WS",
    "Telegram": "TG",
    "Facebook": "FB",
    "Messenger": "FB",
    "Instagram": "IG",
    "InstagramApp": "IG",
    "Signal": "SG",
    "Viber": "VB",
    "Line": "LN",
    "WeChat": "WC",
    "Snapchat": "SC",
    "Discord": "DC",

    # Google / Microsoft / Apple
    "Google": "GG",
    "Gmail": "GG",
    "YouTube": "YT",
    "Microsoft": "MS",
    "Outlook": "MS",
    "Hotmail": "MS",
    "Apple": "AP",
    "iCloud": "AP",

    # Social Media
    "Twitter": "TW",
    "X": "TW",
    "TikTok": "TT",
    "LinkedIn": "IN",
    "Pinterest": "PT",
    "Reddit": "RD",

    # Finance / Payment
    "PayPal": "PP",
    "Payoneer": "PY",
    "Stripe": "ST",
    "CashApp": "CA",
    "Venmo": "VM",
    "Zelle": "ZL",
    "Wise": "WI",
    "Skrill": "SK",
    "Neteller": "NT",

    # Crypto
    "Binance": "BN",
    "Coinbase": "CB",
    "OKX": "OK",
    "Bybit": "BB",
    "KuCoin": "KC",
    "TrustWallet": "TW",
    "Metamask": "MM",

    # Shopping / Services
    "Amazon": "AM",
    "Flipkart": "FK",
    "Shopee": "SP",
    "Lazada": "LZ",
    "AliExpress": "AE",
    "eBay": "EB",

    # Ride / Delivery
    "Uber": "UB",
    "Bolt": "BT",
    "Careem": "CR",
    "Foodpanda": "FP",
    "Grab": "GB",

    # Telecom / Others
    "Truecaller": "TC",
    "Zoom": "ZM",
    "Netflix": "NF",
    "Spotify": "SF",

    # Already short (safe)
    "WS": "WS",
    "TG": "TG",
    "FB": "FB",
    "IG": "IG",
    "GG": "GG",
    "PP": "PP",

    # Unknown / fallback
    "Other": "OT",
    "Unknown": "OT"
}

LANGUAGE_BASE_MAP = {
    "en": ("#EN", "#English"),
    "bn": ("#BN", "#Bangla"),
    "hi": ("#HI", "#Hindi"),
    "ur": ("#UR", "#Urdu"),
    "ar": ("#AR", "#Arabic"),
    "es": ("#ES", "#Spanish"),
    "fr": ("#FR", "#French"),
    "de": ("#DE", "#German"),
    "pt": ("#PT", "#Portuguese"),
    "ru": ("#RU", "#Russian"),
    "tr": ("#TR", "#Turkish"),
    "it": ("#IT", "#Italian"),
    "fa": ("#FA", "#Persian"),
    "id": ("#ID", "#Indonesian"),
    "ms": ("#MS", "#Malay"),
    "th": ("#TH", "#Thai"),
    "vi": ("#VI", "#Vietnamese"),
    "zh-cn": ("#ZH", "#Chinese"),
    "zh-tw": ("#ZH", "#Chinese"),
    "ja": ("#JA", "#Japanese"),
    "ko": ("#KO", "#Korean"),
    "pl": ("#PL", "#Polish"),
    "nl": ("#NL", "#Dutch"),
    "sv": ("#SV", "#Swedish"),
    "no": ("#NO", "#Norwegian"),
    "fi": ("#FI", "#Finnish"),
    "da": ("#DA", "#Danish"),
    "cs": ("#CS", "#Czech"),
    "el": ("#EL", "#Greek"),
    "he": ("#HE", "#Hebrew"),
    "ro": ("#RO", "#Romanian"),
    "hu": ("#HU", "#Hungarian"),
    "uk": ("#UK", "#Ukrainian"),
    "bg": ("#BG", "#Bulgarian"),
    "sr": ("#SR", "#Serbian"),
    "hr": ("#HR", "#Croatian")
}

seen = set()

def get_language_tag(lang_code: str, mode: str = "short") -> str:
    """
    mode = "short"  → #EN
    mode = "full"   → #English
    """
    if not lang_code:
        return "#OT"

    lang_code = lang_code.lower()

    short_tag, full_tag = LANGUAGE_BASE_MAP.get(
        lang_code,
        ("#OT", "#Other")
    )

    return short_tag if mode == "short" else full_tag

def mask_number_rtx(number: str):
    """
    Example:
    input : 8801892651
    output: +8801RTX892651
    """
    number = number.replace("+", "").strip()

    if len(number) < 6:
        return "+" + number

    start = number[:4]      # 8801
    end = number[-6:]       # 892651
    return f"{start}RTX{end}"

def get_sms():
    params = {
        "token": TOKEN,
        "records": 150
    }
    try:
        r = requests.get(API_URL, params=params, timeout=15)
        if r.status_code != 200:
            return []
        data = r.json()
        if data.get("status") == "success":
            return data["data"]
    except:
        pass
    return []

def send_telegram(text, otp_code, full_sms):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": f"📋 কপি OTP: {otp_code}",
                        "callback_data": f"copy_{otp_code}"
                    }
                ],
                [
                    {
                        "text": "📨 সম্পূর্ণ মেসেজ দেখুন",
                        "callback_data": f"show_{hashlib.md5(full_sms.encode()).hexdigest()[:8]}"
                    }
                ]
            ]
        }
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def listen_updates():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    params = {
        "timeout": 30
    }

    if LAST_UPDATE_ID:
        params["offset"] = LAST_UPDATE_ID + 1

    try:
        r = requests.get(url, params=params, timeout=35)
        data = r.json()

        for update in data.get("result", []):
            LAST_UPDATE_ID = update["update_id"]

            if "callback_query" in update:
                handle_callback(update["callback_query"])
            elif "message" in update and "text" in update["message"]:
                if update["message"]["text"].startswith("/start"):
                    handle_start(update)

    except Exception as e:
        print("Update Error:", e)

def handle_callback(callback_query):
    callback_id = callback_query["id"]
    data = callback_query.get("data", "")
    message = callback_query.get("message", {})
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]

    if data.startswith("copy_"):
        otp = data.replace("copy_", "")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
        payload = {
            "callback_query_id": callback_id,
            "text": f"OTP: {otp} (কপি করতে ট্যাপ করে ধরে রাখুন)",
            "show_alert": False
        }
        requests.post(url, json=payload)

    elif data.startswith("show_"):
        # পুরো মেসেজ দেখানোর জন্য আলাদা মেসেজ পাঠানো
        full_sms = "মেসেজ দেখানোর ফিচার আপডেট করা হচ্ছে..."
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"📨 সম্পূর্ণ মেসেজ:\n\n{full_sms}",
            "reply_to_message_id": message_id
        }
        requests.post(url, json=payload)

def detect_language_from_text(text):
    if not text:
        return "#OT"

    # Bengali
    if re.search(r'[\u0980-\u09FF]', text):
        return "#BN"

    # Hindi / Devanagari
    if re.search(r'[\u0900-\u097F]', text):
        return "#HI"

    # Urdu
    if re.search(r'[\u0600-\u06FF]', text) and "ک" in text:
        return "#UR"

    # Arabic
    if re.search(r'[\u0600-\u06FF]', text):
        return "#AR"

    # Persian
    if re.search(r'[پچژگ]', text):
        return "#FA"

    # Russian / Cyrillic
    if re.search(r'[\u0400-\u04FF]', text):
        return "#RU"

    # Chinese
    if re.search(r'[\u4E00-\u9FFF]', text):
        return "#ZH"

    # Japanese
    if re.search(r'[\u3040-\u30FF]', text):
        return "#JA"

    # Korean
    if re.search(r'[\uAC00-\uD7AF]', text):
        return "#KO"

    # Thai
    if re.search(r'[\u0E00-\u0E7F]', text):
        return "#TH"

    # Hebrew
    if re.search(r'[\u0590-\u05FF]', text):
        return "#HE"

    # Greek
    if re.search(r'[\u0370-\u03FF]', text):
        return "#EL"

    # Default Latin
    if re.search(r'[a-zA-Z]', text):
        return "#EN"

    return "#OT"
        
def handle_start(update):
    user = update["message"]["from"]
    chat_id = update["message"]["chat"]["id"]

    first_name = user.get("first_name", "User")

    text = (
        f"👋 হ্যালো {first_name}\n\n"
        "🤖 এটি একটি OTP ফরওয়ার্ড বট — শুধুমাত্র আফগানিস্তান 🇦🇫 নম্বরের জন্য"
    )

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json=payload,
        timeout=10
    )

def mask_number(num):
    digits = re.sub(r'\D', '', num)
    if len(digits) < 7:
        return num
    return digits[:4] + "****" + digits[-3:]

def extract_otp(text):
    cleaned = re.sub(r'[\s\-\–\—\_\.\,\;\:\/\\]+', '', text)
    matches = re.findall(r'\d{3,8}', cleaned)
    if not matches:
        return "Not Found"
    candidates = [m for m in matches if 4 <= len(m) <= 6]
    if candidates:
        return candidates[0]
    return matches[0]

print("CR API → Telegram বট চালু হয়েছে!")
print("শুধু আফগানিস্তান 🇦🇫 নম্বরের জন্য কাজ করবে")
print("Bot Ready\n")

while True:
    listen_updates()
    sms_list = get_sms()

    for sms in sms_list:
        unique = sms["dt"] + sms["num"] + sms["message"]
        msg_hash = hashlib.md5(unique.encode()).hexdigest()

        if msg_hash in seen:
            continue
        seen.add(msg_hash)

        # 📞 digits only
        digits_only = re.sub(r'\D', '', sms['num'])

        # 🌍 Country detect - শুধু আফগানিস্তান চেক করা হবে
        country_flag = "🌍"
        country_short = "OT"
        
        # শুধু 93 (আফগানিস্তান) কোড চেক করা হবে
        if digits_only.startswith("93"):
            country_short, country_flag = COUNTRY_MAP["93"]
        else:
            continue  # আফগানিস্তান না হলে স্কিপ করবে

        # 🔐 OTP
        otp = extract_otp(sms['message'])

        # ☎️ RTX number format
        display_number = mask_number_rtx(digits_only)

        # ⚙️ Service short → full
        raw_service = sms.get('cli', 'Other')

        service_short = SERVICE_SHORT_MAP.get(
            raw_service,
            raw_service[:2].upper() if len(raw_service) >= 2 else "OT"
        )

        service_full = SERVICE_MAP.get(
            service_short,
            raw_service.upper() if raw_service else "OTHER"
        )

        # 🌐 Language detect
        language_tag = detect_language_from_text(sms['message'])

        # ✅ FINAL message
        message = (
            f"<b>#{country_short} #{service_short} "
            f"{country_flag} <code>{display_number}</code> {language_tag}</b>"
        )

        send_telegram(message, otp, sms['message'])
        print(f"Sent→{display_number}|{service_short}|{otp}")

    time.sleep(6)
