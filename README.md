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
  <img src="https://raw.githubusercontent.com/chelipika/ig_tg_win/main/assets/demo.gif" alt="Demo GIF" width="600">
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

## 🎮 Demo

Add [@ReelyFastBot](https://t.me/ReelyFastBot) on Telegram and start downloading your favorite Instagram content instantly!

<p align="center">
  <img src="https://raw.githubusercontent.com/chelipika/ig_tg_win/main/assets/usage-example.png" alt="Usage Example" width="300">
</p>

## 🔧 Installation

### Prerequisites

- Windows 10/11
- Python 3.8+
- Telegram Bot Token (from [BotFather](https://t.me/BotFather))
- Instagram credentials
- Database setup (see configuration)

### Setup

1. Clone the repository:
   ```cmd
   git clone https://github.com/chelipika/ig_tg_win.git
   cd ig_tg_win
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

3. Create a `config.py` file (see [Configuration](#configuration) section)

4. Run the bot:
   ```cmd
   python main.py
   ```

### Windows Installation Shortcut

You can also use the included batch file for quick setup:

```cmd
setup.bat
```

## 📝 Configuration

Create a `config.py` file in the project root with the following variables:

```python
# Instagram credentials
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"

# Telegram settings
TOKEN = "your_telegram_bot_token"
CHANNEL_ID = "@your_channel_id"  # Channel users need to subscribe to
CHANNEL_LINK = "https://t.me/your_channel"  # Public link to your channel
```

## 🪟 Windows-Specific Features

This version includes several optimizations for Windows systems:

- **File Path Handling**: Uses Windows-compatible path separation
- **System Tray Integration**: Run the bot in the background with system tray icon
- **Automated Startup**: Option to run the bot at Windows startup
- **Resource Management**: Optimized for Windows memory and CPU usage patterns
- **Batch Scripts**: Includes `.bat` files for common operations:
  - `setup.bat`: One-click installation and setup
  - `run.bat`: Quick start the bot
  - `update.bat`: Update the bot to the latest version

### System Requirements

- Windows 10 or 11 (64-bit recommended)
- At least 4GB RAM
- 100MB free disk space
- Internet connection

## 📚 Project Structure

```
ig_tg_win/
├── config.py                 # Configuration variables
├── main.py                   # Bot initialization and startup
├── database/
│   └── requests.py           # Database operations
├── reely/
│   └── keyboards.py          # Telegram inline keyboards
├── scripts/
│   ├── setup.bat             # Windows setup script
│   ├── run.bat               # Windows run script
│   └── update.bat            # Windows update script
└── requirements.txt          # Python dependencies
```

## 🚀 Usage

Once the bot is running, users can:

1. Start the bot with `/start`
2. Subscribe to the required channel (if enabled)
3. Send any Instagram post/reel URL
4. Receive the downloaded content directly in the chat

### Windows System Tray

Right-click the system tray icon to access these options:
- **Open Dashboard**: Opens the bot control panel
- **Pause/Resume**: Temporarily stop or restart the bot
- **Check for Updates**: Manually check for updates
- **Exit**: Completely shut down the bot

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
- [PyInstaller](https://www.pyinstaller.org/) - Used for creating Windows executables

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/chelipika">chelipika</a>
</p>

<p align="center">
  <a href="https://github.com/chelipika/ig_tg_d">Linux Version</a> •
  <a href="https://github.com/chelipika/ig_tg_win">Windows Version</a>
</p>
