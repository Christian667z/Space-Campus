package main

import (
	"log"
	"os"

	"asta-backend/config"
	"asta-backend/models"
	"asta-backend/routes"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/joho/godotenv"
)

func main() {
	// Charger les variables d'environnement
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found, relying on system environment variables")
	}

	// Connecter à la base de données
	config.ConnectDB()

	// Migrations GORM
	err = config.DB.AutoMigrate(
		&models.User{}, 
		&models.RefreshToken{},
		&models.AuditLog{},
		&models.AdminLog{},
		&models.Note{},
		&models.Progress{},
		&models.DailyXP{},
		&models.QuizStat{},
		&models.CompletedMission{},
		&models.UserGrade{},
	)
	if err != nil {
		log.Fatal("Migration failed:", err)
	}

	// Initialiser l'application Fiber
	app := fiber.New(fiber.Config{
		AppName: "Asta Académie Backend v2.0",
	})

	// Middlewares
	app.Use(recover.New())
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowHeaders: "Origin, Content-Type, Accept, Authorization",
	}))

	// Routes de base
	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"status":  "success",
			"message": "Bienvenue sur l'API Asta Académie (Go + PostgreSQL)",
		})
	})

	// Initialiser les routes
	routes.SetupRoutes(app)

	// Démarrer le serveur
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	
	log.Printf("Server listening on port %s", port)
	log.Fatal(app.Listen(":" + port))
}
