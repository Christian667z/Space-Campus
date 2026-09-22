package models

import (
	"time"

	"gorm.io/gorm"
)

type RefreshToken struct {
	ID         uint           `gorm:"primaryKey" json:"id"`
	UserID     uint           `gorm:"index;not null" json:"user_id"`
	User       User           `gorm:"foreignKey:UserID;constraint:OnDelete:CASCADE;" json:"-"`
	TokenHash  string         `gorm:"not null" json:"-"`
	ExpiresAt  time.Time      `gorm:"not null" json:"expires_at"`
	Revoked    bool           `gorm:"default:false;index" json:"revoked"`
	DeviceName string         `json:"device_name"`
	CreatedAt  time.Time      `json:"created_at"`
	UpdatedAt  time.Time      `json:"updated_at"`
	DeletedAt  gorm.DeletedAt `gorm:"index" json:"-"`
}
