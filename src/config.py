"""
Configuration module for Lead Scoring Agent.
Manages API keys, data source settings, and feature flags.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APIConfig:
    """API configuration for external services."""
    
    # PubMed (NCBI) - Free, no key required but optional for higher rate limits
    pubmed_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('NCBI_API_KEY')
    )
    pubmed_email: Optional[str] = field(
        default_factory=lambda: os.getenv('NCBI_EMAIL')
    )
    
    # LinkedIn / Proxycurl - Paid API for real LinkedIn data
    proxycurl_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('PROXYCURL_API_KEY')
    )
    
    # Apollo.io - Sales intelligence platform
    apollo_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('APOLLO_API_KEY')
    )
    
    # Hunter.io - Email finder
    hunter_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('HUNTER_API_KEY')
    )
    
    # Crunchbase - Company/funding data
    crunchbase_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('CRUNCHBASE_API_KEY')
    )
    
    # OpenAI / Gemini for enrichment
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('OPENAI_API_KEY')
    )
    gemini_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv('GEMINI_API_KEY')
    )
    
    # Google Sheets output
    google_creds_path: Optional[str] = field(
        default_factory=lambda: os.getenv('GOOGLE_CREDS_JSON', 'google_creds.json')
    )
    google_sheet_id: Optional[str] = field(
        default_factory=lambda: os.getenv('SHEET_ID')
    )


@dataclass
class DataSourceConfig:
    """Configuration for data sources."""
    
    # Which sources to use
    use_mock_linkedin: bool = True       # Use mock data for LinkedIn
    use_real_pubmed: bool = True         # Use real PubMed API
    use_mock_conferences: bool = True    # Use mock conference data
    
    # PubMed settings
    pubmed_max_results: int = 20
    pubmed_years_back: int = 2
    
    # Mock data settings
    mock_lead_count: int = 75


@dataclass
class ScoringConfig:
    """Configuration for lead scoring weights."""
    
    # Weights (must sum to reasonable total)
    weight_role_fit: int = 30
    weight_company_intent: int = 20
    weight_tech_fit: int = 15
    weight_nams: int = 10
    weight_location: int = 10
    weight_publication: int = 40
    
    @property
    def max_score(self) -> int:
        return (
            self.weight_role_fit + 
            self.weight_company_intent +
            self.weight_tech_fit + 
            self.weight_nams +
            self.weight_location + 
            self.weight_publication
        )
    
    def to_dict(self) -> Dict[str, int]:
        return {
            'role_fit': self.weight_role_fit,
            'company_intent': self.weight_company_intent,
            'tech_fit': self.weight_tech_fit,
            'nams': self.weight_nams,
            'location': self.weight_location,
            'publication': self.weight_publication
        }


@dataclass
class AppConfig:
    """Main application configuration."""
    
    api: APIConfig = field(default_factory=APIConfig)
    data_sources: DataSourceConfig = field(default_factory=DataSourceConfig)
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    
    # App settings
    app_title: str = "3D In-Vitro Lead Qualification Dashboard"
    app_description: str = "Identifying high-potential leads for 3D in-vitro model solutions"
    
    # Feature flags
    enable_csv_export: bool = True
    enable_google_sheets: bool = False  # Requires credentials
    enable_email_enrichment: bool = False  # Requires Hunter.io
    show_debug_info: bool = False


# Global config instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the application configuration."""
    return config


def update_config(**kwargs) -> AppConfig:
    """Update configuration with custom values."""
    global config
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        elif hasattr(config.data_sources, key):
            setattr(config.data_sources, key, value)
        elif hasattr(config.scoring, key):
            setattr(config.scoring, key, value)
    
    return config
