# 📂 File Converter Bot  

A **Python-based Telegram bot** that allows users to **convert and manipulate various file formats**.  
This bot supports **TXT, DOCX, and PDF conversions**, as well as **PDF splitting and merging**.  

Built using **Aiogram**, this bot ensures **fast, accurate, and automated file processing** for users.  

---

## Features  

### 📄 File Conversion  
- **Convert TXT to Various Formats**  
- **Convert DOCX to Different Formats**  
- **Convert PDFs Easily**  
- **Handle Multiple File Types**  

### ✂️ PDF Splitting & Merging  
- **Split Large PDF Files** into smaller sections  
- **Merge Multiple PDFs** into a single document  
- **Preserve Original Formatting**  

### 🔄 Smart File Handling  
- **Automated File Detection & Processing**  
- **Error Handling for Smooth User Experience**  
- **Fast & Secure Processing**  

---

## Requirements  

- **Python 3.x**  
- **All dependencies are listed in `requirements.txt`** 

---

## 🛠 Installation  

1. Clone the Repository
```bash
git clone https://github.com/GhostKX/File-Converter-Bot.git
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot

- Create a .env file to store your Telegram API Key
- Add your Telegram Bot Token:

```
API_KEY=your-telegram-bot-token
```

4. Navigate to the project directory
```bash
cd File-Converter-Bot
```

5. Run the bot
```bash
python main.py
```

---

## Usage  

### Sending a File  
- Start the bot by sending `/start`  
- Upload a **TXT, DOCX, or PDF file**  
- The bot **automatically detects the file type** and provides conversion options  

### File Conversion Process  
- **TXT Conversion** → Convert text files into other formats  
- **DOCX Conversion** → Convert Word documents into different formats  
- **PDF Processing** → Convert, split, or merge PDFs  

### Receiving the Converted File  
- Once processing is complete, the bot **sends back the converted file**  
- The **original file is deleted** after processing to save storage  

---

## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/File-Converter-Bot)**