import time
import datetime
import telebot
import requests
import re
import codecs
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import unquote

bot = telebot.TeleBot("6923585464:AAHCOf8QQtiyPvmX4B_X5PFJhu82VfkwPrA")
setlan = None
usernum = 0
timer = 0
country_codes = {
    "AF": "Afghanistan",
    "AX": "Åland Islands",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo, The Democratic Republic of the",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Côte d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (Malvinas)",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and McDonald Islands",
    "VA": "Holy See (Vatican City State)",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran, Islamic Republic of",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao People's Democratic Republic",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libyan Arab Jamahiriya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MK": "Macedonia, The Former Yugoslav Republic of",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia, Federated States of",
    "MD": "Moldova, Republic of",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "AN": "Netherlands Antilles",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestinian Territory, Occupied",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan, Province of China",
    "TJ": "Tajikistan",
    "TZ": "Tanzania, United Republic of",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "UM": "United States Minor Outlying Islands",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela",
    "VN": "Viet Nam",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
}


country_codes_ar = {
    "AF": "أفغانستان",
    "AX": "جزر آلاند",
    "AL": "ألبانيا",
    "DZ": "الجزائر",
    "AS": "ساموا الأمريكية",
    "AD": "أندورا",
    "AO": "أنغولا",
    "AI": "أنغيلا",
    "AQ": "القارة القطبية الجنوبية",
    "AG": "أنتيغوا وباربودا",
    "AR": "الأرجنتين",
    "AM": "أرمينيا",
    "AW": "أروبا",
    "AU": "أستراليا",
    "AT": "النمسا",
    "AZ": "أذربيجان",
    "BS": "جزر البهاما",
    "BH": "البحرين",
    "BD": "بنغلاديش",
    "BB": "باربادوس",
    "BY": "بيلاروسيا",
    "BE": "بلجيكا",
    "BZ": "بليز",
    "BJ": "بنين",
    "BM": "برمودا",
    "BT": "بوتان",
    "BO": "بوليفيا",
    "BA": "البوسنة والهرسك",
    "BW": "بوتسوانا",
    "BV": "جزيرة بوفيت",
    "BR": "البرازيل",
    "IO": "الإقليم البريطاني في المحيط الهندي",
    "BN": "بروناي",
    "BG": "بلغاريا",
    "BF": "بوركينا فاسو",
    "BI": "بوروندي",
    "KH": "كمبوديا",
    "CM": "الكاميرون",
    "CA": "كندا",
    "CV": "الرأس الأخضر",
    "KY": "جزر كايمان",
    "CF": "جمهورية أفريقيا الوسطى",
    "TD": "تشاد",
    "CL": "شيلي",
    "CN": "الصين",
    "CX": "جزيرة عيد الميلاد",
    "CC": "جزر كوكوس (كيلينج)",
    "CO": "كولومبيا",
    "KM": "جزر القمر",
    "CG": "الكونغو",
    "CD": "جمهورية الكونغو الديمقراطية",
    "CK": "جزر كوك",
    "CR": "كوستاريكا",
    "CI": "ساحل العاج",
    "HR": "كرواتيا",
    "CU": "كوبا",
    "CY": "قبرص",
    "CZ": "الجمهورية التشيكية",
    "DK": "الدنمارك",
    "DJ": "جيبوتي",
    "DM": "دومينيكا",
    "DO": "جمهورية الدومينيكان",
    "EC": "الإكوادور",
    "EG": "مصر",
    "SV": "السلفادور",
    "GQ": "غينيا الاستوائية",
    "ER": "إريتريا",
    "EE": "إستونيا",
    "ET": "إثيوبيا",
    "FK": "جزر فوكلاند (مالفيناس)",
    "FO": "جزر فارو",
    "FJ": "فيجي",
    "FI": "فنلندا",
    "FR": "فرنسا",
    "GF": "غويانا الفرنسية",
    "PF": "بولينزيا الفرنسية",
    "TF": "المناطق الجنوبية لفرنسا",
    "GA": "الغابون",
    "GM": "غامبيا",
    "GE": "جورجيا",
    "DE": "ألمانيا",
    "GH": "غانا",
    "GI": "جبل طارق",
    "GR": "اليونان",
    "GL": "جرينلاند",
    "GD": "غرينادا",
    "GP": "جوادلوب",
    "GU": "غوام",
    "GT": "غواتيمالا",
    "GG": "جيرنزي",
    "GN": "غينيا",
    "GW": "غينيا بيساو",
    "GY": "غيانا",
    "HT": "هايتي",
    "HM": "جزيرة هيرد وجزر ماكدونالد",
    "VA": "الفاتيكان",
    "HN": "هندوراس",
    "HK": "هونغ كونغ",
    "HU": "هنغاريا",
    "IS": "آيسلندا",
    "IN": "الهند",
    "ID": "إندونيسيا",
    "IR": "إيران",
    "IQ": "العراق",
    "IE": "أيرلندا",
    "IM": "جزيرة مان",
    "IL": "إسرائيل",
    "IT": "إيطاليا",
    "JM": "جامايكا",
    "JP": "اليابان",
    "JE": "جيرسي",
    "JO": "الأردن",
    "KZ": "كازاخستان",
    "KE": "كينيا",
    "KI": "كيريباتي",
    "KP": "كوريا الشمالية",
    "KR": "كوريا الجنوبية",
    "KW": "الكويت",
    "KG": "قيرغيزستان",
    "LA": "جمهورية لاو الديمقراطية الشعبية",
    "LV": "لاتفيا",
    "LB": "لبنان",
    "LS": "ليسوتو",
    "LR": "ليبيريا",
    "LY": "ليبيا",
    "LI": "ليختنشتاين",
    "LT": "ليتوانيا",
    "LU": "لوكسمبورج",
    "MO": "ماكاو",
    "MK": "مقدونيا، جمهورية يوغوسلافيا السابقة",
    "MG": "مدغشقر",
    "MW": "ملاوي",
    "MY": "ماليزيا",
    "MV": "جزر المالديف",
    "ML": "مالي",
    "MT": "مالطا",
    "MH": "جزر مارشال",
    "MQ": "مارتينيك",
    "MR": "موريتانيا",
    "MU": "موريشيوس",
    "YT": "مايوت",
    "MX": "المكسيك",
    "FM": "ولايات ميكرونيزيا الموحدة",
    "MD": "جمهورية مولدوفا",
    "MC": "موناكو",
    "MN": "منغوليا",
    "ME": "الجبل الأسود",
    "MS": "مونتسرات",
    "MA": "المغرب",
    "MZ": "موزمبيق",
    "MM": "ميانمار",
    "NA": "ناميبيا",
    "NR": "ناورو",
    "NP": "نيبال",
    "NL": "هولندا",
    "NC": "كاليدونيا الجديدة",
    "NZ": "نيوزيلندا",
    "NI": "نيكاراغوا",
    "NE": "النيجر",
    "NG": "نيجيريا",
    "NU": "نيوي",
    "NF": "جزيرة نورفولك",
    "MP": "جزر ماريانا الشمالية",
    "NO": "النرويج",
    "OM": "عمان",
    "PK": "باكستان",
    "PW": "بالاو",
    "PS": "الأراضي الفلسطينية المحتلة",
    "PA": "بنما",
    "PG": "بابوا غينيا الجديدة",
    "PY": "باراغواي",
    "PE": "بيرو",
    "PH": "الفلبين",
    "PN": "بيتكيرن",
    "PL": "بولندا",
    "PT": "البرتغال",
    "PR": "بورتو ريكو",
    "QA": "قطر",
    "RE": "لا ريونيون",
    "RO": "رومانيا",
    "RU": "الاتحاد الروسي",
    "RW": "رواندا",
    "BL": "سان بارتيليمي",
    "SH": "سانت هيلينا",
    "KN": "سانت كيتس ونيفيس",
    "LC": "سانت لوسيا",
    "MF": "سانت مارتن (الجزء الهولندي)",
    "PM": "سانت بيير وميكلون",
    "VC": "سانت فينسنت وجزر غرينادين",
    "WS": "ساموا",
    "SM": "سان مارينو",
    "ST": "ساو تومي وبرينسيبي",
    "SA": "المملكة العربية السعودية",
    "SN": "السنغال",
    "RS": "صربيا",
    "SC": "سيشل",
    "SL": "سيراليون",
    "SG": "سنغافورة",
    "SK": "سلوفاكيا",
    "SI": "سلوفينيا",
    "SB": "جزر سليمان",
    "SO": "الصومال",
    "ZA": "جمهورية جنوب إفريقيا",
    "GS": "جورجيا الجنوبية وجزر ساندويتش الجنوبية",
    "ES": "إسبانيا",
    "LK": "سريلانكا",
    "SD": "السودان",
    "SR": "سورينام",
    "SJ": "سفالبارد وجان ماين",
    "SZ": "سوازيلاند",
    "SE": "السويد",
    "CH": "سويسرا",
    "SY": "الجمهورية العربية السورية",
    "TW": "تايوان، جمهورية الصين",
    "TJ": "طاجيكستان",
    "TZ": "تانزانيا، جمهورية المتحدة",
    "TH": "تايلاند",
    "TL": "تيمور الشرقية",
    "TG": "توغو",
    "TK": "توكيلو",
    "TO": "تونغا",
    "TT": "ترينيداد وتوباغو",
    "TN": "تونس",
    "TR": "تركيا",
    "TM": "تركمانستان",
    "TC": "جزر تركس وكايكوس",
    "TV": "توفالو",
    "UG": "أوغندا",
    "UA": "أوكرانيا",
    "AE": "الإمارات العربية المتحدة",
    "GB": "المملكة المتحدة",
    "US": "الولايات المتحدة",
    "UM": "جزر الولايات المتحدة البعيدة الصغيرة",
    "UY": "الأورغواي",
    "UZ": "أوزبكستان",
    "VU": "فانواتو",
    "VE": "فنزويلا",
    "VN": "فيتنام",
    "VG": "جزر فيرجن البريطانية",
    "VI": "جزر فيرجن الأمريكية",
    "WF": "والس وفوتونا",
    "EH": "الصحراء الغربية",
    "YE": "اليمن",
    "ZM": "زامبيا",
    "ZW": "زيمبابوي",
    }

