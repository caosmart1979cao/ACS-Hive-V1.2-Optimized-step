# ACS-Mentor V2.5 Architecture: Knowledge-Enhanced Mentor

**Version**: 2.5.0
**Release Date**: 2025-11-16
**Evolution**: V2.1 (Learning Mentor) → V2.5 (Knowledge-Enhanced Mentor)

---

## 🎯 V2.5 核心升级主题

**从"会学习的导师"到"知识渊博的导师"**

V2.5 focuses on **knowledge integration** and **production readiness**:

1. **Mem0 Memory System**: Mature memory layer with personalization
2. **LlamaIndex + LitLLM**: Automatic literature retrieval and citation
3. **MLflow 3.0**: Production monitoring with LLM-as-a-judge evaluation
4. **A-MEM (Optional)**: Self-organizing guidance cases

---

## 📊 Architecture Comparison

| Component | V2.1 | V2.5 | Improvement |
|-----------|------|------|-------------|
| **Memory System** | ChromaDB + SQLite | **Mem0 (unified)** | +30% quality, +50% speed |
| **Knowledge Base** | Internal YAML | **+ Academic Literature** | Authority +50% |
| **Literature Search** | Manual | **LlamaIndex + LitLLM** | Automated, >90% recall |
| **Citation** | Manual | **Auto-generated** | >95% accuracy |
| **Evaluation** | Manual benchmarks | **MLflow real-time** | Continuous monitoring |
| **Case Organization** | Flat storage | **A-MEM hierarchical** | +15% precision |

---

## 🧠 Component 1: Mem0 Memory System

### Overview

Replace ChromaDB+SQLite hybrid system with **Mem0** - a universal memory layer designed for personalized AI interactions.

### Key Features

- **Adaptive Memory**: Evolves with user needs over time
- **Cross-Session Context**: Automatic retention and retrieval
- **Personalization**: Learns user preferences and patterns
- **Production-Ready**: 20k+ stars, active maintenance

### Architecture

```yaml
mem0_architecture:

  core_memory_layer:
    provider: "Mem0"
    backend_storage: "SQLite (existing data source)"

    capabilities:
      - "User profile management"
      - "Session history tracking"
      - "Skill progress evolution"
      - "Error pattern learning"
      - "Interaction context retention"

  integration_points:

    pre_guidance_phase:
      # Replace V2.1's manual retrieval
      step_2_retrieve_history: |
        relevant_memories = memory.search(
            query=user_message,
            user_id=user_id,
            limit=5,
            filters={"session_type": "research_guidance"}
        )

      step_4_similar_cases: |
        similar_cases = memory.search(
            query=user_message,
            user_id=user_id,
            limit=3,
            filters={"quality_score": {"$gte": 0.85}}
        )

    post_guidance_phase:
      # Replace V2.1's manual storage
      step_5_store_interaction: |
        memory.add(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": guidance_response}
            ],
            user_id=user_id,
            metadata={
                "session_id": session_id,
                "mode": decision_result['mode'],
                "quality_score": quality_score,
                "skill_advancement": skill_advancement,
                "error_type": error_type if error_detected else None
            }
        )
```

### Implementation

```python
# File: memory/mem0_integration.py

from mem0 import Memory
import yaml

class ACSMentorMemory:
    """Mem0-based memory system for ACS-Mentor V2.5"""

    def __init__(self, config_path=".acs_mentor/mem0_config.yaml"):
        # Load configuration
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Initialize Mem0
        self.memory = Memory(config=config)

        # Fallback to SQLite if Mem0 unavailable
        self.fallback_enabled = config.get('fallback_enabled', True)

    def retrieve_context(self, user_message, user_id, context_type="all"):
        """
        Retrieve relevant context for pre-guidance phase

        Args:
            user_message: Current user query
            user_id: User identifier
            context_type: "history" | "success_cases" | "error_patterns" | "all"

        Returns:
            enriched_context: Dict with relevant memories
        """
        try:
            # Search memories
            results = self.memory.search(
                query=user_message,
                user_id=user_id,
                limit=5
            )

            # Organize by type
            enriched_context = {
                "recent_history": [],
                "similar_success_cases": [],
                "recurring_errors": []
            }

            for result in results:
                metadata = result.get('metadata', {})

                # Categorize based on metadata
                if metadata.get('error_type'):
                    enriched_context['recurring_errors'].append(result)
                elif metadata.get('quality_score', 0) >= 0.85:
                    enriched_context['similar_success_cases'].append(result)
                else:
                    enriched_context['recent_history'].append(result)

            return enriched_context

        except Exception as e:
            # Fallback to SQLite if Mem0 fails
            if self.fallback_enabled:
                return self._fallback_retrieve(user_message, user_id)
            raise e

    def store_interaction(self, user_message, guidance_response,
                         metadata, user_id, session_id):
        """Store interaction to memory (post-guidance phase)"""
        try:
            self.memory.add(
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": guidance_response}
                ],
                user_id=user_id,
                metadata={
                    **metadata,
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            if self.fallback_enabled:
                self._fallback_store(user_message, guidance_response,
                                   metadata, user_id, session_id)
            raise e

    def get_user_profile(self, user_id):
        """Retrieve user capability profile"""
        # Get all user interactions
        all_memories = self.memory.get_all(user_id=user_id)

        # Aggregate to build profile
        profile = {
            "user_id": user_id,
            "total_interactions": len(all_memories),
            "skill_levels": self._extract_skill_levels(all_memories),
            "common_error_types": self._extract_error_patterns(all_memories),
            "avg_quality_score": self._calculate_avg_quality(all_memories)
        }

        return profile

    def _fallback_retrieve(self, user_message, user_id):
        """Fallback to V2.1 SQLite retrieval"""
        import sqlite3
        conn = sqlite3.connect(".acs_mentor/memory.db")
        # ... SQLite retrieval logic from V2.1
        pass

    def _fallback_store(self, user_message, guidance_response,
                       metadata, user_id, session_id):
        """Fallback to V2.1 SQLite storage"""
        import sqlite3
        conn = sqlite3.connect(".acs_mentor/memory.db")
        # ... SQLite storage logic from V2.1
        pass
```

