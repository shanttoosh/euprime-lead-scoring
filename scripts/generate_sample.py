"""
Generate sample CSV output for Google Sheets.
Run this to create the output file.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_sources.mock_data import generate_mock_leads
from src.scoring import LeadScorer
import pandas as pd
from datetime import datetime


def main():
    print("🧬 Generating Lead Scoring Sample Output...")
    
    # Generate leads
    print("  → Generating mock leads...")
    leads = generate_mock_leads(75)
    print(f"    Generated {len(leads)} leads")
    
    # Score leads
    print("  → Scoring leads...")
    scorer = LeadScorer()
    results = scorer.score_and_rank_leads(leads)
    
    # Convert to DataFrame
    data = [r.to_dict() for r in results]
    df = pd.DataFrame(data)
    
    # Add priority column
    def get_priority(score):
        if score >= 80:
            return "Very High"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Low"
        else:
            return "Very Low"
    
    df['Priority'] = df['Probability (%)'].apply(get_priority)
    
    # Reorder columns
    columns = [
        'Rank', 'Priority', 'Probability (%)', 'Name', 'Title',
        'Company', 'Person Location', 'HQ Location',
        'Email', 'LinkedIn', 'Score Breakdown',
        'Role Score', 'Funding Score', 'Tech Score', 
        'NAMs Score', 'Location Score', 'Publication Score'
    ]
    df = df[columns]
    
    # Save CSV
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"qualified_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    
    print(f"\n✅ Output saved to: {filepath}")
    print(f"\n📊 Summary:")
    print(f"   Total leads: {len(df)}")
    print(f"   Very High Priority (80%+): {len(df[df['Probability (%)'] >= 80])}")
    print(f"   High Priority (60-79%): {len(df[(df['Probability (%)'] >= 60) & (df['Probability (%)'] < 80)])}")
    print(f"   Average Score: {df['Probability (%)'].mean():.1f}%")
    print(f"   Top Score: {df['Probability (%)'].max():.1f}%")
    
    # Print top 5
    print(f"\n🔝 Top 5 Leads:")
    for _, row in df.head(5).iterrows():
        print(f"   {row['Rank']}. {row['Name']} - {row['Title']} @ {row['Company']} ({row['Probability (%)']:.0f}%)")


if __name__ == "__main__":
    main()
