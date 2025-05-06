
# Lodi – Your Personal Moving Assistant 🧳

![Python](https://img.shields.io/badge/python-3.9+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![SerpAPI](https://img.shields.io/badge/API-SerpAPI-blue)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-success)


Lodi is a task based CLI assistant that helps automate long distance move planning. It uses live search, contact scraping, Google Sheets integration, and GPT support to simplify relocation logistics.

![Lodi Demo](assets/lodi_demo.gif)

---

## 🚀 Features

- ✅ **Checklist-Based CLI** – Step by step relocation workflow
- ✅ **Live Mover Search** – Real time Google search via SerpAPI
- ✅ **Contact Scraping** – Extracts phone/email from mover websites using BeautifulSoup
- ✅ **Google Sheets Integration** – Writes search results to a shared spreadsheet using GCP IAM
- ✅ **Search Logging** – Tracks SerpAPI usage to stay within quota
- ✅ **GPT Integration (Modular)** – Uses GPT-4o for utility setup tips and generic relocation help

---

## ☁️ Google Cloud Setup

Lodi connects securely to Google Sheets using a GCP service account.

- Create a service account in GCP IAM with `Editor` or `Sheets API` permissions.
- Generate a JSON key and save it locally as `creds/lodi-key.json`.
- Ensure the key file is excluded using `.gitignore`.

---

## 📋 Default Task Checklist

- Find long-distance movers  

[TODO]
- Update address  
- Book movers  
- Set up utilities  
- Transfer internet service  
- Change driver license  
- Find local services  

---

## 🛠️ Setup

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Add Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your-openai-key
SERPAPI_KEY=your-serpapi-key
```

### 3. Add Google Sheets Key

Save your GCP key file to:

```
creds/lodi-key.json
```

---

## 🖥️ Usage

Start the assistant:

```bash
python lodi.py
```

- The app walks through each task.
- Use the `find_long_distance_movers` task to search movers, scrape contact info, and save results.

**Example Output:**

```json
{
  "name": "Best NY to Atlanta Movers",
  "phone": "(212) 651-7273",
  "email": "info@...",
  "website": "https://...",
  "description": "Full-service movers with next-day delivery"
}
```

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `lodi.py` | Main CLI logic |
| `lodi_progress.json` | Task tracking state |
| `serper_log.json` | SerpAPI usage logs |
| `creds/lodi-key.json` | GCP Sheets key (ignored) |
| `assets/` | Diagrams, screenshots, and demo GIFs |

---

## 🧠 Next Improvements

### Minor Tasks
- Label low-quality results (e.g., Reddit) as "discussion"
- Add basic ranking/scoring logic

### Major Tasks
- Deduplication for repeated companies
- Classify results (official vs. aggregator vs. discussion)
- Add fallback to scrape `/contact` pages when needed

---

## 💬 Feedback & Contributions

Lodi is a personal showcase project to demonstrate applied AI tooling, API integration, and CLI design.  
Feel free to fork, adapt, and build your own assistant.

> Built by Vince Allen