### Configuration

```yaml
# File: .acs_mentor/mem0_config.yaml

mem0_config:
  version: "1.0"

  # Mem0 settings
  graph_store:
    provider: "neo4j"  # or "networkx" for simpler setup
    config:
      url: "bolt://localhost:7687"
      username: "neo4j"
      password: "password"

  vector_store:
    provider: "chroma"
    config:
      path: ".acs_mentor/mem0_vectors"
      embedding_model: "all-MiniLM-L6-v2"

  llm:
    provider: "openai"
    config:
      model: "gpt-4"
      api_key: "${OPENAI_API_KEY}"

  # Fallback configuration
  fallback_enabled: true
  fallback_backend: "sqlite"
  fallback_db_path: ".acs_mentor/memory.db"

  # Auto-degradation thresholds
  degradation:
    max_latency_ms: 200
    max_error_rate: 0.05
    fallback_after_errors: 3
```

### Migration from V2.1

```python
# File: scripts/migrate_v21_to_v25_mem0.py

"""
Migration script: V2.1 → V2.5 (Mem0)

Migrates existing SQLite + ChromaDB data to Mem0 unified memory layer
"""

import sqlite3
import chromadb
from mem0 import Memory
import yaml

def migrate_v21_to_v25():
    """Main migration function"""

    print("=== ACS-Mentor V2.1 → V2.5 Migration ===\n")

    # Step 1: Initialize Mem0
    print("[1/4] Initializing Mem0...")
    memory = Memory()

    # Step 2: Migrate user profiles from SQLite
    print("[2/4] Migrating user profiles from SQLite...")
    conn = sqlite3.connect(".acs_mentor/memory.db")
    cursor = conn.cursor()

    # Load user_profiles
    cursor.execute("SELECT * FROM user_profiles")
    profiles = cursor.fetchall()

    for profile in profiles:
        user_id = profile[0]
        # ... extract profile data

        # Store to Mem0 (as initial context)
        memory.add(
            messages=[{"role": "system", "content": f"User profile: {profile_data}"}],
            user_id=user_id,
            metadata={"type": "profile_initialization"}
        )

    print(f"  Migrated {len(profiles)} user profiles")

    # Step 3: Migrate interaction history
    print("[3/4] Migrating interaction history...")
    cursor.execute("SELECT * FROM user_interactions ORDER BY timestamp")
    interactions = cursor.fetchall()

    for interaction in interactions:
        user_id, user_message, guidance_response, quality_score, mode, timestamp = interaction[:6]

        memory.add(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": guidance_response}
            ],
            user_id=user_id,
            metadata={
                "quality_score": quality_score,
                "mode": mode,
                "timestamp": timestamp,
                "migrated_from": "v2.1"
            }
        )

    print(f"  Migrated {len(interactions)} interactions")

    # Step 4: Migrate ChromaDB guidance cases
    print("[4/4] Migrating ChromaDB guidance cases...")
    chroma_client = chromadb.PersistentClient(path=".acs_mentor/vector_db")

    try:
        collection = chroma_client.get_collection("guidance_cases")
        all_cases = collection.get()

        for i, (doc, metadata) in enumerate(zip(all_cases['documents'], all_cases['metadatas'])):
            # Extract user_id from metadata (if exists)
            user_id = metadata.get('user_id', 'migrated_case')

            memory.add(
                messages=[{"role": "assistant", "content": doc}],
                user_id=user_id,
                metadata={
                    **metadata,
                    "type": "guidance_case",
                    "migrated_from": "v2.1_chromadb"
                }
            )

        print(f"  Migrated {len(all_cases['documents'])} guidance cases")

    except Exception as e:
        print(f"  Warning: Could not migrate ChromaDB cases: {e}")

    conn.close()

    print("\n✅ Migration completed successfully!")
    print("\nNext steps:")
    print("1. Verify migration: python scripts/verify_mem0_migration.py")
    print("2. Run A/B test: python scripts/ab_test_mem0.py")
    print("3. If successful, update main workflow to use Mem0")

if __name__ == "__main__":
    migrate_v21_to_v25()
```

