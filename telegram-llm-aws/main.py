import os
import redis
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ===================== 配置 =====================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HKBU_API_KEY = os.getenv("HKBU_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# ===================== Redis 存储 =====================
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True,
    socket_timeout=5
)

# ===================== HKBU GPT 官方代码 =====================
def hkbu_chat(prompt):
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            base_url = "https://genai.hkbu.edu.hk/api/v0/rest"
            model = "gpt-5-mini"
            api_ver = "2024-12-01-preview"

            url = f"{base_url}/deployments/{model}/chat/completions?api-version={api_ver}"

            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "api-key": HKBU_API_KEY,
            }

            messages = [
                {"role": "system", "content": "You are a helpful university assistant."},
                {"role": "user", "content": prompt},
            ]

            payload = {
                "messages": messages,
                "temperature": 1,
                "max_tokens": 150,
                "top_p": 1,
                "stream": False
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Truncate to fit Telegram's message limit (max 4096 characters)
                if len(content) > 4000:
                    content = content[:4000] + "... (truncated)"
                return content
            else:
                return f"LLM Error {response.status_code}: {response.text[:50]}"
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                import time
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            return "LLM 连接超时，请稍后重试"
        except Exception as e:
            return f"LLM connect error: {str(e)}"

# ===================== Telegram 机器人 =====================
async def start(update: Update, context):
    await update.message.reply_text("✅ HKBU AWS Cloud Bot 已启动！")

async def chat_message(update: Update, context):
    user_id = update.effective_user.id
    text = update.message.text

    # 保存聊天记录到 Redis
    try:
        redis_client.lpush(f"user:{user_id}:history", text)
    except:
        pass

    # 调用 HKBU GPT
    reply = hkbu_chat(text)
    await update.message.reply_text(reply)

# ===================== 启动 =====================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message))
    app.run_polling()

if __name__ == "__main__":
    main()
