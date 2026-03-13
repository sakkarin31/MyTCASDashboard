# MyTCASDashboard
### ศักรินทร์ เหล็กแท้ รหัสนักศึกษา 6610110297
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
```
📦 project_root/
├── 🙈 .gitignore                    # Git ignore patterns
├── 🔍 admis.py                      # Data analysis and helper script
├── 📊 Dashboard.py                  # Main Streamlit dashboard application
├── 📋 MainData.csv                  # Primary dataset for dashboard
├── 🎯 MyTCAS.py                     # TCAS related analysis script
├── 💰 programs_with_fee.csv         # Program data with tuition fees
├── 📅 programs_with_rounds.csv      # Program data with admission rounds
├── 📦 requirements.txt              # Python dependencies list
└── 📖 README.md                     # Project documentation (this file)
```
---

## 🚀 Getting Started

### 1️⃣ Setup Python Environment and Install Dependencies

```bash
cd Finalweb

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

###  2️⃣ Run the Streamlit Dashboard

```bash
streamlit run Dashboard.py
```
