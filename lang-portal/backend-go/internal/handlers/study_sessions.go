package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type StudySessionsHandler struct {
	service *service.CompositeService
}

func NewStudySessionsHandler(svc *service.CompositeService) *StudySessionsHandler {
	return &StudySessionsHandler{service: svc}
}

// RegisterRoutes registers all routes for the study sessions handler
func (h *StudySessionsHandler) RegisterRoutes(r *gin.RouterGroup) {
	sessions := r.Group("/study_sessions")
	{
		sessions.GET("", h.ListStudySessions)
		sessions.GET("/:id", h.GetStudySession)
		sessions.GET("/:id/words", h.ListStudySessionWords)
		sessions.POST("", h.CreateStudySession)
		sessions.POST("/:id/words/:word_id/review", h.AddWordReview)
	}
}

// ListStudySessions handles GET /api/study_sessions
func (h *StudySessionsHandler) ListStudySessions(c *gin.Context) {
	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	sessions, total, err := h.service.GetStudySessions(page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	totalPages := (total + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": sessions,
		"pagination": gin.H{
			"current_page":    page,
			"total_pages":     totalPages,
			"total_items":     total,
			"items_per_page":  perPage,
		},
	})
}

// GetStudySession handles GET /api/study_sessions/:id
func (h *StudySessionsHandler) GetStudySession(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	session, err := h.service.GetStudySessionByID(id)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "Study session not found"})
		return
	}

	c.JSON(http.StatusOK, session)
}

// ListStudySessionWords handles GET /api/study_sessions/:id/words
func (h *StudySessionsHandler) ListStudySessionWords(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	words, total, err := h.service.GetStudySessionWords(id, page, perPage)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "Study session not found or error retrieving words"})
		return
	}

	totalPages := (total + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": words,
		"pagination": gin.H{
			"current_page":    page,
			"total_pages":     totalPages,
			"total_items":     total,
			"items_per_page":  perPage,
		},
	})
}

// CreateStudySession handles POST /api/study_sessions
func (h *StudySessionsHandler) CreateStudySession(c *gin.Context) {
	var req struct {
		GroupID         int `json:"group_id" binding:"required,min=1"`
		StudyActivityID int `json:"study_activity_id" binding:"required,min=1"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	session, err := h.service.CreateStudySession(req.GroupID, req.StudyActivityID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, session)
}

// AddWordReview handles POST /api/study_sessions/:id/words/:word_id/review
func (h *StudySessionsHandler) AddWordReview(c *gin.Context) {
	sessionID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	wordID, err := strconv.Atoi(c.Param("word_id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid word ID"})
		return
	}

	var req struct {
		Correct bool `json:"correct" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err = h.service.AddWordReview(sessionID, wordID, req.Correct)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success":          true,
		"word_id":         wordID,
		"study_session_id": sessionID,
		"correct":         req.Correct,
	})
} 