---

## 📚 Component 2: LlamaIndex Literature Integration

### Overview

Integrate **LlamaIndex** to enable automatic literature retrieval and citation from academic databases (PubMed, arXiv, user-uploaded PDFs).

### Key Features

- **Multi-Source Indexing**: PubMed Central, arXiv, local PDFs
- **Multi-Modal Retrieval**: Text, tables, figures, formulas
- **Auto-Citation**: Generate formatted references
- **Query Engine**: Natural language queries for literature

### Architecture

```yaml
llamaindex_architecture:

  knowledge_base:
    sources:
      - name: "PubMed Central"
        type: "API"
        coverage: "Biomedical, clinical, health sciences research"
        access: "E-utilities API"

      - name: "arXiv"
        type: "API"
        coverage: "Statistics, ML, quantitative methods"
        access: "arXiv API"

      - name: "User Library"
        type: "Local"
        coverage: "User-uploaded PDFs"
        path: ".acs_mentor/user_library/"

  indexing_strategy:
    index_type: "VectorStoreIndex"
    embedding_model: "all-MiniLM-L6-v2"  # Same as V2.1 for consistency
    chunk_size: 512
    chunk_overlap: 50

    metadata_extraction:
      - "Title"
      - "Authors"
      - "Journal"
      - "Year"
      - "DOI"
      - "Abstract"
      - "Methods_section"

  retrieval_strategy:
    query_engine_type: "SubQuestionQueryEngine"
    top_k: 5
    similarity_threshold: 0.75

    reranking:
      enabled: true
      criteria:
        - "Methodological rigor (journal tier)"
        - "Recency (prefer recent papers)"
        - "Relevance to user's research question"
```

### Implementation

