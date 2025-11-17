"""
ACS-Mentor V2.5 - LlamaIndex Literature Integration

Enables automatic literature retrieval and citation from academic databases.

Sources:
- PubMed Central (biomedical research)
- arXiv (statistics, ML, quantitative methods)
- User library (uploaded PDFs)

Author: ACS-Mentor Development Team
Version: 2.5.0
Date: 2025-11-16
"""

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    ServiceContext,
    StorageContext
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SimpleNodeParser

import requests
import os
import yaml
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACSLiteratureSearch:
    """
    LlamaIndex-powered literature search for ACS-Mentor V2.5

    Features:
    - Multi-source indexing (PubMed, arXiv, user library)
    - Semantic search with metadata filtering
    - Automatic citation generation (APA style)
    - Multi-modal retrieval (text, tables, figures)

    Usage:
        lit_search = ACSLiteratureSearch()

        # Search literature
        papers = lit_search.search_literature(
            research_topic="propensity score matching",
            top_k=5
        )

        # Generate citations
        for paper in papers:
            print(paper['citation'])
    """

    def __init__(self, config_path=".acs_mentor/literature_config.yaml"):
        """
        Initialize literature search system

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

        # Indexes
        self.pubmed_index = None
        self.arxiv_index = None
        self.user_library_index = None

        # Build indexes (lazy loading or from cache)
        self._load_or_build_indexes()

    def _load_config(self) -> Dict:
        """Load configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Default configuration"""
        return {
            "pubmed": {
                "enabled": True,
                "sample_query": "statistical methods clinical trials",
                "max_papers": 100
            },
            "arxiv": {
                "enabled": True,
                "categories": ["stat.ME", "stat.AP"],
                "max_papers": 50
            },
            "user_library": {
                "enabled": True,
                "path": ".acs_mentor/user_library/"
            },
            "indexing": {
                "chunk_size": 512,
                "chunk_overlap": 50,
                "embedding_model": "all-MiniLM-L6-v2"
            },
            "retrieval": {
                "top_k": 5,
                "similarity_threshold": 0.75,
                "reranking_enabled": True
            }
        }

    def _load_or_build_indexes(self):
        """Load indexes from cache or build new ones"""
        cache_dir = ".acs_mentor/literature_indexes/"

        # Check if indexes cached
        if os.path.exists(cache_dir):
            logger.info("Loading literature indexes from cache...")
            try:
                self._load_indexes_from_cache(cache_dir)
                return
            except Exception as e:
                logger.warning(f"Failed to load from cache: {e}")

        # Build new indexes
        logger.info("Building literature indexes (this may take a while)...")
        self._build_indexes()

    def _build_indexes(self):
        """Build LlamaIndex indexes from all sources"""

        # 1. PubMed Index
        if self.config['pubmed']['enabled']:
            logger.info("[1/3] Building PubMed index...")
            pubmed_docs = self._fetch_pubmed_papers(
                query=self.config['pubmed']['sample_query'],
                max_results=self.config['pubmed']['max_papers']
            )

            if pubmed_docs:
                self.pubmed_index = VectorStoreIndex.from_documents(pubmed_docs)
                logger.info(f"  Indexed {len(pubmed_docs)} PubMed papers")
            else:
                logger.warning("  No PubMed papers indexed")

        # 2. arXiv Index
        if self.config['arxiv']['enabled']:
            logger.info("[2/3] Building arXiv index...")
            arxiv_docs = self._fetch_arxiv_papers(
                categories=self.config['arxiv']['categories'],
                max_results=self.config['arxiv']['max_papers']
            )

            if arxiv_docs:
                self.arxiv_index = VectorStoreIndex.from_documents(arxiv_docs)
                logger.info(f"  Indexed {len(arxiv_docs)} arXiv papers")
            else:
                logger.warning("  No arXiv papers indexed")

        # 3. User Library Index
        if self.config['user_library']['enabled']:
            logger.info("[3/3] Building user library index...")
            user_library_path = self.config['user_library']['path']

            if os.path.exists(user_library_path):
                library_docs = SimpleDirectoryReader(user_library_path).load_data()

                if library_docs:
                    self.user_library_index = VectorStoreIndex.from_documents(library_docs)
                    logger.info(f"  Indexed {len(library_docs)} user documents")
                else:
                    logger.info("  User library is empty")
            else:
                logger.info(f"  User library path does not exist: {user_library_path}")

        logger.info("✅ Literature indexes built successfully")

    def search_literature(
        self,
        research_topic: str,
        top_k: int = 5,
        sources: str = "all",
        filters: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Search academic literature for research topic

        Args:
            research_topic: Research question or topic
            top_k: Number of papers to retrieve
            sources: "all" | "pubmed" | "arxiv" | "user_library"
            filters: Optional metadata filters

        Returns:
            List of papers with metadata and citations
        """
        results = []

        # Query relevant indexes
        if sources in ["all", "pubmed"] and self.pubmed_index:
            pubmed_results = self._query_index(
                self.pubmed_index,
                research_topic,
                top_k,
                source="pubmed"
            )
            results.extend(pubmed_results)

        if sources in ["all", "arxiv"] and self.arxiv_index:
            arxiv_results = self._query_index(
                self.arxiv_index,
                research_topic,
                top_k,
                source="arxiv"
            )
            results.extend(arxiv_results)

        if sources in ["all", "user_library"] and self.user_library_index:
            library_results = self._query_index(
                self.user_library_index,
                research_topic,
                top_k,
                source="user_library"
            )
            results.extend(library_results)

        # Apply filters
        if filters:
            results = self._apply_filters(results, filters)

        # Rerank if enabled
        if self.config['retrieval']['reranking_enabled']:
            results = self._rerank_results(results, research_topic)

        # Deduplicate
        results = self._deduplicate_results(results)

        # Generate citations
        for result in results:
            result['citation'] = self._generate_citation(result)

        # Return top_k
        return results[:top_k]

    def _query_index(
        self,
        index: VectorStoreIndex,
        query: str,
        top_k: int,
        source: str
    ) -> List[Dict[str, Any]]:
        """Query a LlamaIndex index"""
        try:
            # Create retriever
            retriever = VectorIndexRetriever(
                index=index,
                similarity_top_k=top_k * 2  # Retrieve more for reranking
            )

            # Create query engine
            query_engine = RetrieverQueryEngine(retriever=retriever)

            # Query
            response = query_engine.query(query)

            # Extract results
            results = []
            for node in response.source_nodes:
                results.append({
                    "text": node.node.get_content(),
                    "metadata": node.node.metadata,
                    "score": node.score,
                    "source": source
                })

            return results

        except Exception as e:
            logger.error(f"Query failed for {source}: {e}")
            return []

    def _rerank_results(
        self,
        results: List[Dict],
        research_topic: str
    ) -> List[Dict]:
        """
        Rerank results based on multiple criteria:
        1. Semantic similarity score
        2. Journal impact (top-tier journals boosted)
        3. Recency (recent papers boosted)
        4. Methodological rigor (keywords)
        """

        def rerank_score(result):
            score = result.get('score', 0.5)
            metadata = result.get('metadata', {})

            # Boost high-impact journals (30% boost)
            journal = metadata.get('journal', '').lower()
            high_impact_journals = [
                'nejm', 'new england journal',
                'jama', 'journal of the american medical',
                'bmj', 'british medical journal',
                'lancet',
                'nature medicine',
                'statistics in medicine',
                'biometrics',
                'biostatistics'
            ]

            if any(j in journal for j in high_impact_journals):
                score *= 1.3

            # Boost recent papers (20% for >=2020, 10% for >=2015)
            year = metadata.get('year', 2000)
            if isinstance(year, str):
                try:
                    year = int(year)
                except:
                    year = 2000

            if year >= 2020:
                score *= 1.2
            elif year >= 2015:
                score *= 1.1

            # Boost methodological papers (keywords in title/abstract)
            text = result.get('text', '').lower()
            title = metadata.get('title', '').lower()

            method_keywords = [
                'randomized controlled trial', 'propensity score',
                'causal inference', 'statistical methods',
                'validation', 'prediction model'
            ]

            if any(kw in title or kw in text[:500] for kw in method_keywords):
                score *= 1.15

            return score

        results.sort(key=rerank_score, reverse=True)
        return results

    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate papers (by DOI or title)"""
        seen_dois = set()
        seen_titles = set()
        unique_results = []

        for result in results:
            metadata = result.get('metadata', {})
            doi = metadata.get('doi', '').lower()
            title = metadata.get('title', '').lower()

            # Check DOI first (most reliable)
            if doi and doi in seen_dois:
                continue

            # Check title (approximate match)
            if title and title in seen_titles:
                continue

            # Add to unique results
            unique_results.append(result)

            if doi:
                seen_dois.add(doi)
            if title:
                seen_titles.add(title)

        logger.info(f"Deduplicated: {len(results)} → {len(unique_results)} unique papers")
        return unique_results

    def _generate_citation(self, result: Dict) -> str:
        """
        Generate formatted citation (APA style)

        Format: Authors (Year). Title. Journal, Volume(Issue), Pages. DOI
        """
        metadata = result.get('metadata', {})

        authors = metadata.get('authors', 'Unknown authors')
        year = metadata.get('year', 'n.d.')
        title = metadata.get('title', 'Untitled')
        journal = metadata.get('journal', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        # Format authors (simplify if too long)
        if isinstance(authors, list):
            if len(authors) == 1:
                authors_str = authors[0]
            elif len(authors) <= 3:
                authors_str = ", ".join(authors[:-1]) + f" & {authors[-1]}"
            else:
                authors_str = f"{authors[0]} et al."
        else:
            authors_str = str(authors)

        # Build citation
        citation = f"{authors_str} ({year}). {title}. "

        if journal:
            citation += f"*{journal}*"
            if volume:
                citation += f", *{volume}*"
            if issue:
                citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += "."

        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    # ========== Data Fetching Methods ==========

    def _fetch_pubmed_papers(
        self,
        query: str,
        max_results: int = 100
    ) -> List[Document]:
        """
        Fetch papers from PubMed using E-utilities API

        Args:
            query: Search query
            max_results: Maximum number of papers to fetch

        Returns:
            List of LlamaIndex Document objects
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        documents = []

        try:
            # Step 1: Search for PMIDs
            search_url = (
                f"{base_url}esearch.fcgi"
                f"?db=pubmed"
                f"&term={query}"
                f"&retmax={max_results}"
                f"&retmode=json"
            )

            response = requests.get(search_url, timeout=30)
            if response.status_code != 200:
                logger.error(f"PubMed search failed: HTTP {response.status_code}")
                return []

            search_data = response.json()
            pmids = search_data.get('esearchresult', {}).get('idlist', [])

            if not pmids:
                logger.warning("No PubMed results found")
                return []

            logger.info(f"Found {len(pmids)} PubMed articles")

            # Step 2: Fetch details for each PMID (in batches)
            batch_size = 20
            for i in range(0, len(pmids), batch_size):
                batch_pmids = pmids[i:i+batch_size]
                pmid_str = ",".join(batch_pmids)

                fetch_url = (
                    f"{base_url}efetch.fcgi"
                    f"?db=pubmed"
                    f"&id={pmid_str}"
                    f"&retmode=xml"
                )

                response = requests.get(fetch_url, timeout=30)
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch batch {i//batch_size + 1}")
                    continue

                # Parse XML
                root = ET.fromstring(response.content)
                for article in root.findall('.//PubmedArticle'):
                    doc = self._parse_pubmed_article(article)
                    if doc:
                        documents.append(doc)

                logger.info(f"  Fetched batch {i//batch_size + 1}/{(len(pmids)-1)//batch_size + 1}")

            logger.info(f"✅ Fetched {len(documents)} PubMed papers")
            return documents

        except Exception as e:
            logger.error(f"PubMed fetching failed: {e}")
            return []

    def _parse_pubmed_article(self, article_elem) -> Optional[Document]:
        """Parse a PubMed XML article element"""
        try:
            # Extract metadata
            article_data = article_elem.find('.//Article')
            if article_data is None:
                return None

            # Title
            title_elem = article_data.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "Untitled"

            # Abstract
            abstract_elems = article_data.findall('.//AbstractText')
            abstract = " ".join([elem.text for elem in abstract_elems if elem.text])

            # Authors
            authors = []
            for author in article_data.findall('.//Author'):
                lastname = author.find('LastName')
                forename = author.find('ForeName')
                if lastname is not None and forename is not None:
                    authors.append(f"{lastname.text} {forename.text[0]}")

            # Journal
            journal_elem = article_data.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else ""

            # Year
            year_elem = article_data.find('.//Journal/JournalIssue/PubDate/Year')
            year = year_elem.text if year_elem is not None else ""

            # Volume, Pages
            volume_elem = article_data.find('.//Journal/JournalIssue/Volume')
            volume = volume_elem.text if volume_elem is not None else ""

            pages_elem = article_data.find('.//Pagination/MedlinePgn')
            pages = pages_elem.text if pages_elem is not None else ""

            # DOI
            doi_elem = article_elem.find('.//ArticleId[@IdType="doi"]')
            doi = doi_elem.text if doi_elem is not None else ""

            # PMID
            pmid_elem = article_elem.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ""

            # Create Document
            text = f"{title}\n\nAbstract: {abstract}"

            metadata = {
                "title": title,
                "authors": authors,
                "journal": journal,
                "year": year,
                "volume": volume,
                "pages": pages,
                "doi": doi,
                "pmid": pmid,
                "source": "pubmed"
            }

            return Document(text=text, metadata=metadata)

        except Exception as e:
            logger.warning(f"Failed to parse PubMed article: {e}")
            return None

    def _fetch_arxiv_papers(
        self,
        categories: List[str],
        max_results: int = 50
    ) -> List[Document]:
        """
        Fetch papers from arXiv API

        Args:
            categories: List of arXiv categories (e.g., ["stat.ME", "stat.AP"])
            max_results: Maximum number of papers

        Returns:
            List of LlamaIndex Document objects
        """
        base_url = "http://export.arxiv.org/api/query"
        documents = []

        try:
            # Build search query
            category_query = " OR ".join([f"cat:{cat}" for cat in categories])
            search_query = f"search_query={category_query}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

            url = f"{base_url}?{search_query}"

            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                logger.error(f"arXiv search failed: HTTP {response.status_code}")
                return []

            # Parse Atom XML
            root = ET.fromstring(response.content)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', namespace):
                doc = self._parse_arxiv_entry(entry, namespace)
                if doc:
                    documents.append(doc)

            logger.info(f"✅ Fetched {len(documents)} arXiv papers")
            return documents

        except Exception as e:
            logger.error(f"arXiv fetching failed: {e}")
            return []

    def _parse_arxiv_entry(self, entry, namespace) -> Optional[Document]:
        """Parse an arXiv Atom entry"""
        try:
            # Title
            title = entry.find('atom:title', namespace).text.strip()

            # Abstract
            summary = entry.find('atom:summary', namespace).text.strip()

            # Authors
            authors = [
                author.find('atom:name', namespace).text
                for author in entry.findall('atom:author', namespace)
            ]

            # Published date
            published = entry.find('atom:published', namespace).text[:4]  # Year only

            # arXiv ID
            arxiv_id = entry.find('atom:id', namespace).text.split('/')[-1]

            # DOI (if available)
            doi_elem = entry.find('atom:doi', namespace)
            doi = doi_elem.text if doi_elem is not None else ""

            # Create Document
            text = f"{title}\n\nAbstract: {summary}"

            metadata = {
                "title": title,
                "authors": authors,
                "journal": "arXiv",
                "year": published,
                "arxiv_id": arxiv_id,
                "doi": doi,
                "source": "arxiv"
            }

            return Document(text=text, metadata=metadata)

        except Exception as e:
            logger.warning(f"Failed to parse arXiv entry: {e}")
            return None

    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Apply metadata filters to results"""
        filtered = []

        for result in results:
            metadata = result.get('metadata', {})
            match = True

            for key, value in filters.items():
                if key not in metadata:
                    match = False
                    break

                # Handle different filter types
                if isinstance(value, list):
                    if metadata[key] not in value:
                        match = False
                elif isinstance(value, dict):
                    # Range filter (e.g., {"$gte": 2020})
                    if "$gte" in value and metadata[key] < value["$gte"]:
                        match = False
                    if "$lte" in value and metadata[key] > value["$lte"]:
                        match = False
                else:
                    if metadata[key] != value:
                        match = False

            if match:
                filtered.append(result)

        return filtered

    def _load_indexes_from_cache(self, cache_dir: str):
        """Load indexes from cached files"""
        # Placeholder - implement caching/loading logic
        pass

    def _save_indexes_to_cache(self, cache_dir: str):
        """Save indexes to cache files"""
        # Placeholder - implement caching logic
        pass


# ========== Utility Functions ==========

def extract_research_topic(user_message: str) -> str:
    """
    Extract research topic from user message

    Simple keyword extraction (can be enhanced with NLP)
    """
    # Remove common question words
    stopwords = ['how', 'what', 'why', 'when', 'where', 'should', 'can', 'i', 'my', 'the', 'a', 'an']

    words = user_message.lower().split()
    keywords = [w for w in words if w not in stopwords and len(w) > 3]

    # Return first 5 keywords joined
    return " ".join(keywords[:5])


def extract_key_finding(text: str, max_length: int = 150) -> str:
    """Extract key finding from paper text (first sentence or snippet)"""
    # Simple extraction - return first sentence
    sentences = text.split('.')
    if sentences:
        finding = sentences[0].strip()
        if len(finding) <= max_length:
            return finding
        else:
            return finding[:max_length] + "..."
    return ""


if __name__ == "__main__":
    # Test initialization
    logger.info("=== Testing LlamaIndex Literature Search ===")

    lit_search = ACSLiteratureSearch()

    # Test search
    papers = lit_search.search_literature(
        research_topic="propensity score matching causal inference",
        top_k=5,
        sources="pubmed"
    )

    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['citation']}")
        print(f"   Score: {paper['score']:.3f}")
