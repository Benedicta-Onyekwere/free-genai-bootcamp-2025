package service

import (
	"database/sql"
	"log"
	"lang-portal/backend-go/internal/models"
)

// CompositeService combines all services into one
type CompositeService struct {
	db *sql.DB
	*WordService
	*GroupService
	*StudySessionService
	*DashboardService
	*SystemService
	*StudyActivityService
}

// NewCompositeService creates a new composite service
func NewCompositeService(db *sql.DB) *CompositeService {
	base := NewBaseService(db)
	studyActivityService := NewStudyActivityService(base)
	log.Printf("Creating composite service with study activity service: %+v", studyActivityService)
	return &CompositeService{
		db:                  db,
		WordService:         NewWordService(base),
		GroupService:        NewGroupService(base),
		StudySessionService: NewStudySessionService(base),
		DashboardService:    NewDashboardService(base),
		SystemService:       NewSystemService(base),
		StudyActivityService: studyActivityService,
	}
}

// CreateStudyActivity creates a new study activity
func (s *CompositeService) CreateStudyActivity(name, description, thumbnailURL string) (*models.StudyActivity, error) {
	log.Printf("CompositeService: Creating study activity with name=%s, description=%s", name, description)
	if s.StudyActivityService == nil {
		log.Printf("CompositeService: StudyActivityService is nil!")
		return nil, nil
	}
	return s.StudyActivityService.CreateStudyActivity(name, description, thumbnailURL)
}

// GetStudyActivityByID retrieves a study activity by its ID
func (s *CompositeService) GetStudyActivityByID(id int) (*models.StudyActivity, error) {
	log.Printf("CompositeService: Getting study activity with ID=%d", id)
	if s.StudyActivityService == nil {
		log.Printf("CompositeService: StudyActivityService is nil!")
		return nil, nil
	}
	return s.StudyActivityService.GetStudyActivityByID(id)
}

// GetStudyActivities retrieves all study activities
func (s *CompositeService) GetStudyActivities() ([]*models.StudyActivity, error) {
	log.Printf("CompositeService: Getting all study activities")
	if s.StudyActivityService == nil {
		log.Printf("CompositeService: StudyActivityService is nil!")
		return nil, nil
	}
	return s.StudyActivityService.GetStudyActivities()
} 