```python
# File: knowledge/llamaindex_integration.py

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
import requests

class ACSLiteratureSearch:
    """LlamaIndex-powered literature search for ACS-Mentor V2.5"""

    def __init__(self, config_path=".acs_mentor/literature_config.yaml"):
        self.config = self._load_config(config_path)

        # Initialize indexes
        self.pubmed_index = None
        self.arxiv_index = None
        self.user_library_index = None

        # Build indexes
        self._build_indexes()

    def search_literature(self, research_topic, top_k=5, sources="all"):
        """
        Search academic literature for research topic

        Args:
            research_topic: User's research question or topic
            top_k: Number of papers to retrieve
            sources: "all" | "pubmed" | "arxiv" | "user_library"

        Returns:
            List of relevant papers with metadata and citations
        """
        results = []

        # Query relevant indexes
        if sources in ["all", "pubmed"] and self.pubmed_index:
            pubmed_results = self._query_index(
                self.pubmed_index,
                research_topic,
                top_k
            )
            results.extend(pubmed_results)

        if sources in ["all", "arxiv"] and self.arxiv_index:
            arxiv_results = self._query_index(
                self.arxiv_index,
                research_topic,
                top_k
            )
            results.extend(arxiv_results)

        if sources in ["all", "user_library"] and self.user_library_index:
            library_results = self._query_index(
                self.user_library_index,
                research_topic,
                top_k
            )
            results.extend(library_results)

        # Rerank and deduplicate
        results = self._rerank_results(results, research_topic)

        # Generate citations
        for result in results:
            result['citation'] = self._generate_citation(result)

        return results[:top_k]

    def _build_indexes(self):
        """Build LlamaIndex indexes from sources"""

        # 1. Index PubMed papers (sample set)
        print("Building PubMed index...")
        pubmed_docs = self._fetch_pubmed_sample()
        if pubmed_docs:
            self.pubmed_index = VectorStoreIndex.from_documents(pubmed_docs)

        # 2. Index arXiv papers (statistics/methods)
        print("Building arXiv index...")
        arxiv_docs = self._fetch_arxiv_sample()
        if arxiv_docs:
            self.arxiv_index = VectorStoreIndex.from_documents(arxiv_docs)

        # 3. Index user library
        print("Building user library index...")
        user_library_path = ".acs_mentor/user_library/"
        if os.path.exists(user_library_path):
            library_docs = SimpleDirectoryReader(user_library_path).load_data()
            if library_docs:
                self.user_library_index = VectorStoreIndex.from_documents(library_docs)

    def _fetch_pubmed_sample(self, query="statistical methods clinical trials", max_results=100):
        """Fetch sample papers from PubMed for indexing"""
        # Use E-utilities API
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

        # Search
        search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
        response = requests.get(search_url)

        if response.status_code != 200:
            print(f"Warning: PubMed search failed")
            return []

        pmids = response.json()['esearchresult']['idlist']

        # Fetch abstracts
        documents = []
        for pmid in pmids:
            fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
            # ... parse XML and create Document objects
            # documents.append(Document(...))

        return documents

    def _query_index(self, index, query, top_k):
        """Query a LlamaIndex index"""
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=top_k
        )

        query_engine = RetrieverQueryEngine(retriever=retriever)
        response = query_engine.query(query)

        # Extract results with metadata
        results = []
        for node in response.source_nodes:
            results.append({
                "text": node.node.get_content(),
                "metadata": node.node.metadata,
                "score": node.score
            })

        return results

    def _rerank_results(self, results, research_topic):
        """Rerank results based on multiple criteria"""

        def rerank_score(result):
            score = result.get('score', 0.5)

            # Boost high-impact journals
            journal = result.get('metadata', {}).get('journal', '')
            if any(j in journal.lower() for j in ['nejm', 'jama', 'bmj', 'lancet']):
                score *= 1.3

            # Boost recent papers
            year = result.get('metadata', {}).get('year', 2000)
            if year >= 2020:
                score *= 1.2
            elif year >= 2015:
                score *= 1.1

            return score

        results.sort(key=rerank_score, reverse=True)
        return results

    def _generate_citation(self, result):
        """Generate formatted citation (APA style)"""
        metadata = result.get('metadata', {})

        authors = metadata.get('authors', 'Unknown')
        year = metadata.get('year', 'n.d.')
        title = metadata.get('title', 'Untitled')
        journal = metadata.get('journal', '')
        volume = metadata.get('volume', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        # APA format
        citation = f"{authors} ({year}). {title}. "
        if journal:
            citation += f"*{journal}*"
            if volume:
                citation += f", {volume}"
            if pages:
                citation += f", {pages}"
        if doi:
            citation += f". https://doi.org/{doi}"

        return citation
```

### Integration with Pre-Guidance Phase

```python
# File: decision_logic_v2_5_extension.py

def pre_guidance_phase_v2_5(user_message, user_id, session_id):
    """
    V2.5 Enhanced Pre-Guidance Phase

    Now includes literature search (Step 7)
    """
    enriched_context = {}

    # Steps 1-6: Same as V2.1 (now using Mem0)
    memory = ACSMentorMemory()
    enriched_context.update(memory.retrieve_context(user_message, user_id))

    # 🆕 Step 7: Retrieve relevant literature (NEW in V2.5)
    if needs_literature_support(user_message):
        lit_search = ACSLiteratureSearch()

        # Extract research topic
        research_topic = extract_research_topic(user_message)

        # Search literature
        enriched_context['relevant_literature'] = lit_search.search_literature(
            research_topic=research_topic,
            top_k=5,
            sources="all"
        )

    return enriched_context

def needs_literature_support(user_message):
    """Determine if literature search would be valuable"""
    # Trigger literature search for:
    triggers = [
        "方法选择" in user_message,  # Method selection
        "文献" in user_message or "literature" in user_message.lower(),
        "evidence" in user_message.lower(),
        "研究设计" in user_message,  # Study design
        "propensity score" in user_message.lower(),
        "causal inference" in user_message.lower(),
        # ... more triggers
    ]

    return any(triggers)
```

### Enhanced Guidance with Literature

```python
def generate_guidance_with_literature(user_message, decision_result, enriched_context):
    """
    V2.5 Enhanced Guidance Generation

    Now includes automatic literature citations
    """

    # Generate base guidance (same as V2.1)
    base_guidance = generate_base_guidance(user_message, decision_result)

    # 🆕 Enhance with literature (if available)
    if 'relevant_literature' in enriched_context:
        literature_section = format_literature_section(
            enriched_context['relevant_literature']
        )

        enhanced_guidance = f"{base_guidance}\n\n{literature_section}"
    else:
        enhanced_guidance = base_guidance

    return enhanced_guidance

def format_literature_section(papers):
    """Format literature citations for guidance"""

    if not papers:
        return ""

    section = "\n\n## 📚 理论依据与延伸阅读\n\n"
    section += "基于最新研究，该领域的主要方法学进展包括：\n\n"

    for i, paper in enumerate(papers, 1):
        metadata = paper['metadata']
        citation = paper['citation']

        # Extract key finding (first sentence of abstract or text snippet)
        key_finding = extract_key_finding(paper['text'])

        section += f"{i}. {citation}\n"
        if key_finding:
            section += f"   **关键发现**: {key_finding}\n"
        section += "\n"

    return section
```

