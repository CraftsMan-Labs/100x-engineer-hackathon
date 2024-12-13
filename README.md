# 100x-engineer-hackathon# 100x Engineer: AI-Powered Market Intelligence Platform

🔗 [Live Demo](https://marketedgeagent.craftsmanlabs.net/)
📦 [Frontend Code Repository](https://github.com/CraftsMan-Labs/market-mind-scout)

## Overview

This project is an advanced AI-driven market intelligence platform designed to help businesses and entrepreneurs gain deep insights into market dynamics, customer needs, and strategic opportunities.

## Screenshots

### Market Intelligence Platform

![Market Intelligence Platform](screenshots/image.png)
_Transform your business decisions with AI-powered market insights and real-time competitor analysis_

## System Architecture

### Knowledge Storage and Retrieval

```mermaid
flowchart TD
    A[User Query] --> B{Query Router}

    %% RAG System with Pinecone
    B --> |Semantic Search| C[Pinecone RAG]
    C --> C1[Text Chunking]
    C1 --> C2[OpenAI Embeddings]
    C2 --> C3[Vector Storage]
    C3 --> C4[Similarity Search]

    %% Graph Database with Neo4j
    B --> |Relationship Query| D[Neo4j Graph DB]
    D --> D1[Memory Storage]
    D1 --> D2[Graph Relationships]
    D2 --> D3[Multi-dimensional Query]

    %% Integration Layer
    C4 & D3 --> E[Integrated Results]
    E --> F[AI Processing]
    F --> G[Actionable Insights]

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style G fill:#bbf,stroke:#333,stroke-width:4px
```

Our system leverages two powerful storage and retrieval mechanisms:

1. **Pinecone RAG (Retrieval-Augmented Generation)**

   - Automatic text chunking (500-word segments)
   - OpenAI embeddings (text-embedding-3-small model)
   - Vector similarity search
   - Efficient document retrieval with metadata

2. **Neo4j Graph Database**
   - Memory-based knowledge storage
   - Complex relationship mapping
   - Multi-dimensional querying capabilities
   - Temporal and contextual connections

This hybrid approach enables:

- Semantic search through vector embeddings
- Relationship-aware queries through graph traversal
- Combined insights from both structured and unstructured data

•⁠ ⁠[Detailed System Workflow](docs/workflow_visualizer/system_architecture.md)

## Product Workflow

```mermaid
flowchart TD
    %% System Entry Points
    A[User Input/Query] --> B{Query Type}

    %% Main Workflow Branches
    B --> |Market Analysis| C[Market Analysis Module]
    B --> |Customer Discovery| D[Customer Discovery Module]
    B --> |Market Expansion| E[Market Expansion Module]
    B --> |Product Evolution| F[Product Evolution Module]

    %% Market Analysis Workflow
    C --> MA1[Initialize Market Analyzer]
    MA1 --> MA2[Generate Search Queries]
    MA2 --> MA3[Search Internet via Jina/Exa APIs]
    MA3 --> MA4[Analyze Search Results]
    MA4 --> MA5[Breakdown Problem Space]
    MA5 --> MA6[Generate Trend Visualization]
    MA6 --> MA7[Compile Comprehensive Report]

    %% Customer Discovery Workflow
    D --> CD1[Initialize Customer Discoverer]
    CD1 --> CD2[Market Segmentation]
    CD2 --> CD3[Identify Target Niches]
    CD3 --> CD4[Create Ideal Customer Profile]
    CD4 --> CD5[Analyze Market Potential]

    %% Market Expansion Workflow
    E --> ME1[Analyze Current Market Position]
    ME1 --> ME2[Identify Expansion Domains]
    ME2 --> ME3[Evaluate Strategic Opportunities]
    ME3 --> ME4[Develop Expansion Strategy]

    %% Product Evolution Workflow
    F --> PE1[Collect Input Reports]
    PE1 --> PE2[Extract Key Market Insights]
    PE2 --> PE3[Generate Product Evolution Strategy]
    PE3 --> PE4[Define Product Phases]
    PE4 --> PE5[Create User Adoption Trend]
    PE5 --> PE6[Visualize Product Strategy]

    %% Shared AI Processing
    MA2 & CD2 & ME2 & PE2 --> AI[LLM Processing Center]
    AI --> LLM1[GPT-4o Model]
    LLM1 --> LLM2[Response Parsing]
    LLM2 --> LLM3[Structured Output Generation]

    %% Data Flow and Integration
    MA7 & CD5 & ME4 & PE6 --> G[Integrated Intelligence Report]

    %% Visualization and Endpoints
    G --> H[FastAPI Endpoints]
    H --> I[Frontend Visualization]

    %% Styling
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style I fill:#bbf,stroke:#333,stroke-width:4px
    style AI fill:#ff9,stroke:#333,stroke-width:2px
```

## Key Features

### 🔍 Market Analysis

•⁠ ⁠Comprehensive market research using advanced AI techniques
•⁠ ⁠Multi-source data aggregation and analysis
•⁠ ⁠Intelligent query breakdown and insight generation

### 🚀 Market Expansion

•⁠ ⁠Strategic market expansion recommendations
•⁠ ⁠Competitive landscape assessment
•⁠ ⁠Opportunity identification and prioritization

### 📈 Product Evolution

•⁠ ⁠Data-driven product evolution strategies
•⁠ ⁠Customer segment targeting
•⁠ ⁠Risk mitigation and success metrics tracking

## Backend Architecture

### Core Technologies

-⁠ ⁠*API Framework*: FastAPI
-⁠ ⁠*Authentication*: Supabase Auth
-⁠ ⁠*Primary Database*: Supabase PostgreSQL
-⁠ ⁠*Vector Database*: Pinecone
-⁠ ⁠*Graph Database*: Neo4j
-⁠ ⁠*Memory System*: Mem0
-⁠ ⁠*AI Integration*: LiteLLM, OpenAI
-⁠ ⁠*Search APIs*: Jina AI, Exa
-⁠ ⁠*Data Modeling*: Pydantic
-⁠ ⁠*API Documentation*: OpenAPI (Swagger)

### RAG (Retrieval Augmented Generation)

Our system implements three complementary RAG approaches:

1. **Vector RAG with Pinecone**
   - Document chunking and preprocessing
   - OpenAI embeddings generation
   - Semantic similarity search
   - Context-aware response generation
   - Metadata filtering and ranking

2. **Graph RAG with Neo4j**
   - Knowledge graph construction
   - Entity relationship mapping
   - Graph traversal queries
   - Context enrichment
   - Multi-hop reasoning

3. **Memory RAG with Mem0**
   - Semantic memory storage
   - Contextual memory retrieval
   - Memory-augmented responses
   - Long-term knowledge retention
   - Adaptive learning capabilities

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant FastAPI
    participant Supabase
    
    User->>Frontend: Login Request
    Frontend->>Supabase: Auth Request
    Supabase-->>Frontend: JWT Token
    Frontend->>FastAPI: API Request + JWT
    FastAPI->>Supabase: Verify Token
    Supabase-->>FastAPI: Token Valid
    FastAPI-->>Frontend: Protected Data
```

### Database Architecture

1. **Supabase PostgreSQL**
   - User profiles and preferences
   - Application state and configurations
   - Audit logs and analytics
   - Real-time subscriptions

2. **Pinecone Vector DB**
   - Document embeddings
   - Semantic search indices
   - Similarity matching
   - Dimension reduction

3. **Neo4j Graph DB**
   - Entity relationships
   - Knowledge graph
   - Contextual connections
   - Pattern matching

### API Documentation

![FastAPI Swagger UI](screenshots/fast_api_swagger.png)
_Interactive API documentation with Swagger UI_

### API Structure

```python
src/
├── app/
│   ├── routers/
│   │   ├── market_analysis.py
│   │   ├── customer_discovery.py
│   │   ├── market_expansion.py
│   │   ├── product_evolution.py
│   │   └── chat.py
│   ├── db.py          # Database connections
│   ├── auth.py        # Supabase authentication
│   ├── pinecone.py    # Vector store operations
│   ├── neo4j.py       # Graph operations
│   ├── mem0_client.py # Memory operations
│   └── main.py        # FastAPI application
```

## Getting Started

### Prerequisites

•⁠ ⁠Python 3.10+
•⁠ ⁠Poetry (dependency management)

### Installation

⁠ bash
git clone https://github.com/yourusername/100x-engineer.git
cd 100x-engineer
poetry install
 ⁠

### Environment Configuration

Create a ⁠ .env ⁠ file with the following variables:
•⁠ ⁠⁠ OPENAI_API_KEY ⁠
•⁠ ⁠⁠ JINA_API_KEY ⁠
•⁠ ⁠⁠ EXA_API_KEY ⁠

### Running the Application

1. **Start the Backend Server**
   ```bash
   # Start FastAPI server
   uvicorn src.app.main:app --reload --port 8000
   ```

2. **Access the API Documentation**
   - Open http://localhost:8000/docs for Swagger UI
   - Open http://localhost:8000/redoc for ReDoc

3. **Run Tests**
   ```bash
   # Run all tests
   pytest
   
   # Run with coverage report
   pytest --cov=src
   ```

## Core Modules

•⁠ ⁠*Customer Discovery*: Advanced customer segmentation

•⁠ ⁠*Market Analysis*: Comprehensive market research

•⁠ ⁠*Market Expansion*: Strategic growth recommendations

•⁠ ⁠*Product Evolution*: Data-driven product strategy

For detailed product analysis and market insights, check out our:

- [Comprehensive Market Analysis Report](sample_comprehensive_reports/FINAL_REPORT.md)
- [Sample Reports Collection](sample_comprehensive_reports/)

## Workflow Visualizations

Detailed workflow diagrams are available to understand the internal processes of our core modules:

### 📊 Workflow Visualizers

•⁠ ⁠[Customer Discovery Workflow](docs/workflow_visualizer/customer_discovery.md)

•⁠ ⁠[Market Analysis Workflow](docs/workflow_visualizer/market_analyser.md)

•⁠ ⁠[Market Expansion Workflow](docs/workflow_visualizer/market_expansion.md)

•⁠ ⁠[Product Evolution Workflow](docs/workflow_visualizer/product_evolution.md)

•⁠ ⁠[Competitive Analysis Workflow](docs/workflow_visualizer/competitive_analysis.md)

These Mermaid-based flowcharts provide insights into the AI-driven processes powering our intelligent market research platform.

## Contributing

1.⁠ ⁠Fork the repository
2.⁠ ⁠Create your feature branch (⁠ git checkout -b feature/AmazingFeature ⁠)
3.⁠ ⁠Commit your changes (⁠ git commit -m 'Add some AmazingFeature' ⁠)
4.⁠ ⁠Push to the branch (⁠ git push origin feature/AmazingFeature ⁠)
5.⁠ ⁠Open a Pull Request

## License

Distributed under the MIT License. See ⁠ LICENSE ⁠ for more information.

## Contact

- Rishub C R - rishub@craftsmanlabs.net - https://www.linkedin.com/in/rishub-c-r/ - Craftsmanlabs.net
- Nazim Girach - https://www.linkedin.com/in/nazim-girach/
- Irshad Girach - https://www.linkedin.com/in/irshad-girach-42b88a189/
- Ammar Khatri - https://www.linkedin.com/in/ammar-khatri-458544211/

## Application Screenshots

### Dashboard Overview

![Dashboard](screenshots/image_1.png)
_Real-time market intelligence dashboard with key metrics and global prospect heatmap_

### Competitor Analysis

![Competitor Analysis](screenshots/image_2.png)
_Detailed competitor mapping with market share and SWOT analysis_

### Strategic Planning

![Strategic Insights](screenshots/image_3.png)
_Strategic insights dashboard showing growth opportunities and market trends_

### AI Chat Assistant

![Chat Assistant](screenshots/imag4.png)
_AI-powered chat assistant for real-time market insights_

### Audience Analytics

![Audience Insights](screenshots/image_5.png)
_Detailed audience demographics and platform engagement metrics_

### Performance Analytics

![Data Analytics](screenshots/image_6.png)
_Comprehensive performance metrics and trend analysis_

### Custom Reporting

![Custom Report](screenshots/image_7.png)
_Customizable reporting with growth trends and key business insights_
