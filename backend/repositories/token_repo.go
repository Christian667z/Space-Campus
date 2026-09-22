package repositories

import (
	"asta-backend/config"
	"asta-backend/models"
	"time"
)

type TokenRepository interface {
	Create(token *models.RefreshToken) error
	FindByUserIDAndDevice(userID uint, deviceName string) (*models.RefreshToken, error)
	Revoke(id uint) error
	RevokeAllForUser(userID uint) error
}

type tokenRepository struct{}

func NewTokenRepository() TokenRepository {
	return &tokenRepository{}
}

func (r *tokenRepository) Create(token *models.RefreshToken) error {
	return config.DB.Create(token).Error
}

func (r *tokenRepository) FindByUserIDAndDevice(userID uint, deviceName string) (*models.RefreshToken, error) {
	var token models.RefreshToken
	err := config.DB.Where("user_id = ? AND device_name = ? AND revoked = ? AND expires_at > ?", userID, deviceName, false, time.Now()).First(&token).Error
	return &token, err
}

func (r *tokenRepository) Revoke(id uint) error {
	return config.DB.Model(&models.RefreshToken{}).Where("id = ?", id).Update("revoked", true).Error
}

func (r *tokenRepository) RevokeAllForUser(userID uint) error {
	return config.DB.Model(&models.RefreshToken{}).Where("user_id = ? AND revoked = ?", userID, false).Update("revoked", true).Error
}