language_codes = {
    "en": "English",
    "ar": "Arabic",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ru": "Russian",
    "zh": "Chinese",
    "hi": "Hindi",
    "pt": "Portuguese",
    "tr": "Turkish",
    "ko": "Korean",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "zh-CN": "Mandarin",
    "zh-HK": "Cantonese",
    "nl": "Dutch",
    "cs": "Czech",
    "pl": "Polish",
    "hu": "Hungarian",
    "ro": "Romanian",
    "hr": "Croatian",
    "sl": "Slovenian",
    "sr": "Serbian",
    "el": "Greek",
    "he": "Hebrew",
    "da": "Danish",
    "sv": "Swedish",
    "fi": "Finnish",
    "no": "Norwegian",
    "is": "Icelandic",
    "et": "Estonian",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "ku": "Kurdish",
    "az": "Azerbaijani",
    "uk": "Ukrainian",
    "ka": "Georgian",
    "hy": "Armenian",
    "bg": "Bulgarian",
    "sr-Latn": "Serbian (Latin)",
}

language_codes_ar = {
    "en": "الإنجليزية",
    "ar": "العربية",
    "fr": "الفرنسية",
    "es": "الإسبانية",
    "de": "الألمانية",
    "it": "الإيطالية",
    "ja": "اليابانية",
    "ru": "الروسية",
    "zh": "الصينية",
    "hi": "الهندية",
    "pt": "البرتغالية",
    "tr": "التركية",
    "ko": "الكورية",
    "th": "التايلاندية",
    "vi": "الفيتنامية",
    "id": "الإندونيسية",
    "zh-CN": "الماندرين",
    "zh-HK": "الكانتونية",
    "nl": "الهولندية",
    "cs": "التشيكية",
    "pl": "البولندية",
    "hu": "المجرية",
    "ro": "الرومانية",
    "hr": "الكرواتية",
    "sl": "السلوفينية",
    "sr": "الصربية",
    "el": "اليونانية",
    "he": "العبرية",
    "da": "الدنماركية",
    "sv": "السويدية",
    "fi": "الفنلندية",
    "no": "النرويجية",
    "is": "الأيسلندية",
    "et": "الإستونية",
    "lv": "اللاتفية",
    "lt": "اللتوانية",
    "ku": "الكردي",
    "az": "الأذرية",
    "uk": "الأوكرانية",
    "ka": "الجورجية",
    "hy": "الأرمنية",
    "bg": "البلغارية",
    "sr-Latn": "الصربية (لاتينية)",
}


