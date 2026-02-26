-- ================================================================
-- VERIX MASTER MANDATE: STRICT SQL VIEWS
-- Run this ONCE in Supabase SQL Editor
-- ================================================================

-- ================================================================
-- SCIENCE VIEWS
-- ================================================================

CREATE OR REPLACE VIEW view_science_1_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%science%' AND marks = 1
  ORDER BY random();

CREATE OR REPLACE VIEW view_science_2_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%science%' AND marks = 2
  ORDER BY random();

CREATE OR REPLACE VIEW view_science_3_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%science%' AND marks = 3
  ORDER BY random();

CREATE OR REPLACE VIEW view_science_5_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%science%' AND marks = 5
  ORDER BY random();

CREATE OR REPLACE VIEW view_science_case_studies AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%science%'
    AND marks = 4
    AND question_type ILIKE '%case%'
  ORDER BY random();

-- ================================================================
-- MATHEMATICS VIEWS
-- ================================================================

CREATE OR REPLACE VIEW view_math_1_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%math%' AND marks = 1
  ORDER BY random();

CREATE OR REPLACE VIEW view_math_2_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%math%' AND marks = 2
  ORDER BY random();

CREATE OR REPLACE VIEW view_math_3_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%math%' AND marks = 3
  ORDER BY random();

CREATE OR REPLACE VIEW view_math_5_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%math%' AND marks = 5
  ORDER BY random();

CREATE OR REPLACE VIEW view_math_case_studies AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%math%'
    AND marks = 4
    AND question_type ILIKE '%case%'
  ORDER BY random();

-- ================================================================
-- SOCIAL SCIENCE / SST VIEWS
-- ================================================================

CREATE OR REPLACE VIEW view_sst_1_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%social%' AND marks = 1
  ORDER BY random();

CREATE OR REPLACE VIEW view_sst_3_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%social%' AND marks = 3
  ORDER BY random();

CREATE OR REPLACE VIEW view_sst_5_markers AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%social%' AND marks = 5
    AND question_type NOT ILIKE '%map%'
  ORDER BY random();

CREATE OR REPLACE VIEW view_sst_map_questions AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%social%'
    AND (question_type ILIKE '%map%' OR chapter ILIKE '%map%')
  ORDER BY random();

CREATE OR REPLACE VIEW view_sst_case_studies AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%social%'
    AND marks = 4
    AND question_type ILIKE '%case%'
  ORDER BY random();

-- ================================================================
-- ENGLISH VIEWS
-- ================================================================

CREATE OR REPLACE VIEW view_english_reading AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%english%'
    AND (question_type ILIKE '%reading%' OR question_type ILIKE '%comprehension%' OR question_type ILIKE '%passage%')
  ORDER BY random();

CREATE OR REPLACE VIEW view_english_writing AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%english%'
    AND question_type ILIKE '%writing%'
  ORDER BY random();

CREATE OR REPLACE VIEW view_english_grammar AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%english%'
    AND question_type ILIKE '%grammar%'
  ORDER BY random();

CREATE OR REPLACE VIEW view_english_literature AS
  SELECT * FROM class9_question_bank
  WHERE subject ILIKE '%english%'
    AND (question_type ILIKE '%literature%' OR question_type ILIKE '%poem%' OR question_type ILIKE '%prose%')
  ORDER BY random();

-- ================================================================
-- UNIVERSAL RPC: get_random_questions_v2
-- Supports sub_subject filtering. Use from frontend.
-- ================================================================

CREATE OR REPLACE FUNCTION get_random_questions_v2(
  p_subject TEXT,
  p_marks INT,
  p_question_type TEXT DEFAULT NULL,
  p_sub_subject TEXT DEFAULT NULL,
  p_limit INT DEFAULT 10,
  p_exclude_ids BIGINT[] DEFAULT ARRAY[]::BIGINT[]
)
RETURNS SETOF public.class9_question_bank
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM public.class9_question_bank
  WHERE
    subject ILIKE ('%' || p_subject || '%')
    AND marks = p_marks
    AND (p_question_type IS NULL OR question_type ILIKE ('%' || p_question_type || '%'))
    AND (p_sub_subject IS NULL OR sub_subject ILIKE ('%' || p_sub_subject || '%'))
    AND (cardinality(p_exclude_ids) = 0 OR id != ALL(p_exclude_ids))
  ORDER BY random()
  LIMIT p_limit;
END;
$$;

GRANT EXECUTE ON FUNCTION get_random_questions_v2(TEXT, INT, TEXT, TEXT, INT, BIGINT[]) TO anon;
GRANT EXECUTE ON FUNCTION get_random_questions_v2(TEXT, INT, TEXT, TEXT, INT, BIGINT[]) TO authenticated;

-- Grant SELECT on all views to public
GRANT SELECT ON view_science_1_markers TO anon;
GRANT SELECT ON view_science_2_markers TO anon;
GRANT SELECT ON view_science_3_markers TO anon;
GRANT SELECT ON view_science_5_markers TO anon;
GRANT SELECT ON view_science_case_studies TO anon;
GRANT SELECT ON view_math_1_markers TO anon;
GRANT SELECT ON view_math_2_markers TO anon;
GRANT SELECT ON view_math_3_markers TO anon;
GRANT SELECT ON view_math_5_markers TO anon;
GRANT SELECT ON view_math_case_studies TO anon;
GRANT SELECT ON view_sst_1_markers TO anon;
GRANT SELECT ON view_sst_3_markers TO anon;
GRANT SELECT ON view_sst_5_markers TO anon;
GRANT SELECT ON view_sst_map_questions TO anon;
GRANT SELECT ON view_sst_case_studies TO anon;
GRANT SELECT ON view_english_reading TO anon;
GRANT SELECT ON view_english_writing TO anon;
GRANT SELECT ON view_english_grammar TO anon;
GRANT SELECT ON view_english_literature TO anon;
