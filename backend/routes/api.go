package routes

import (
	"asta-backend/controllers"
	"asta-backend/middleware"

	"github.com/gofiber/fiber/v2"
)

func SetupRoutes(app *fiber.App) {
	// Global Middleware
	app.Use(middleware.PanicRecovery())

	api := app.Group("/api/v1")

	// Health Check
	api.Get("/health", controllers.HealthCheck)

	// Routes Publiques
	auth := api.Group("/auth", middleware.AuthLimiter())
	auth.Post("/register", controllers.Register)
	auth.Post("/login", controllers.Login)
	auth.Post("/refresh", controllers.RefreshToken)

	// Routes Protégées
	protected := api.Group("/", middleware.Protected())

	// Auth routes protégées
	protected.Post("/auth/logout", controllers.Logout)
	protected.Get("/auth/me", controllers.Me)

	// Users
	users := protected.Group("/users")
	users.Get("/", controllers.GetAllUsers)
	users.Delete("/:id", controllers.DeleteUser)
	users.Patch("/:id/status", controllers.ToggleUserStatus)

	// Logs
	logs := protected.Group("/logs")
	logs.Get("/", controllers.GetAuditLogs)
	logs.Delete("/", controllers.ClearAuditLogs)

	// Dashboard
	protected.Get("/dashboard/metrics", controllers.GetDashboardMetrics)

	// Notes
	notes := protected.Group("/notes")
	notes.Get("/", controllers.GetNotes)
	notes.Post("/", controllers.SaveNote)
	notes.Delete("/:id", controllers.DeleteNote)

	// Progress & XP
	progress := protected.Group("/progress")
	progress.Get("/", controllers.GetProgress)
	progress.Post("/", controllers.UpdateProgress)
	progress.Get("/xp", controllers.GetWeeklyXP)
	progress.Post("/xp", controllers.LogXP)

	// Quiz
	quiz := protected.Group("/quiz")
	quiz.Get("/", controllers.GetQuizStats)
	quiz.Post("/", controllers.UpdateQuizStats)

	// Grades
	grades := protected.Group("/grades")
	grades.Get("/", controllers.GetUserGrades)
	grades.Post("/", controllers.SaveUserGrades)

	// Missions
	missions := protected.Group("/missions")
	missions.Get("/", controllers.GetCompletedMissions)
	missions.Post("/", controllers.AddCompletedMission)
}
