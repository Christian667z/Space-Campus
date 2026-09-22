package controllers

import (
	"asta-backend/config"

	"github.com/gofiber/fiber/v2"
)

func HealthCheck(c *fiber.Ctx) error {
	// Vérifie si la connexion à la base de données est active
	db, err := config.DB.DB()
	dbStatus := "down"
	if err == nil {
		if err := db.Ping(); err == nil {
			dbStatus = "up"
		}
	}

	status := "ok"
	if dbStatus == "down" {
		status = "degraded"
	}

	return c.JSON(fiber.Map{
		"status": status,
		"db":     dbStatus,
	})
}
