# Telegram LLM AWS

## Project Introduction

This is an intelligent chat system based on Telegram bot and AWS cloud services, using HKBU GPT model for natural language interaction.

## Features

- 🤖 Telegram bot interface
- 🌐 HKBU GPT model integration
- 📦 Docker containerized deployment
- 🗄️ Redis chat history storage
- 🔄 Auto-retry mechanism
- 📱 Message length limit handling

## Tech Stack

- Python 3.10+
- python-telegram-bot 20.7
- Redis
- Docker & Docker Compose
- HKBU GPT API

## Quick Start

### 1. Environment Setup

Copy the `.env` file and fill in the configuration:

```bash
cp .env.example .env
```

Edit the `.env` file and fill in the following configurations:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
HKBU_API_KEY=your_hkbu_api_key
REDIS_HOST=your_redis_host
REDIS_PORT=6379
```

### 2. Build and Run

Build and start the service using Docker Compose:

```bash
docker-compose up -d
```

Check logs:

```bash
docker-compose logs -f
```

### 3. Usage

1. Search for your bot in Telegram and start a conversation
2. Enter `/start` command to begin
3. Directly input questions or conversation content
4. The bot will generate responses using HKBU GPT

## Project Structure

```
telegram-llm-aws/
├── main.py          # Main program file
├── requirements.txt # Dependency list
├── Dockerfile       # Docker build file
├── docker-compose.yml # Docker Compose configuration
└── .env            # Environment variables
```

## Error Handling

- **Message too long**: Auto-truncate replies over 4000 characters
- **Connection timeout**: Auto-retry 3 times with exponential backoff
- **Redis connection failure**: Log but don't affect main functionality
- **API errors**: Return friendly error messages

## Notes

1. Ensure network access to HKBU GPT API
2. Ensure Redis service is running properly
3. Telegram Bot Token must be correctly configured
4. HKBU API Key must be valid

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check if Telegram Token is correct
2. **LLM connection failure**: Check network connection and HKBU API Key
3. **Redis error**: Check Redis service status
4. **Message send failure**: Check if message length exceeds limit

## License

MIT License

## Contact

For any questions or issues, please contact the project maintainer.