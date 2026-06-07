-- ============================================================
-- AMAZON PL BOT — Supabase Schema Setup
-- Run this in Supabase Dashboard → SQL Editor
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_chunks (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  source_type TEXT NOT NULL,
  source_url TEXT,
  source_title TEXT,
  chunk_index INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION match_knowledge(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.7,
  match_count INT DEFAULT 5
)
RETURNS TABLE (
  id BIGINT, content TEXT, source_type TEXT,
  source_title TEXT, source_url TEXT, similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT k.id, k.content, k.source_type, k.source_title, k.source_url,
         1 - (k.embedding <=> query_embedding) AS similarity
  FROM knowledge_chunks k
  WHERE 1 - (k.embedding <=> query_embedding) > match_threshold
  ORDER BY k.embedding <=> query_embedding
  LIMIT match_count;
END; $$;

ALTER TABLE knowledge_chunks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON knowledge_chunks FOR ALL USING (true) WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_knowledge_source ON knowledge_chunks (source_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_created ON knowledge_chunks (created_at DESC);

CREATE TABLE IF NOT EXISTS chat_history (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  sources JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON chat_history FOR ALL USING (true) WITH CHECK (true);