package controllers

import (
	"asta-backend/repositories"
	"asta-backend/services"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

var (
	userRepo    = repositories.NewUserRepository()
	tokenRepo   = repositories.NewTokenRepository()
	authService = services.NewAuthService(userRepo, tokenRepo)
)

type AuthRequest struct {
	Nom      string `json:"nom"`
	Password string `json:"password"`
}

type RefreshRequest struct {
	UserID       uint   `json:"user_id"`
	RefreshToken string `json:"refresh_token"`
	DeviceName   string `json:"device_name"`
}

type LoginRequest struct {
	Nom        string `json:"nom"`
	Password   string `json:"password"`
	DeviceName string `json:"device_name"`
}

func Register(c *fiber.Ctx) error {
	var req AuthRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Requête invalide"})
	}

	user, err := authService.Register(req.Nom, req.Password)
	if err != nil {
		status := fiber.StatusInternalServerError
		if err.Error() == "utilisateur déjà existant" || err.Error() == "le mot de passe doit contenir au moins 8 caractères" {
			status = fiber.StatusBadRequest
		}
		return c.Status(status).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{
		"message": "Utilisateur enregistré avec succès",
		"user":    user,
	})
}

func Login(c *fiber.Ctx) error {
	var req LoginRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Requête invalide"})
	}

	if req.DeviceName == "" {
		req.DeviceName = "unknown"
	}

	accessToken, refreshToken, user, err := authService.Login(req.Nom, req.Password, req.DeviceName)
	if err != nil {
		status := fiber.StatusUnauthorized
		if err.Error() == "compte bloqué" {
			status = fiber.StatusForbidden
		}
		return c.Status(status).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{
		"access_token":  accessToken,
		"refresh_token": refreshToken,
		"user":          user,
	})
}

func RefreshToken(c *fiber.Ctx) error {
	var req RefreshRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Requête invalide"})
	}

	accessToken, refreshToken, err := authService.RefreshToken(req.UserID, req.RefreshToken, req.DeviceName)
	if err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{
		"access_token":  accessToken,
		"refresh_token": refreshToken,
	})
}

func Logout(c *fiber.Ctx) error {
	type LogoutReq struct {
		UserID uint `json:"user_id"`
	}
	var req LogoutReq
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Requête invalide"})
	}

	if err := authService.Logout(req.UserID); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Erreur lors de la déconnexion"})
	}

	return c.JSON(fiber.Map{"message": "Déconnexion réussie"})
}

func Me(c *fiber.Ctx) error {
	userToken, ok := c.Locals("user").(*jwt.Token)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Token invalide"})
	}
	claims, ok := userToken.Claims.(jwt.MapClaims)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Claims invalides"})
	}
	
	userIDFloat, ok := claims["sub"].(float64)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "ID utilisateur invalide dans le token"})
	}

	user, err := userRepo.FindByID(uint(userIDFloat))
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Utilisateur non trouvé"})
	}

	return c.JSON(fiber.Map{"user": user})
}
