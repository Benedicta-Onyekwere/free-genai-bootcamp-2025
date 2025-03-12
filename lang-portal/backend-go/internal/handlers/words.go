package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/backend-go/internal/service"
)

type WordsHandler struct {
	service *service.CompositeService
}

func NewWordsHandler(svc *service.CompositeService) *WordsHandler {
	return &WordsHandler{service: svc}
}

// RegisterRoutes registers all routes for the words handler
func (h *WordsHandler) RegisterRoutes(r *gin.RouterGroup) {
	words := r.Group("/words")
	{
		words.GET("", h.ListWords)
		words.GET("/:id", h.GetWord)
	}
}

// ListWords handles GET /api/words
func (h *WordsHandler) ListWords(c *gin.Context) {
	page, err := strconv.Atoi(c.DefaultQuery("page", "1"))
	if err != nil || page < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid page number"})
		return
	}

	perPage := 100 // As per specification

	words, total, err := h.service.GetWords(page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
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

// GetWord handles GET /api/words/:id
func (h *WordsHandler) GetWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid word ID"})
		return
	}

	word, err := h.service.GetWordByID(id)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "sql: no rows in result set" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": "Word not found"})
		return
	}

	c.JSON(http.StatusOK, word)
} 