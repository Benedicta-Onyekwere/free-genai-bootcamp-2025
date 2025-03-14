package service

import (
	"database/sql"
	"errors"
	"log"
	"lang-portal/backend-go/internal/models"
)

type StudyActivityService struct {
	*BaseService
}

func NewStudyActivityService(base *BaseService) *StudyActivityService {
	log.Printf("Creating new StudyActivityService with base service: %+v", base)
	if base == nil {
		log.Fatal("StudyActivityService: base service cannot be nil")
	}
	if base.GetDB() == nil {
		log.Fatal("StudyActivityService: database connection cannot be nil")
	}
	return &StudyActivityService{base}
}

func (s *StudyActivityService) CreateStudyActivity(name, description, thumbnailURL string) (*models.StudyActivity, error) {
	log.Printf("StudyActivityService: Creating study activity with name=%s, description=%s", name, description)
	if s.GetDB() == nil {
		log.Printf("StudyActivityService: Database connection is nil!")
		return nil, errors.New("database connection is not initialized")
	}
	activity, err := models.CreateStudyActivity(s.GetDB(), name, description, thumbnailURL)
	if err != nil {
		log.Printf("StudyActivityService: Error creating study activity: %v", err)
		return nil, err
	}
	if activity == nil {
		log.Printf("StudyActivityService: Model returned nil activity without error")
		return nil, errors.New("failed to create study activity")
	}
	log.Printf("StudyActivityService: Created study activity with ID=%d", activity.ID)
	return activity, nil
}

func (s *StudyActivityService) GetStudyActivityByID(id int) (*models.StudyActivity, error) {
	log.Printf("StudyActivityService: Getting study activity with ID=%d", id)
	if s.GetDB() == nil {
		log.Printf("StudyActivityService: Database connection is nil!")
		return nil, errors.New("database connection is not initialized")
	}
	activity, err := models.GetStudyActivityByID(s.GetDB(), id)
	if err != nil {
		if err == sql.ErrNoRows {
			log.Printf("StudyActivityService: Study activity not found: %d", id)
		} else {
			log.Printf("StudyActivityService: Error getting study activity: %v", err)
		}
		return nil, err
	}
	if activity == nil {
		log.Printf("StudyActivityService: Model returned nil activity without error")
		return nil, sql.ErrNoRows
	}
	return activity, nil
}

func (s *StudyActivityService) GetStudyActivities() ([]*models.StudyActivity, error) {
	log.Printf("StudyActivityService: Getting all study activities")
	if s.GetDB() == nil {
		log.Printf("StudyActivityService: Database connection is nil!")
		return nil, errors.New("database connection is not initialized")
	}
	activities, err := models.GetStudyActivities(s.GetDB())
	if err != nil {
		log.Printf("StudyActivityService: Error getting study activities: %v", err)
		return nil, err
	}
	if activities == nil {
		activities = []*models.StudyActivity{}
	}
	log.Printf("StudyActivityService: Found %d study activities", len(activities))
	return activities, nil
} 