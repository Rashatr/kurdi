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
        time.sleep(5)
