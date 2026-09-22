package controllers

import (
	"strconv"
	"time"

	"asta-backend/config"
	"asta-backend/models"

	"github.com/gofiber/fiber/v2"
)

func GetAuditLogs(c *fiber.Ctx) error {
	limit, _ := strconv.Atoi(c.Query("limit", "500"))
	offset, _ := strconv.Atoi(c.Query("offset", "0"))
	levelFilter := c.Query("level", "ALL")
	searchKw := c.Query("search", "")

	var logs []models.AuditLog
	query := config.DB.Preload("User").Order("id desc")

	if levelFilter != "ALL" {
		query = query.Where("level = ?", levelFilter)
	}

	if searchKw != "" {
		query = query.Joins("LEFT JOIN users ON users.id = audit_logs.user_id").
			Where("audit_logs.action LIKE ? OR users.nom LIKE ?", "%"+searchKw+"%", "%"+searchKw+"%")
	}

	var total int64
	query.Model(&models.AuditLog{}).Count(&total)

	query.Limit(limit).Offset(offset).Find(&logs)

	// Format pour coller avec l'UI Python
	var formattedLogs []map[string]interface{}
	for _, l := range logs {
		nom := "SYSTEM"
		hwid := "N/A"
		if l.User.ID != 0 {
			nom = l.User.Nom
			hwid = l.User.HWID
		}
		formattedLogs = append(formattedLogs, map[string]interface{}{
			"id":        l.ID,
			"timestamp": l.Timestamp.Format("2006-01-02 15:04:05"),
			"nom":       nom,
			"level":     l.Level,
			"action":    l.Action,
			"hwid":      hwid,
		})
	}

	return c.JSON(fiber.Map{
		"total": total,
		"logs":  formattedLogs,
	})
}

func ClearAuditLogs(c *fiber.Ctx) error {
	config.DB.Exec("DELETE FROM audit_logs")
	return c.JSON(fiber.Map{"message": "All logs cleared"})
}

func GetDashboardMetrics(c *fiber.Ctx) error {
	var totalUsers int64
	var activeUsers int64
	var todayErrors int64

	config.DB.Model(&models.User{}).Count(&totalUsers)
	config.DB.Model(&models.User{}).Where("is_active = ?", true).Count(&activeUsers)
	
	today := time.Now().Format("2006-01-02")
	config.DB.Model(&models.AuditLog{}).
		Where("level = ? AND DATE(timestamp) = ?", "ERROR", today).
		Count(&todayErrors)

	var stats []struct {
		Level string
		Count int
	}
	config.DB.Model(&models.AuditLog{}).Select("level, count(*) as count").Group("level").Scan(&stats)

	chartStats := map[string]int{"SYSTEM": 0, "SECURITY": 0, "ERROR": 0, "HACKING": 0}
	for _, s := range stats {
		chartStats[s.Level] = s.Count
	}

	return c.JSON(fiber.Map{
		"total_users":  totalUsers,
		"active_users": activeUsers,
		"today_errors": todayErrors,
		"chart_stats":  chartStats,
	})
}
