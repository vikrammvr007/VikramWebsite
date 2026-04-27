-- ============================================================
-- PORTFOLIO APP — UPGRADED SUPABASE SCHEMA
-- Run this entire file in Supabase SQL Editor
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── PERSONS ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS persons (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name       TEXT NOT NULL,
    phone      TEXT,
    role       TEXT,
    summary    TEXT,
    age        INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── EMAILS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS emails (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES persons(id) ON DELETE CASCADE,
    email     TEXT NOT NULL
);

-- ── SOCIAL LINKS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS social_links (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES persons(id) ON DELETE CASCADE,
    platform  TEXT NOT NULL,
    url       TEXT NOT NULL
);

-- ── SKILL CATEGORIES ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skill_categories (
    id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

-- ── SKILLS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skills (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID REFERENCES skill_categories(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    percentage  INT DEFAULT 80
);

-- ── WORK EXPERIENCE ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS work_experience (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id  UUID REFERENCES persons(id) ON DELETE CASCADE,
    role       TEXT NOT NULL,
    company    TEXT NOT NULL,
    duration   TEXT,
    start_year TEXT,
    end_year   TEXT
);

-- ── EXPERIENCE RESPONSIBILITIES ──────────────────────────────
CREATE TABLE IF NOT EXISTS experience_responsibilities (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experience_id UUID REFERENCES work_experience(id) ON DELETE CASCADE,
    description   TEXT NOT NULL
);

-- ── EXPERIENCE TECHNOLOGIES ──────────────────────────────────
CREATE TABLE IF NOT EXISTS experience_technologies (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experience_id UUID REFERENCES work_experience(id) ON DELETE CASCADE,
    name          TEXT NOT NULL
);

-- ── PROJECTS ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id         UUID REFERENCES persons(id) ON DELETE CASCADE,
    title             TEXT NOT NULL,
    description       TEXT,
    category          TEXT,
    github_url        TEXT,
    demo_url          TEXT,
    include_in_resume BOOLEAN DEFAULT TRUE
);

-- ── PROJECT METRICS ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_metrics (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id  UUID REFERENCES projects(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    value       TEXT NOT NULL
);

-- ── PROJECT TOOLS ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_tools (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name       TEXT NOT NULL
);

-- ── PROJECT ALGORITHMS ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_algorithms (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name       TEXT NOT NULL
);

-- ── CERTIFICATIONS ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certifications (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name              TEXT NOT NULL,
    platform          TEXT,
    duration          TEXT,
    start_date        DATE,
    include_in_resume BOOLEAN DEFAULT TRUE
);

-- ── CERTIFICATION TOPICS (NEW) ───────────────────────────────
CREATE TABLE IF NOT EXISTS certification_topics (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cert_id    UUID REFERENCES certifications(id) ON DELETE CASCADE,
    topic      TEXT NOT NULL,
    sort_order INT DEFAULT 99
);

-- ── EDUCATION ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS education (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    degree      TEXT NOT NULL,
    institution TEXT NOT NULL,
    place       TEXT,
    year        TEXT,
    percentage  TEXT,
    status      TEXT,
    sort_order  INT DEFAULT 99
);

-- ── SOFT SKILLS ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS soft_skills (
    id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

-- ============================================================
-- SEED DATA — Vikramaraj M
-- ============================================================

-- Person
INSERT INTO persons (name, phone, role, age, summary) VALUES (
    'Vikramaraj M',
    '6383723994',
    'Data Engineer & ML Enthusiast',
    26,
    'A Data Engineer with 1 year of experience at Avasoft, specializing in data migration, pipeline development, and business intelligence. Hands-on experience with Apache Spark, Databricks, and Power BI. Strong foundation in Python, machine learning, Deep Learning, and data analytics.'
);

-- NOTE: After running the above, get the person UUID and replace <PERSON_UUID> below
-- Run: SELECT id FROM persons LIMIT 1;
