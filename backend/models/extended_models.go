package models

import (
	"time"
)

type Note struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	UserID    uint      `json:"user_id"`
	Titre     string    `gorm:"not null" json:"titre"`
	Contenu   string    `json:"contenu"`
	UpdatedAt time.Time `gorm:"autoUpdateTime" json:"updated_at"`
}

type Progress struct {
	ID     uint   `gorm:"primaryKey" json:"id"`
	UserID uint   `gorm:"uniqueIndex" json:"user_id"`
	Points int    `gorm:"default:0" json:"points"`
	Streak int    `gorm:"default:0" json:"streak"`
	Niveau string `gorm:"default:'L2'" json:"niveau"`
}

type DailyXP struct {
	ID       uint   `gorm:"primaryKey" json:"id"`
	UserID   uint   `gorm:"uniqueIndex:idx_user_date" json:"user_id"`
	DateStr  string `gorm:"uniqueIndex:idx_user_date;not null" json:"date_str"`
	XPEarned int    `gorm:"default:0" json:"xp_earned"`
}

type QuizStat struct {
	UserID    uint `gorm:"primaryKey" json:"user_id"`
	QuizScore int  `gorm:"default:0" json:"quiz_score"`
	QuizTotal int  `gorm:"default:0" json:"quiz_total"`
}

type CompletedMission struct {
	ID          uint      `gorm:"primaryKey" json:"id"`
	UserID      uint      `gorm:"uniqueIndex:idx_user_mission" json:"user_id"`
	MissionID   string    `gorm:"uniqueIndex:idx_user_mission;not null" json:"mission_id"`
	CompletedAt time.Time `gorm:"autoCreateTime" json:"completed_at"`
}

type UserGrade struct {
	ID      uint    `gorm:"primaryKey" json:"id"`
	UserID  uint    `json:"user_id"`
	Matiere string  `gorm:"not null" json:"matiere"`
	Intra   float64 `gorm:"default:0.0" json:"intra"`
	Final   float64 `gorm:"default:0.0" json:"final"`
}
