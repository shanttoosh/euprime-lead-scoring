# Lead Scoring Agent for Biotech Lead Generation
# Identifying, enriching, and ranking leads for 3D in-vitro model sales

from src.models import Lead, Company, ScoringResult
from src.scoring import LeadScorer
from src.data_sources.mock_data import generate_mock_leads

__version__ = "1.0.0"
