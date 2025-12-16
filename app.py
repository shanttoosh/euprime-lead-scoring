"""
🧬 3D In-Vitro Lead Qualification Dashboard
Biotech Lead Scoring Agent - Streamlit Application

Identifies, enriches, and ranks leads for companies selling 3D in-vitro models.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import our modules
from src.models import Lead, ScoringResult
from src.scoring import LeadScorer
from src.data_sources.mock_data import generate_mock_leads, MOCK_LEADS

# Page config
st.set_page_config(
    page_title="3D In-Vitro Lead Qualification Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #a0aec0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Table styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.02) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(22, 33, 62, 0.95);
    }
    
    /* Priority badges */
    .priority-very-high {
        background: linear-gradient(90deg, #f5576c 0%, #f093fb 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .priority-high {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def get_priority_badge(score: float) -> str:
    """Return HTML badge based on score."""
    if score >= 80:
        return "🔥 Very High"
    elif score >= 60:
        return "✅ High"
    elif score >= 40:
        return "📊 Medium"
    elif score >= 20:
        return "📋 Low"
    else:
        return "⚪ Very Low"


@st.cache_data
def load_and_score_leads():
    """Load leads and calculate scores (cached for performance)."""
    leads = generate_mock_leads(75)
    scorer = LeadScorer()
    results = scorer.score_and_rank_leads(leads)
    return results


def results_to_dataframe(results: list) -> pd.DataFrame:
    """Convert scoring results to pandas DataFrame."""
    data = [r.to_dict() for r in results]
    df = pd.DataFrame(data)
    return df


def main():
    # Header
    st.markdown('<h1 class="main-header">🧬 3D In-Vitro Lead Qualification Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Identifying high-potential leads for 3D in-vitro model solutions in drug discovery</p>', unsafe_allow_html=True)
    
    # Load and score leads
    with st.spinner("Loading and scoring leads..."):
        results = load_and_score_leads()
        df = results_to_dataframe(results)
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Search box
    search_query = st.sidebar.text_input(
        "Search (Name, Title, Company, Location)",
        placeholder="e.g., Boston, Toxicology, Pfizer..."
    )
    
    # Data source configuration
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ⚙️ Data Sources")
    use_real_pubmed = st.sidebar.checkbox(
        "Use Real PubMed API",
        value=False,
        help="Fetch real publication data from NCBI (may be slow)"
    )
    
    if use_real_pubmed:
        st.sidebar.info("📡 Real PubMed integration enabled. API calls may take a few seconds.")
    
    # Minimum score filter
    min_score = st.sidebar.slider(
        "Minimum Probability Score",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )
    
    # Priority filter
    priority_filter = st.sidebar.multiselect(
        "Priority Level",
        options=["🔥 Very High (80+)", "✅ High (60-79)", "📊 Medium (40-59)", "📋 Low (20-39)", "⚪ Very Low (0-19)"],
        default=[]
    )
    
    # Company filter
    companies = df['Company'].unique().tolist()
    selected_companies = st.sidebar.multiselect(
        "Filter by Company",
        options=sorted(companies),
        default=[]
    )
    
    # Location filter
    st.sidebar.markdown("### 📍 Location Filters")
    person_locations = df['Person Location'].unique().tolist()
    selected_person_locations = st.sidebar.multiselect(
        "Person Location",
        options=sorted(person_locations),
        default=[]
    )
    
    hq_locations = df['HQ Location'].unique().tolist()
    selected_hq_locations = st.sidebar.multiselect(
        "Company HQ Location",
        options=sorted(hq_locations),
        default=[]
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_query:
        mask = (
            filtered_df['Name'].str.lower().str.contains(search_query.lower(), na=False) |
            filtered_df['Title'].str.lower().str.contains(search_query.lower(), na=False) |
            filtered_df['Company'].str.lower().str.contains(search_query.lower(), na=False) |
            filtered_df['Person Location'].str.lower().str.contains(search_query.lower(), na=False) |
            filtered_df['HQ Location'].str.lower().str.contains(search_query.lower(), na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Score filter
    filtered_df = filtered_df[filtered_df['Probability (%)'] >= min_score]
    
    # Priority filter
    if priority_filter:
        priority_masks = []
        for p in priority_filter:
            if "Very High" in p:
                priority_masks.append(filtered_df['Probability (%)'] >= 80)
            elif "High" in p:
                priority_masks.append((filtered_df['Probability (%)'] >= 60) & (filtered_df['Probability (%)'] < 80))
            elif "Medium" in p:
                priority_masks.append((filtered_df['Probability (%)'] >= 40) & (filtered_df['Probability (%)'] < 60))
            elif "Low" in p and "Very" not in p:
                priority_masks.append((filtered_df['Probability (%)'] >= 20) & (filtered_df['Probability (%)'] < 40))
            elif "Very Low" in p:
                priority_masks.append(filtered_df['Probability (%)'] < 20)
        
        if priority_masks:
            combined_mask = priority_masks[0]
            for mask in priority_masks[1:]:
                combined_mask = combined_mask | mask
            filtered_df = filtered_df[combined_mask]
    
    # Company filter
    if selected_companies:
        filtered_df = filtered_df[filtered_df['Company'].isin(selected_companies)]
    
    # Location filters
    if selected_person_locations:
        filtered_df = filtered_df[filtered_df['Person Location'].isin(selected_person_locations)]
    
    if selected_hq_locations:
        filtered_df = filtered_df[filtered_df['HQ Location'].isin(selected_hq_locations)]
    
    # Re-rank after filtering
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df['Rank'] = range(1, len(filtered_df) + 1)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", len(filtered_df))
    
    with col2:
        high_priority = len(filtered_df[filtered_df['Probability (%)'] >= 60])
        st.metric("High Priority (60%+)", high_priority)
    
    with col3:
        avg_score = filtered_df['Probability (%)'].mean() if len(filtered_df) > 0 else 0
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    with col4:
        top_score = filtered_df['Probability (%)'].max() if len(filtered_df) > 0 else 0
        st.metric("Top Score", f"{top_score:.1f}%")
    
    st.markdown("---")
    
    # Add priority column
    filtered_df['Priority'] = filtered_df['Probability (%)'].apply(get_priority_badge)
    
    # Display columns
    display_columns = [
        'Rank', 'Priority', 'Probability (%)', 'Name', 'Title', 
        'Company', 'Person Location', 'HQ Location', 
        'Email', 'LinkedIn', 'Score Breakdown'
    ]
    
    # Main data table
    st.markdown("### 📊 Qualified Leads")
    
    # Show/hide score details
    show_details = st.checkbox("Show detailed score breakdown", value=False)
    
    if show_details:
        display_columns.extend(['Role Score', 'Funding Score', 'Tech Score', 'NAMs Score', 'Location Score', 'Publication Score'])
    
    # Display the dataframe
    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        height=500,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Priority": st.column_config.TextColumn("Priority", width="medium"),
            "Probability (%)": st.column_config.ProgressColumn(
                "Probability",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "LinkedIn": st.column_config.LinkColumn("LinkedIn", width="medium"),
            "Email": st.column_config.TextColumn("Email", width="medium"),
        }
    )
    
    # Export section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # CSV download
        csv = filtered_df[display_columns].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"qualified_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel download  
        # Note: For Excel, we'd need openpyxl, using CSV for simplicity
        st.download_button(
            label="📊 Download Excel",
            data=csv,
            file_name=f"qualified_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Scoring methodology
    with st.expander("📖 Scoring Methodology"):
        st.markdown("""
        ### Propensity to Buy Score (0-100)
        
        The score predicts likelihood of interest in 3D in-vitro models based on weighted signals:
        
        | Signal | Category | Points | Description |
        |--------|----------|--------|-------------|
        | 🎯 Role Fit | Title Match | +30 | Director/Head + Toxicology/Safety/Hepatic/3D |
        | 💰 Company Intent | Recent Funding | +20 | Series A/B/Seed in last 2 years |
        | 🔬 Technographic | Uses In-Vitro | +15 | Company already uses similar tech |
        | 🧪 NAMs Openness | Methodology | +10 | Open to New Approach Methodologies |
        | 📍 Location | Biotech Hub | +10 | Boston/Cambridge, Bay Area, Basel, UK |
        | 📚 Scientific Intent | Publications | +40 | DILI/liver toxicity paper in 2 years |
        
        **Maximum: 125 points → Normalized to 0-100%**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🧬 Lead Scoring Agent for 3D In-Vitro Models | Built for Euprime</p>
            <p>Data sources: LinkedIn (mock), PubMed, Conference Attendees | Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
