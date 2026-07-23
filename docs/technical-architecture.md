# Enterprise Intelligence Platform Technical Architecture

## 1. Purpose

This document defines the technical architecture and source-code organization of the Enterprise Intelligence Platform.

The architecture is designed to support:

- Enterprise document management
- Nested folders and bulk document ingestion
- Retrieval-Augmented Generation (RAG)
- Multi-agent AI workflows
- Multiple intelligence domains
- Background processing
- External enterprise integrations
- Multi-tenant data isolation
- Independent and testable application layers

The platform should remain modular, production-ready, and easy to extend.

---

## 2. Architecture Principles

The platform follows these principles:

### Separation of Concerns

Each part of the application has one clear responsibility.

For example:

- API routes receive HTTP requests.
- Services contain business logic.
- Repositories communicate with the database.
- RAG components retrieve knowledge.
- Agents perform reasoning and coordination.
- Workers execute long-running background tasks.

### Modular Design

Each major feature is organized into an independent module.

Examples:

- Authentication
- Documents
- Document collections
- Ingestion
- Conversations
- Intelligence
- RAG
- Agents

### Dependency Direction

Higher-level layers may depend on lower-level abstractions, but database and infrastructure details should not control business logic.

The standard request flow is:

```text
Client
↓
API Router
↓
Service
↓
Repository
↓
Database
```

### Deterministic Processing Before Agent Reasoning

Predictable operations should use normal backend services.

Examples:

- Reading a PDF
- Extracting text
- Splitting text into chunks
- Generating embeddings
- Saving records
- Updating processing status

Agents should be used only for tasks that require reasoning, decision-making, tool selection, or coordination.

### Multi-Tenant Isolation

Organization-specific data must be isolated using:

```text
organization_id
```

The authenticated user's organization context must be applied throughout the API, service, repository, RAG, and agent layers.

---

## 3. Repository Structure

