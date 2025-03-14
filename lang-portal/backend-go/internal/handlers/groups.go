package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type GroupsHandler struct {
	service *service.CompositeService
}

func NewGroupsHandler(svc *service.CompositeService) *GroupsHandler {
	return &GroupsHandler{service: svc}
}

// RegisterRoutes registers all routes for the groups handler
func (h *GroupsHandler) RegisterRoutes(r *gin.RouterGroup) {
	groups := r.Group("/groups")
	{
		groups.GET("", h.ListGroups)
		groups.GET("/:id", h.GetGroup)
		groups.GET("/:id/words", h.ListGroupWords)
		groups.GET("/:id/study_sessions", h.ListGroupStudySessions)
	}
}

// ListGroups handles GET /api/groups
func (h *GroupsHandler) ListGroups(c *gin.Context) {
	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	groups, total, err := h.service.GetGroups(page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	totalPages := (total + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": groups,
		"pagination": gin.H{
			"current_page":    page,
			"total_pages":     totalPages,
			"total_items":     total,
			"items_per_page":  perPage,
		},
	})
}

// GetGroup handles GET /api/groups/:id
func (h *GroupsHandler) GetGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid group ID"})
		return
	}

	group, err := h.service.GetGroupByID(id)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "Group not found"})
		return
	}

	c.JSON(http.StatusOK, group)
}

// ListGroupWords handles GET /api/groups/:id/words
func (h *GroupsHandler) ListGroupWords(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid group ID"})
		return
	}

	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	words, total, err := h.service.GetGroupWords(id, page, perPage)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "Group not found or error retrieving words"})
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

// ListGroupStudySessions handles GET /api/groups/:id/study_sessions
func (h *GroupsHandler) ListGroupStudySessions(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid group ID"})
		return
	}

	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	// Explicitly use StudySessionService to avoid ambiguity
	sessions, total, err := h.service.StudySessionService.GetStudySessionsByGroup(id, page, perPage)
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