# GDG MIET Google Cloud Skill Badge Tracker

A clean, modern, and responsive Streamlit web application designed for the **GDG MIET community** to track students' progress across the 10 predefined Google Cloud Skill Badges from their public Google Skills Boost profile.

---

## 🎨 Theme & UI Highlights

- **GDG MIET Branding**: Google 4-color strip (Blue, Red, Yellow, Green) with Google Material design styling.
- **Compact Header**: Minimal header (under 170px) with community title and subtitle.
- **Privacy First**: Masks profile IDs (e.g., `skills.google/public_profiles/abc12...99z`).
- **4 Key Metrics**: Completed, Remaining, Credits earned, and Completion rate.
- **Interactive Filters & Sorting**:
  - Filter by status: *All*, *Not started*, *Completed*
  - Filter by category: *Compute*, *Security and IAM*, *AI and ML*, *Generative AI*, *Gemini*, *DeepMind*
  - Sort by: *Incomplete first* (default), *Completed first*, *Campaign order*, *Highest credits*, *Lowest credits*
- **Action-Oriented Cards**: Shows *Start badge* or *View badge* with direct official links and credit indicators.

---

## 🚀 How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```

The application will be accessible at **`http://localhost:8501`**.

---

## 📁 Project Structure

```text
gdg_cloud_calci/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── badge_card.py              # Accessible badge card rendering component
├── profile_scraper.py         # Requests & BeautifulSoup scraper for Google Skills Boost
├── utils.py                   # URL validation, privacy masking, credit helpers
│
└── data/
    └── campaign_badges.json   # 10 predefined campaign skill badges
```
