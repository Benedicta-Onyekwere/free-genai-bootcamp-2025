package service

import (
	"lang-portal/backend-go/internal/models"
)

// StudySessionService handles business logic for study sessions
type StudySessionService struct {
	*BaseService
}

// NewStudySessionService creates a new study session service
func NewStudySessionService(base *BaseService) *StudySessionService {
	return &StudySessionService{BaseService: base}
}

// GetStudySessions retrieves a paginated list of study sessions
func (s *StudySessionService) GetStudySessions(page, perPage int) (interface{}, int, error) {
	return models.GetStudySessions(s.db, page, perPage)
}

// GetStudySessionByID retrieves a single study session by ID
func (s *StudySessionService) GetStudySessionByID(id int) (interface{}, error) {
	return models.GetStudySessionByID(s.db, id)
}

// GetStudySessionWords retrieves words for a specific study session
func (s *StudySessionService) GetStudySessionWords(sessionID, page, perPage int) (interface{}, int, error) {
	return models.GetStudySessionWords(s.db, sessionID, page, perPage)
}

// CreateStudySession creates a new study session
func (s *StudySessionService) CreateStudySession(groupID, activityID int) (interface{}, error) {
	return models.CreateStudySession(s.db, groupID, activityID)
}

// AddWordReview adds a word review to a study session
func (s *StudySessionService) AddWordReview(sessionID, wordID int, correct bool) error {
	return models.AddWordReview(s.db, sessionID, wordID, correct)
}

// GetStudySessionsByGroup retrieves study sessions for a specific group
func (s *StudySessionService) GetStudySessionsByGroup(groupID, page, perPage int) (interface{}, int, error) {
	return models.GetStudySessionsByGroup(s.db, groupID, page, perPage)
} 