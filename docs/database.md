# Enterprise Intelligence Platform Database Design

## 1. Database Overview

The platform uses PostgreSQL as its primary relational database.

The database is designed to support:

- Multiple organizations
- Multiple users per organization
- Role-based access control
- Document and knowledge management
- Nested document folders
- Bulk document ingestion
- AI conversations
- RAG document retrieval
- Multiple intelligence domains
- External system integrations
- Audit logging

The platform follows a multi-tenant architecture.

Each organization's data is isolated using an `organization_id`.

---

## 2. Main Entities

### Organizations

Represents companies or institutions using the platform.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR | Organization name |
| slug | VARCHAR | Unique organization identifier |
| industry | VARCHAR | Legal, finance, healthcare, government, etc. |
| is_active | BOOLEAN | Organization status |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update date |

---

### Users

Represents platform users.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| email | VARCHAR | Unique user email |
| password_hash | VARCHAR | Encrypted password |
| first_name | VARCHAR | User first name |
| last_name | VARCHAR | User last name |
| is_active | BOOLEAN | Account status |
| created_at | TIMESTAMP | Account creation date |
| updated_at | TIMESTAMP | Last update date |

Passwords must never be stored as plain text.

---

### Organization Memberships

Connects users to organizations.

A user may belong to more than one organization.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| user_id | UUID | References users |
| role | VARCHAR | owner, admin, analyst, member, viewer |
| joined_at | TIMESTAMP | Membership creation date |

A unique constraint must exist on:

```text
organization_id + user_id
```

---

### Intelligence Modules

Represents the business domains enabled for an organization.

Examples:

- Legal Intelligence
- Financial Intelligence
- Healthcare Intelligence
- Risk Intelligence
- Market Intelligence

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| name | VARCHAR | Module name |
| code | VARCHAR | legal, finance, healthcare, risk |
| is_enabled | BOOLEAN | Module status |
| configuration | JSONB | Module configuration |
| created_at | TIMESTAMP | Creation date |

---

### Document Collections

Represents folders and nested folders containing enterprise documents.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| name | VARCHAR | Folder or collection name |
| parent_id | UUID | Optional reference to a parent collection |
| source_path | TEXT | Original folder path |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update date |

The `parent_id` field allows nested folder structures.

Example:

```text
Company Documents
├── Contracts
│   ├── Active
│   └── Expired
├── Policies
└── Reports
```

A root folder has:

```text
parent_id = null
```

A nested folder references another collection using:

```text
parent_id = parent collection UUID
```

---

### Documents

Stores metadata about uploaded or connected documents.

The actual file is stored in object storage, not directly inside PostgreSQL.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| uploaded_by | UUID | References users |
| module_id | UUID | Optional intelligence module |
| collection_id | UUID | Optional document collection |
| title | VARCHAR | Document title |
| file_name | VARCHAR | Original file name |
| file_type | VARCHAR | PDF, DOCX, TXT, CSV |
| storage_path | TEXT | File location in object storage |
| source_type | VARCHAR | upload, folder, Google Drive, SharePoint, API |
| status | VARCHAR | uploaded, processing, ready, failed |
| metadata | JSONB | Additional document metadata |
| created_at | TIMESTAMP | Upload date |
| updated_at | TIMESTAMP | Last update date |

A document may belong to a collection.

Example:

```text
Contracts
└── employment-contract.pdf
```

In this case, the document's `collection_id` references the Contracts collection.

---

### Document Chunks

Stores the smaller text sections created from documents for RAG.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| document_id | UUID | References documents |
| organization_id | UUID | References organizations |
| chunk_index | INTEGER | Chunk order |
| content | TEXT | Extracted text |
| token_count | INTEGER | Number of tokens |
| page_number | INTEGER | Source page |
| vector_id | VARCHAR | Reference to vector database |
| metadata | JSONB | Additional chunk metadata |
| created_at | TIMESTAMP | Creation date |

The embeddings may be stored in a vector database or using PostgreSQL with pgvector.

---

### Ingestion Jobs

Tracks bulk document import and processing operations.

An ingestion job is created when the platform imports a folder or a large group of documents.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| created_by | UUID | References users |
| source_type | VARCHAR | folder, upload, drive, sharepoint |
| source_path | TEXT | Source folder or integration path |
| status | VARCHAR | pending, scanning, processing, completed, failed |
| total_files | INTEGER | Total discovered files |
| processed_files | INTEGER | Successfully processed files |
| failed_files | INTEGER | Failed files |
| error_message | TEXT | Processing error details |
| started_at | TIMESTAMP | Processing start date |
| completed_at | TIMESTAMP | Processing completion date |
| created_at | TIMESTAMP | Job creation date |

Example ingestion lifecycle:

```text
pending
↓
scanning
↓
processing
↓
completed
```

If an error occurs:

```text
failed
```

An ingestion job may process hundreds or thousands of documents in the background.

---

### Conversations

Represents AI Assistant conversations.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| user_id | UUID | References users |
| module_id | UUID | Optional intelligence module |
| title | VARCHAR | Conversation title |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last message date |

---

### Messages

