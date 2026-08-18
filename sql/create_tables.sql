-- ============================================
-- BEHAVIORLENS DATABASE SCHEMA
-- ============================================

-- 1. INDUSTRIES
CREATE TABLE IF NOT EXISTS industries (
    industry_id SERIAL PRIMARY KEY,
    industry_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);


-- 2. BRANDS
CREATE TABLE IF NOT EXISTS brands (
    brand_id SERIAL PRIMARY KEY,

    brand_name VARCHAR(150) NOT NULL UNIQUE,

    industry_id INTEGER NOT NULL,

    founded_year INTEGER,

    headquarters VARCHAR(200),

    website TEXT,

    industry_type VARCHAR(150),

    CONSTRAINT fk_brands_industry
        FOREIGN KEY (industry_id)
        REFERENCES industries(industry_id)
);


-- 3. REVIEWS
CREATE TABLE IF NOT EXISTS reviews (
    review_id BIGSERIAL PRIMARY KEY,

    brand_id INTEGER NOT NULL,

    source_review_id VARCHAR(255),

    review_text TEXT NOT NULL,

    clean_text TEXT,

    rating INTEGER,

    review_date TIMESTAMP,

    source VARCHAR(100),

    app_version VARCHAR(100),

    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_brand
        FOREIGN KEY (brand_id)
        REFERENCES brands(brand_id),

    CONSTRAINT check_rating
        CHECK (rating IS NULL OR rating BETWEEN 1 AND 5)
);


-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_brands_industry
    ON brands(industry_id);

CREATE INDEX IF NOT EXISTS idx_reviews_brand
    ON reviews(brand_id);

CREATE INDEX IF NOT EXISTS idx_reviews_date
    ON reviews(review_date);

CREATE INDEX IF NOT EXISTS idx_reviews_rating
    ON reviews(rating);