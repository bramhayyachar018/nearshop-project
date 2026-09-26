# 🛍️ NearShop — AI Powered Product and Inventory Search for Local Retailers

NearShop is a hyper-local backend system that allows customers to discover products from nearby local retailers. It utilizes FastAPI, PostgreSQL, and pgvector for high-performance spatial and semantic AI search.

## 🚀 Features

- **Relational Inventory Management:** Full schema for Retailers, Stores, Products, and per-Store Inventory tracking.
- **AI-Powered Semantic Search:** Integrates `pgvector` for L2/cosine distance similarity searches on product embeddings.
- **High-Performance:** Uses SQLAlchemy connection pooling and FastAPI asynchronous capabilities.
- **Predictable API:** Standardized JSON responses for frontend reliability.

## 🏗️ Architecture Stack

- **Framework:** Python 3 + FastAPI
- **Database:** PostgreSQL + pgvector
- **ORM:** SQLAlchemy + Pydantic
- **Containerization:** Docker Compose

---

## 🛠️ Setup Instructions

### 1. Requirements

Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Python 3.10+](https://www.python.org/downloads/) installed.

### 2. Configure Environment

Rename `.env.example` to `.env` and configure your credentials:

```bash
cp .env.example .env
```

### 3. Start PostgreSQL Database

We provide a `docker-compose.yml` that includes PostgreSQL pre-configured with the `pgvector` extension.

```bash
docker-compose up -d
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Server

Start the FastAPI application. The initial run will automatically create the required database tables via SQLAlchemy.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access Documentation

FastAPI auto-generates API documentation. Navigate to:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application initialization
│   ├── database.py      # SQLAlchemy engine & pooling setup
│   ├── models.py        # Database schema (Retailer, Store, Product, Inventory)
│   ├── schemas.py       # Pydantic models for request/response validation
│   ├── utils.py         # Shared utility functions (e.g., standard_response)
│   └── routers/         # API Controllers
│       ├── retailer.py
│       ├── store.py
│       ├── product.py
│       ├── inventory.py
│       └── search.py
├── tests/               # Pytest testing suite
├── docker-compose.yml   # PostgreSQL + pgvector Docker config
├── .env.example         # Environment variable template
└── requirements.txt     # Python dependencies
```