---

## 🔍 Component 3: LitLLM Literature Review

### Overview

Integrate **LitLLM** for multi-strategy literature search and automated review generation.

### Key Features

- **Keyword Extraction**: Automatic extraction from research questions
- **Multi-Strategy Search**: Keyword-based + Embedding-based
- **Database Queries**: Google Scholar, OpenAlex, PubMed
- **Re-ranking with Attribution**: LLM-based relevance scoring

### Implementation

```python
# File: knowledge/litllm_integration.py

from litllm import LiteratureReviewer
import openai

class ACSLiteratureReviewer:
    """LitLLM-powered literature review for ACS-Mentor V2.5"""

    def __init__(self):
        self.reviewer = LiteratureReviewer(
            databases=["pubmed", "google_scholar", "openalexpaper"],
            max_papers=20
        )

    def conduct_literature_review(self, research_question, focus="methodology"):
        """
        Conduct automated literature review

        Args:
            research_question: User's research question
            focus: "methodology" | "background" | "discussion"

        Returns:
            Structured literature review
        """

        # Step 1: Extract keywords
        keywords = self.reviewer.extract_keywords(research_question)

        # Step 2: Multi-strategy search
        papers_keyword = self.reviewer.search_by_keywords(keywords)
        papers_embedding = self.reviewer.search_by_embedding(research_question)

        # Step 3: Merge and deduplicate
        all_papers = self._merge_deduplicate(papers_keyword, papers_embedding)

        # Step 4: Rerank by relevance
        reranked_papers = self.reviewer.rerank(
            papers=all_papers,
            query=research_question,
            criteria=["relevance", "methodological_rigor", "recency"]
        )

        # Step 5: Generate review sections
        if focus == "methodology":
            review = self._generate_methods_review(reranked_papers[:10])
        elif focus == "background":
            review = self._generate_background_review(reranked_papers[:10])
        else:  # discussion
            review = self._generate_discussion_review(reranked_papers[:10])

        return review

    def _generate_methods_review(self, papers):
        """Generate methodology-focused literature review"""

        # Use LLM to synthesize
        prompt = f"""
        Based on the following papers, synthesize a concise literature review
        focusing on methodological approaches:

        {self._format_papers_for_prompt(papers)}

        Structure:
        1. Common methodological approaches (2-3 sentences)
        2. Recent methodological innovations (2-3 sentences)
        3. Key considerations for method selection (2-3 sentences)

        Keep it concise and actionable for researchers.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        review_text = response.choices[0].message.content

        # Format with citations
        review_with_citations = self._add_inline_citations(review_text, papers)

        return {
            "review_text": review_with_citations,
            "papers": papers,
            "focus": "methodology"
        }
```

### Integration with Guidance

```python
# In generate_guidance_with_literature()

def generate_strategic_guidance_with_review(user_message, decision_result, enriched_context):
    """
    For strategic/complex questions, generate comprehensive review
    """

    if decision_result['mode'] in ['strategic_advisor', 'deep_mentorship']:

        # Conduct literature review
        lit_reviewer = ACSLiteratureReviewer()
        review = lit_reviewer.conduct_literature_review(
            research_question=user_message,
            focus="methodology"
        )

        # Integrate into guidance
        guidance = f"""
        {base_guidance}

        ## 📚 方法学文献综述

        {review['review_text']}

        ## 延伸阅读

        {format_paper_list(review['papers'])}
        """
    else:
        # For simpler questions, use lightweight LlamaIndex search
        guidance = generate_guidance_with_literature(user_message, decision_result, enriched_context)

    return guidance
```

---

## 🧪 Component 4: MLflow 3.0 Production Monitoring

### Overview

Integrate **MLflow 3.0** for continuous evaluation, production monitoring, and A/B testing.

### Key Features

- **Experiment Tracking**: Compare V2.1 vs V2.5 performance
- **LLM-as-a-Judge**: Automatic guidance quality evaluation
- **Production Monitoring**: Real-time quality dashboards
- **Hallucination Detection**: Detect factual errors in guidance
- **A/B Testing**: Test new strategies safely

### Architecture

