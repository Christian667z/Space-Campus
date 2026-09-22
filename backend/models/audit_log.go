package models

import (
	"time"
)

type AuditLog struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	UserID    uint      `gorm:"index" json:"user_id"`
	User      User      `gorm:"foreignKey:UserID" json:"user,omitempty"`
	Level     string    `gorm:"index;not null" json:"level"` // SYSTEM, ERROR, SECURITY, HACKING
	Action    string    `gorm:"not null" json:"action"`
	Timestamp time.Time `gorm:"autoCreateTime;index" json:"timestamp"`
}
