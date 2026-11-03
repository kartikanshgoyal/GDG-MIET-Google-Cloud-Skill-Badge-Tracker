# ☁️ GDG on Campus MIET - Google Cloud Skill Badge Tracker

A simple and automated web application built with **Python & Streamlit** that enables students to track their progress across the 10 predefined Google Cloud Skill Badges from their public Google Skills Boost profile.

---

## 🚀 Live Demo & Workflow

1. Paste your public **Google Cloud Skills Boost** profile URL into the input field.
2. Click **🚀 Check My Progress**.
3. The application automatically fetches your public profile:
   - Displays your verified name and profile avatar.
   - Shows all **Completed Badges** under *Fetched Badges* along with completion dates and official badge artwork.
   - Lists all **Remaining Badges** with direct course links to complete them.
   - Calculates your live **Completion Rate (%)** and progress metrics.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Backend & Logic:** Python 3.10+
- **Data Scraping & Extraction:** Requests, BeautifulSoup4
- **Data Storage:** JSON

---

## 📋 Predefined 10 Google Cloud Skill Badges

| # | Badge Title | Category |
|---|---|---|
| 1 | The Basics of Google Cloud Compute | Compute |
| 2 | Configure Service Accounts and IAM Roles for Google Cloud | Security and IAM |
| 3 | Implement Speech and Language Solutions with Pre-trained APIs | AI and ML |
| 4 | Develop AI-Powered Prototypes in Google AI Studio | Generative AI |
| 5 | Analyze Images with the Cloud Vision API | AI and ML |
| 6 | Prompt Design in Agent Platform | Generative AI |
| 7 | Explore Generative AI in Agent Platform | Generative AI |
| 8 | Create Your First Gemini Enterprise Application | Gemini |
| 9 | Orchestrate Multi-agent Workflows with Gemini Enterprise | Gemini |
| 10 | Google DeepMind: Train A Small Language Model | DeepMind |

---

## 💻 Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/kartikanshgoyal/GDG-MIET-Google-Cloud-Skill-Badge-Tracker.git
cd GDG-MIET-Google-Cloud-Skill-Badge-Tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application
```bash
streamlit run app.py
```

The app will launch in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
├── app.py                     # Main Streamlit dashboard application
├── badge_card.py              # Badge card UI component with official artwork
├── profile_scraper.py         # Google Skills Boost profile scraper
├── utils.py                   # URL validation and privacy masking helpers
├── data/
│   └── campaign_badges.json   # Predefined 10 campaign skill badges data
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 👥 Community

Built for the **GDG on Campus MIET** community.