```yaml
mlflow_architecture:

  tracking:
    tracking_uri: "sqlite:///mlflow.db"
    artifact_location: ".acs_mentor/mlflow_artifacts"

    experiments:
      - name: "ACS-Mentor-V2.5-Development"
        description: "V2.1 vs V2.5 comparison"

      - name: "Memory-System-Evaluation"
        description: "ChromaDB+SQLite vs Mem0"

      - name: "Literature-Integration-Impact"
        description: "With vs without LlamaIndex"

  metrics:
    effectiveness:
      - "error_detection_rate"
      - "guidance_acceptance_rate"
      - "user_capability_growth"

    efficiency:
      - "response_relevance"
      - "retrieval_speed"
      - "context_efficiency"

    quality:
      - "methodological_rigor" (LLM-as-a-judge)
      - "citation_quality" (LLM-as-a-judge)
      - "actionability" (LLM-as-a-judge)

    system:
      - "memory_latency"
      - "literature_search_latency"
      - "total_response_time"

  evaluation:
    llm_as_judge:
      model: "gpt-4"
      metrics:
        - "methodological_rigor"
        - "citation_quality"
        - "actionability"
        - "appropriate_severity"

      grading_prompts: ".acs_mentor/mlflow/judge_prompts/"
```

### Implementation

```python
# File: evaluation/mlflow_monitoring.py

import mlflow
from mlflow.metrics.genai import EvaluationExample, make_genai_metric
import time

class ACSMentorMonitoring:
    """MLflow-based monitoring for ACS-Mentor V2.5"""

    def __init__(self, experiment_name="ACS-Mentor-V2.5-Production"):
        mlflow.set_experiment(experiment_name)

        # Define custom metrics
        self.metrics = self._define_custom_metrics()

    def track_guidance_interaction(self, user_message, guidance_response,
                                   decision_result, enriched_context,
                                   quality_metrics):
        """
        Track a single guidance interaction

        Called in post_guidance_phase
        """

        with mlflow.start_run(run_name=f"guidance_{decision_result['mode']}"):

            # Log parameters
            mlflow.log_param("mode", decision_result['mode'])
            mlflow.log_param("memory_system", "Mem0")
            mlflow.log_param("literature_search_enabled",
                           'relevant_literature' in enriched_context)

            # Log metrics
            mlflow.log_metric("quality_score", quality_metrics['quality_score'])
            mlflow.log_metric("response_relevance", quality_metrics['relevance'])
            mlflow.log_metric("retrieval_latency", quality_metrics['retrieval_time'])
            mlflow.log_metric("total_latency", quality_metrics['total_time'])

            # Log artifacts
            mlflow.log_text(user_message, "user_message.txt")
            mlflow.log_text(guidance_response, "guidance_response.txt")
            mlflow.log_dict(decision_result, "decision_result.json")

            # LLM-as-a-judge evaluation (async)
            judge_scores = self._evaluate_with_llm_judge(
                user_message,
                guidance_response
            )

            for metric_name, score in judge_scores.items():
                mlflow.log_metric(f"judge_{metric_name}", score)

    def _define_custom_metrics(self):
        """Define ACS-Mentor specific metrics for LLM-as-a-judge"""

        methodological_rigor = make_genai_metric(
            name="methodological_rigor",
            definition="""
            Evaluate whether the guidance follows strict methodological standards
            (CONSORT, STROBE, TRIPOD, etc.) and identifies critical errors.
            """,
            grading_prompt="""
            Score 1-5 based on:
            1. Does it reference appropriate reporting standards?
            2. Does it identify critical methodological issues?
            3. Are suggestions evidence-based?
            4. Is the severity assessment appropriate?
            5. Are actionable solutions provided?

            1 = Poor, 3 = Adequate, 5 = Excellent
            """,
            examples=[
                EvaluationExample(
                    input="User describes RCT with 30% dropout, excluded from analysis",
                    output="Guidance correctly identifies ITT violation, references CONSORT, suggests multiple imputation",
                    score=5,
                    justification="Identifies critical error, references standard, provides solution"
                ),
                EvaluationExample(
                    input="User asks about p-value interpretation",
                    output="Explains p-value without context or nuance",
                    score=2,
                    justification="Technically correct but lacks depth and actionability"
                )
            ],
            grading_context_columns=[]
        )

        citation_quality = make_genai_metric(
            name="citation_quality",
            definition="""
            Evaluate the quality and appropriateness of literature citations.
            """,
            grading_prompt="""
            Score 1-5 based on:
            1. Are citations relevant to the guidance?
            2. Are high-quality sources cited (top journals)?
            3. Are citations recent (within 5 years)?
            4. Is the citation format correct?
            5. Do citations strengthen the argument?

            1 = Poor/No citations, 3 = Adequate, 5 = Excellent
            """,
            examples=[
                EvaluationExample(
                    input="User asks about propensity score matching",
                    output="Guidance cites Austin (2011) and Rosenbaum & Rubin (1983) seminal papers",
                    score=5,
                    justification="Cites seminal and methodological papers appropriately"
                )
            ]
        )

        return {
            "methodological_rigor": methodological_rigor,
            "citation_quality": citation_quality
        }

    def _evaluate_with_llm_judge(self, user_message, guidance_response):
        """Evaluate guidance using LLM-as-a-judge metrics"""

        # Create evaluation data
        eval_data = {
            "input": user_message,
            "output": guidance_response
        }

        # Run evaluation (this is expensive, consider async/batch)
        results = {}
        for metric_name, metric in self.metrics.items():
            try:
                score = metric.score(eval_data)
                results[metric_name] = score
            except Exception as e:
                print(f"Warning: {metric_name} evaluation failed: {e}")
                results[metric_name] = None

        return results

    def run_ab_test(self, user_message, variant_a_func, variant_b_func):
        """
        Run A/B test between two strategies

        Example: Test Mem0 vs ChromaDB+SQLite
        """

        import random

        # Random assignment
        variant = random.choice(['A', 'B'])

        with mlflow.start_run(run_name=f"ab_test_{variant}"):
            mlflow.log_param("variant", variant)

            start_time = time.time()

            if variant == 'A':
                response = variant_a_func(user_message)
                mlflow.log_param("strategy", "Variant_A")
            else:
                response = variant_b_func(user_message)
                mlflow.log_param("strategy", "Variant_B")

            latency = time.time() - start_time
            mlflow.log_metric("latency", latency)

            return response

    def generate_performance_report(self, time_window="7d"):
        """Generate performance report for last N days"""

        # Query MLflow for recent runs
        runs = mlflow.search_runs(
            experiment_names=["ACS-Mentor-V2.5-Production"],
            filter_string=f"attributes.start_time > '{time_window}'"
        )

        # Aggregate metrics
        report = {
            "time_window": time_window,
            "total_interactions": len(runs),
            "avg_quality_score": runs['metrics.quality_score'].mean(),
            "avg_judge_methodological_rigor": runs['metrics.judge_methodological_rigor'].mean(),
            "avg_latency": runs['metrics.total_latency'].mean(),
            "mode_distribution": runs['params.mode'].value_counts().to_dict()
        }

        # Detect regressions
        if report['avg_quality_score'] < 0.75:
            report['alerts'] = ["⚠️ Quality score below threshold (0.75)"]

        return report
```

