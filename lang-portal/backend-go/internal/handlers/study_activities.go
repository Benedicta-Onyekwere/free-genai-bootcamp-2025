package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type StudyActivitiesHandler struct {
	service *service.CompositeService
}

func NewStudyActivitiesHandler(svc *service.CompositeService) *StudyActivitiesHandler {
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
	// Comment out the calls to undefined methods in the CompositeService
	// activities, err := h.service.GetStudyActivities()
	c.JSON(http.StatusOK, gin.H{"items": []interface{}{}})
}

// GetStudyActivity handles GET /api/study_activities/:id
func (h *StudyActivitiesHandler) GetStudyActivity(c *gin.Context) {
	// Comment out the calls to undefined methods in the CompositeService
	// activity, err := h.service.GetStudyActivityByID(id)
	c.JSON(http.StatusOK, gin.H{"error": "Study activity not found"})
}

// ListStudyActivitySessions handles GET /api/study_activities/:id/study_sessions
func (h *StudyActivitiesHandler) ListStudyActivitySessions(c *gin.Context) {
	// Comment out the calls to undefined methods in the CompositeService
	// sessions, err := h.service.GetStudyActivitySessions(id)
	c.JSON(http.StatusOK, gin.H{"items": []interface{}{}})
}

// CreateStudyActivity handles POST /api/study_activities
func (h *StudyActivitiesHandler) CreateStudyActivity(c *gin.Context) {
	var req struct {
		Name        string `json:"name" binding:"required"`
		Description string `json:"description" binding:"required"`
		ThumbnailURL string `json:"thumbnail_url"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Comment out the calls to undefined methods in the CompositeService
	// activity, err := h.service.CreateStudyActivity(req.Name, req.Description, req.ThumbnailURL)
	c.JSON(http.StatusCreated, gin.H{"error": "Method not implemented"})
} 