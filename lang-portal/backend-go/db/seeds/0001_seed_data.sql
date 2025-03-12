-- Seed data for words
INSERT INTO words (japanese, romaji, english, parts) VALUES
('こんにちは', 'konnichiwa', 'hello', '{"part_of_speech": "greeting"}'),
('ありがとう', 'arigatou', 'thank you', '{"part_of_speech": "expression"}');

-- Seed data for groups
INSERT INTO groups (name) VALUES
('Basic Greetings'),
('Expressions');

-- Seed data for words_groups
INSERT INTO words_groups (word_id, group_id) VALUES
(1, 1),
(2, 2);

-- Seed data for study_sessions
INSERT INTO study_sessions (group_id, study_activity_id) VALUES
(1, 1),
(2, 2);

-- Seed data for study_activities
INSERT INTO study_activities (study_session_id, group_id) VALUES
(1, 1),
(2, 2);

-- Seed data for word_review_items
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(1, 1, true),
(2, 2, false); 