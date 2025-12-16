"""
Mock Data Generator for Lead Scoring Demo.
Generates realistic biotech/pharma leads for demonstration.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List

from ..models import Lead, Company, Publication


# Biotech companies with funding data (inspired by real data)
MOCK_COMPANIES = [
    Company(
        name="Iambic Therapeutics",
        domain="iambic.ai",
        hq_location="San Diego, CA",
        country="USA",
        funding_round="Series B",
        funding_amount_usd=100_000_000,
        funding_date=datetime(2025, 11, 11),
        investors=["Sequoia", "Alexandria Ventures", "ARK"],
        lead_investor="Sequoia",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=15
    ),
    Company(
        name="Neros Technologies",
        domain="neros.tech",
        hq_location="Cambridge, MA",
        country="USA",
        funding_round="Series B",
        funding_amount_usd=75_000_000,
        funding_date=datetime(2025, 11, 11),
        investors=["Sequoia Capital", "Vy Capital"],
        lead_investor="Sequoia Capital",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=23
    ),
    Company(
        name="Insitro",
        domain="insitro.com",
        hq_location="South San Francisco, CA",
        country="USA",
        funding_round="Series C",
        funding_amount_usd=400_000_000,
        funding_date=datetime(2024, 3, 15),
        investors=["a16z", "GV", "ARCH Venture Partners"],
        lead_investor="a16z",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=45
    ),
    Company(
        name="Recursion Pharmaceuticals",
        domain="recursion.com",
        hq_location="Salt Lake City, UT",
        country="USA",
        funding_round="Series D",
        funding_amount_usd=239_000_000,
        funding_date=datetime(2023, 8, 20),
        investors=["SoftBank", "Baillie Gifford"],
        lead_investor="SoftBank",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=30
    ),
    Company(
        name="Evotec",
        domain="evotec.com",
        hq_location="Hamburg, Germany",
        country="Germany",
        funding_round="Public",
        funding_amount_usd=0,
        funding_date=None,
        investors=[],
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="B",
        tech_roles_count=20
    ),
    Company(
        name="Mimetas",
        domain="mimetas.com",
        hq_location="Leiden, Netherlands",
        country="Netherlands",
        funding_round="Series B",
        funding_amount_usd=25_000_000,
        funding_date=datetime(2024, 6, 10),
        investors=["Life Sciences Partners", "Merck Ventures"],
        lead_investor="Life Sciences Partners",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="B",
        tech_roles_count=8
    ),
    Company(
        name="Cypre Bio",
        domain="cyprebio.com",
        hq_location="San Francisco, CA",
        country="USA",
        funding_round="Series A",
        funding_amount_usd=15_000_000,
        funding_date=datetime(2025, 2, 28),
        investors=["DCVC", "8VC"],
        lead_investor="DCVC",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="B",
        tech_roles_count=5
    ),
    Company(
        name="Hubrecht Organoid Technology",
        domain="huborganoid.com",
        hq_location="Utrecht, Netherlands",
        country="Netherlands",
        funding_round="Series A",
        funding_amount_usd=12_000_000,
        funding_date=datetime(2024, 9, 15),
        investors=["EQT Life Sciences"],
        lead_investor="EQT Life Sciences",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="C",
        tech_roles_count=3
    ),
    Company(
        name="Pfizer",
        domain="pfizer.com",
        hq_location="New York, NY",
        country="USA",
        funding_round="Public",
        funding_amount_usd=0,
        funding_date=None,
        investors=[],
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=200
    ),
    Company(
        name="Roche",
        domain="roche.com",
        hq_location="Basel, Switzerland",
        country="Switzerland",
        funding_round="Public",
        funding_amount_usd=0,
        funding_date=None,
        investors=[],
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=150
    ),
    Company(
        name="Novartis",
        domain="novartis.com",
        hq_location="Basel, Switzerland",
        country="Switzerland",
        funding_round="Public",
        funding_amount_usd=0,
        funding_date=None,
        investors=[],
        uses_invitro_models=True,
        open_to_nams=False,
        hiring_tier="A",
        tech_roles_count=180
    ),
    Company(
        name="BioNova Therapeutics",
        domain="bionovathx.com",
        hq_location="Boston, MA",
        country="USA",
        funding_round="Series A",
        funding_amount_usd=35_000_000,
        funding_date=datetime(2025, 1, 15),
        investors=["Atlas Venture", "Flagship Pioneering"],
        lead_investor="Atlas Venture",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="B",
        tech_roles_count=12
    ),
    Company(
        name="ToxSafe Labs",
        domain="toxsafelabs.com",
        hq_location="Cambridge, UK",
        country="UK",
        funding_round="Seed",
        funding_amount_usd=5_000_000,
        funding_date=datetime(2025, 4, 20),
        investors=["Oxford Sciences Innovation"],
        lead_investor="Oxford Sciences Innovation",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="C",
        tech_roles_count=4
    ),
    Company(
        name="HepatoCell Inc",
        domain="hepatocell.com",
        hq_location="San Diego, CA",
        country="USA",
        funding_round="Series B",
        funding_amount_usd=45_000_000,
        funding_date=datetime(2024, 11, 5),
        investors=["Frazier Healthcare", "OrbiMed"],
        lead_investor="Frazier Healthcare",
        uses_invitro_models=True,
        open_to_nams=True,
        hiring_tier="A",
        tech_roles_count=18
    ),
    Company(
        name="Generic Biotech Startup",
        domain="genericbio.com",
        hq_location="Austin, TX",
        country="USA",
        funding_round="",
        funding_amount_usd=0,
        funding_date=None,
        investors=[],
        uses_invitro_models=False,
        open_to_nams=False,
        hiring_tier="C",
        tech_roles_count=2
    ),
]

# Job titles for biotech professionals
SENIOR_TITLES = [
    "Director of Toxicology",
    "Head of Preclinical Safety",
    "VP of Safety Assessment",
    "Director of Drug Safety",
    "Head of In Vitro Sciences",
    "Director of ADME-Tox",
    "Chief Scientific Officer",
    "VP of Preclinical Development",
    "Director of Hepatic Research",
    "Head of 3D Cell Culture",
    "Director of Investigative Toxicology",
    "VP of Nonclinical Development",
    "Principal Scientist, Toxicology",
    "Senior Director of Safety Sciences",
    "Head of New Approach Methodologies",
]

JUNIOR_TITLES = [
    "Scientist, Toxicology",
    "Research Associate",
    "Lab Technician",
    "Junior Scientist",
    "Postdoctoral Fellow",
    "Research Scientist",
    "Associate Scientist",
    "Staff Scientist",
]

# Sample publication titles
RELEVANT_PUBLICATIONS = [
    "Drug-Induced Liver Injury Assessment Using 3D Hepatic Spheroids",
    "Novel In Vitro Model for Hepatotoxicity Screening",
    "Organ-on-Chip Technology for Predictive Toxicology",
    "Three-Dimensional Cell Culture Models in Drug Discovery",
    "Microphysiological Systems for ADME-Tox Assessment",
    "Hepatic Organoids for Drug Safety Evaluation",
    "New Approach Methodologies in Regulatory Toxicology",
    "In Vitro-In Vivo Extrapolation for Hepatotoxicity Prediction",
    "3D Liver Models for DILI Risk Assessment",
    "Investigative Toxicology: From 2D to 3D Systems",
]

IRRELEVANT_PUBLICATIONS = [
    "Marketing Strategies in Pharmaceutical Industry",
    "Supply Chain Optimization for Drug Manufacturing",
    "Clinical Trial Design Best Practices",
    "Patent Landscape Analysis in Biotech",
]

# Names generator
FIRST_NAMES = [
    "Sarah", "Michael", "Jennifer", "David", "Emily", "James", "Jessica", 
    "Robert", "Amanda", "William", "Ashley", "Christopher", "Stephanie",
    "Daniel", "Nicole", "Matthew", "Elizabeth", "Andrew", "Megan", "Joshua",
    "Hans", "Maria", "Pierre", "Yuki", "Priya", "Wei", "Carlos", "Anna",
]

LAST_NAMES = [
    "Chen", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
    "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor",
    "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Müller", "Schmidt", "Tanaka", "Patel", "Kumar", "Wang", "Kim", "Park",
]

LOCATIONS = [
    "Boston, MA", "Cambridge, MA", "San Francisco, CA", "San Diego, CA",
    "New York, NY", "New Jersey, NJ", "Basel, Switzerland", "London, UK",
    "Cambridge, UK", "Oxford, UK", "Munich, Germany", "Paris, France",
    "Remote - Texas", "Remote - Colorado", "Remote - Florida",
    "Seattle, WA", "Chicago, IL", "Philadelphia, PA", "Research Triangle, NC",
]


def generate_publication(relevant: bool = True) -> Publication:
    """Generate a mock publication."""
    titles = RELEVANT_PUBLICATIONS if relevant else IRRELEVANT_PUBLICATIONS
    
    pub_date = datetime.now() - timedelta(days=random.randint(30, 800))
    
    return Publication(
        title=random.choice(titles),
        authors=[f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" 
                 for _ in range(random.randint(2, 5))],
        journal=random.choice([
            "Toxicological Sciences", "Drug Metabolism and Disposition",
            "Chemical Research in Toxicology", "Archives of Toxicology",
            "Toxicology In Vitro", "ALTEX", "Lab on a Chip"
        ]),
        pub_date=pub_date,
        pmid=f"PMID{random.randint(30000000, 39999999)}",
        keywords=["hepatotoxicity", "3D models", "in vitro"] if relevant else ["marketing"],
        is_corresponding_author=random.choice([True, False])
    )


def generate_mock_lead(
    company: Company,
    senior: bool = True,
    has_publications: bool = False
) -> Lead:
    """Generate a single mock lead."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    title = random.choice(SENIOR_TITLES if senior else JUNIOR_TITLES)
    location = random.choice(LOCATIONS)
    
    email = f"{first_name.lower()}.{last_name.lower()}@{company.domain}"
    linkedin = f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(1000, 9999)}"
    
    publications = []
    if has_publications:
        # 1-3 relevant publications
        num_pubs = random.randint(1, 3)
        publications = [generate_publication(relevant=True) for _ in range(num_pubs)]
    
    return Lead(
        id=str(uuid.uuid4()),
        name=name,
        title=title,
        person_location=location,
        email=email,
        linkedin_url=linkedin,
        phone=f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        company=company,
        publications=publications,
        years_in_role=random.randint(1, 15)
    )


def generate_mock_leads(count: int = 50) -> List[Lead]:
    """Generate a diverse set of mock leads for demo."""
    leads = []
    
    # Generate leads with varying profiles to demonstrate scoring
    for company in MOCK_COMPANIES:
        # High-value leads: senior + publications
        num_high = random.randint(1, 3)
        for _ in range(num_high):
            leads.append(generate_mock_lead(company, senior=True, has_publications=True))
        
        # Medium leads: senior without publications
        num_medium = random.randint(1, 2)
        for _ in range(num_medium):
            leads.append(generate_mock_lead(company, senior=True, has_publications=False))
        
        # Lower leads: junior scientists
        num_low = random.randint(0, 2)
        for _ in range(num_low):
            leads.append(generate_mock_lead(company, senior=False, has_publications=False))
    
    # Shuffle and limit
    random.shuffle(leads)
    return leads[:count]


# Pre-generate some leads for quick access
MOCK_LEADS = generate_mock_leads(75)
