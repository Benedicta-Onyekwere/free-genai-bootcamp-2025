package handlers

import (
	"database/sql"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/models"
	"lang-portal/backend-go/internal/service"
)

type StudyActivitiesHandler struct {
	service *service.CompositeService
}

func NewStudyActivitiesHandler(svc *service.CompositeService) *StudyActivitiesHandler {
	if svc == nil {
		log.Fatal("StudyActivitiesHandler: service cannot be nil")
	}
	if svc.StudyActivityService == nil {
		log.Fatal("StudyActivitiesHandler: study activity service cannot be nil")
	}
	return &StudyActivitiesHandler{service: svc}
}

// RegisterRoutes registers all routes for the study activities handler
func (h *StudyActivitiesHandler) RegisterRoutes(r *gin.RouterGroup) {
	activities := r.Group("/study_activities")
	{
		activities.GET("", h.ListStudyActivities)
		activities.GET(":id", h.GetStudyActivity)
		activities.GET(":id/study_sessions", h.ListStudyActivitySessions)
		activities.POST("", h.CreateStudyActivity)
	}
}

// ListStudyActivities handles GET /api/study_activities
func (h *StudyActivitiesHandler) ListStudyActivities(c *gin.Context) {
	log.Printf("StudyActivitiesHandler: Listing study activities")
	activities, err := h.service.GetStudyActivities()
	if err != nil {
		log.Printf("StudyActivitiesHandler: Error getting study activities: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	if activities == nil {
		activities = []*models.StudyActivity{}
	}
	c.JSON(http.StatusOK, gin.H{"items": activities})
}

// GetStudyActivity handles GET /api/study_activities/:id
func (h *StudyActivitiesHandler) GetStudyActivity(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		log.Printf("StudyActivitiesHandler: Invalid ID format: %v", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID format"})
		return
	}

	log.Printf("StudyActivitiesHandler: Getting study activity with ID=%d", id)
	activity, err := h.service.GetStudyActivityByID(id)
	if err != nil {
		if err == sql.ErrNoRows {
			log.Printf("StudyActivitiesHandler: Study activity not found: %d", id)
			c.JSON(http.StatusNotFound, gin.H{"error": "Study activity not found"})
			return
		}
		log.Printf("StudyActivitiesHandler: Error getting study activity: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, activity)
}

// ListStudyActivitySessions handles GET /api/study_activities/:id/study_sessions
func (h *StudyActivitiesHandler) ListStudyActivitySessions(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"items": []interface{}{}})
}

// CreateStudyActivity handles POST /api/study_activities
func (h *StudyActivitiesHandler) CreateStudyActivity(c *gin.Context) {
	var req struct {
		Name         string `json:"name" binding:"required"`
		Description  string `json:"description" binding:"required"`
		ThumbnailURL string `json:"thumbnail_url"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		log.Printf("StudyActivitiesHandler: Invalid request body: %v", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	log.Printf("StudyActivitiesHandler: Creating study activity: %+v", req)
	activity, err := h.service.CreateStudyActivity(req.Name, req.Description, req.ThumbnailURL)
	if err != nil {
		log.Printf("StudyActivitiesHandler: Error creating study activity: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	if activity == nil {
		log.Printf("StudyActivitiesHandler: Service returned nil activity without error")
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create study activity"})
		return
	}

	c.JSON(http.StatusCreated, activity)
} 