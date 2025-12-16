"""
Data models for the Lead Scoring Agent.
Defines Lead, Company, and ScoringResult dataclasses.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class Company:
    """Company information for lead enrichment."""
    name: str
    domain: str
    hq_location: str
    country: str
    funding_round: Optional[str] = None
    funding_amount_usd: Optional[int] = None
    funding_date: Optional[datetime] = None
    investors: List[str] = field(default_factory=list)
    lead_investor: Optional[str] = None
    uses_invitro_models: bool = False
    open_to_nams: bool = False  # New Approach Methodologies
    hiring_tier: str = "C"  # A, B, C
    tech_roles_count: int = 0
    careers_url: Optional[str] = None
    
    @property
    def is_recently_funded(self) -> bool:
        """Check if funded within last 2 years with Series A/B."""
        if not self.funding_round or not self.funding_date:
            return False
        valid_rounds = ['series a', 'series b', 'seed']
        if self.funding_round.lower() not in valid_rounds:
            return False
        days_since_funding = (datetime.now() - self.funding_date).days
        return days_since_funding <= 730  # 2 years
    
    @property
    def is_biotech_hub(self) -> bool:
        """Check if HQ is in major biotech hub."""
        hubs = [
            'boston', 'cambridge', 'ma', 'massachusetts',
            'san francisco', 'bay area', 'south san francisco', 'ca',
            'basel', 'switzerland',
            'oxford', 'cambridge uk', 'london', 'uk golden triangle',
            'san diego', 'new jersey', 'nj'
        ]
        location_lower = self.hq_location.lower()
        return any(hub in location_lower for hub in hubs)


@dataclass
class Publication:
    """Scientific publication data from PubMed."""
    title: str
    authors: List[str]
    journal: str
    pub_date: datetime
    pmid: str
    keywords: List[str] = field(default_factory=list)
    is_corresponding_author: bool = False
    
    @property
    def is_relevant(self) -> bool:
        """Check if publication is relevant to 3D in-vitro models."""
        relevant_terms = [
            'dili', 'drug-induced liver injury', 'hepatotoxicity',
            '3d cell culture', 'organ-on-chip', 'hepatic spheroid',
            'in vitro', 'investigative toxicology', 'microphysiological',
            'organoid', 'liver model', 'toxicity screening'
        ]
        text = f"{self.title} {' '.join(self.keywords)}".lower()
        return any(term in text for term in relevant_terms)


@dataclass 
class Lead:
    """Individual lead/person data."""
    id: str
    name: str
    title: str
    person_location: str  # Where they live/work (may be remote)
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[Company] = None
    publications: List[Publication] = field(default_factory=list)
    years_in_role: int = 0
    
    @property
    def has_relevant_title(self) -> bool:
        """Check if title indicates decision-maker in toxicology/safety."""
        relevant_keywords = [
            'toxicology', 'toxicologist', 'safety', 'preclinical',
            'hepatic', '3d', 'in vitro', 'invitro', 'adme',
            'pharmacology', 'drug safety', 'nonclinical'
        ]
        relevant_levels = [
            'director', 'head', 'vp', 'vice president', 
            'chief', 'principal', 'senior', 'lead', 'manager'
        ]
        title_lower = self.title.lower()
        has_keyword = any(kw in title_lower for kw in relevant_keywords)
        has_level = any(lvl in title_lower for lvl in relevant_levels)
        return has_keyword and has_level
    
    @property
    def has_recent_publications(self) -> bool:
        """Check for relevant publications in last 2 years."""
        cutoff = datetime.now().replace(year=datetime.now().year - 2)
        return any(
            pub.is_relevant and pub.pub_date >= cutoff 
            for pub in self.publications
        )


@dataclass
class ScoringResult:
    """Detailed scoring breakdown for a lead."""
    lead: Lead
    total_score: float  # 0-100 normalized
    raw_score: float    # Raw weighted sum
    
    # Individual signal scores
    role_fit_score: float = 0.0      # max +30
    company_intent_score: float = 0.0  # max +20
    tech_fit_score: float = 0.0      # max +15
    nams_score: float = 0.0          # max +10
    location_score: float = 0.0      # max +10
    publication_score: float = 0.0   # max +40
    
    rank: int = 0
    
    @property
    def score_breakdown(self) -> str:
        """Human-readable score breakdown."""
        parts = []
        if self.role_fit_score > 0:
            parts.append(f"Role:+{int(self.role_fit_score)}")
        if self.company_intent_score > 0:
            parts.append(f"Funding:+{int(self.company_intent_score)}")
        if self.tech_fit_score > 0:
            parts.append(f"Tech:+{int(self.tech_fit_score)}")
        if self.nams_score > 0:
            parts.append(f"NAMs:+{int(self.nams_score)}")
        if self.location_score > 0:
            parts.append(f"Location:+{int(self.location_score)}")
        if self.publication_score > 0:
            parts.append(f"Pub:+{int(self.publication_score)}")
        return ", ".join(parts) if parts else "No signals"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for DataFrame/export."""
        return {
            'Rank': self.rank,
            'Probability (%)': round(self.total_score, 1),
            'Name': self.lead.name,
            'Title': self.lead.title,
            'Company': self.lead.company.name if self.lead.company else '',
            'Person Location': self.lead.person_location,
            'HQ Location': self.lead.company.hq_location if self.lead.company else '',
            'Email': self.lead.email or '',
            'LinkedIn': self.lead.linkedin_url or '',
            'Score Breakdown': self.score_breakdown,
            'Raw Score': self.raw_score,
            'Role Score': self.role_fit_score,
            'Funding Score': self.company_intent_score,
            'Tech Score': self.tech_fit_score,
            'NAMs Score': self.nams_score,
            'Location Score': self.location_score,
            'Publication Score': self.publication_score
        }
