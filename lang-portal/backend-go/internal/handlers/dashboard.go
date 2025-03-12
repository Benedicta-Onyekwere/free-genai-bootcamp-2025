package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type DashboardHandler struct {
	service *service.CompositeService
}

func NewDashboardHandler(svc *service.CompositeService) *DashboardHandler {
	return &DashboardHandler{service: svc}
}

// RegisterRoutes registers all routes for the dashboard handler
func (h *DashboardHandler) RegisterRoutes(r *gin.RouterGroup) {
	dashboard := r.Group("/dashboard")
	{
		dashboard.GET("/last_study_session", h.GetLastStudySession)
		dashboard.GET("/study_progress", h.GetStudyProgress)
		dashboard.GET("/quick-stats", h.GetQuickStats)
	}
}

// GetLastStudySession handles GET /api/dashboard/last_study_session
func (h *DashboardHandler) GetLastStudySession(c *gin.Context) {
	session, err := h.service.GetLastStudySession()
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "No study sessions found"})
		return
	}

	c.JSON(http.StatusOK, session)
}

// GetStudyProgress handles GET /api/dashboard/study_progress
func (h *DashboardHandler) GetStudyProgress(c *gin.Context) {
	progress, err := h.service.GetStudyProgress()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, progress)
}

// GetQuickStats handles GET /api/dashboard/quick-stats
func (h *DashboardHandler) GetQuickStats(c *gin.Context) {
	stats, err := h.service.GetQuickStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, stats)
} 