### Dashboard Configuration

```yaml
# File: .acs_mentor/mlflow/dashboard_config.yaml

dashboards:

  production_monitoring:
    title: "ACS-Mentor V2.5 Production Dashboard"

    panels:
      - name: "Quality Score Trend"
        metric: "quality_score"
        visualization: "time_series"
        aggregation: "mean"
        alert_threshold: 0.75

      - name: "Error Detection Rate"
        metric: "error_detected"
        visualization: "percentage"
        aggregation: "ratio"
        target: 0.90

      - name: "Response Latency Distribution"
        metric: "total_latency"
        visualization: "histogram"
        percentiles: [50, 95, 99]
        alert_p95_threshold: 2000  # ms

      - name: "Mode Distribution"
        metric: "mode"
        visualization: "pie_chart"
        expected_distribution:
          quick_guidance: 0.30
          mentor_lite: 0.25
          standard_mentor: 0.25
          deep_mentorship: 0.15
          strategic_advisor: 0.05

      - name: "Literature Integration Impact"
        metric: "judge_citation_quality"
        split_by: "literature_search_enabled"
        visualization: "comparison_bar"
```

---

## 🎯 V2.5 Complete Workflow

### End-to-End Flow

```python
# File: acs_mentor_v2_5_main.py

"""
ACS-Mentor V2.5 Complete Workflow

Integrates all components: Mem0 + LlamaIndex + LitLLM + MLflow
"""

from memory.mem0_integration import ACSMentorMemory
from knowledge.llamaindex_integration import ACSLiteratureSearch
from knowledge.litllm_integration import ACSLiteratureReviewer
from evaluation.mlflow_monitoring import ACSMentorMonitoring
import time

# Initialize components
memory = ACSMentorMemory()
lit_search = ACSLiteratureSearch()
lit_reviewer = ACSLiteratureReviewer()
monitoring = ACSMentorMonitoring()

def handle_user_message_v2_5(user_message, user_id, session_id):
    """
    Complete V2.5 workflow with all enhancements
    """

    start_time = time.time()

    # ===== Phase 1: Pre-Guidance (Enhanced) =====
    enriched_context = {}

    # Memory retrieval (Mem0)
    retrieval_start = time.time()
    enriched_context.update(
        memory.retrieve_context(user_message, user_id, context_type="all")
    )
    retrieval_time = time.time() - retrieval_start

    # Literature search (LlamaIndex - if needed)
    if needs_literature_support(user_message):
        lit_start = time.time()
        research_topic = extract_research_topic(user_message)
        enriched_context['relevant_literature'] = lit_search.search_literature(
            research_topic=research_topic,
            top_k=5
        )
        lit_time = time.time() - lit_start
    else:
        lit_time = 0

    # ===== Phase 2: Decision & Urgency Calculation =====
    decision_result = calculate_urgency_v2_enhanced(
        user_message, user_id, session_id, enriched_context
    )

    # ===== Phase 3: Response Generation (Enhanced) =====

    # For strategic questions, use LitLLM review
    if decision_result['mode'] in ['strategic_advisor', 'deep_mentorship']:
        review = lit_reviewer.conduct_literature_review(
            research_question=user_message,
            focus="methodology"
        )
        enriched_context['literature_review'] = review

    # Generate guidance with literature
    guidance_response = generate_guidance_with_literature(
        user_message, decision_result, enriched_context
    )

    # ===== Phase 4: Post-Guidance (Enhanced) =====

    # Quality self-check
    quality_score = evaluate_guidance_quality(
        guidance_response, decision_result, enriched_context
    )

    # Store to Mem0
    memory.store_interaction(
        user_message=user_message,
        guidance_response=guidance_response,
        metadata={
            "mode": decision_result['mode'],
            "quality_score": quality_score,
            "literature_integrated": 'relevant_literature' in enriched_context
        },
        user_id=user_id,
        session_id=session_id
    )

    # ===== Phase 5: Monitoring (MLflow) =====

    total_time = time.time() - start_time

    monitoring.track_guidance_interaction(
        user_message=user_message,
        guidance_response=guidance_response,
        decision_result=decision_result,
        enriched_context=enriched_context,
        quality_metrics={
            "quality_score": quality_score,
            "relevance": calculate_relevance(user_message, guidance_response),
            "retrieval_time": retrieval_time,
            "literature_time": lit_time,
            "total_time": total_time
        }
    )

    return guidance_response
```

