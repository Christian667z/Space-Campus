package repositories

import (
	"asta-backend/config"
	"asta-backend/models"
)

type UserRepository interface {
	Create(user *models.User) error
	FindByNom(nom string) (*models.User, error)
	FindByID(id uint) (*models.User, error)
	Update(user *models.User) error
}

type userRepository struct{}

func NewUserRepository() UserRepository {
	return &userRepository{}
}

func (r *userRepository) Create(user *models.User) error {
	return config.DB.Create(user).Error
}

func (r *userRepository) FindByNom(nom string) (*models.User, error) {
	var user models.User
	err := config.DB.Where("nom = ?", nom).First(&user).Error
	return &user, err
}

func (r *userRepository) FindByID(id uint) (*models.User, error) {
	var user models.User
	err := config.DB.First(&user, id).Error
	return &user, err
}

func (r *userRepository) Update(user *models.User) error {
	return config.DB.Save(user).Error
}
