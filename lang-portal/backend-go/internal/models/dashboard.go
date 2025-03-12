package models

import (
	"database/sql"
	"time"
)

// LastStudySession represents the most recent study session
type LastStudySession struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
	GroupName       string    `json:"group_name"`
}

// StudyProgress represents overall study progress
type StudyProgress struct {
	TotalWordsStudied    int `json:"total_words_studied"`
	TotalAvailableWords int `json:"total_available_words"`
}

// QuickStats represents quick overview statistics
type QuickStats struct {
	SuccessRate       float64 `json:"success_rate"`
	TotalStudySessions int    `json:"total_study_sessions"`
	TotalActiveGroups  int    `json:"total_active_groups"`
	StudyStreakDays    int    `json:"study_streak_days"`
}

// GetLastStudySession retrieves information about the most recent study session
func GetLastStudySession(db *sql.DB) (*LastStudySession, error) {
	query := `
		SELECT 
			ss.id, ss.group_id, ss.created_at, ss.study_activity_id,
			g.name as group_name
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		ORDER BY ss.created_at DESC
		LIMIT 1
	`

	var session LastStudySession
	err := db.QueryRow(query).Scan(
		&session.ID, &session.GroupID, &session.CreatedAt,
		&session.StudyActivityID, &session.GroupName,
	)
	if err != nil {
		return nil, err
	}

	return &session, nil
}

// GetStudyProgress retrieves overall study progress statistics
func GetStudyProgress(db *sql.DB) (*StudyProgress, error) {
	// Get total available words
	var totalWords int
	err := db.QueryRow("SELECT COUNT(*) FROM words").Scan(&totalWords)
	if err != nil {
		return nil, err
	}

	// Get total words studied (words with at least one review)
	var studiedWords int
	err = db.QueryRow(`
		SELECT COUNT(DISTINCT word_id)
		FROM word_review_items
	`).Scan(&studiedWords)
	if err != nil {
		return nil, err
	}

	return &StudyProgress{
		TotalWordsStudied:    studiedWords,
		TotalAvailableWords: totalWords,
	}, nil
}

// GetQuickStats retrieves quick overview statistics
func GetQuickStats(db *sql.DB) (*QuickStats, error) {
	// Get success rate
	var correctCount, totalCount int
	err := db.QueryRow(`
		SELECT 
			COUNT(CASE WHEN correct = 1 THEN 1 END),
			COUNT(*)
		FROM word_review_items
	`).Scan(&correctCount, &totalCount)
	if err != nil {
		return nil, err
	}

	var successRate float64
	if totalCount > 0 {
		successRate = float64(correctCount) * 100 / float64(totalCount)
	}

	// Get total study sessions
	var totalSessions int
	err = db.QueryRow("SELECT COUNT(*) FROM study_sessions").Scan(&totalSessions)
	if err != nil {
		return nil, err
	}

	// Get total active groups (groups with at least one study session)
	var activeGroups int
	err = db.QueryRow(`
		SELECT COUNT(DISTINCT group_id)
		FROM study_sessions
	`).Scan(&activeGroups)
	if err != nil {
		return nil, err
	}

	// Calculate study streak
	var streakDays int
	err = db.QueryRow(`
		WITH RECURSIVE dates(date) AS (
			SELECT date(MAX(created_at)) FROM study_sessions
			UNION ALL
			SELECT date(date, '-1 day')
			FROM dates
			WHERE EXISTS (
				SELECT 1 FROM study_sessions
				WHERE date(created_at) = date(date, '-1 day')
			)
		)
		SELECT COUNT(*) FROM dates
	`).Scan(&streakDays)
	if err != nil {
		return nil, err
	}

	return &QuickStats{
		SuccessRate:        successRate,
		TotalStudySessions: totalSessions,
		TotalActiveGroups:  activeGroups,
		StudyStreakDays:    streakDays,
	}, nil
} 