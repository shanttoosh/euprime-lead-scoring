"""
PubMed API Integration - Real Scientific Publication Data.
Uses NCBI E-utilities API (free, no key required for basic use).

API Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25500/
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
import time

from ..models import Publication


class PubMedClient:
    """
    Client for querying PubMed database.
    
    Rate limits: 3 requests/second without API key
    With API key: 10 requests/second (optional, get from NCBI)
    """
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """
        Initialize PubMed client.
        
        Args:
            api_key: Optional NCBI API key for higher rate limits
            email: Optional email for NCBI to contact if issues
        """
        self.api_key = api_key
        self.email = email
    
    def _make_request(self, endpoint: str, params: dict) -> requests.Response:
        """Make request to PubMed API with rate limiting."""
        if self.api_key:
            params['api_key'] = self.api_key
        if self.email:
            params['email'] = self.email
        
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Rate limiting (be nice to NCBI)
        time.sleep(0.4)  # ~2.5 requests/second
        return response
    
    def search(
        self, 
        query: str, 
        max_results: int = 20,
        min_date: Optional[str] = None,
        max_date: Optional[str] = None
    ) -> List[str]:
        """
        Search PubMed and return PMIDs.
        
        Args:
            query: Search query (e.g., "drug-induced liver injury 3D model")
            max_results: Maximum number of results
            min_date: Start date (YYYY/MM/DD)
            max_date: End date (YYYY/MM/DD)
        
        Returns:
            List of PubMed IDs (PMIDs)
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': 'relevance'
        }
        
        if min_date:
            params['mindate'] = min_date
        if max_date:
            params['maxdate'] = max_date
        if min_date or max_date:
            params['datetype'] = 'pdat'  # Publication date
        
        response = self._make_request('esearch.fcgi', params)
        data = response.json()
        
        return data.get('esearchresult', {}).get('idlist', [])
    
    def fetch_details(self, pmids: List[str]) -> List[Publication]:
        """
        Fetch publication details for given PMIDs.
        
        Args:
            pmids: List of PubMed IDs
        
        Returns:
            List of Publication objects
        """
        if not pmids:
            return []
        
        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml'
        }
        
        response = self._make_request('efetch.fcgi', params)
        
        # Parse XML response
        publications = []
        root = ET.fromstring(response.content)
        
        for article in root.findall('.//PubmedArticle'):
            try:
                pub = self._parse_article(article)
                if pub:
                    publications.append(pub)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        
        return publications
    
    def _parse_article(self, article_elem) -> Optional[Publication]:
        """Parse XML article element into Publication object."""
        medline = article_elem.find('.//MedlineCitation')
        if medline is None:
            return None
        
        pmid_elem = medline.find('.//PMID')
        pmid = pmid_elem.text if pmid_elem is not None else ''
        
        article = medline.find('.//Article')
        if article is None:
            return None
        
        # Title
        title_elem = article.find('.//ArticleTitle')
        title = title_elem.text if title_elem is not None else 'Unknown Title'
        
        # Authors
        authors = []
        author_list = article.find('.//AuthorList')
        if author_list is not None:
            for author in author_list.findall('.//Author'):
                lastname = author.find('LastName')
                forename = author.find('ForeName')
                if lastname is not None:
                    name = lastname.text
                    if forename is not None:
                        name = f"{forename.text} {name}"
                    authors.append(name)
        
        # Journal
        journal_elem = article.find('.//Journal/Title')
        journal = journal_elem.text if journal_elem is not None else 'Unknown Journal'
        
        # Publication date
        pub_date = datetime.now()
        date_elem = article.find('.//PubDate')
        if date_elem is not None:
            year = date_elem.find('Year')
            month = date_elem.find('Month')
            day = date_elem.find('Day')
            
            try:
                year_val = int(year.text) if year is not None else datetime.now().year
                month_val = 1
                if month is not None:
                    # Month can be text like "Jan" or number
                    month_text = month.text
                    month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                                 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
                    month_val = month_map.get(month_text.lower()[:3], 1) if not month_text.isdigit() else int(month_text)
                day_val = int(day.text) if day is not None else 1
                pub_date = datetime(year_val, month_val, day_val)
            except (ValueError, AttributeError):
                pass
        
        # Keywords/MeSH terms
        keywords = []
        mesh_list = medline.find('.//MeshHeadingList')
        if mesh_list is not None:
            for mesh in mesh_list.findall('.//DescriptorName'):
                if mesh.text:
                    keywords.append(mesh.text)
        
        return Publication(
            title=title or 'Unknown Title',
            authors=authors[:5],  # Limit to first 5 authors
            journal=journal or 'Unknown Journal',
            pub_date=pub_date,
            pmid=f"PMID{pmid}",
            keywords=keywords[:10],  # Limit keywords
            is_corresponding_author=False  # Would need more parsing
        )
    
    def search_relevant_publications(
        self,
        author_name: Optional[str] = None,
        max_results: int = 10
    ) -> List[Publication]:
        """
        Search for publications relevant to 3D in-vitro models.
        
        Args:
            author_name: Optional author name to search
            max_results: Maximum publications to return
        
        Returns:
            List of Publication objects
        """
        # Build query for relevant topics
        base_terms = [
            '"drug-induced liver injury"',
            '"3D cell culture"',
            '"hepatic spheroid"',
            '"organ-on-chip"',
            '"in vitro toxicology"',
            '"microphysiological system"',
            '"hepatotoxicity model"'
        ]
        
        # Combine with OR for broader search
        query = ' OR '.join(base_terms)
        
        if author_name:
            # Search for specific author with relevant topics
            query = f'({query}) AND {author_name}[Author]'
        
        # Get papers from last 2 years
        two_years_ago = datetime.now().replace(year=datetime.now().year - 2)
        min_date = two_years_ago.strftime('%Y/%m/%d')
        
        pmids = self.search(query, max_results=max_results, min_date=min_date)
        
        if pmids:
            return self.fetch_details(pmids)
        return []


# Convenient function for quick searches
def search_pubmed_for_toxicology(max_results: int = 20) -> List[Publication]:
    """
    Quick search for recent toxicology/3D model publications.
    
    Returns:
        List of relevant publications
    """
    client = PubMedClient()
    return client.search_relevant_publications(max_results=max_results)


# Example usage
if __name__ == "__main__":
    print("Searching PubMed for relevant publications...")
    pubs = search_pubmed_for_toxicology(max_results=5)
    
    for pub in pubs:
        print(f"\n📄 {pub.title}")
        print(f"   Authors: {', '.join(pub.authors[:3])}")
        print(f"   Journal: {pub.journal}")
        print(f"   Date: {pub.pub_date.strftime('%Y-%m')}")
        print(f"   PMID: {pub.pmid}")
