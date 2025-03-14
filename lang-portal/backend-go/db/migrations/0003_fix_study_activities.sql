-- Fix study_activities table if needed
DROP TABLE IF EXISTS study_activities;

CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    thumbnail_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_study_activities_created_at ON study_activities(created_at);

-- Add default study activity if it doesn't exist
INSERT OR IGNORE INTO study_activities (id, name, description, thumbnail_url) 
VALUES (1, 'Vocabulary Quiz', 'Practice your vocabulary with flashcards', 'https://example.com/vocab-quiz-thumb.jpg'); 