package service

import (
	"lang-portal/backend-go/internal/models"
)

// WordService handles business logic for words
type WordService struct {
	*BaseService
}

// NewWordService creates a new word service
func NewWordService(base *BaseService) *WordService {
	return &WordService{BaseService: base}
}

// GetWords retrieves a paginated list of words
func (s *WordService) GetWords(page, perPage int) (interface{}, int, error) {
	return models.GetWords(s.db, page, perPage)
}

// GetWordByID retrieves a single word by ID
func (s *WordService) GetWordByID(id int) (interface{}, error) {
	return models.GetWordByID(s.db, id)
}

// GetWordsByGroup retrieves words for a specific group
func (s *WordService) GetWordsByGroup(groupID, page, perPage int) (interface{}, int, error) {
	return models.GetGroupWords(s.db, groupID, page, perPage)
}

// GetWordsByStudySession retrieves words for a specific study session
func (s *WordService) GetWordsByStudySession(sessionID, page, perPage int) (interface{}, int, error) {
	return models.GetStudySessionWords(s.db, sessionID, page, perPage)
} 