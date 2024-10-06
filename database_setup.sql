CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cik VARCHAR(10) UNIQUE,
    website VARCHAR(255),
    esg_score FLOAT,
    last_updated TIMESTAMP
);

CREATE TABLE sec_filings (
    id SERIAL PRIMARY KEY,
    company_cik VARCHAR(10) REFERENCES companies(cik),
    filing_type VARCHAR(10),
    filing_date DATE,
    accession_number VARCHAR(20),
    content TEXT,
    UNIQUE(company_cik, accession_number)
);

CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    content TEXT,
    published_at TIMESTAMP,
    source VARCHAR(255),
    UNIQUE(company_name, title, published_at)
);

CREATE TABLE website_data (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) UNIQUE,
    content TEXT,
    scraped_at TIMESTAMP
);

CREATE TABLE esg_scores (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    environmental_score FLOAT,
    social_score FLOAT,
    governance_score FLOAT,
    total_score FLOAT,
    date DATE
);