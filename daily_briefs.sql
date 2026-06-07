-- Daily Briefs table for the JMPL Logistics dashboard
CREATE TABLE daily_briefs (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  brief_date DATE NOT NULL UNIQUE,
  title TEXT DEFAULT '',
  priorities TEXT DEFAULT '',
  tasks TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE daily_briefs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all on daily_briefs" ON daily_briefs FOR ALL USING (true) WITH CHECK (true);
CREATE INDEX idx_briefs_date ON daily_briefs (brief_date DESC);