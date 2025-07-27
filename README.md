# MyTCASDashboard
# 🎓 Thai Computer Engineering Dashboard & Web Scraper

A system developed to **collect** and **visualize** computer engineering program data from universities across Thailand.  
Supports **automated fee data scraping** from websites and **interactive dashboard visualization**.

> 💡 Built with Python, Playwright, Pandas, Plotly, and Streamlit.

---

## 🌐 Key Features

### 🔎 1. Web Scraping (Automated Data Collection)
- Scrapes computer engineering program data from TCAS websites.
- Automatically processes and analyzes tuition fees per semester.
- Stores data in CSV format for further use.

### 📊 2. Dashboard Visualization (Interactive Analytics)
- Analyze data by:
  - University type (Top, Technology, Rajabhat, Private)
  - Tuition fee range
  - Admission rounds and quota
- Visualizations include:
  - Box Plot, Pie Chart, Scatter Plot
  - Rankings of universities with lowest fees and highest admission quotas
- User-friendly sidebar interface for easy navigation.

---

## 📁 Project Structure

📦 project_root/
├── .gitignore
├── admis.py # Data analysis or helper script
├── Dashboard.py # Main Streamlit dashboard
├── MainData.csv # Primary data used in the dashboard
├── MyTCAS.py # Additional TCAS related script
├── programs_with_fee.csv # Programs data with fees after scraping
├── programs_with_rounds.csv # Programs data with admission rounds info
├── requirements.txt # Python dependencies list
└── README.md # This file

---

## 🚀 Getting Started

### 1️⃣ Setup Python Environment and Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate          # For Windows
# or
source venv/bin/activate       # For macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install 
```

###2️⃣ Run the Streamlit Dashboard

```bash
streamlit run Dashboard.py
```