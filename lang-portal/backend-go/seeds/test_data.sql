-- Insert test groups
INSERT INTO groups (name) VALUES 
('Basic Japanese'),
('JLPT N5 Vocabulary'),
('Common Phrases');

-- Insert test words
INSERT INTO words (japanese, romaji, english) VALUES 
('犬', 'inu', 'dog'),
('猫', 'neko', 'cat'),
('魚', 'sakana', 'fish'),
('鳥', 'tori', 'bird'),
('本', 'hon', 'book');

-- Insert test study activities
INSERT INTO study_activities (name, description) VALUES
('Vocabulary Quiz', 'Practice your vocabulary with flashcards'),
('Writing Practice', 'Practice writing Japanese characters');

-- Insert test study sessions
INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES
(1, 1, datetime('now', '-1 day')),
(2, 1, datetime('now', '-2 hours'));

-- Insert test word reviews
INSERT INTO word_review_items (study_session_id, word_id, correct, created_at) VALUES
(1, 1, true, datetime('now', '-1 day')),
(1, 2, true, datetime('now', '-1 day')),
(1, 3, false, datetime('now', '-1 day')),
(2, 4, true, datetime('now', '-2 hours')),
(2, 5, true, datetime('now', '-2 hours')); 