package models

import (
	"database/sql"
	"time"
)

// StudySession represents a study session in the system
type StudySession struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
}

// StudySessionDetail includes session information with activity and group names
type StudySessionDetail struct {
	ID               int       `json:"id"`
	ActivityName     string    `json:"activity_name"`
	GroupName        string    `json:"group_name"`
	StartTime        time.Time `json:"start_time"`
	EndTime          time.Time `json:"end_time"`
	ReviewItemsCount int       `json:"review_items_count"`
}

// GetStudySessions retrieves a paginated list of study sessions
func GetStudySessions(db *sql.DB, page, perPage int) ([]StudySessionDetail, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := db.QueryRow("SELECT COUNT(*) FROM study_sessions").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get study sessions with details - simplified query
	query := `
		SELECT 
			ss.id,
			COALESCE(sa.name, 'Unknown Activity') as activity_name,
			COALESCE(g.name, 'Unknown Group') as group_name,
			ss.created_at as start_time,
			ss.created_at as end_time,
			0 as review_items_count
		FROM study_sessions ss
		LEFT JOIN groups g ON ss.group_id = g.id
		LEFT JOIN study_activities sa ON ss.study_activity_id = sa.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var sessions []StudySessionDetail
	for rows.Next() {
		var s StudySessionDetail
		err := rows.Scan(
			&s.ID, &s.ActivityName, &s.GroupName,
			&s.StartTime, &s.EndTime, &s.ReviewItemsCount,
		)
		if err != nil {
			return nil, 0, err
		}

		// Get review count in a separate query
		err = db.QueryRow(`
			SELECT COUNT(*) 
			FROM word_review_items 
			WHERE study_session_id = ?
		`, s.ID).Scan(&s.ReviewItemsCount)
		if err != nil {
			// Don't fail if we can't get review count
			s.ReviewItemsCount = 0
		}

		sessions = append(sessions, s)
	}

	return sessions, total, nil
}

// GetStudySessionByID retrieves a single study session by its ID
func GetStudySessionByID(db *sql.DB, id int) (*StudySessionDetail, error) {
	// First check if session exists
	var exists bool
	err := db.QueryRow("SELECT EXISTS(SELECT 1 FROM study_sessions WHERE id = ?)", id).Scan(&exists)
	if err != nil {
		return nil, err
	}
	if !exists {
		return nil, sql.ErrNoRows
	}

	// Get session details
	query := `
		SELECT 
			ss.id,
			COALESCE(sa.name, 'Unknown Activity') as activity_name,
			COALESCE(g.name, 'Unknown Group') as group_name,
			ss.created_at as start_time,
			ss.created_at as end_time,
			0 as review_items_count
		FROM study_sessions ss
		LEFT JOIN groups g ON ss.group_id = g.id
		LEFT JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.id = ?
	`

	var s StudySessionDetail
	err = db.QueryRow(query, id).Scan(
		&s.ID,
		&s.ActivityName,
		&s.GroupName,
		&s.StartTime,
		&s.EndTime,
		&s.ReviewItemsCount,
	)
	if err != nil {
		return nil, err
	}

	// Get review count in a separate query
	err = db.QueryRow(`
		SELECT COUNT(*) 
		FROM word_review_items 
		WHERE study_session_id = ?
	`, id).Scan(&s.ReviewItemsCount)
	if err != nil {
		// Don't fail if we can't get review count
		s.ReviewItemsCount = 0
	}

	return &s, nil
}

// GetStudySessionWords retrieves all words reviewed in a study session
func GetStudySessionWords(db *sql.DB, sessionID int, page, perPage int) ([]WordWithStats, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := db.QueryRow(`
		SELECT COUNT(DISTINCT w.id)
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?
	`, sessionID).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get words with stats for this session
	query := `
		SELECT 
			w.id, w.japanese, w.romaji, w.english,
			SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END) as correct_count,
			SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END) as wrong_count
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?
		GROUP BY w.id
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, sessionID, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var words []WordWithStats
	for rows.Next() {
		var w WordWithStats
		err := rows.Scan(
			&w.ID, &w.Japanese, &w.Romaji, &w.English,
			&w.CorrectCount, &w.WrongCount,
		)
		if err != nil {
			return nil, 0, err
		}
		words = append(words, w)
	}

	return words, total, nil
}

// CreateStudySession creates a new study session
func CreateStudySession(db *sql.DB, groupID, studyActivityID int) (*StudySession, error) {
	result, err := db.Exec(`
		INSERT INTO study_sessions (group_id, study_activity_id)
		VALUES (?, ?)
	`, groupID, studyActivityID)
	if err != nil {
		return nil, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}

	return &StudySession{
		ID:              int(id),
		GroupID:         groupID,
		StudyActivityID: studyActivityID,
		CreatedAt:       time.Now(),
	}, nil
}

// AddWordReview adds a word review item to a study session
func AddWordReview(db *sql.DB, sessionID, wordID int, correct bool) error {
	_, err := db.Exec(`
		INSERT INTO word_review_items (study_session_id, word_id, correct)
		VALUES (?, ?, ?)
	`, sessionID, wordID, correct)
	return err
}

// GetStudySessionsByGroup retrieves study sessions for a specific group
func GetStudySessionsByGroup(db *sql.DB, groupID, page, perPage int) ([]StudySessionDetail, int, error) {
	offset := (page - 1) * perPage

	// First check if group exists
	var exists bool
	err := db.QueryRow("SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)", groupID).Scan(&exists)
	if err != nil {
		return nil, 0, err
	}
	if !exists {
		return nil, 0, sql.ErrNoRows
	}

	// Get total count
	var total int
	err = db.QueryRow(`
		SELECT COUNT(*)
		FROM study_sessions
		WHERE group_id = ?
	`, groupID).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get study sessions with details
	query := `
		SELECT 
			ss.id,
			COALESCE(sa.name, 'Unknown Activity') as activity_name,
			COALESCE(g.name, 'Unknown Group') as group_name,
			ss.created_at as start_time,
			ss.created_at as end_time,
			0 as review_items_count
		FROM study_sessions ss
		LEFT JOIN groups g ON ss.group_id = g.id
		LEFT JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.group_id = ?
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`

	rows, err := db.Query(query, groupID, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var sessions []StudySessionDetail
	for rows.Next() {
		var s StudySessionDetail
		err := rows.Scan(
			&s.ID,
			&s.ActivityName,
			&s.GroupName,
			&s.StartTime,
			&s.EndTime,
			&s.ReviewItemsCount,
		)
		if err != nil {
			return nil, 0, err
		}

		// Get review count in a separate query
		err = db.QueryRow(`
			SELECT COUNT(*) 
			FROM word_review_items 
			WHERE study_session_id = ?
		`, s.ID).Scan(&s.ReviewItemsCount)
		if err != nil {
			// Don't fail if we can't get review count
			s.ReviewItemsCount = 0
		}

		sessions = append(sessions, s)
	}

	if err = rows.Err(); err != nil {
		return nil, 0, err
	}

	return sessions, total, nil
} 