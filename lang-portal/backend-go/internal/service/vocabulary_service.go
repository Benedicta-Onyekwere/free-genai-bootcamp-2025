package service

import (
	"database/sql"
	"lang-portal/backend-go/internal/models"
)

type VocabularyService struct {
	db *sql.DB
}

func NewVocabularyService(db *sql.DB) *VocabularyService {
	return &VocabularyService{db: db}
}

// GetWords retrieves a paginated list of words
func (s *VocabularyService) GetWords(page, perPage int) ([]models.WordWithStats, int, error) {
	return models.GetWords(s.db, page, perPage)
}

// GetWordByID retrieves a single word by its ID
func (s *VocabularyService) GetWordByID(id int) (*models.WordWithStats, error) {
	return models.GetWordByID(s.db, id)
}

// GetGroups retrieves a paginated list of groups
func (s *VocabularyService) GetGroups(page, perPage int) ([]models.GroupWithStats, int, error) {
	return models.GetGroups(s.db, page, perPage)
}

// GetGroupByID retrieves a single group by its ID
func (s *VocabularyService) GetGroupByID(id int) (*models.GroupWithStats, error) {
	return models.GetGroupByID(s.db, id)
}

// GetGroupWords retrieves words for a specific group
func (s *VocabularyService) GetGroupWords(groupID, page, perPage int) ([]models.WordWithStats, int, error) {
	return models.GetGroupWords(s.db, groupID, page, perPage)
}

// ResetHistory clears all study history
func (s *VocabularyService) ResetHistory() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Delete all word review items
	if _, err := tx.Exec("DELETE FROM word_review_items"); err != nil {
		return err
	}

	// Delete all study sessions
	if _, err := tx.Exec("DELETE FROM study_sessions"); err != nil {
		return err
	}

	return tx.Commit()
}

// FullReset resets the entire system
func (s *VocabularyService) FullReset() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Delete all data
	tables := []string{
		"word_review_items",
		"study_sessions",
		"words_groups",
		"words",
		"groups",
		"study_activities",
	}

	for _, table := range tables {
		if _, err := tx.Exec("DELETE FROM " + table); err != nil {
			return err
		}
	}

	return tx.Commit()
} 