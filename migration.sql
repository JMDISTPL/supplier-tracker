-- Create product_niches table
CREATE TABLE product_niches (
  id BIGSERIAL PRIMARY KEY,
  niche_name TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'kitchen',
  price_range TEXT,
  monthly_sales_min INTEGER,
  monthly_sales_max INTEGER,
  est_cpc NUMERIC(4,2),
  competition_level TEXT,
  weight_kg NUMERIC(4,2),
  top_reviews_range TEXT,
  est_production_cost NUMERIC(6,2),
  pros TEXT[],
  cons TEXT[],
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'denied')),
  denial_reason TEXT,
  market_context TEXT,
  source_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create niche_archive table (learning memory)
CREATE TABLE niche_archive (
  id BIGSERIAL PRIMARY KEY,
  niche_name TEXT NOT NULL,
  category TEXT,
  denial_reason TEXT NOT NULL,
  pros TEXT[],
  cons TEXT[],
  market_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE product_niches ENABLE ROW LEVEL SECURITY;
ALTER TABLE niche_archive ENABLE ROW LEVEL SECURITY;

-- Allow public access (anon key)
CREATE POLICY "anon_all_product_niches" ON product_niches FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon_all_niche_archive" ON niche_archive FOR ALL TO anon USING (true) WITH CHECK (true);