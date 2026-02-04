import os, time, requests, telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = """
وەڵام بە کوردی بدە.
هەمیشە بەڵگە بهێنە (سورە/ئایەت).
ئەگەر دڵنیایت نییە بڵێ نازانم.
فۆرمات:
وەڵام:
...
بەڵگە:
- ...
"""

def ask(q):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":q}
            ]
        }
    )
    return r.json()["choices"][0]["message"]["content"]

@bot.message_handler(func=lambda m: True)
def reply(m):
    try:
        bot.reply_to(m, ask(m.text))
    except:
        bot.reply_to(m, "کێشەیەک ڕوویدا")

while True:
    try:
        bot.polling()
    except:
        time.sleep(5) تەنها ئەگەر دڵنیایت بە ناوی کتێب و سەرچاوەکە. بەڵگە دروست مەکە و ژمارەی ساختە مەهێنە.
5) بۆ بابەتە گرنگەکان (طلاق، میراث، نکاح، قەزا، تاوان…):
   هەمیشە بڵێ "ئەمە فتوا نییە، تەنها ڕێنماییە" و ڕێنمایی بکە بە پرسیارکردن لە موفتی/مامۆستا.
6) وەڵامەکەت هەمیشە بە فۆرماتێکی دیاریکراو بێت:

وەڵام:
(وەڵامی ڕوون و سادە)

بەڵگە:
- (سورە:ئایەت) یان (سەرچاوەی دڵنیاتر)
- ئەگەر بەڵگە نییە: بنووسە "بەڵگەی دڵنیایی نییە"

تێبینی:
- (ئەگەر پێویست بوو: "ئەمە فتوا نییە")
"""

def ask_ai(user_text: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_text.strip()},
        ],
    }

    r = requests.post(url, headers=headers, json=payload, timeout=45)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    text = (m.text or "").strip()
    if not text:
        bot.reply_to(m, "تکایە پرسیارێک بنووسە.")
        return

    try:
        reply = ask_ai(text)

        # Telegram message length safety
        if len(reply) > 3800:
            reply = reply[:3800] + "\n...\n(وەڵام زۆر درێژ بوو، دەتوانیت داوای بەش بەش بکەیت.)"

        bot.reply_to(m, reply)

    except requests.HTTPError as e:
        # If API returns an error, don't crash the bot
        bot.reply_to(m, "ببورە، کێشەیەک ڕوویدا لە پەیوەستبوون بە AI. دواتر دووبارە هەوڵ بدە.")
        print("HTTPError:", e, getattr(e, "response", None).text if getattr(e, "response", None) else "")
    except Exception as e:
        bot.reply_to(m, "ببورە، هەڵەیەک ڕوویدا. دووبارە هەوڵ بدە.")
        print("Error:", e)

# Keep running forever (auto-restart on crash)
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        print("Polling crashed, restarting in 5s:", e)
        time.sleep(5)