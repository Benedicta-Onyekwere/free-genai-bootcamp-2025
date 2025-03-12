package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type ResetHandler struct {
	service *service.CompositeService
}

func NewResetHandler(svc *service.CompositeService) *ResetHandler {
	return &ResetHandler{service: svc}
}

// RegisterRoutes registers all routes for the reset handler
func (h *ResetHandler) RegisterRoutes(r *gin.RouterGroup) {
	reset := r.Group("/reset")
	{
		reset.POST("/history", h.ResetHistory)
		reset.POST("/full", h.FullReset)
	}
}

// ResetHistory handles POST /api/reset/history
func (h *ResetHandler) ResetHistory(c *gin.Context) {
	err := h.service.ResetHistory()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": true, "message": "Study history has been reset"})
}

// FullReset handles POST /api/reset/full
func (h *ResetHandler) FullReset(c *gin.Context) {
	err := h.service.FullReset()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": true, "message": "System has been fully reset"})
} 