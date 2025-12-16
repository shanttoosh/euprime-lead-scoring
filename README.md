# 🧬 Lead Scoring Agent for 3D In-Vitro Models

An automated lead qualification pipeline that identifies, enriches, and ranks potential customers for companies selling 3D in-vitro models in drug discovery.

## 📊 Live Demo

**Streamlit App**: [Coming Soon - Deploy to Streamlit Cloud]

**Sample Output**: [Google Sheets Link - Coming Soon]

## 🏛️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Data Sources  │────▶│  Scoring Engine │────▶│    Dashboard    │
│                 │     │                 │     │                 │
│ • LinkedIn      │     │ • Role Fit +30  │     │ • Search/Filter │
│ • PubMed        │     │ • Funding +20   │     │ • Rank Table    │
│ • Conferences   │     │ • Tech +15      │     │ • CSV Export    │
└─────────────────┘     │ • NAMs +10      │     └─────────────────┘
                        │ • Location +10  │
                        │ • Pubs +40      │
                        └─────────────────┘
```

## 🎯 Scoring Methodology

The **Propensity to Buy** score (0-100) is calculated from weighted signals:

| Signal | Category | Points | Description |
|--------|----------|--------|-------------|
| 🎯 Role Fit | Title Match | +30 | Director/Head + Toxicology/Safety/Hepatic/3D |
| 💰 Company Intent | Recent Funding | +20 | Series A/B/Seed in last 2 years |
| 🔬 Technographic | Uses In-Vitro | +15 | Company already uses similar tech |
| 🧪 NAMs Openness | Methodology | +10 | Open to New Approach Methodologies |
| 📍 Location | Biotech Hub | +10 | Boston, Bay Area, Basel, UK Golden Triangle |
| 📚 Scientific Intent | Publications | +40 | DILI/liver toxicity paper in last 2 years |

**Score Interpretation:**
- 🔥 **80-100**: Very High Priority - Immediate outreach recommended
- ✅ **60-79**: High Priority - Strong fit, follow up soon
- 📊 **40-59**: Medium Priority - Worth nurturing
- 📋 **20-39**: Low Priority - Monitor for changes
- ⚪ **0-19**: Very Low - Not a current fit

## 🛠️ Tech Stack

- **Python 3.9+** - Core language
- **Streamlit** - Interactive dashboard
- **Pandas** - Data processing
- **Mock Data** - LinkedIn-style profiles (production would use APIs)

## 🔧 Local Setup

1. **Clone & setup environment**
```bash
git clone <repo-url>
cd Euprime
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
Euprime/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── models.py             # Lead, Company, ScoringResult classes
│   ├── scoring.py            # Propensity scoring engine
│   ├── config.py             # API keys & feature configuration
│   └── data_sources/
│       ├── __init__.py
│       ├── mock_data.py      # Mock lead generator (75+ leads)
│       └── pubmed.py         # Real PubMed API integration
├── data/
│   └── output/               # Generated CSV outputs
└── scripts/
    └── generate_sample.py    # Sample output generator
```

## 🔌 Data Sources

| Source | Status | Description |
|--------|--------|-------------|
| **Mock LinkedIn** | ✅ Ready | 75+ realistic biotech profiles |
| **Real PubMed** | ✅ Ready | NCBI E-utilities API (free, no key) |
| **Mock Conferences** | ✅ Ready | SOT attendee simulation |
| **Proxycurl** | 🔧 Configured | LinkedIn API (add key in .env) |
| **Apollo.io** | 🔧 Configured | Sales intelligence (add key) |
| **Hunter.io** | 🔧 Configured | Email finder (add key) |
| **Crunchbase** | 🔧 Configured | Funding data (add key) |

## 📤 Output Format

The dashboard exports leads with these columns:

| Column | Description |
|--------|-------------|
| Rank | Position by propensity score |
| Priority | Visual priority indicator |
| Probability (%) | 0-100 propensity score |
| Name | Full name |
| Title | Job title |
| Company | Company name |
| Person Location | Where they work/live |
| HQ Location | Company headquarters |
| Email | Business email |
| LinkedIn | Profile URL |
| Score Breakdown | Individual signal contributions |

## ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy!

## 🔮 Future Enhancements

- [ ] Real LinkedIn API integration (via Proxycurl)
- [ ] Live PubMed search
- [ ] Conference attendee list imports
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Email campaign automation
- [ ] Slack/Teams notifications

## 📄 License

MIT License - Built for Euprime AI Internship

---

**Author**: [Your Name]  
**Date**: December 2025  
**Contact**: akash@euprime.org
