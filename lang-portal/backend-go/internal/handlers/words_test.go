package handlers

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"lang-portal/backend-go/internal/service"
)

func setupTestDB() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		return nil, err
	}

	// Run migrations or create tables needed for tests
	_, err = db.Exec(`CREATE TABLE words (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		japanese TEXT,
		romaji TEXT,
		english TEXT
	)`)
	if err != nil {
		return nil, err
	}

	// Add initial data to the test database
	_, err = db.Exec(`INSERT INTO words (japanese, romaji, english) VALUES ('こんにちは', 'konnichiwa', 'hello')`)
	if err != nil {
		return nil, err
	}

	return db, nil
}

func TestListWords(t *testing.T) {
	// Set up a test router
	gin.SetMode(gin.TestMode)
	r := gin.Default()

	// Initialize test database
	db, err := setupTestDB()
	if err != nil {
		t.Fatalf("Failed to set up test database: %v", err)
	}
	defer db.Close()

	// Initialize service with test database
	compositeService := service.NewCompositeService(db)

	wordsHandler := NewWordsHandler(compositeService)
	wordsHandler.RegisterRoutes(r.Group("/api"))

	// Create a test request
	req, _ := http.NewRequest(http.MethodGet, "/api/words", nil)
	w := httptest.NewRecorder()

	// Perform the request
	r.ServeHTTP(w, req)

	// Check the response
	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "items")
}

func TestGetWord(t *testing.T) {
	// Set up a test router
	gin.SetMode(gin.TestMode)
	r := gin.Default()

	// Mock service
	mockService := &service.CompositeService{}
	wordsHandler := NewWordsHandler(mockService)
	wordsHandler.RegisterRoutes(r.Group("/api"))

	// Create a test request
	req, _ := http.NewRequest(http.MethodGet, "/api/words/1", nil)
	w := httptest.NewRecorder()

	// Perform the request
	r.ServeHTTP(w, req)

	// Check the response
	assert.Equal(t, http.StatusOK, w.Code)
	assert.Contains(t, w.Body.String(), "japanese")
} 