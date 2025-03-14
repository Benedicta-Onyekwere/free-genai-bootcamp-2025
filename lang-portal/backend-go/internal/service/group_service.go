package service

import (
	"lang-portal/backend-go/internal/models"
)

// GroupService handles business logic for groups
type GroupService struct {
	*BaseService
}

// NewGroupService creates a new group service
func NewGroupService(base *BaseService) *GroupService {
	return &GroupService{BaseService: base}
}

// GetGroups retrieves a paginated list of groups
func (s *GroupService) GetGroups(page, perPage int) (interface{}, int, error) {
	return models.GetGroups(s.db, page, perPage)
}

// GetGroupByID retrieves a single group by ID
func (s *GroupService) GetGroupByID(id int) (interface{}, error) {
	return models.GetGroupByID(s.db, id)
}

// GetGroupWords retrieves words for a specific group
func (s *GroupService) GetGroupWords(groupID, page, perPage int) (interface{}, int, error) {
	return models.GetGroupWords(s.db, groupID, page, perPage)
}