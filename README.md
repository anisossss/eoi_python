# CSIR EOI 8119 - Mining Data Analytics API

<div align="center">

![CSIR Logo](https://img.shields.io/badge/CSIR-EOI_8119-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)

**Mining Data Analytics API - Demonstrating Python & PostgreSQL Proficiency**

</div>

---

## 📋 Project Overview

This project is part of the **CSIR EOI No. 8119/06/02/2026** submission, demonstrating proficiency in:

- **Python** programming with FastAPI framework
- **PostgreSQL** relational database with SQL queries
- **Background Processing** with Celery and Redis
- **Docker** containerization
- **Cloud-ready** architecture

### Technical Evaluation Criteria Addressed

| Criterion               | Implementation                               |
| ----------------------- | -------------------------------------------- |
| Python proficiency      | FastAPI, Pydantic, SQLAlchemy                |
| PostgreSQL              | Relational database with complex SQL queries |
| SQL/NoSQL databases     | SQL with JOINs, aggregations, GROUP BY       |
| Background processing   | Celery workers with scheduled tasks          |
| Docker containerization | Multi-stage Dockerfile, Docker Compose       |
| Software design         | Clean architecture, separation of concerns   |

---

## 🛠 Technology Stack

| Component      | Technology            | Purpose               |
| -------------- | --------------------- | --------------------- |
| Backend        | Python 3.12 + FastAPI | REST API framework    |
| Database       | PostgreSQL 16         | Relational database   |
| ORM            | SQLAlchemy 2.0        | Database abstraction  |
| Task Queue     | Celery 5.3            | Background processing |
| Message Broker | Redis 7               | Task queue broker     |
| Auth           | JWT (python-jose)     | Authentication        |
| Container      | Docker                | Containerization      |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   Auth   │  │  Shifts  │  │Equipment │  │   Analytics      │ │
│  │   API    │  │   API    │  │   API    │  │      API         │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
        │                                              │
        ▼                                              ▼
┌───────────────┐                            ┌─────────────────┐
│  PostgreSQL   │                            │      Redis      │
│   Database    │                            │  (Broker/Cache) │
└───────────────┘                            └─────────────────┘
                                                      │
                                                      ▼
                                            ┌─────────────────┐
                                            │  Celery Worker  │
                                            │  Celery Beat    │
                                            └─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)

### Docker Deployment (Recommended)

```bash
# Clone and navigate to project
cd EIO2_python

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Flower: http://localhost:5555
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and Redis (with Docker)
docker-compose up -d postgres redis

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info

# In another terminal, start Celery beat (scheduler)
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 📖 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Overview

| Resource       | Endpoint             | Methods                |
| -------------- | -------------------- | ---------------------- |
| Authentication | `/api/auth/*`        | POST, GET              |
| Mining Shifts  | `/api/shifts/*`      | GET, POST, PUT, DELETE |
| Production     | `/api/production/*`  | GET, POST, PUT         |
| Equipment      | `/api/equipment/*`   | GET, POST, PUT         |
| Maintenance    | `/api/maintenance/*` | GET, POST, PUT         |
| Analytics      | `/api/analytics/*`   | GET                    |

### Example API Calls

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "operator@mining.co.za",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Miner",
    "role": "operator"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=operator@mining.co.za&password=SecurePass123"

# Get production statistics (with auth token)
curl http://localhost:8000/api/analytics/production-stats?start_date=2026-01-01&end_date=2026-01-31 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🔧 Background Tasks (Celery)

### Scheduled Tasks

| Task                          | Schedule        | Description                     |
| ----------------------------- | --------------- | ------------------------------- |
| `generate_daily_report`       | Daily at 6 AM   | Generate production report      |
| `process_production_data`     | Every hour      | Process and aggregate data      |
| `calculate_equipment_metrics` | Every 4 hours   | Calculate equipment performance |
| `send_maintenance_alerts`     | Daily at 8 AM   | Check maintenance schedules     |
| `cleanup_old_records`         | Weekly (Sunday) | Archive old data                |

### Manual Task Execution

```python
from app.tasks import generate_daily_report, export_data

# Trigger daily report
result = generate_daily_report.delay()
print(result.get())

# Export data for date range
result = export_data.delay("2026-01-01", "2026-01-31", "json")
print(result.get())
```

---

## 🗄 Database Schema

### Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────────┐
│    Users    │       │   MiningShifts   │       │ ProductionRecords│
├─────────────┤       ├──────────────────┤       ├─────────────────┤
│ id (PK)     │──────▶│ id (PK)          │◀──────│ id (PK)         │
│ email       │       │ supervisor_id(FK)│       │ shift_id (FK)   │
│ password    │       │ shift_date       │       │ equipment_id(FK)│
│ first_name  │       │ shift_type       │       │ ore_extracted   │
│ last_name   │       │ mine_section     │       │ waste_removed   │
│ role        │       │ workers_count    │       │ ore_grade       │
└─────────────┘       └──────────────────┘       └─────────────────┘
                                                          │
        ┌─────────────────┐       ┌─────────────────┐     │
        │   Equipment     │       │ MaintenanceLogs │     │
        ├─────────────────┤       ├─────────────────┤     │
        │ id (PK)         │◀──────│ id (PK)         │     │
        │ equipment_code  │       │ equipment_id(FK)│◀────┘
        │ name            │       │ maintenance_type│
        │ equipment_type  │       │ description     │
        │ status          │       │ labor_hours     │
        │ operating_hours │       │ is_completed    │
        └─────────────────┘       └─────────────────┘
```

---

## 🐳 Docker Hub

### Pull Command

```bash
# Pull the API image
docker pull csireoi8119/mining-api:latest

# Pull all services with docker-compose
docker-compose pull
```

### Build and Push

```bash
# Build the image
docker build -t csireoi8119/mining-api:latest .

# Push to Docker Hub
docker login
docker push csireoi8119/mining-api:latest
```

---

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

---

## 📊 SQL Query Examples

The project demonstrates SQL proficiency through various query patterns:

### Aggregation Queries

```sql
-- Daily production summary
SELECT
    shift_date,
    SUM(ore_extracted_tonnes) as total_ore,
    AVG(ore_grade_percentage) as avg_grade
FROM production_records pr
JOIN mining_shifts ms ON pr.shift_id = ms.id
GROUP BY shift_date
ORDER BY shift_date;
```

### Complex Joins

```sql
-- Equipment utilization report
SELECT
    e.equipment_code,
    e.name,
    COUNT(pr.id) as production_records,
    SUM(pr.ore_extracted_tonnes) as total_ore
FROM equipment e
LEFT JOIN production_records pr ON e.id = pr.equipment_id
GROUP BY e.id
ORDER BY total_ore DESC;
```

---

## 📞 Contact

For inquiries regarding this EOI submission:

- **Email**: tender@csir.co.za
- **EOI Reference**: 8119/06/02/2026

---

<div align="center">

**Built for CSIR EOI 8119/06/02/2026**

_Demonstrating Python, PostgreSQL, and Background Processing Proficiency_

</div>
