# EIO2 Python - Architecture Documentation

## CSIR EOI 8119 - Mining Data Analytics API

### System Architecture

```mermaid
flowchart TB
    subgraph client [Clients]
        Web[Web Application]
        Mobile[Mobile App]
        CLI[API Clients]
    end

    subgraph api [API Layer - FastAPI]
        FastAPI[FastAPI Application]
        Auth[JWT Authentication]
        Validation[Request Validation]
    end

    subgraph services [Service Layer]
        AuthService[Auth Service]
        MiningService[Mining Service]
    end

    subgraph background [Background Processing]
        Celery[Celery Workers]
        Beat[Celery Beat Scheduler]
        Flower[Flower Monitor]
    end

    subgraph data [Data Layer]
        PostgreSQL[(PostgreSQL)]
        Redis[(Redis)]
    end

    Web --> FastAPI
    Mobile --> FastAPI
    CLI --> FastAPI

    FastAPI --> Auth
    Auth --> Validation
    Validation --> AuthService
    Validation --> MiningService

    MiningService --> PostgreSQL
    AuthService --> PostgreSQL

    Celery --> PostgreSQL
    Celery --> Redis
    Beat --> Celery
    Flower --> Celery
```

### Class Diagram - Database Models

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string hashed_password
        +string first_name
        +string last_name
        +string role
        +bool is_active
        +datetime created_at
        +datetime updated_at
    }

    class MiningShift {
        +int id
        +date shift_date
        +ShiftType shift_type
        +string mine_section
        +int supervisor_id
        +int workers_count
        +datetime start_time
        +datetime end_time
        +string notes
    }

    class ProductionRecord {
        +int id
        +int shift_id
        +int equipment_id
        +float ore_extracted_tonnes
        +float waste_removed_tonnes
        +float ore_grade_percentage
        +float depth_meters
        +string mining_level
        +string stope_number
    }

    class Equipment {
        +int id
        +string equipment_code
        +string name
        +string equipment_type
        +EquipmentStatus status
        +float capacity_tonnes
        +float operating_hours
        +date last_maintenance_date
    }

    class MaintenanceLog {
        +int id
        +int equipment_id
        +MaintenanceType maintenance_type
        +string description
        +float labor_hours
        +float total_cost
        +bool is_completed
    }

    User "1" --> "*" MiningShift : supervises
    MiningShift "1" --> "*" ProductionRecord : contains
    Equipment "1" --> "*" ProductionRecord : produces
    Equipment "1" --> "*" MaintenanceLog : has
```

### API Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant AuthMiddleware
    participant Service
    participant PostgreSQL
    participant Celery

    Client->>FastAPI: POST /api/production
    FastAPI->>AuthMiddleware: Verify JWT Token
    AuthMiddleware-->>FastAPI: User authenticated
    FastAPI->>Service: create_production_record
    Service->>PostgreSQL: INSERT production_record
    PostgreSQL-->>Service: Record created
    Service->>Celery: Trigger analytics update
    Service-->>FastAPI: Return record
    FastAPI-->>Client: 201 Created
```

### Background Task Architecture

```mermaid
flowchart LR
    subgraph scheduler [Celery Beat]
        Daily[Daily Report<br/>6 AM]
        Hourly[Data Processing<br/>Every Hour]
        FourHour[Equipment Metrics<br/>Every 4 Hours]
        Weekly[Cleanup<br/>Weekly]
    end

    subgraph broker [Message Broker]
        Redis[(Redis Queue)]
    end

    subgraph workers [Celery Workers]
        W1[Worker 1]
        W2[Worker 2]
        W3[Worker 3]
        W4[Worker 4]
    end

    subgraph database [Database]
        PostgreSQL[(PostgreSQL)]
    end

    Daily --> Redis
    Hourly --> Redis
    FourHour --> Redis
    Weekly --> Redis

    Redis --> W1
    Redis --> W2
    Redis --> W3
    Redis --> W4

    W1 --> PostgreSQL
    W2 --> PostgreSQL
    W3 --> PostgreSQL
    W4 --> PostgreSQL
```

### Database Schema (ERD)

```mermaid
erDiagram
    users ||--o{ mining_shifts : supervises
    mining_shifts ||--o{ production_records : contains
    equipment ||--o{ production_records : produces
    equipment ||--o{ maintenance_logs : has

    users {
        int id PK
        string email UK
        string hashed_password
        string first_name
        string last_name
        string role
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    mining_shifts {
        int id PK
        date shift_date
        enum shift_type
        string mine_section
        int supervisor_id FK
        int workers_count
        timestamp start_time
        timestamp end_time
    }

    production_records {
        int id PK
        int shift_id FK
        int equipment_id FK
        float ore_extracted_tonnes
        float waste_removed_tonnes
        float ore_grade_percentage
        float depth_meters
        timestamp recorded_at
    }

    equipment {
        int id PK
        string equipment_code UK
        string name
        string equipment_type
        enum status
        float capacity_tonnes
        float operating_hours
        date next_maintenance_date
    }

    maintenance_logs {
        int id PK
        int equipment_id FK
        enum maintenance_type
        string description
        float labor_hours
        float total_cost
        boolean is_completed
    }
```

### Deployment Architecture

```mermaid
flowchart TB
    subgraph compose [Docker Compose Stack]
        API[FastAPI Container<br/>Port 8000]
        Worker[Celery Worker]
        Beat[Celery Beat]
        Flower[Flower UI<br/>Port 5555]
        PG[(PostgreSQL<br/>Port 5432)]
        RD[(Redis<br/>Port 6379)]
    end

    subgraph volumes [Volumes]
        pgData[postgres_data]
        redisData[redis_data]
    end

    API --> PG
    API --> RD
    Worker --> PG
    Worker --> RD
    Beat --> RD
    Flower --> RD
    PG --> pgData
    RD --> redisData

    User[API Clients] --> API
```
