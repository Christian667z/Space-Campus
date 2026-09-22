package models

import (
	"time"
)

type AdminLog struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	UserID    uint      `gorm:"index" json:"user_id"`
	User      User      `gorm:"foreignKey:UserID" json:"user,omitempty"`
	Action    string    `gorm:"not null" json:"action"`
	Target    string    `json:"target"`
	CreatedAt time.Time `gorm:"autoCreateTime;index" json:"created_at"`
}
