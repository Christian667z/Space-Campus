package middleware

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/recover"
)

// PanicRecovery intercepte les paniques et évite le crash du serveur
func PanicRecovery() fiber.Handler {
	return recover.New(recover.Config{
		EnableStackTrace: true,
	})
}
