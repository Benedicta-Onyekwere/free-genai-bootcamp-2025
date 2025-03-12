package main

import (
	"database/sql"
	"log"
	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"lang-portal/backend-go/internal/handlers"
	"lang-portal/backend-go/internal/service"
)

func main() {
	// Open database connection
	db, err := sql.Open("sqlite3", "./words.db")
	if err != nil {
		log.Fatal("Failed to open database:", err)
	}
	defer db.Close()

	// Test database connection
	if err := db.Ping(); err != nil {
		log.Fatal("Failed to ping database:", err)
	}

	// Create a default gin router
	r := gin.Default()

	// Add CORS middleware
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		
		c.Next()

		// Error handling
		if len(c.Errors) > 0 {
			c.JSON(-1, gin.H{"errors": c.Errors.JSON()})
		}
	})

	// Create composite service
	svc := service.NewCompositeService(db)

	// Create handlers
	wordsHandler := handlers.NewWordsHandler(svc)
	groupsHandler := handlers.NewGroupsHandler(svc)
	studySessionsHandler := handlers.NewStudySessionsHandler(svc)
	dashboardHandler := handlers.NewDashboardHandler(svc)
	studyActivitiesHandler := handlers.NewStudyActivitiesHandler(svc)
	resetHandler := handlers.NewResetHandler(svc)

	// API routes
	api := r.Group("/api")
	{
		// Register routes for each handler
		wordsHandler.RegisterRoutes(api)
		groupsHandler.RegisterRoutes(api)
		studySessionsHandler.RegisterRoutes(api)
		dashboardHandler.RegisterRoutes(api)
		studyActivitiesHandler.RegisterRoutes(api)
		resetHandler.RegisterRoutes(api)
	}

	// Start the server
	log.Println("Starting server on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatal("Failed to start server:", err)
	}
} 