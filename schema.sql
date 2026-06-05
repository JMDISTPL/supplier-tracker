-- Create the suppliers table for the Amazon PL tracking dashboard
CREATE TABLE suppliers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  company TEXT NOT NULL,
  storefront_link TEXT DEFAULT '',
  email TEXT DEFAULT '',
  status TEXT DEFAULT 'Prospects' CHECK (status IN ('Prospects', 'Contacted', 'Negotiating', 'Sampling', 'Partners')),
  notes TEXT DEFAULT '',
  verified_pro BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;

-- Allow public read/write for now (it's your personal dashboard)
CREATE POLICY "Allow all on suppliers"
  ON suppliers
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Create an index for searching
CREATE INDEX idx_suppliers_company ON suppliers (company);
CREATE INDEX idx_suppliers_status ON suppliers (status);