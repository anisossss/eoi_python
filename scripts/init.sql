-- CSIR EOI 8119 - Mining Data Analytics API
-- PostgreSQL Database Initialization Script
-- Demonstrates SQL proficiency

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types (enums)
DO $$ BEGIN
    CREATE TYPE shift_type AS ENUM ('day', 'night', 'morning', 'afternoon');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE equipment_status AS ENUM ('operational', 'maintenance', 'repair', 'decommissioned');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE maintenance_type AS ENUM ('preventive', 'corrective', 'emergency', 'scheduled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mining_db TO mining_user;

-- Note: Tables are created by SQLAlchemy ORM
-- This script sets up the database environment

-- Create indexes for performance (if tables exist)
-- These will be created after SQLAlchemy creates the tables

-- Sample data insertion (for demonstration)
-- This will be handled by the application's seed script
