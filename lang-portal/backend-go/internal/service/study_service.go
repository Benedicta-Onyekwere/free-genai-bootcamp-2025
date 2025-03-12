package service

import (
	"database/sql"
	"lang-portal/backend-go/internal/models"
)

type StudyService struct {
	db *sql.DB
}

func NewStudyService(db *sql.DB) *StudyService {
	return &StudyService{db: db}
}

// StartStudySession creates a new study session for a group
func (s *StudyService) StartStudySession(groupID, activityID int) (*models.StudySession, error) {
	// Begin transaction
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer tx.Rollback()

	// Create study session
	session, err := models.CreateStudySession(s.db, groupID, activityID)
	if err != nil {
		return nil, err
	}

	// Commit transaction
	if err := tx.Commit(); err != nil {
		return nil, err
	}

	return session, nil
}

// SubmitWordReview records a word review result
func (s *StudyService) SubmitWordReview(sessionID, wordID int, correct bool) error {
	// Begin transaction
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Add word review
	if err := models.AddWordReview(s.db, sessionID, wordID, correct); err != nil {
		return err
	}

	// Commit transaction
	return tx.Commit()
}

// GetStudyProgress calculates overall study progress
func (s *StudyService) GetStudyProgress() (*models.StudyProgress, error) {
	return models.GetStudyProgress(s.db)
}

// GetStudyStats retrieves study statistics
func (s *StudyService) GetStudyStats() (*models.QuickStats, error) {
	return models.GetQuickStats(s.db)
}

// GetLastStudySession retrieves the most recent study session
func (s *StudyService) GetLastStudySession() (*models.LastStudySession, error) {
	return models.GetLastStudySession(s.db)
}

// GetStudySessionsByGroup retrieves study sessions for a specific group
func (s *StudyService) GetStudySessionsByGroup(groupID, page, perPage int) ([]models.StudySessionDetail, int, error) {
	return models.GetStudySessionsByGroup(s.db, groupID, page, perPage)
} 