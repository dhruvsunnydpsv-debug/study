-- ================================================================
-- VERIX AUDIT ENGINE: CLASS 9 CBSE QUESTION BANK SCHEMA
-- Run this ONCE in Supabase SQL Editor
-- ================================================================

-- 1. Drop old table if it exists
DROP TABLE IF EXISTS question_bank;

-- 2. Create the master table
CREATE TABLE class9_question_bank (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  subject TEXT NOT NULL, 
  chapter TEXT NOT NULL, 
  question_text TEXT NOT NULL,
  options JSONB,
  correct_answer TEXT,
  diagram_url TEXT,
  marks INTEGER,
  question_type TEXT,
  source_reference TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(subject, chapter, question_text)
);

-- 3. Performance indexes
CREATE INDEX idx_subject_chapter ON class9_question_bank(subject, chapter);
CREATE INDEX idx_question_type ON class9_question_bank(question_type);

-- 4. Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TRIGGER update_class9_modtime
BEFORE UPDATE ON class9_question_bank
FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

-- 5. Enable Row Level Security but allow public read
ALTER TABLE class9_question_bank ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read" ON class9_question_bank
  FOR SELECT USING (true);

CREATE POLICY "Allow service insert" ON class9_question_bank
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow service update" ON class9_question_bank
  FOR UPDATE USING (true);

CREATE POLICY "Allow service delete" ON class9_question_bank
  FOR DELETE USING (true);