def make_request(url, user_agent):
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    return response

@bot.message_handler(regexp=r'https?://[^\s]+')
def extract_url(message):
   timerv = 0
   global setlan  # قم بتعريف المتغير كـ global لاستخدامه لاحقًا
   if setlan == "ar":
        down_meg = "جاري تنزيل الفيديو...."
        done = "✅ عملية المعالجة"
   elif setlan == "en":
        down_meg = "Downloading video...."
        done = "✅ Treatment process"
   if setlan is None:
        user = message.from_user
        markup = telebot.types.InlineKeyboardMarkup()
        english_button = telebot.types.InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = telebot.types.InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
   else:
       wait_message = bot.send_message(message.chat.id, f"{done}\n{down_meg}\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
       url_tiktok = message.text.strip()
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜")
       headers = {
           "Content-Type": "application/json",
           "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
       }
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜")
       data = {
           "url": f"{url_tiktok}"
       }
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜")
       url = "https://www.veed.io/video-downloader-ap/api/download-content"
       response = requests.post(url, headers=headers, json=data)
       
       if response.status_code == 200:
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"{done}\n{down_meg}\n🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜")
           response_data = response.json()
           
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜")
           title = response_data.get("title", "")
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜")
           username = response_data.get("username", "")
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜")
           media = response_data.get("media", [])
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜")

           if media:
               first_media_url = media[0].get("url", "")
               media_format = media[0].get("format", "")
               cleaned_media_url = first_media_url.replace("/video-downloader-ap/api/stream-media?url=", "")
               cleaned_media_url_decoded = unquote(cleaned_media_url)
               bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                   text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")
               print(cleaned_media_url)
               if setlan == "en":
                    caption_text = f"Video Title: <code>{title}</code>\nVideo owner's account name: <code>{username}</code>"
               elif setlan == "ar":
                    caption_text = f"عنوان الفيديو: <code>{title}</code>\nاسم حساب مالك الفيديو: <code>{username}</code>"
               bot.send_video(message.chat.id, cleaned_media_url_decoded, caption=caption_text, parse_mode='HTML')

       else:
           if setlan == "en":
              bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"There is a problem with the link!\n      \n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥")
           elif setlan == "ar":
              bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"هناك مشكلة في الرابط!\n      \n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥")

