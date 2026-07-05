<div align="center">

# 🤖 Discord Bot Extractor

Extract Discord Bot information directly from bot tokens.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-black?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Simple • Fast • Lightweight

</div>

---

## ✨ Features

- 📄 Read unlimited bot tokens from `tokensbot.txt`
- 🆔 Give you Bot IDs directly from tokens
- 👤 Fetch bot usernames using the Discord API
- 💾 Export results as TXT and JSON
- ⚡ Fast processing
- 🔍 Automatic duplicate removal
- 🌐 Cross-platform support

---

## 📦 Installation

### Clone

```bash
git clone https://github.com/harm-ac/Token2ID.git
cd Token2ID
```

### Install Requirements

```bash
pip install -r requirements.txt
```

or simply run

```
SETUP.bat
```

---

## 📁 Project Structure

```
Discord-Bot-Extractor/
│
├── main.py
├── tokensbot.txt
├── requirements.txt
├── SETUP.bat
├── README.md
│
├── bots_output.txt
└── bots_data.json
```

---

## 🚀 Usage

### 1. Put your bot tokens inside

`tokensbot.txt`

Example

```
TOKEN_1
TOKEN_2
TOKEN_3
```

### 2. Start the extractor

```bash
python main.py
```

---

## 📤 Output

### Console

```
TOKEN
│
├── Bot ID
└── Bot Name
```

Example

```
MTA...xxxx
→ 123456789012345678
→ MusicBot
```

---

### TXT Output

```
token:id:name
```

Example

```
TOKEN:123456789012345678:MusicBot
```

---

### JSON Output

```json
{
  "total_bots": 2,
  "bots": [
    {
      "token": "...",
      "id": "...",
      "name": "MusicBot"
    }
  ]
}
```

---

## ⚙ Requirements

- Python 3.8+
- requests

---

## 📸 Workflow

```text
tokensbot.txt
       │
       ▼
 Read Tokens
       │
       ▼
 Decode Bot ID
       │
       ▼
 Discord API
       │
       ▼
 Get Bot Name
       │
       ▼
 Export Results
```

---

## ⚡ Performance

- Supports thousands of tokens
- Automatic duplicate removal
- Automatic error handling
- API fallback support

---

## 📝 Files Generated

| File | Description |
|------|-------------|
| bots_output.txt | token:id:name |
| bots_data.json | Full JSON export |

---

## ❗ Notes

- Internet connection is required when using the Discord API.
- Invalid tokens will be skipped automatically.
- Discord API rate limits may apply for very large token lists.

---

## 📜 Disclaimer

This project is intended for educational purposes and for managing bot tokens that you own or are authorized to use. Always comply with Discord's Terms of Service and applicable laws.

---

<div align="center">

Made with ❤️ using Python

</div>
