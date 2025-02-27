# 🚀 ReelyFastBot for Windows


<p align="center">
  <img src="https://img.shields.io/github/license/chelipika/ig_tg_win" alt="License">
  <img src="https://img.shields.io/github/stars/chelipika/ig_tg_win" alt="Stars">
  <img src="https://img.shields.io/github/forks/chelipika/ig_tg_win" alt="Forks">
  <img src="https://img.shields.io/github/issues/chelipika/ig_tg_win" alt="Issues">
</p>

**ReelyFastBot for Windows** is a Windows-optimized version of the powerful Telegram bot that allows users to easily download content from Instagram, including Reels, Videos, Photos, and Carousels.

> 🔗 Looking for the Linux version? Check out [ig_tg_d](https://github.com/chelipika/ig_tg_d)

<p align="center">
  <img src="https://raw.githubusercontent.com/chelipika/ig_tg_win/main/assets/demo.gif" alt="Demo GIF" width="100">
</p>

## ✨ Features

- ⚡ **Lightning Fast Downloads**: Get your Instagram content in seconds
- 🎬 **Multiple Format Support**: Download Reels, Videos, Photos, and Carousels
- 📱 **User-Friendly Interface**: Simple paste-and-go functionality
- 🔄 **Channel Subscription System**: Optional channel subscription requirement
- 📊 **User Tracking**: Basic database integration for user management
- 🎁 **Fun Facts**: Displays random Instagram facts during download
- 👥 **Group Support**: Can be added to Telegram groups
- 🪟 **Windows Optimized**: Specifically designed to run smoothly on Windows systems
- ⚡ **Concurrent Downloads**: Uses ThreadPoolExecutor for efficient parallel processing
- 🔄 **Asynchronous Architecture**: Non-blocking operation for better performance

## 🎮 Demo

Add [@ReelyFastBot](https://t.me/ReelyFastBot) on Telegram and start downloading your favorite Instagram content instantly!

<a href="https://github.com/chelipika/ig_tg_win/blob/main/demo.md">Demo img and gif</a>

## 🔧 Installation

### Prerequisites

- Windows 10/11
- Python 3.8+
- Telegram Bot Token (from [BotFather](https://t.me/BotFather))
- Required Python packages:
  - aiogram
  - instaloader
  - asyncio

### Setup

1. Clone the repository:
   ```cmd
   git clone https://github.com/chelipika/ig_tg_win.git
   cd ig_tg_win
   ```

2. Install dependencies:
   ```cmd
   pip install aiogram instaloader
   ```

3. Create a `config.py` file (see [Configuration](#configuration) section)

4. Run the bot:
   ```cmd
   python bot.py
   ```

## 📝 Configuration

Update a `config.py` file in the project root with the following variables:

```python
# Telegram settings
TOKEN = "your_telegram_bot_token"
CHANNEL_ID = "@your_channel_id"  # Channel users need to subscribe to
CHANNEL_LINK = "https://t.me/your_channel"  # Public link to your channel
```

## 📚 Project Structure

```
ig_tg_win/
├── config.py                 # Configuration variables
├── main.py                   # Bot initialization and startup
├── database/
│   └── requests.py           # Database operations
├── reely/
│   └── keyboards.py          # Telegram inline keyboards
└── README.md                 # This documentation
```

## 🚀 Usage

Once the bot is running, users can:

1. Start the bot with `/start`
2. Subscribe to the required channel (if enabled)
3. Send any Instagram post/reel URL
4. Receive the downloaded content directly in the chat

### Advanced Features

- **Concurrent Processing**: The bot can handle multiple requests simultaneously
- **Automatic Cleanup**: Downloaded files are removed after sending
- **Admin Broadcasting**: Use `/narrator` command to send messages to all users

## 🙌 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [instaloader](https://github.com/instaloader/instaloader) - Instagram scraping library
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [asyncio](https://docs.python.org/3/library/asyncio.html) - Python's asynchronous I/O framework

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/chelipika">chelipika</a>
</p>

<p align="center">
  <a href="https://github.com/chelipika/ig_tg_d">Linux Version</a> •
  <a href="https://github.com/chelipika/ig_tg_win">Windows Version</a>
</p>
