package models

import (
	"time"

	"gorm.io/gorm"
)

type User struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	Nom       string         `gorm:"uniqueIndex;not null" json:"nom"`
	Password  string         `gorm:"not null" json:"-"` // Non exposé dans le JSON
	Role      string         `gorm:"default:'ROLE_USER'" json:"role"`
	IsActive  bool           `gorm:"default:true;index" json:"is_active"`
	HWID      string         `json:"hwid"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

const (
	RoleUser  = "ROLE_USER"
	RoleAdmin = "ROLE_ADMIN"
	RoleOwner = "ROLE_OWNER"
)
