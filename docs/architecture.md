# Enterprise Intelligence Platform Architecture

```mermaid
    U[Enterprise Users]

    subgraph FE[Frontend Layer]
        WEB[Web Dashboard]
        ADMIN[Admin Portal]
        CHAT[AI Assistant Interface]
    end

    subgraph API[Backend API Layer]
        GATEWAY[FastAPI API Gateway]
        AUTH[Authentication & Authorization]
        USERS[User & Organization Management]
        DOCS[Document Management]
        INTEL[Intelligence APIs]
        INTEGRATIONS[Integration APIs]
    end

    subgraph AI[AI Services Layer]
        ORCH[AI Orchestrator]
        RAG[RAG Pipeline]
        PROMPT[Prompt Management]
        CONTRACT[Legal Intelligence Module]
        EXEC[Executive Intelligence Module]
        MARKET[Market & Competitor Intelligence]
        RISK[Risk Intelligence]
    end

    subgraph DATA[Data & Knowledge Layer]
        PG[(PostgreSQL)]
        VECTOR[(Vector Database)]
        FILES[(Object / File Storage)]
        CACHE[(Redis Cache)]
    end

    subgraph SOURCES[Enterprise Data Sources]
        SQLSRC[Company SQL Systems]
        DRIVE[Google Drive / SharePoint]
        EMAIL[Outlook / Email]
        APIEXT[External APIs]
        WEBEXT[Regulations / News / Market Data]
        UPLOAD[Uploaded Documents]
    end

    subgraph MODELS[Model Providers]
        LLM[LLM API]
        EMBED[Embedding Model]
    end

    subgraph OPS[Infrastructure & Operations]
        DOCKER[Docker]
        NGINX[Nginx]
        LOGS[Logging & Monitoring]
        CICD[CI/CD]
    end

    U --> FE

    WEB --> GATEWAY
    ADMIN --> GATEWAY
    CHAT --> GATEWAY

    GATEWAY --> AUTH
    GATEWAY --> USERS
    GATEWAY --> DOCS
    GATEWAY --> INTEL
    GATEWAY --> INTEGRATIONS

    INTEL --> ORCH
    DOCS --> RAG
    ORCH --> RAG
    ORCH --> PROMPT
    ORCH --> CONTRACT
    ORCH --> EXEC
    ORCH --> MARKET
    ORCH --> RISK

    RAG --> VECTOR
    RAG --> FILES
    RAG --> EMBED
    ORCH --> LLM

    AUTH --> PG
    USERS --> PG
    DOCS --> PG
    INTEL --> PG
    GATEWAY --> CACHE

    INTEGRATIONS --> SQLSRC
    INTEGRATIONS --> DRIVE
    INTEGRATIONS --> EMAIL
    INTEGRATIONS --> APIEXT
    INTEGRATIONS --> WEBEXT
    DOCS --> UPLOAD

    SQLSRC --> PG
    DRIVE --> FILES
    EMAIL --> FILES
    APIEXT --> PG
    WEBEXT --> FILES
    UPLOAD --> FILES

    DOCKER --> GATEWAY
    DOCKER --> AI
    NGINX --> FE
    NGINX --> GATEWAY
    LOGS --> GATEWAY
    LOGS --> AI
    CICD --> DOCKER
    ```
