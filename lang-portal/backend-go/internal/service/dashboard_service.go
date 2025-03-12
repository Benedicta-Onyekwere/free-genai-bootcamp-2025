package service

import (
	"lang-portal/backend-go/internal/models"
)

// DashboardService handles business logic for the dashboard
type DashboardService struct {
	*BaseService
}

// NewDashboardService creates a new dashboard service
func NewDashboardService(base *BaseService) *DashboardService {
	return &DashboardService{BaseService: base}
}

// GetLastStudySession retrieves information about the most recent study session
func (s *DashboardService) GetLastStudySession() (interface{}, error) {
	return models.GetLastStudySession(s.db)
}

// GetStudyProgress retrieves overall study progress statistics
func (s *DashboardService) GetStudyProgress() (interface{}, error) {
	return models.GetStudyProgress(s.db)
}

// GetQuickStats retrieves quick overview statistics
func (s *DashboardService) GetQuickStats() (interface{}, error) {
	return models.GetQuickStats(s.db)
} 