```text
Enterprise-intelligence-platform/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── router.py
│   │   │   │   │
│   │   │   │   ├── auth/
│   │   │   │   │   ├── router.py
│   │   │   │   │   └── dependencies.py
│   │   │   │   │
│   │   │   │   ├── users/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── organizations/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── documents/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── collections/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── ingestion/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── conversations/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   ├── intelligence/
│   │   │   │   │   └── router.py
│   │   │   │   │
│   │   │   │   └── health/
│   │   │   │       └── router.py
│   │   │   │
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   ├── exceptions.py
│   │   │   └── constants.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   │
│   │   ├── models/
│   │   │   ├── organization.py
│   │   │   ├── user.py
│   │   │   ├── organization_membership.py
│   │   │   ├── intelligence_module.py
│   │   │   ├── document_collection.py
│   │   │   ├── document.py
│   │   │   ├── document_chunk.py
│   │   │   ├── ingestion_job.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── ai_run.py
│   │   │   ├── ai_source.py
│   │   │   ├── integration.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── document.py
│   │   │   ├── document_collection.py
│   │   │   ├── ingestion.py
│   │   │   ├── conversation.py
│   │   │   └── intelligence.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── base.py
│   │   │   ├── user_repository.py
│   │   │   ├── organization_repository.py
│   │   │   ├── document_repository.py
│   │   │   ├── collection_repository.py
│   │   │   ├── ingestion_repository.py
│   │   │   └── conversation_repository.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── organization_service.py
│   │   │   ├── document_service.py
│   │   │   ├── collection_service.py
│   │   │   ├── ingestion_service.py
│   │   │   ├── conversation_service.py
│   │   │   └── intelligence_service.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── scanners/
│   │   │   │   ├── folder_scanner.py
│   │   │   │   └── file_validator.py
│   │   │   │
│   │   │   ├── extractors/
│   │   │   │   ├── pdf_extractor.py
│   │   │   │   ├── docx_extractor.py
│   │   │   │   └── text_extractor.py
│   │   │   │
│   │   │   └── pipeline.py
│   │   │
│   │   ├── rag/
│   │   │   ├── chunking/
│   │   │   │   ├── base.py
│   │   │   │   └── text_chunker.py
│   │   │   │
│   │   │   ├── embeddings/
│   │   │   │   ├── base.py
│   │   │   │   └── embedding_service.py
│   │   │   │
│   │   │   ├── retrieval/
│   │   │   │   ├── retriever.py
│   │   │   │   └── filters.py
│   │   │   │
│   │   │   ├── vector_store/
│   │   │   │   ├── base.py
│   │   │   │   └── vector_store.py
│   │   │   │
│   │   │   └── pipeline.py
│   │   │
│   │   ├── agents/
│   │   │   ├── state.py
│   │   │   ├── graph.py
│   │   │   │
│   │   │   ├── manager/
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── contract_analysis/
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── legal_research/
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── compliance/
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── drafting/
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   └── case_management/
│   │   │       ├── agent.py
│   │   │       └── prompts.py
│   │   │
│   │   ├── tools/
│   │   │   ├── document_tools.py
│   │   │   ├── retrieval_tools.py
│   │   │   ├── legal_tools.py
│   │   │   ├── task_tools.py
│   │   │   └── integration_tools.py
│   │   │
│   │   ├── workers/
│   │   │   ├── document_worker.py
│   │   │   ├── ingestion_worker.py
│   │   │   └── embedding_worker.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── base.py
│   │   │   ├── google_drive.py
│   │   │   ├── sharepoint.py
│   │   │   ├── sql_database.py
│   │   │   └── external_api.py
│   │   │
│   │   ├── storage/
│   │   │   ├── base.py
│   │   │   ├── local_storage.py
│   │   │   └── object_storage.py
│   │   │
│   │   ├── utils/
│   │   │   ├── file_utils.py
│   │   │   ├── datetime_utils.py
│   │   │   └── identifiers.py
│   │   │
│   │   └── main.py
│   │
│   ├── migrations/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   │
│   ├── requirements.txt
│   ├── alembic.ini
│   └── Dockerfile
│
├── ai-services/
│   └── README.md
│
├── frontend/
│   └── README.md
│
├── infrastructure/
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── technical-architecture.md
│   ├── database.md
│   ├── api-design.md
│   └── roadmap.md
│
├── tests/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 4. API Layer

Location:

```text
backend/app/api/
```

The API layer is responsible for:

- Receiving HTTP requests
- Validating request data using Pydantic schemas
- Applying authentication and authorization dependencies
- Calling the appropriate service
- Returning HTTP responses
- Mapping application errors to HTTP status codes

The API layer must not contain database queries or complex business logic.

Example request flow:

```text
POST /api/v1/documents
↓
documents/router.py
↓
document_service.py
↓
document_repository.py
↓
PostgreSQL
```

All version-one endpoints are grouped under:

```text
/api/v1
```

A central router located at:

```text
backend/app/api/v1/router.py
```

combines the feature routers.

---

## 5. Core Layer

Location:

```text
backend/app/core/
```

The core layer contains application-wide configuration and shared infrastructure.

### config.py

Loads environment variables and settings such as:

- Application name
- Environment
- Database URL
- Redis URL
- Object storage settings
- JWT configuration
- LLM provider settings
- Vector database settings

### security.py

Contains:

- Password hashing
- Password verification
- Access token generation
- Token validation
- Authentication security utilities

### logging.py

Configures structured application logging.

Logs should include relevant context such as:

- Request ID
- Organization ID
- User ID
- Ingestion job ID
- AI run ID

Sensitive information must never be written to logs.

### exceptions.py

Defines application-specific exceptions.

Examples:

- ResourceNotFoundError
- PermissionDeniedError
- InvalidFileError
- IngestionError
- AIProcessingError

### constants.py

Contains shared constants and enum-like values.

Examples:

- Document statuses
- Ingestion statuses
- User roles
- Supported file types
- AI run statuses

---

## 6. Database Layer

Location:

```text
backend/app/db/
```

The database layer manages SQLAlchemy configuration and sessions.

### base.py

Provides the declarative SQLAlchemy base used by all database models.

### session.py

Creates the database engine and session factory.

### init_db.py

Contains optional database initialization logic such as:

- Creating initial organization data
- Creating a system administrator
- Adding default intelligence modules

Database schema changes should be managed through Alembic migrations rather than direct table creation in production.

---

## 7. Models Layer

Location:

```text
backend/app/models/
```

Models represent PostgreSQL tables using SQLAlchemy.

Each major entity has a separate model file.

Examples:

```text
user.py
document.py
document_collection.py
ingestion_job.py
conversation.py
```

Models define:

- Table names
- Columns
- Primary keys
- Foreign keys
- Constraints
- Relationships
- Indexes

Models must not contain API or agent logic.

---

## 8. Schemas Layer

Location:

```text
backend/app/schemas/
```

Schemas define Pydantic request and response models.

Examples:

```text
UserCreate
UserResponse
LoginRequest
DocumentCreate
DocumentResponse
IngestionJobResponse
ConversationCreate
```

Schemas protect the API from exposing internal database fields.

For example, a user response must not expose:

```text
password_hash
```

Database models and API schemas must remain separate.

---

## 9. Repository Layer

Location:

```text
backend/app/repositories/
```

Repositories contain database access logic.

Responsibilities include:

- Creating records
- Reading records
- Updating records
- Deleting records
- Applying organization filters
- Managing database queries
- Handling pagination and query filters

Example:

```text
DocumentRepository
├── create()
├── get_by_id()
├── list_by_organization()
├── update_status()
└── delete()
```

Repositories should not contain HTTP logic, LLM prompts, or agent coordination.

All organization-specific queries must include the authenticated organization context.

---

## 10. Service Layer

Location:

```text
backend/app/services/
```

Services contain the application's business logic.

Services coordinate:

- Repositories
- Storage providers
- RAG pipelines
- Ingestion pipelines
- Integrations
- Agents
- Background jobs

Example document upload flow:

```text
Document API
↓
Document Service
├── Validate file
├── Store file
├── Create database record
└── Start background processing
```

The service layer should remain independent from FastAPI-specific request and response objects whenever possible.

---

## 11. Document Ingestion Layer

Location:

```text
backend/app/ingestion/
```

The ingestion layer handles deterministic document processing.

Main responsibilities:

- Scan folders recursively
- Validate file types
- Preserve nested folder structures
- Register document collections
- Extract text
- Create document records
- Start chunking and embedding processing
- Track ingestion progress
- Handle failed files

The standard ingestion flow is:

```text
Folder or Document
↓
Scanner
↓
Validator
↓
Extractor
↓
Chunker
↓
Embedding Service
↓
Vector Store
↓
Database Status Update
```

This layer must not use AI agents for predictable file-processing steps.

---

## 12. RAG Layer

Location:

```text
backend/app/rag/
```

The RAG layer provides enterprise knowledge retrieval.

It contains four primary components:

### Chunking

Splits extracted text into smaller searchable sections.

### Embeddings

Converts text chunks into numerical vectors.

### Vector Store

Stores and searches embedding vectors.

### Retrieval

Selects the most relevant document chunks for a user query.

The retrieval process must apply:

- Organization filters
- Document access filters
- Collection filters
- Module filters
- Relevance thresholds

Standard RAG flow:

```text
User Query
↓
Query Embedding
↓
Vector Search
↓
Metadata Filtering
↓
Relevant Document Chunks
↓
LLM Context
↓
Generated Answer with Citations
```

---

## 13. Agent Layer

Location:

```text
backend/app/agents/
```

The agent layer handles reasoning and dynamic workflow coordination.

LangGraph will be used to define the multi-agent graph.

### Shared Agent State

The file:

```text
agents/state.py
```

defines the shared LangGraph state.

Possible state fields include:

- User request
- Organization ID
- User ID
- Conversation ID
- Selected agents
- Retrieved sources
- Intermediate results
- Risk level
- Draft output
- Final response
- Errors

### Agent Graph

The file:

```text
agents/graph.py
```

constructs and compiles the LangGraph workflow.

### Manager Agent

The Manager Agent:

- Receives the user's request
- Determines the request type
- Selects specialized agents
- Controls execution order
- Combines intermediate outputs
- Produces the final response

### Specialized Agents

Initial specialized agents include:

- Contract Analysis Agent
- Legal Research Agent
- Compliance Agent
- Drafting Agent
- Case Management Agent

Each agent should be implemented as an independent LangGraph node.

Agents must not directly contain database credentials, storage credentials, or external API credentials.

They access capabilities through tools and services.

---

## 14. Tools Layer

Location:

```text
backend/app/tools/
```

Tools provide controlled capabilities to agents.

Examples:

- Retrieve document chunks
- Read document text
- Search regulations
- Create a case task
- Update a deadline
- Query an enterprise integration
- Generate a document summary

Tools must be separate from agents so that they can be:

- Reused
- Tested independently
- Permission-controlled
- Logged
- Replaced without rewriting agent logic

A tool should perform one clear operation and return structured output.

---

## 15. Workers Layer

Location:

```text
backend/app/workers/
```

Workers handle long-running or resource-intensive operations.

Examples:

- Processing thousands of PDF files
- Extracting document text
- Generating embeddings
- Synchronizing external systems
- Running scheduled intelligence reports
- Retrying failed ingestion jobs

FastAPI should submit background work instead of keeping HTTP requests open until processing finishes.

The initial development version may use FastAPI background tasks.

A production version may use:

- Celery
- Dramatiq
- Redis Queue
- Another distributed task system

Worker tasks must be idempotent where possible, meaning retrying a task should not create duplicate data.

---

## 16. Integrations Layer

Location:

```text
backend/app/integrations/
```

This layer connects the platform to external enterprise systems.

Examples:

- Google Drive
- SharePoint
- SQL databases
- External APIs
- Internal file servers

Each integration should implement a shared interface where possible.

Example operations:

```text
connect()
test_connection()
list_documents()
fetch_document()
synchronize()
disconnect()
```

Sensitive credentials must be stored using a secure secrets-management solution.

---

## 17. Storage Layer

Location:

```text
backend/app/storage/
```

The storage layer provides a common interface for file storage.

Development may use:

```text
Local file storage
```

Production may use:

```text
S3-compatible object storage
Azure Blob Storage
Google Cloud Storage
MinIO
```

The rest of the application should depend on a storage interface rather than a specific storage provider.

---

## 18. Request Flows

### Standard API Request

```text
Frontend
↓
FastAPI Router
↓
Authentication Dependency
↓
Service
↓
Repository
↓
PostgreSQL
↓
Response Schema
↓
Frontend
```

### Single Document Upload

```text
Frontend
↓
Documents API
↓
Document Service
├── Validate file
├── Save file to storage
├── Create document record
└── Submit processing task
↓
Return document status
```

### Bulk Folder Ingestion

```text
Folder Source
↓
Ingestion API
↓
Ingestion Service
├── Create ingestion job
├── Scan nested folders
├── Create document collections
├── Register documents
└── Submit worker tasks
↓
Workers process documents
↓
Update ingestion progress
```

### RAG Question Answering

```text
User Question
↓
Intelligence API
↓
Intelligence Service
↓
Retriever
↓
Vector Store
↓
Relevant Chunks
↓
LLM
↓
Answer with Sources
```

### Multi-Agent Request

```text
User Request
↓
Intelligence API
↓
Intelligence Service
↓
Manager Agent
↓
Selected Specialized Agents
↓
Tools and RAG
↓
Combined Final Response
```

---

## 19. Dependency Rules

The following rules must be maintained:

```text
API may call Services.
Services may call Repositories.
Services may call RAG, Ingestion, Storage, Integrations, and Agents.
Repositories may call the Database.
Agents may call approved Tools.
Tools may call Services, RAG, or Integrations.
Workers may call Services and Pipelines.
```

The following dependencies should be avoided:

```text
Repositories calling API routers
Models calling Services
Agents directly querying PostgreSQL
API routers containing SQL queries
RAG components handling HTTP responses
Tools importing FastAPI routers
```

These rules prevent circular dependencies and keep the system testable.

---

## 20. Testing Strategy

Tests are organized into:

### Unit Tests

Test individual components in isolation.

Examples:

- Password hashing
- File validation
- Chunking
- Repository methods
- Service logic
- Agent routing decisions

### Integration Tests

Test communication between multiple components.

Examples:

- Service and PostgreSQL
- Ingestion and object storage
- RAG and vector storage
- Agents and tools

### API Tests

Test HTTP endpoints.

Examples:

- Registration
- Login
- Document upload
- Collection listing
- Ingestion job status
- AI conversation requests

Tests must verify organization-level data isolation.

---

## 21. Security Considerations

The architecture must apply:

- Secure password hashing
- JWT or secure session authentication
- Role-based access control
- Organization-level data isolation
- File type and file size validation
- Malware scanning where required
- Rate limiting
- Secure secret storage
- Audit logging
- Input validation
- Safe error responses
- Restricted agent tool permissions

Agents must not be allowed to perform unrestricted database or infrastructure operations.

---

## 22. Initial Implementation Scope

The complete architecture defines the long-term structure, but the first implementation will use only the required components.

Initial implementation order:

```text
1. FastAPI application
2. Health endpoint
3. Configuration management
4. PostgreSQL connection
5. SQLAlchemy models
6. Alembic migrations
7. Authentication
8. Document collections
9. Document upload
10. Folder ingestion
11. Text extraction
12. Chunking and embeddings
13. RAG retrieval
14. Conversations
15. LangGraph agent workflow
16. Background workers
17. Enterprise integrations
```

Unused folders should not contain unnecessary implementation code.

They may begin with only an:

```text
__init__.py
```

and be expanded when their feature is implemented.

---

## 23. Technology Stack

### Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
Alembic
```

### Database and Storage

```text
PostgreSQL
pgvector or a dedicated vector database
Redis
S3-compatible object storage
```

### AI

```text
LangGraph
LangChain components where useful
LLM provider APIs
Embedding models
RAG
```

### Background Processing

```text
FastAPI BackgroundTasks during early development
Redis-based distributed workers for production
```

### Infrastructure

```text
Docker
Docker Compose
Nginx
CI/CD
Monitoring and structured logging
```

---

## 24. Future Extensibility

The architecture should allow new intelligence domains to be added without rewriting the platform core.

Possible future modules include:

- Financial Intelligence
- Human Resources Intelligence
- Procurement Intelligence
- Healthcare Intelligence
- Executive Intelligence
- Market and Competitor Intelligence
- Government Compliance Intelligence

New agents, tools, integrations, and services should be added as independent modules while sharing the core platform infrastructure.