Stores messages inside conversations.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| conversation_id | UUID | References conversations |
| organization_id | UUID | References organizations |
| role | VARCHAR | user, assistant, system |
| content | TEXT | Message content |
| model_name | VARCHAR | AI model used |
| token_count | INTEGER | Tokens consumed |
| created_at | TIMESTAMP | Message creation date |

---

### AI Runs

Stores information about each AI processing operation.

Examples:

- RAG question answering
- Contract analysis
- Risk classification
- Executive summary generation
- Document classification
- Draft generation

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| user_id | UUID | References users |
| conversation_id | UUID | Optional conversation |
| module_id | UUID | Optional intelligence module |
| run_type | VARCHAR | chat, rag, summary, classification, analysis |
| model_name | VARCHAR | AI model used |
| status | VARCHAR | pending, running, completed, failed |
| input_tokens | INTEGER | Input token count |
| output_tokens | INTEGER | Output token count |
| latency_ms | INTEGER | Processing duration |
| error_message | TEXT | Error details |
| created_at | TIMESTAMP | Run start date |
| completed_at | TIMESTAMP | Run completion date |

---

### AI Sources

Stores the document chunks used to generate an AI response.

This allows the platform to display citations.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| ai_run_id | UUID | References AI runs |
| document_id | UUID | References documents |
| chunk_id | UUID | References document chunks |
| relevance_score | DECIMAL | Retrieval similarity score |
| created_at | TIMESTAMP | Creation date |

---

### Integrations

Represents external enterprise data sources.

Examples:

- Google Drive
- SharePoint
- Outlook
- SQL databases
- External APIs
- Internal file servers

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| created_by | UUID | References users |
| integration_type | VARCHAR | Google Drive, SharePoint, SQL, API, file server |
| name | VARCHAR | Integration display name |
| status | VARCHAR | active, disconnected, error |
| configuration | JSONB | Non-sensitive settings |
| credentials_reference | TEXT | Secure secrets-manager reference |
| last_synced_at | TIMESTAMP | Last synchronization |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update date |

Sensitive credentials must not be stored directly inside the database.

---

### Audit Logs

Stores important activities for security and compliance.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| organization_id | UUID | References organizations |
| user_id | UUID | References users |
| action | VARCHAR | login, upload_document, delete_document |
| resource_type | VARCHAR | document, user, integration, ingestion_job |
| resource_id | UUID | Affected resource |
| ip_address | VARCHAR | User IP address |
| user_agent | TEXT | Client information |
| details | JSONB | Additional event details |
| created_at | TIMESTAMP | Event date |

---

## 3. Entity Relationship Diagram

```mermaid
erDiagram

    ORGANIZATIONS {
        uuid id PK
        varchar name
        varchar slug UK
        varchar industry
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    USERS {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar first_name
        varchar last_name
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    ORGANIZATION_MEMBERSHIPS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        varchar role
        timestamp joined_at
    }

    INTELLIGENCE_MODULES {
        uuid id PK
        uuid organization_id FK
        varchar name
        varchar code
        boolean is_enabled
        jsonb configuration
        timestamp created_at
    }

    DOCUMENT_COLLECTIONS {
        uuid id PK
        uuid organization_id FK
        uuid parent_id FK
        varchar name
        text source_path
        timestamp created_at
        timestamp updated_at
    }

    DOCUMENTS {
        uuid id PK
        uuid organization_id FK
        uuid uploaded_by FK
        uuid module_id FK
        uuid collection_id FK
        varchar title
        varchar file_name
        varchar file_type
        text storage_path
        varchar source_type
        varchar status
        jsonb metadata
        timestamp created_at
        timestamp updated_at
    }

    DOCUMENT_CHUNKS {
        uuid id PK
        uuid document_id FK
        uuid organization_id FK
        integer chunk_index
        text content
        integer token_count
        integer page_number
        varchar vector_id
        jsonb metadata
        timestamp created_at
    }

    INGESTION_JOBS {
        uuid id PK
        uuid organization_id FK
        uuid created_by FK
        varchar source_type
        text source_path
        varchar status
        integer total_files
        integer processed_files
        integer failed_files
        text error_message
        timestamp started_at
        timestamp completed_at
        timestamp created_at
    }

    CONVERSATIONS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        uuid module_id FK
        varchar title
        timestamp created_at
        timestamp updated_at
    }

    MESSAGES {
        uuid id PK
        uuid conversation_id FK
        uuid organization_id FK
        varchar role
        text content
        varchar model_name
        integer token_count
        timestamp created_at
    }

    AI_RUNS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        uuid conversation_id FK
        uuid module_id FK
        varchar run_type
        varchar model_name
        varchar status
        integer input_tokens
        integer output_tokens
        integer latency_ms
        text error_message
        timestamp created_at
        timestamp completed_at
    }

    AI_SOURCES {
        uuid id PK
        uuid ai_run_id FK
        uuid document_id FK
        uuid chunk_id FK
        decimal relevance_score
        timestamp created_at
    }

    INTEGRATIONS {
        uuid id PK
        uuid organization_id FK
        uuid created_by FK
        varchar integration_type
        varchar name
        varchar status
        jsonb configuration
        text credentials_reference
        timestamp last_synced_at
        timestamp created_at
        timestamp updated_at
    }

    AUDIT_LOGS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        varchar action
        varchar resource_type
        uuid resource_id
        varchar ip_address
        text user_agent
        jsonb details
        timestamp created_at
    }

    ORGANIZATIONS ||--o{ ORGANIZATION_MEMBERSHIPS : has
    USERS ||--o{ ORGANIZATION_MEMBERSHIPS : belongs_to

    ORGANIZATIONS ||--o{ INTELLIGENCE_MODULES : enables

    ORGANIZATIONS ||--o{ DOCUMENT_COLLECTIONS : owns
    DOCUMENT_COLLECTIONS ||--o{ DOCUMENT_COLLECTIONS : contains

    ORGANIZATIONS ||--o{ DOCUMENTS : owns
    USERS ||--o{ DOCUMENTS : uploads
    INTELLIGENCE_MODULES ||--o{ DOCUMENTS : categorizes
    DOCUMENT_COLLECTIONS ||--o{ DOCUMENTS : organizes
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : contains

    ORGANIZATIONS ||--o{ INGESTION_JOBS : owns
    USERS ||--o{ INGESTION_JOBS : creates

    ORGANIZATIONS ||--o{ CONVERSATIONS : owns
    USERS ||--o{ CONVERSATIONS : starts
    INTELLIGENCE_MODULES ||--o{ CONVERSATIONS : supports
    CONVERSATIONS ||--o{ MESSAGES : contains

    ORGANIZATIONS ||--o{ AI_RUNS : owns
    USERS ||--o{ AI_RUNS : triggers
    CONVERSATIONS ||--o{ AI_RUNS : generates
    INTELLIGENCE_MODULES ||--o{ AI_RUNS : processes

    AI_RUNS ||--o{ AI_SOURCES : uses
    DOCUMENTS ||--o{ AI_SOURCES : cited_from
    DOCUMENT_CHUNKS ||--o{ AI_SOURCES : retrieved_from

    ORGANIZATIONS ||--o{ INTEGRATIONS : configures
    USERS ||--o{ INTEGRATIONS : creates

    ORGANIZATIONS ||--o{ AUDIT_LOGS : records
    USERS ||--o{ AUDIT_LOGS : performs
```