@bot.message_handler(commands=['start'])
def start(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    elif setlan == "ar":
       
        bot.send_message(message.chat.id, "مرحبا, أنا بوت تلجرام متعدد الأدوات لي التيكتوك\n ارسل /help لكي  تري كيف تستعملني.")
    elif setlan == "en":
        bot.send_message(message.chat.id, "Hello, I am a multi-tool Telegram bot for Tiktok.\n Send /help to see how to use me.")

@bot.message_handler(commands=['help'])
def start(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    elif setlan == "ar":
        bot.send_message(message.chat.id, "للحصول علي معلومات حساب التيكتوك فقط قم بارسال اليوزر.\n لتنزيل فيديو بدون علامه مائيه فقط قم بارسال الرابط.")
    elif setlan == "en":
        bot.send_message(message.chat.id, "To obtain Tiktok account information, just send the user.\n To download a video without a watermark, just send the link.")


@bot.message_handler(commands=['language'])
def choose_language(message):
    user = message.from_user
    markup = InlineKeyboardMarkup()
    english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
    arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
    markup.add(english_button, arabic_button)
    helloen = "Please choose your language 🇬🇧"
    helloar = "الرجاء اختيار لغتك 🇪🇬"
    bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global setlan

    if call.data == 'en':
        bot.answer_callback_query(call.id, text="You chose English 🇬🇧")
        setlan = "en"
        bot.send_message(call.message.chat.id, "Hello, I am a multi-tool Telegram bot for Tiktok.\n Send /help to see how to use me.")
    elif call.data == 'ar':
        bot.answer_callback_query(call.id, text="اخترت العربية 🇪🇬")
        setlan = "ar"
        bot.send_message(call.message.chat.id, "        مرحبا, أنا بوت تلجرام متعدد الأدوات لي التيكتوك\n ارسل /help لكي  تري كيف تستعملني.")

@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    else:
        global timer
        def reply(message):
            global usernum
            usernum += 1
            user = message.from_user
            chat_id = 6683148299
            user_id = user.id
            user_first_name = user.first_name
            user_last_name = user.last_name
            user_username = user.username
            user_language_code = user.language_code
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            username = message.text
            url = f"https://www.tiktok.com/@{username}?lang=en"
            user_agent = "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36"
            response = make_request(url, user_agent)
            key = "uniqueId"

            if key in response.text:
                info_message = bot.send_message(message.chat.id, f"{wait_m}\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
                text = response.text
                pattern = r'{"userInfo":{"user":.*?"itemList":\[\]}'
                match = re.search(pattern, text)

                if match:
                    extracted_text = match.group()
                    text1 = extracted_text
                    start1 = """{"userInfo":{"user":{"id":"""
                    end1 = """","shortId"""
                    pattern1 = re.compile(re.escape(start1) + r"(.*?)" + re.escape(end1))
                    match1 = pattern1.search(text1)

                    if match1:
                        id = match1.group(1)
                        id = id.replace('"', '')

                    start2 = """uniqueId":"""
                    end2 = ""","nickname":"""
                    pattern2 = re.compile(re.escape(start2) + r"(.*?)" + re.escape(end2))
                    match2 = pattern2.search(text1)

                    if match2:
                        uniqueId = match2.group(1)
                        uniqueId = uniqueId.replace('"', '')

                    start3 = ""","nickname":"""
                    end3 = ""","avatarLarger":"""
                    pattern3 = re.compile(re.escape(start3) + r"(.*?)" + re.escape(end3))
                    match3 = pattern3.search(text1)

                    if match3:
                        nickname = match3.group(1)
                        nickname = nickname.replace('"', '')

                    start4 = ""","avatarLarger":"""
                    end4 = ""","avatarMedium":"""
                    pattern4 = re.compile(re.escape(start4) + r"(.*?)" + re.escape(end4))
                    match4 = pattern4.search(text1)

                    if match4:
                        avatarLarger1 = match4.group(1)
                        avatarLarger = codecs.decode(avatarLarger1, 'unicode_escape')
                        avatarLarger = avatarLarger.replace('"', '')

                    start5 = ""","signature":"""
                    end5 = ""","createTime":"""
                    pattern5 = re.compile(re.escape(start5) + r"(.*?)" + re.escape(end5))
                    match5 = pattern5.search(text1)

                    if match5:
                        signature = match5.group(1)
                        signature = signature.replace('"', '')

                    start6 = ""","createTime":"""
                    end6 = ""","verified"""
                    pattern6 = re.compile(re.escape(start6) + r"(.*?)" + re.escape(end6))
                    match6 = pattern6.search(text1)

                    if match6:
                        createTime = match6.group(1)
                        if createTime == "0":
                            if setlan == "en":
                                createTime = "unknown"
                            else:
                                createTime = "غير معروف"

                    start7 = ""","verified":"""
                    end7 = ""","secUid":"""
                    pattern7 = re.compile(re.escape(start7) + r"(.*?)" + re.escape(end7))
                    match7 = pattern7.search(text1)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜")

                    if match7:
                        verified = match7.group(1)
                    if verified == "true":
                        if setlan == "en":
                            verified = "yes"
                        else:
                            verified = "نعم"
                    else:
                        if setlan == "en":
                            verified = "no"
                        else:
                            verified = "لا"

                    start8 = ""","secUid":"""
                    end8 = ""","ftc":"""
                    pattern8 = re.compile(re.escape(start8) + r"(.*?)" + re.escape(end8))
                    match8 = pattern8.search(text1)

                    if match8:
                        secUid = match8.group(1)
                        secUid = secUid.replace('"', '')

                    start9 = ""","ftc":"""
                    end9 = ""","relation":"""
                    pattern9 = re.compile(re.escape(start9) + r"(.*?)" + re.escape(end9))
                    match9 = pattern9.search(text1)

                    if match9:
                        ftc = match9.group(1)
                        if ftc == "true":
                          if setlan == "en":
                            ftc = "yes"
                          else:
                            ftc = "نعم"
                        else:
                          if setlan == "en":
                            ftc = "no"
                          else:
                            ftc = "لا"

                    start10 = ""","relation":"""
                    end10 = ""","openFavorite":"""
                    pattern10 = re.compile(re.escape(start10) + r"(.*?)" + re.escape(end10))
                    match10 = pattern10.search(text1)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜")
                    if match10:
                        relation = match10.group(1)
                        if relation == "0":
                          if setlan == "en":
                            relation = "not found"
                          else:
                            relation = "لا يوجد"
                        else:
                          relation = match10.group(1)

                    if """bioLink""" in text1:
                        start39 = """:{"link":"""
                        end39 = ""","risk"""
                        pattern39 = re.compile(re.escape(start39) + r"(.*?)" + re.escape(end39))
                        match39 = pattern39.search(text1)
                        if match39:
                            bioLink = match39.group(1)
                            bioLink = bioLink.replace('"', '')
                            global end11
                            end11 = ""","bioLink":"""
                    else:
                        end11 = ""","commentSetting":"""
                        if setlan == "en":
                           bioLink = "not found"
                        else:
                           bioLink = "لا يوجد"

                    if """openFavorite""" in text1:
                     start11 = ""","openFavorite":"""
                     pattern11 = re.compile(re.escape(start11) + r"(.*?)" + re.escape(end11))
                     match11 = pattern11.search(text1)

                     if match11:
                         openFavorite = match11.group(1)
                         if openFavorite == "true":
                           if setlan == "en":
                             openFavorite = "yes"
                           else:
                             openFavorite = "نعم"
                         else:
                           if setlan == "en":
                             openFavorite = "no"
                           else:
                             openFavorite = "لا"

                    start12 = ""","commentSetting":"""
                    end12 = ""","commerceUserInfo":"""
                    pattern12 = re.compile(re.escape(start12) + r"(.*?)" + re.escape(end12))
                    match12 = pattern12.search(text1)

                    if match12:
                        commentSetting = match12.group(1)
                        if commentSetting == "0":
                           if setlan == "en":
                              commentSetting = "closed"
                           else:
                              commentSetting = "مغلقه"
                        else:
                           if setlan == "en":
                              commentSetting = "opened"
                           else:
                              commentSetting = "مفتوحه"

                    start14 = ""","category":"""
                    end14 = ""","categoryButton":"""
                    pattern14 = re.compile(re.escape(start14) + r"(.*?)" + re.escape(end14))
                    match14 = pattern14.search(text1)

                    if match14:
                        category = match14.group(1)
                    else:
                        start38 = """showPlayListTab ":"""
                        end38 = """},"followingVisibility":"""
                        pattern38 = re.compile(re.escape(start38) + r"(.*?)" + re.escape(end38))
                        match38 = pattern38.search(text1)

                        if match38:
                            category = match38.group(1)
                        else:
                            if setlan == "ar":
                              category = "غير معروف"
                            else:
                              category = "unknown"

                    start15 = """},"followingVisibility":"""
                    end15 = ""","recommendReason":"""
                    pattern15 = re.compile(re.escape(start15) + r"(.*?)" + re.escape(end15))
                    match15 = pattern15.search(text1)

                    if match15:
                        followingVisibility = match15.group(1)
                        if followingVisibility == "1":
                          if setlan == "en":
                            followingVisibility = "yes"
                          else:
                            followingVisibility = "نعم"
                        else:
                          if setlan == "en":
                            followingVisibility = "no"
                          else:
                            followingVisibility = "لا"

                    start16 = """},"duetSetting":"""
                    end16 = ""","stitchSetting":"""
                    pattern16 = re.compile(re.escape(start16) + r"(.*?)" + re.escape(end16))
                    match16 = pattern16.search(text1)

                    if match16:
                        duetSetting = match16.group(1)
                        if duetSetting == "0":
                           if setlan == "en":
                              duetSetting = "closed"
                           else:
                              duetSetting = "مغلقه"
                        else:
                           if setlan == "en":
                              duetSetting = "opened"
                           else:
                              duetSetting = "مفتوحه"

                    start17 = ""","stitchSetting":"""
                    end17 = ""","privateAccount":"""
                    pattern17 = re.compile(re.escape(start17) + r"(.*?)" + re.escape(end17))
                    match17 = pattern17.search(text1)

                    if match17:
                        stitchSetting = match17.group(1)
                        if stitchSetting == "0":
                           if setlan == "en":
                              stitchSetting = "closed"
                           else:
                              stitchSetting = "مغلقه"
                        else:
                           if setlan == "en":
                              stitchSetting = "opened"
                           else:
                              stitchSetting = "مفتوحه"

                    start18 = ""","privateAccount":"""
                    end18 = ""","secret":"""
                    pattern18 = re.compile(re.escape(start18) + r"(.*?)" + re.escape(end18))
                    match18 = pattern18.search(text1)

                    if match18:
                        privateAccount = match18.group(1)
                        if privateAccount == "true":
                          if setlan == "en":
                            privateAccount = "yes"
                          else:
                            privateAccount = "نعم"
                        else:
                          if setlan == "en":
                            privateAccount = "no"
                          else:
                            privateAccount = "لا"


                    start19 = ""","secret":"""
                    end19 = ""","isADVirtual":"""
                    pattern19 = re.compile(re.escape(start19) + r"(.*?)" + re.escape(end19))
                    match19 = pattern19.search(text1)

                    if match19:
                        secret = match19.group(1)
                        if secret == "true":
                          if setlan == "en":
                            secret = "yes"
                          else:
                            secret = "نعم"
                        else:
                          if setlan == "en":
                            secret = "no"
                          else:
                            secret = "لا"

                    start20 = ""","isADVirtual":"""
                    end20 = ""","roomId":"","""
                    pattern20 = re.compile(re.escape(start20) + r"(.*?)" + re.escape(end20))
                    match20 = pattern20.search(text1)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜")
                    if match20:
                        isADVirtual = match20.group(1)
                        if isADVirtual == "true":
                          if setlan == "en":
                            isADVirtual = "yes"
                          else:
                            isADVirtual = "نعم"
                        else:
                          if setlan == "en":
                            isADVirtual = "no"
                          else:
                            isADVirtual = "لا"

                    start21 = ""","uniqueIdModifyTime":"""
                    end21 = ""","ttSeller":"""
                    pattern21 = re.compile(re.escape(start21) + r"(.*?)" + re.escape(end21))
                    match21 = pattern21.search(text1)

                    if match21:
                        uniqueIdModifyTime = match21.group(1)
                        if uniqueIdModifyTime == "0":
                          if setlan == "en":
                            uniqueIdModifyTime = "not found"
                          else:
                            uniqueIdModifyTime = "لا يوجد"
                        else:
                          uniqueIdModifyTime = match21.group(1)

                    start22 = ""","ttSeller":"""
                    end22 = ""","region":"""
                    pattern22 = re.compile(re.escape(start22) + r"(.*?)" + re.escape(end22))
                    match22 = pattern22.search(text1)

                    if match22:
                        ttSeller = match22.group(1)
                        if ttSeller == "true":
                          if setlan == "en":
                            ttSeller = "yes"
                          else:
                            ttSeller = "نعم"
                        else:
                          if setlan == "en":
                            ttSeller = "no"
                          else:
                            ttSeller = "لا"

                    start23 = ""","region":"""
                    end23 = ""","profileTab":{"showMusicTab":"""
                    pattern23 = re.compile(re.escape(start23) + r"(.*?)" + re.escape(end23))
                    match23 = pattern23.search(text1)

                    if match23:
                        country_code = match23.group(1)
                        country_code = country_code.replace('"', '')
                        if setlan == "en":
                          region = country_codes.get(country_code, "unknown")
                        else:
                          region = country_codes_ar.get(country_code, "غير معروفه")


                    start27 = """nickNameModifyTime":"""
                    end27 = ""","isEmbedBanned":"""
                    pattern27 = re.compile(re.escape(start27) + r"(.*?)" + re.escape(end27))
                    match27 = pattern27.search(text1)

                    if match27:
                        nickNameModifyTime = match27.group(1)
                        if nickNameModifyTime == "0":
                          if setlan == "en":
                            nickNameModifyTime = "unknown"
                          else:
                            nickNameModifyTime = "غير معروف"
                        else:
                          nickNameModifyTime = match27.group(1)

                    start28 = ""","isEmbedBanned":"""
                    end28 = ""","canExpPlaylist":"""
                    pattern28 = re.compile(re.escape(start28) + r"(.*?)" + re.escape(end28))
                    match28 = pattern28.search(text1)

                    if match28:
                        isEmbedBanned = match28.group(1)
                        if isEmbedBanned == "true":
                          if setlan == "en":
                            isEmbedBanned = "yes"
                          else:
                            isEmbedBanned = "نعم"
                        else:
                          if setlan == "en":
                            isEmbedBanned = "no"
                          else:
                            isEmbedBanned = "لا"

                    start29 = ""","canExpPlaylist":"""
                    end29 = ""","profileEmbedPermission":"""
                    pattern29 = re.compile(re.escape(start29) + r"(.*?)" + re.escape(end29))
                    match29 = pattern29.search(text1)

                    if match29:
                        canExpPlaylist = match29.group(1)
                        if canExpPlaylist == "true":
                          if setlan == "en":
                            canExpPlaylist = "yes"
                          else:
                            canExpPlaylist = "نعم"
                        else:
                          if setlan == "en":
                            canExpPlaylist = "no"
                          else:
                            canExpPlaylist = "لا"

                    start30 = """profileEmbedPermission":"""
                    end30 = ""","language":"""
                    pattern30 = re.compile(re.escape(start30) + r"(.*?)" + re.escape(end30))
                    match30 = pattern30.search(text1)

                    if match30:
                        profileEmbedPermission = match30.group(1)
                        if profileEmbedPermission == "0":
                           if selan == "en":
                              profileEmbedPermission = "closed"
                           else:
                              profileEmbedPermission = "مغلقه"
                        else:
                           if setlan == "en":
                              profileEmbedPermission = "opened"
                           else:
                              profileEmbedPermission = "مفتوحه"

                    start31 = ""","language":"""
                    end31 = ""","eventList":"""
                    pattern31 = re.compile(re.escape(start31) + r"(.*?)" + re.escape(end31))
                    match31 = pattern31.search(text1)

                    if match31:
                        language_code = match31.group(1)
                        language_code = language_code.replace('"', '')
                        if setlan == "en":
                          language = language_codes.get(language_code, "unknown")
                        else:
                          language = language_codes_ar.get(language_code, "غير معروفه")
                    else:
                     start40 = ""","language":"""
                     end40 = """},"stats":"""
                     pattern40 = re.compile(re.escape(start40) + r"(.*?)" + re.escape(end40))
                     match40 = pattern40.search(text1)

                     if match40:
                         language_code = match40.group(1)
                         language_code = language_code.replace('"', '')
                         if setlan == "en":
                             language = language_codes.get(language_code, "unknown")
                         else:
                             language = language_codes_ar.get(language_code, "غير معروفه")

                    start32 = """followerCount":"""
                    end32 = ""","followingCount":"""
                    pattern32 = re.compile(re.escape(start32) + r"(.*?)" + re.escape(end32))
                    match32 = pattern32.search(text1)

                    if match32:
                        followerCount = match32.group(1)

                    start33 = ""","followingCount":"""
                    end33 = ""","heart"""
                    pattern33 = re.compile(re.escape(start33) + r"(.*?)" + re.escape(end33))
                    match33 = pattern33.search(text1)

                    if match33:
                        followingCount = match33.group(1)

                    start34 = ""","heartCount":"""
                    end34 = ""","videoCount":"""
                    pattern34 = re.compile(re.escape(start34) + r"(.*?)" + re.escape(end34))
                    match34 = pattern34.search(text1)

                    if match34:
                        heartCount = match34.group(1)

                    start35 = ""","videoCount":"""
                    end35 = ""","diggCount":"""
                    pattern35 = re.compile(re.escape(start35) + r"(.*?)" + re.escape(end35))
                    match35 = pattern35.search(text1)

                    if match35:
                        videoCount = match35.group(1)

                    start36 = ""","diggCount":"""
                    end36 = ""","friendCount":"""
                    pattern36 = re.compile(re.escape(start36) + r"(.*?)" + re.escape(end36))
                    match36 = pattern36.search(text1)

                    if match36:
                        diggCount = match36.group(1)

                    start37 = ""","friendCount":"""
                    end37 = """},"itemList":"""
                    pattern37 = re.compile(re.escape(start37) + r"(.*?)" + re.escape(end37))
                    match37 = pattern37.search(text1)

                    if match37:
                        friendCount = match37.group(1)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜")
                    global infoen
                    global infoar
                    infoen = (
    f"🔵 User IDᬊᬁ\t \nع✯<code>‌{id}‌</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌟 Unique usernameᬊᬁ\t \nع✯<code>{uniqueId}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 Nicknameᬊᬁ\t \nع✯<code>{nickname}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🖼️ Profile pictureᬊᬁ\t \nع✯<code>{avatarLarger}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 Bioᬊᬁ\t \nع✯<code>{signature}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕒 Account creation timeᬊᬁ\t \nع✯<code>{createTime}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔐 Is account verifiedᬊᬁ\t \nع✯<code>{verified}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔑 Another unique identityᬊᬁ\t \nع✯<code>{secUid}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📈 Interaction trend dataᬊᬁ\t \nع✯<code>{ftc}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💑 Account relationshipsᬊᬁ\t \nع✯<code>{relation}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"⭐ Are favorite settings openᬊᬁ\t \nع✯<code>{openFavorite}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔗 Bio linkᬊᬁ\t \nع✯<code>{bioLink}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 Comment settingsᬊᬁ\t \nع✯<code>{commentSetting}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📊 Categoryᬊᬁ\t \nع✯<code>{category}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👁️ Follower visibilityᬊᬁ\t \nع✯<code>{followingVisibility}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🎵 Duet settingsᬊᬁ\t \nع✯<code>{duetSetting}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"✂️ Stitch settingsᬊᬁ\t \nع✯<code>{stitchSetting}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔒 Is account privateᬊᬁ\t \nع✯<code>{privateAccount}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🤫 Is account secretᬊᬁ\t \nع✯<code>{secret}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌐 Is account virtual ADᬊᬁ\t \nع✯<code>{isADVirtual}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ Unique ID modification timeᬊᬁ\t \nع✯<code>{uniqueIdModifyTime}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💼 Is account commercialᬊᬁ\t \nع✯<code>{ttSeller}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌍 Regionᬊᬁ\t \nع✯<code>{region}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ Nickname modification timeᬊᬁ\t \nع✯<code>{nickNameModifyTime}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🚫 Embed banᬊᬁ\t \nع✯<code>{isEmbedBanned}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🎶 Access to experimental playlistᬊᬁ\t \nع✯<code>{canExpPlaylist}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📊 Profile embed permissionᬊᬁ\t \nع✯<code>{profileEmbedPermission}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🗣️ Languageᬊᬁ\t \nع✯<code>{language}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👥 Follower countᬊᬁ\t \nع✯<code>{followerCount}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 Following countᬊᬁ\t \nع✯<code>{followingCount}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"❤️ Like countᬊᬁ\t \nع✯<code>{heartCount}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📹 Video countᬊᬁ\t \nع✯<code>{videoCount}</code>✯\n         \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👫 Friend countᬊᬁ\t \nع✯<code>{friendCount}</code>✯\n         \n✤H࿐e࿐x࿐4≪"
)

                    infoar = (
    f"🔵 معرف المستخدمᬊᬁ\t \n X✯<code>{id}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌟 اسم المستخدم الفريدᬊᬁ\t \n X✯<code>{uniqueId}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 الاسم المستعارᬊᬁ\t \n X✯<code>{nickname}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🖼️ صورة الملف الشخصيᬊᬁ\t \n X✯<code>{avatarLarger}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 السيرة الذاتيةᬊᬁ\t \n X✯<code>{signature}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕒 وقت إنشاء الحسابᬊᬁ\t \n X✯<code>{createTime}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔐 هل الحساب موثقᬊᬁ\t \n X✯<code>{verified}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔑 هوية فريدة أخرىᬊᬁ\t \n X✯<code>{secUid}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📈 بيانات اتجاه التفاعلᬊᬁ\t \n X✯<code>{ftc}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💑 علاقات الحساباتᬊᬁ\t \n X✯<code>{relation}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"⭐ هل إعدادات المفضلة مفتوحةᬊᬁ\t \n X✯<code>{openFavorite}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔗 رابط السيرة الذاتيةᬊᬁ\t \n X✯<code>{bioLink}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 إعدادات التعليقاتᬊᬁ\t \n X✯<code>{commentSetting}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📊 الفئةᬊᬁ\t \n X✯<code>{category}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👁️ رؤية المتابعينᬊᬁ\t \n X✯<code>{followingVisibility}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🎵 إعدادات الدويتᬊᬁ\t \n X✯<code>{duetSetting}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"✂️ إعدادات السحبةᬊᬁ\t \n X✯<code>{stitchSetting}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔒 هل الحساب خاصᬊᬁ\t \n X✯<code>{privateAccount}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🤫 هل الحساب سريᬊᬁ\t \n X✯<code>{secret}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌐 هل الحساب إعلان افتراضيᬊᬁ\t \n X✯<code>{isADVirtual}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ وقت تعديل الهوية الفريدةᬊᬁ\t \n X✯<code>{uniqueIdModifyTime}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💼 هل الحساب تجاريᬊᬁ\t \n X✯<code>{ttSeller}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌍 المنطقةᬊᬁ\t \n X✯<code>{region}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ وقت تعديل الاسم المستعارᬊᬁ\t \n X✯<code>{nickNameModifyTime}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🚫 حظر التضمينᬊᬁ\t \n X✯<code>{isEmbedBanned}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🎶 الوصول إلى قائمة التشغيل التجريبيةᬊᬁ\t \n E✯<code>{canExpPlaylist}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📊 إذن تضمين الملف الشخصيᬊᬁ\t \n X✯<code>{profileEmbedPermission}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🗣️ اللغةᬊᬁ\t \n X✯<code>{language}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👥 عدد المتابعينᬊᬁ\t \n X✯<code>{followerCount}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 عدد المتابعين الذين يتم متابعتهمᬊᬁ\t \n X✯<code>{followingCount}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"❤️ عدد الإعجاباتᬊᬁ\t \n X✯<code>{heartCount}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📹 عدد الفيديوهاتᬊᬁ\t \n X✯<code>{videoCount}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👫 عدد الأصدقاءᬊᬁ\t \n X✯<code>{friendCount}</code>✯\n        \n✤H࿐e࿐x࿐4≪"
)  
                    bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")
                    bot.send_photo(message.chat.id, requests.get(avatarLarger).content)                
                    if setlan == "en":
                        bot.send_message(message.chat.id, text=infoen, parse_mode='HTML')
                    elif setlan == "ar":
                        bot.send_message(message.chat.id, text=infoar, parse_mode='HTML')



            else:
                if setlan == "en":
                    bot.reply_to(message, "This TikTok user does not exist or has no public information.")
                elif setlan == "ar":
                    bot.reply_to(message, "هذا المستخدم على TikTok غير موجود أو ليس لديه معلومات عامة.")

        if setlan == "en":
             wait_m = "Processing your request..."
        elif setlan == "ar":
            wait_m = "معالجة طلبك..."
        if timer != 0:
            if setlan == "en":
               bot.send_message(message.chat.id, f"please wait\n ({timer} sec)")
            elif setlan == "ar":
               bot.send_message(message.chat.id, f"من فضلك انتظر\n ({timer} sec)")
        else:
           reply(message)
           for i in range(5, -1, -1):
              timer = i
              time.sleep(1)

bot.polling()