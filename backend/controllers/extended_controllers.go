package controllers

import (
	"asta-backend/config"
	"asta-backend/models"
	"strconv"
	"github.com/gofiber/fiber/v2"
)

// --- Notes ---
func GetNotes(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var notes []models.Note
	config.DB.Where("user_id = ?", userID).Order("updated_at desc").Find(&notes)
	return c.JSON(notes)
}

func SaveNote(c *fiber.Ctx) error {
	note := new(models.Note)
	if err := c.BodyParser(note); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	if note.ID == 0 {
		config.DB.Create(&note)
	} else {
		config.DB.Save(&note)
	}
	return c.JSON(note)
}

func DeleteNote(c *fiber.Ctx) error {
	id := c.Params("id")
	config.DB.Delete(&models.Note{}, id)
	return c.SendStatus(204)
}

// --- Progress & XP ---
func GetProgress(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var prog models.Progress
	if err := config.DB.Where("user_id = ?", userID).First(&prog).Error; err != nil {
		// Create default
		uid, _ := strconv.Atoi(userID)
		prog = models.Progress{UserID: uint(uid), Niveau: "L2"}
		config.DB.Create(&prog)
	}
	return c.JSON(prog)
}

func UpdateProgress(c *fiber.Ctx) error {
	prog := new(models.Progress)
	if err := c.BodyParser(prog); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	config.DB.Where("user_id = ?", prog.UserID).Updates(prog)
	return c.JSON(prog)
}

func GetWeeklyXP(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var xps []models.DailyXP
	config.DB.Where("user_id = ?", userID).Find(&xps)
	return c.JSON(xps)
}

func LogXP(c *fiber.Ctx) error {
	var input struct {
		UserID   uint   `json:"user_id"`
		DateStr  string `json:"date_str"`
		XPEarned int    `json:"xp_earned"`
	}
	if err := c.BodyParser(&input); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	
	var xp models.DailyXP
	if err := config.DB.Where("user_id = ? AND date_str = ?", input.UserID, input.DateStr).First(&xp).Error; err != nil {
		xp = models.DailyXP{UserID: input.UserID, DateStr: input.DateStr, XPEarned: input.XPEarned}
		config.DB.Create(&xp)
	} else {
		xp.XPEarned += input.XPEarned
		config.DB.Save(&xp)
	}
	return c.JSON(xp)
}

// --- Quiz ---
func GetQuizStats(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var stat models.QuizStat
	config.DB.Where("user_id = ?", userID).First(&stat)
	return c.JSON(stat)
}

func UpdateQuizStats(c *fiber.Ctx) error {
	stat := new(models.QuizStat)
	if err := c.BodyParser(stat); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	config.DB.Save(stat)
	return c.JSON(stat)
}

// --- Grades ---
func GetUserGrades(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var grades []models.UserGrade
	config.DB.Where("user_id = ?", userID).Find(&grades)
	return c.JSON(grades)
}

func SaveUserGrades(c *fiber.Ctx) error {
	var input struct {
		UserID uint               `json:"user_id"`
		Grades []models.UserGrade `json:"grades"`
	}
	if err := c.BodyParser(&input); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	
	config.DB.Where("user_id = ?", input.UserID).Delete(&models.UserGrade{})
	for _, g := range input.Grades {
		g.UserID = input.UserID
		config.DB.Create(&g)
	}
	return c.SendStatus(200)
}

// --- Missions ---
func GetCompletedMissions(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	var missions []models.CompletedMission
	config.DB.Where("user_id = ?", userID).Find(&missions)
	return c.JSON(missions)
}

func AddCompletedMission(c *fiber.Ctx) error {
	var m models.CompletedMission
	if err := c.BodyParser(&m); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": err.Error()})
	}
	config.DB.Create(&m)
	return c.JSON(m)
}
