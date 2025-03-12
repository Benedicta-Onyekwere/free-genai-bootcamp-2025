package service

import (
	"database/sql"
)

// CompositeService combines all services into one
type CompositeService struct {
	*WordService
	*GroupService
	*StudySessionService
	*DashboardService
	*SystemService
}

// NewCompositeService creates a new composite service
func NewCompositeService(db *sql.DB) *CompositeService {
	base := NewBaseService(db)
	return &CompositeService{
		WordService:         NewWordService(base),
		GroupService:        NewGroupService(base),
		StudySessionService: NewStudySessionService(base),
		DashboardService:    NewDashboardService(base),
		SystemService:       NewSystemService(base),
	}
} 