---

## 4. Multi-Tenant Data Isolation

All organization-specific tables must contain:

```text
organization_id
```

Every database query must filter records using the authenticated user's organization.

Example:

```sql
SELECT *
FROM documents
WHERE organization_id = :current_organization_id;
```

This prevents one organization from accessing another organization's data.

The API must not trust an `organization_id` provided directly by the frontend.

The organization must be derived from the authenticated user's identity and membership.

---

## 5. Primary Key Strategy

UUID is used instead of sequential integer IDs.

Example:

```text
550e8400-e29b-41d4-a716-446655440000
```

UUIDs are preferred because they:

- Are difficult to guess
- Work well in distributed systems
- Reduce ID collisions
- Improve security when IDs appear in APIs

---

## 6. Data Storage Strategy

PostgreSQL stores:

- Users
- Organizations
- Permissions
- Document collections
- Document metadata
- Ingestion job status
- Conversations
- AI run history
- Integrations
- Audit logs

Object storage stores:

- PDF files
- Word documents
- Images
- Large uploaded files
- Imported enterprise documents

Vector storage stores:

- Document embeddings
- Semantic search vectors

Redis stores temporary data such as:

- Cached responses
- User sessions
- Rate-limiting counters
- Background task status
- Ingestion job progress

---

## 7. Document Ingestion Flow

The platform supports both single-document uploads and bulk folder ingestion.

### Single Document Upload

```text
Upload document
↓
Create document record
↓
Store file
↓
Extract text
↓
Create chunks
↓
Generate embeddings
↓
Mark document as ready
```

### Bulk Folder Ingestion

```text
Select folder or external source
↓
Create ingestion job
↓
Scan nested folders
↓
Create document collections
↓
Register discovered documents
↓
Process documents in the background
↓
Update ingestion progress
↓
Mark job as completed
```

The original folder structure should be preserved using `document_collections`.

---

## 8. Agent and Automation Data Considerations

AI agents should operate on top of the core document and RAG infrastructure.

Agents may perform tasks such as:

- Document classification
- Contract analysis
- Risk detection
- Research across multiple documents
- Draft generation
- Workflow coordination

Deterministic tasks should remain standard backend services.

Examples:

```text
PDF extraction
Chunking
Embedding generation
File storage
Database updates
```

These tasks do not require agents.

Agent execution records may be stored in the `ai_runs` table.

Future versions may add:

- agent_name
- workflow_id
- parent_run_id
- tool_calls
- agent_output
- execution_trace

These fields are not required for the initial MVP.

---

## 9. Initial MVP Tables

The first implementation will begin with:

1. organizations
2. users
3. organization_memberships
4. document_collections
5. documents
6. document_chunks
7. ingestion_jobs
8. conversations
9. messages

The following tables will be introduced gradually:

1. intelligence_modules
2. ai_runs
3. ai_sources
4. integrations
5. audit_logs