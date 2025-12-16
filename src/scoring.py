"""
Lead Scoring Engine - Propensity to Buy Calculator.
Implements weighted scoring algorithm for biotech lead qualification.
"""

from typing import List
from .models import Lead, ScoringResult


class LeadScorer:
    """
    Calculates propensity-to-buy scores for leads.
    
    Scoring weights (max 125 points, normalized to 0-100):
    - Role Fit: +30 (Director/Head + Toxicology/Safety/Hepatic/3D)
    - Company Intent: +20 (Series A/B funding in last 2 years)
    - Technographic: +15 (uses in-vitro models)
    - NAMs Openness: +10 (open to New Approach Methodologies)
    - Location: +10 (biotech hub)
    - Scientific Intent: +40 (relevant publication in last 2 years)
    """
    
    # Scoring weights
    WEIGHT_ROLE_FIT = 30
    WEIGHT_COMPANY_INTENT = 20
    WEIGHT_TECH_FIT = 15
    WEIGHT_NAMS = 10
    WEIGHT_LOCATION = 10
    WEIGHT_PUBLICATION = 40
    
    MAX_RAW_SCORE = (
        WEIGHT_ROLE_FIT + WEIGHT_COMPANY_INTENT + 
        WEIGHT_TECH_FIT + WEIGHT_NAMS + 
        WEIGHT_LOCATION + WEIGHT_PUBLICATION
    )  # = 125
    
    def __init__(self, custom_weights: dict = None):
        """Initialize scorer with optional custom weights."""
        if custom_weights:
            self.WEIGHT_ROLE_FIT = custom_weights.get('role_fit', self.WEIGHT_ROLE_FIT)
            self.WEIGHT_COMPANY_INTENT = custom_weights.get('company_intent', self.WEIGHT_COMPANY_INTENT)
            self.WEIGHT_TECH_FIT = custom_weights.get('tech_fit', self.WEIGHT_TECH_FIT)
            self.WEIGHT_NAMS = custom_weights.get('nams', self.WEIGHT_NAMS)
            self.WEIGHT_LOCATION = custom_weights.get('location', self.WEIGHT_LOCATION)
            self.WEIGHT_PUBLICATION = custom_weights.get('publication', self.WEIGHT_PUBLICATION)
            self.MAX_RAW_SCORE = sum([
                self.WEIGHT_ROLE_FIT, self.WEIGHT_COMPANY_INTENT,
                self.WEIGHT_TECH_FIT, self.WEIGHT_NAMS,
                self.WEIGHT_LOCATION, self.WEIGHT_PUBLICATION
            ])
    
    def score_lead(self, lead: Lead) -> ScoringResult:
        """Calculate propensity score for a single lead."""
        
        # Role Fit Score
        role_score = self.WEIGHT_ROLE_FIT if lead.has_relevant_title else 0
        
        # Company Intent Score (recent funding)
        company_score = 0
        if lead.company and lead.company.is_recently_funded:
            company_score = self.WEIGHT_COMPANY_INTENT
        
        # Technographic Score (uses in-vitro)
        tech_score = 0
        if lead.company and lead.company.uses_invitro_models:
            tech_score = self.WEIGHT_TECH_FIT
        
        # NAMs Score
        nams_score = 0
        if lead.company and lead.company.open_to_nams:
            nams_score = self.WEIGHT_NAMS
        
        # Location Score (biotech hub)
        location_score = 0
        if lead.company and lead.company.is_biotech_hub:
            location_score = self.WEIGHT_LOCATION
        
        # Publication Score (recent relevant paper)
        pub_score = self.WEIGHT_PUBLICATION if lead.has_recent_publications else 0
        
        # Calculate raw and normalized scores
        raw_score = (
            role_score + company_score + tech_score + 
            nams_score + location_score + pub_score
        )
        normalized_score = (raw_score / self.MAX_RAW_SCORE) * 100
        
        return ScoringResult(
            lead=lead,
            total_score=normalized_score,
            raw_score=raw_score,
            role_fit_score=role_score,
            company_intent_score=company_score,
            tech_fit_score=tech_score,
            nams_score=nams_score,
            location_score=location_score,
            publication_score=pub_score
        )
    
    def score_and_rank_leads(self, leads: List[Lead]) -> List[ScoringResult]:
        """Score all leads and sort by propensity (highest first)."""
        results = [self.score_lead(lead) for lead in leads]
        
        # Sort by total score descending
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        # Assign ranks
        for i, result in enumerate(results, start=1):
            result.rank = i
        
        return results
    
    @staticmethod
    def get_score_interpretation(score: float) -> str:
        """Get human-readable interpretation of score."""
        if score >= 80:
            return "🔥 Very High Priority"
        elif score >= 60:
            return "✅ High Priority"
        elif score >= 40:
            return "📊 Medium Priority"
        elif score >= 20:
            return "📋 Low Priority"
        else:
            return "⚪ Very Low Priority"
