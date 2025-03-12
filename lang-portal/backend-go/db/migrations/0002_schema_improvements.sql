-- Drop redundant study_activities table
DROP TABLE IF EXISTS study_activities;

-- Create proper study_activities reference table
CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    thumbnail_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add default study activity
INSERT INTO study_activities (id, name, description, thumbnail_url) 
VALUES (1, 'Vocabulary Quiz', 'Practice your vocabulary with flashcards', 'https://example.com/vocab-quiz-thumb.jpg');

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_words_groups_word_id ON words_groups(word_id);
CREATE INDEX IF NOT EXISTS idx_words_groups_group_id ON words_groups(group_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_group_id ON study_sessions(group_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_created_at ON study_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_word_review_items_word_id ON word_review_items(word_id);
CREATE INDEX IF NOT EXISTS idx_word_review_items_study_session_id ON word_review_items(study_session_id);
CREATE INDEX IF NOT EXISTS idx_word_review_items_created_at ON word_review_items(created_at);

-- Add unique constraint to prevent duplicate word-group associations
CREATE UNIQUE INDEX IF NOT EXISTS idx_words_groups_unique ON words_groups(word_id, group_id);

-- Recreate study_sessions table with proper constraints
CREATE TABLE study_sessions_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    study_activity_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);
INSERT INTO study_sessions_new SELECT * FROM study_sessions;
DROP TABLE study_sessions;
ALTER TABLE study_sessions_new RENAME TO study_sessions;

-- Recreate word_review_items with cascade delete
CREATE TABLE word_review_items_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id) ON DELETE CASCADE
);
INSERT INTO word_review_items_new (word_id, study_session_id, correct, created_at)
SELECT word_id, study_session_id, correct, created_at FROM word_review_items;
DROP TABLE word_review_items;
ALTER TABLE word_review_items_new RENAME TO word_review_items;

-- Recreate words_groups with cascade delete
CREATE TABLE words_groups_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);
INSERT INTO words_groups_new SELECT * FROM words_groups;
DROP TABLE words_groups;
ALTER TABLE words_groups_new RENAME TO words_groups; 