package controllers

import (
	"asta-backend/config"
	"asta-backend/models"

	"github.com/gofiber/fiber/v2"
)

func GetAllUsers(c *fiber.Ctx) error {
	var users []models.User
	// Select id, nom, is_active, created_at
	config.DB.Select("id", "nom", "is_active", "created_at").Find(&users)
	return c.JSON(users)
}

func DeleteUser(c *fiber.Ctx) error {
	id := c.Params("id")
	
	// GORM supprime en cascade si bien configuré, sinon suppression manuelle
	config.DB.Where("user_id = ?", id).Delete(&models.AuditLog{})
	config.DB.Delete(&models.User{}, id)
	
	return c.JSON(fiber.Map{"message": "User deleted successfully"})
}

func ToggleUserStatus(c *fiber.Ctx) error {
	id := c.Params("id")
	
	type Request struct {
		IsActive bool `json:"is_active"`
	}
	var req Request
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid input"})
	}

	config.DB.Model(&models.User{}).Where("id = ?", id).Update("is_active", req.IsActive)
	return c.JSON(fiber.Map{"message": "User status updated"})
}
