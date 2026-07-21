# Enterprise Intelligence Platform API Design

## 1. API Overview

The platform backend will expose a REST API using FastAPI.

Base URL:

```text
/api/v1
```

The first version of the API will support:

- Authentication
- Organizations
- Users
- Documents
- Conversations
- AI Assistant

---

## 2. Authentication APIs

### Register User

```http
POST /api/v1/auth/register
```

Request:

```json
{
  "email": "user@example.com",
  "password": "secure-password",
  "first_name": "Lama",
  "last_name": "User",
  "organization_name": "Example Company"
}
```

Response:

```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "organization_id": "organization-uuid"
}
```

---

### Login

```http
POST /api/v1/auth/login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "secure-password"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

---

### Current User

```http
GET /api/v1/auth/me
```

Response:

```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "first_name": "Lama",
  "last_name": "User",
  "organization_id": "organization-uuid",
  "role": "admin"
}
```

---

## 3. Organization APIs

### Get Current Organization

```http
GET /api/v1/organizations/current
```

### Update Current Organization

```http
PATCH /api/v1/organizations/current
```

Request:

```json
{
  "name": "Updated Company Name",
  "industry": "Legal"
}
```

---

## 4. Document APIs

### Upload Document

```http
POST /api/v1/documents
```

Content type:

```text
multipart/form-data
```

Response:

```json
{
  "id": "document-uuid",
  "title": "Employment Contract",
  "file_name": "contract.pdf",
  "status": "uploaded"
}
```

---

### List Documents

```http
GET /api/v1/documents
```

Optional query parameters:

```text
status
file_type
module_id
page
page_size
```

---

### Get Document

```http
GET /api/v1/documents/{document_id}
```

---

### Delete Document

```http
DELETE /api/v1/documents/{document_id}
```

---

### Process Document

```http
POST /api/v1/documents/{document_id}/process
```

This endpoint will:

1. Extract document text
2. Divide the text into chunks
3. Generate embeddings
4. Store chunks for semantic retrieval
5. Change the document status to ready

---

## 5. Conversation APIs

### Create Conversation

```http
POST /api/v1/conversations
```

Request:

```json
{
  "title": "Contract Review",
  "module_id": "legal-module-uuid"
}
```

---

### List Conversations

```http
GET /api/v1/conversations
```

---

### Get Conversation

```http
GET /api/v1/conversations/{conversation_id}
```

---

### Delete Conversation

```http
DELETE /api/v1/conversations/{conversation_id}
```

---

## 6. Message and AI APIs

### Send Message

```http
POST /api/v1/conversations/{conversation_id}/messages
```

Request:

```json
{
  "content": "What are the main risks in this contract?",
  "document_ids": [
    "document-uuid"
  ]
}
```

Response:

```json
{
  "message_id": "message-uuid",
  "role": "assistant",
  "content": "The main risks include...",
  "sources": [
    {
      "document_id": "document-uuid",
      "page_number": 4,
      "relevance_score": 0.92
    }
  ]
}
```

---

### List Conversation Messages

```http
GET /api/v1/conversations/{conversation_id}/messages
```

---

## 7. Health Check API

```http
GET /api/v1/health
```

Response:

```json
{
  "status": "healthy",
  "service": "enterprise-intelligence-api"
}
```

This will be the first endpoint implemented in FastAPI.

---

## 8. Standard Error Response

All API errors should follow one consistent structure:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "The requested document was not found.",
    "details": null
  }
}
```

Common HTTP status codes:

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Access denied |
| 404 | Resource not found |
| 409 | Resource conflict |
| 422 | Validation error |
| 500 | Internal server error |

---

## 9. Multi-Tenant Security

Every protected request must determine:

```text
current_user
current_organization
```

A user may only access resources belonging to their organization.

Example:

```sql
SELECT *
FROM documents
WHERE id = :document_id
AND organization_id = :current_organization_id;
```

The API must never trust an `organization_id` sent directly by the frontend.

It must derive the organization from the authenticated user's token.

---

## 10. MVP Implementation Order

The APIs will be implemented in this order:

1. Health check
2. User registration
3. User login
4. Current user
5. Document upload
6. Document listing
7. Conversations
8. AI messages