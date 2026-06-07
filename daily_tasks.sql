-- Daily Tasks checklist for the JMPL Logistics calendar
CREATE TABLE daily_tasks (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  task_date DATE NOT NULL,
  task_text TEXT NOT NULL,
  completed BOOLEAN DEFAULT false,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE daily_tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all on daily_tasks" ON daily_tasks FOR ALL USING (true) WITH CHECK (true);
CREATE INDEX idx_tasks_date ON daily_tasks (task_date);