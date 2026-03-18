# 🧪 Combinations API

A lightweight FastAPI backend for generating combinatorial sets from a list of items, exporting results as CSV, and archiving data to the [Open Science Framework (OSF)](https://osf.io).

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [API Reference](#api-reference)
  - [POST /generate-combinations](#post-generate-combinations)
  - [POST /create-csv](#post-create-csv)
  - [POST /upload-to-osf](#post-upload-to-osf)
  - [GET /osf-whoami](#get-osf-whoami)
  - [GET /osf-perms](#get-osf-perms)
- [Data Models](#data-models)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Notes & Gotchas](#notes--gotchas)

---

## Overview

This API is designed for research workflows that need to:

1. **Generate** all k-combinations from a given list of items (e.g. materials, compounds, conditions)
2. **Export** the results as a downloadable CSV
3. **Archive** data files to an OSF project node for reproducibility and open science

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| HTTP Client | [httpx](https://www.python-httpx.org/) |
| Data Validation | [Pydantic](https://docs.pydantic.dev/) (via FastAPI) |
| CSV Streaming | Python stdlib `csv` + `io` |
| OSF Integration | [OSF WaterButler API](https://developer.osf.io/) |
| Config | `python-dotenv` |

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [OSF account](https://osf.io) with a personal access token
- An OSF project node (you'll need its short ID, e.g. `abc12`)

### Installation

```bash
git clone https://github.com/your-org/combinations-api.git
cd combinations-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
PROJECT_ID=your_osf_project_id     # e.g. abc12 — the short ID in the OSF URL
OSF_TOKEN=your_osf_personal_token  # generate at osf.io/settings/tokens
```

> **Never commit `.env` to version control.** Add it to `.gitignore`.

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

---

## API Reference

### `POST /generate-combinations`

Generates all k-combinations from a list of items using `itertools.combinations`.

**Request Body**

```json
{
  "items": ["A", "B", "C", "D"],
  "size": 2
}
```

| Field | Type | Description |
|---|---|---|
| `items` | `string[]` | The pool of items to combine |
| `size` | `int` | The size `k` of each combination (must be ≥ 1 and ≤ `len(items)`) |

**Response**

```json
{
  "status": "good",
  "combinations": [
    { "compound_number": 1, "materials": ["A", "B"] },
    { "compound_number": 2, "materials": ["A", "C"] },
    ...
  ],
  "generated_at": "2025-01-15 02:30 PM EST"
}
```

**Errors**

| Status | Reason |
|---|---|
| `400` | `size` is less than 1 |
| `400` | `size` is greater than the number of items |

---

### `POST /create-csv`

Serialises a set of combinations into a downloadable CSV file, streamed directly to the client.

**Request Body**

```json
{
  "size": 2,
  "items": ["A", "B", "C"],
  "combos": 3,
  "combinations": ["A, B", "A, C", "B, C"]
}
```

**Response**

Streams a `text/csv` file as an attachment. The filename is formatted as:

```
{uuid}_{ISO-timestamp}.csv
```

**CSV Format**

```
job_id,<uuid>
size,2
items,A | B | C
combos,3

index,combination
1,"A, B"
2,"A, C"
3,"B, C"
```

---

### `POST /upload-to-osf`

Uploads a CSV file to OSF storage under the configured project node.

**Request** — `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | `File` | ✅ | A valid `.csv` file |
| `job_id` | `string` | ❌ | Used to construct the uploaded filename |

**Response**

```json
{
  "ok": true,
  "uploaded_filename": "abc123_20250115_143000.csv",
  "osf_file_page_url": "https://osf.io/<project_id>/files/osfstorage/<file_id>/",
  "osf_file_id": "<file_id>"
}
```

**Validation**

Before uploading, the file is validated with `is_csv()`:
- Must have a `.csv` extension
- Must be non-empty and UTF-8 decodable (BOM-safe)
- First row must have at least 2 columns

**Errors**

| Status | Reason |
|---|---|
| `400` | Empty file or invalid CSV |
| `500` | Missing `OSF_TOKEN` or `PROJECT_ID` env vars |
| OSF status code | Forwarded from OSF if their API rejects the upload |

---

### `GET /osf-whoami`

Debug endpoint. Checks the authenticated OSF user and verifies the configured project node is accessible.

**Response**

```json
{
  "me_status": 200,
  "me": "{ ... first 300 chars of OSF /users/me/ response ... }",
  "node_status": 200,
  "node": "{ ... first 300 chars of OSF node response ... }"
}
```

> Use this to verify your `OSF_TOKEN` and `PROJECT_ID` are correctly configured.

---

### `GET /osf-perms`

Debug endpoint. Returns contributor permissions for the configured OSF project node.

**Response**

```json
{
  "status": 200,
  "body": "{ ... first 2000 chars of contributors response ... }"
}
```

> Use this to confirm your token has write access to the project.

---

## Data Models

Defined in `model.py` and `model_csv.py` (Pydantic):

### `Combinations` (`model.py`)

```python
class Combinations(BaseModel):
    items: list[str]
    size: int
```

### `Output_Csv` (`model_csv.py`)

```python
class Output_Csv(BaseModel):
    size: int
    items: list[str]
    combos: int
    combinations: list[str]
```

---

## Project Structure

```
.
├── main.py            # FastAPI app, all route handlers
├── model.py           # Pydantic model for /generate-combinations
├── model_csv.py       # Pydantic model for /create-csv
├── .env               # Local secrets (not committed)
├── .env.example       # Template for env vars
├── requirements.txt
└── README.md
```

---

## Error Handling

- `HTTPException` is re-raised directly so FastAPI returns clean, structured error responses.
- Unexpected exceptions on `/generate-combinations` return a `{"status": "error", "message": "..."}` JSON body instead of a 500 — intentional for frontend resilience.
- All other endpoints raise `HTTPException` on failure so clients receive proper HTTP status codes.

---

## Notes & Gotchas

**OSF Upload Filename**
The `job_id` form field on `/upload-to-osf` is optional — if omitted, `make_filename()` will receive `None` and still produce a valid timestamp-based name. You may want to make this required if traceability matters.

**CORS**
Currently configured with `allow_origins=["*"]`. Restrict this to your frontend's domain before deploying to production:

```python
allow_origins=["https://your-frontend.com"]
```

**Timezone**
Combination generation timestamps are logged in `America/Toronto` (Eastern Time). This is hardcoded — adjust in `main.py` if your team is elsewhere.

**Large Combination Sets**
`itertools.combinations` is lazy, but the results are fully materialised into a list before returning. For very large `n choose k` values this can be memory-intensive. Consider streaming or paginating results for production use at scale.

**OSF Rate Limits**
The OSF API does not publish hard rate limits, but be mindful of bulk uploads. The httpx client timeout is set to 120 seconds for uploads.

---

## License

MIT — see `LICENSE` for details.
