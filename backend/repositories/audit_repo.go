package repositories

import (
	"asta-backend/config"
	"asta-backend/models"
)

type AuditRepository interface {
	LogAction(userID uint, action string, target string) error
	GetRecentLogs(limit int) ([]models.AdminLog, error)
}

type auditRepository struct{}

func NewAuditRepository() AuditRepository {
	return &auditRepository{}
}

func (r *auditRepository) LogAction(userID uint, action string, target string) error {
	log := models.AdminLog{
		UserID: userID,
		Action: action,
		Target: target,
	}
	return config.DB.Create(&log).Error
}

func (r *auditRepository) GetRecentLogs(limit int) ([]models.AdminLog, error) {
	var logs []models.AdminLog
	err := config.DB.Order("created_at desc").Limit(limit).Preload("User").Find(&logs).Error
	return logs, err
}
