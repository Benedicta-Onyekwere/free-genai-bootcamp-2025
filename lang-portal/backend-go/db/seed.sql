-- Seed data for testing

-- Insert words
INSERT INTO words (japanese, romaji, english) VALUES
('こんにちは', 'konnichiwa', 'Hello'),
('ありがとう', 'arigatou', 'Thank you'),
('さようなら', 'sayounara', 'Goodbye'),
('おはよう', 'ohayou', 'Good morning'),
('こんばんは', 'konbanwa', 'Good evening');

-- Insert groups
INSERT INTO groups (name) VALUES
('Basic Greetings'),
('Common Phrases');

-- Insert words into groups
INSERT INTO words_groups (word_id, group_id) VALUES
(1, 1), -- こんにちは in Basic Greetings
(2, 1), -- ありがとう in Basic Greetings
(3, 1), -- さようなら in Basic Greetings
(4, 1), -- おはよう in Basic Greetings
(5, 1), -- こんばんは in Basic Greetings
(1, 2), -- こんにちは in Common Phrases
(2, 2), -- ありがとう in Common Phrases
(3, 2); -- さようなら in Common Phrases

-- Insert study sessions
INSERT INTO study_sessions (group_id, study_activity_id) VALUES
(1, 1), -- Basic Greetings quiz
(2, 1); -- Common Phrases quiz 