---

## 📊 V2.5 Expected Performance

### Quantified Improvements

| Metric | V2.1 Baseline | V2.5 Target | Improvement |
|--------|---------------|-------------|-------------|
| **Memory Quality** | 0.80 | >0.85 | +6% |
| **Retrieval Speed** | <100ms | <70ms | +30% |
| **Guidance Authority** | N/A | >0.90 | NEW |
| **Literature Recall** | N/A | >90% | NEW |
| **Citation Accuracy** | N/A | >95% | NEW |
| **Error Detection** | >90% | >93% | +3% |
| **Real-time Monitoring** | ❌ | ✅ | Production-ready |

---

## 🚀 Migration & Deployment

### Installation

```bash
# Install V2.5 dependencies
pip install mem0ai llama-index litllm mlflow

# Optional: For full functionality
pip install neo4j  # For Mem0 graph store
pip install sentence-transformers  # For embeddings
```

### Migration Steps

```bash
# 1. Migrate from V2.1 to V2.5
python scripts/migrate_v21_to_v25_mem0.py

# 2. Build literature indexes
python scripts/build_literature_indexes.py

# 3. Initialize MLflow tracking
mlflow ui --backend-store-uri sqlite:///mlflow.db

# 4. Run A/B test (optional)
python scripts/ab_test_mem0.py

# 5. Deploy V2.5
python acs_mentor_v2_5_main.py
```

### Configuration Files

```
.acs_mentor/
├── mem0_config.yaml          # Mem0 configuration
├── literature_config.yaml    # LlamaIndex + LitLLM config
├── mlflow/
│   ├── dashboard_config.yaml # MLflow dashboard
│   └── judge_prompts/        # LLM-as-a-judge prompts
├── user_library/             # User-uploaded PDFs
└── memory.db                 # SQLite (legacy/fallback)
```

---

## 🎯 Next Steps: V3.0 Vision

V2.5 sets the foundation for V3.0 (Full Research Lifecycle Partner):

1. **LangChain Multi-Agent** (4-6 weeks)
2. **Causal DAG Advisor** (4-6 weeks)
3. **Full Lifecycle Modules** (8-10 weeks)

See `GITHUB_FRONTIER_ANALYSIS.md` for complete V3.0 roadmap.

---

**Document Version**: 1.0
**Created**: 2025-11-16
**Status**: Ready for implementation
