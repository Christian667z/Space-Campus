package services

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"os"
	"time"

	"asta-backend/models"
	"asta-backend/repositories"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

type AuthService interface {
	Register(nom, password string) (*models.User, error)
	Login(nom, password, deviceName string) (string, string, *models.User, error)
	RefreshToken(userID uint, tokenString, deviceName string) (string, string, error)
	Logout(userID uint) error
	ValidatePasswordRules(password string) error
}

type authService struct {
	userRepo  repositories.UserRepository
	tokenRepo repositories.TokenRepository
}

func NewAuthService(userRepo repositories.UserRepository, tokenRepo repositories.TokenRepository) AuthService {
	return &authService{userRepo, tokenRepo}
}

func getSecret() []byte {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		secret = "super_secret_asta_key_2024"
	}
	return []byte(secret)
}

func (s *authService) ValidatePasswordRules(password string) error {
	if len(password) < 8 {
		return errors.New("le mot de passe doit contenir au moins 8 caractères")
	}
	// On pourrait ajouter d'autres vérifications (regex pour majuscules, chiffres)
	return nil
}

func (s *authService) Register(nom, password string) (*models.User, error) {
	if err := s.ValidatePasswordRules(password); err != nil {
		return nil, err
	}

	existingUser, _ := s.userRepo.FindByNom(nom)
	if existingUser != nil {
		return nil, errors.New("utilisateur déjà existant")
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	user := &models.User{
		Nom:      nom,
		Password: string(hashedPassword),
		Role:     models.RoleUser,
		IsActive: true,
	}

	if err := s.userRepo.Create(user); err != nil {
		return nil, err
	}
	return user, nil
}

func generateRandomToken() string {
	b := make([]byte, 32)
	rand.Read(b)
	return hex.EncodeToString(b)
}

func (s *authService) generateTokens(user *models.User, deviceName string) (string, string, error) {
	// 1. Access Token (JWT) - 15 minutes
	accessClaims := jwt.MapClaims{
		"sub":  user.ID,
		"role": user.Role,
		"exp":  time.Now().Add(15 * time.Minute).Unix(),
		"iat":  time.Now().Unix(),
	}
	accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, accessClaims)
	accessString, err := accessToken.SignedString(getSecret())
	if err != nil {
		return "", "", err
	}

	// 2. Refresh Token (Opaque string with UserID) - 7 days
	rawRandomToken := generateRandomToken()
	hashBytes, _ := bcrypt.GenerateFromPassword([]byte(rawRandomToken), bcrypt.DefaultCost)

	// Invalider l'ancien token pour ce device s'il existe
	if oldToken, err := s.tokenRepo.FindByUserIDAndDevice(user.ID, deviceName); err == nil {
		s.tokenRepo.Revoke(oldToken.ID)
	}

	refreshTokenModel := &models.RefreshToken{
		UserID:     user.ID,
		TokenHash:  string(hashBytes),
		ExpiresAt:  time.Now().Add(7 * 24 * time.Hour),
		DeviceName: deviceName,
	}

	if err := s.tokenRepo.Create(refreshTokenModel); err != nil {
		return "", "", err
	}

	// Format: userID:rawToken (en pratique on ferait base64 ou on passerait l'userID à part)
	// Pour l'Asta API, le client l'enverra avec le deviceName
	return accessString, rawRandomToken, nil
}

func (s *authService) Login(nom, password, deviceName string) (string, string, *models.User, error) {
	user, err := s.userRepo.FindByNom(nom)
	if err != nil {
		return "", "", nil, errors.New("identifiants invalides")
	}

	if !user.IsActive {
		return "", "", nil, errors.New("compte bloqué")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return "", "", nil, errors.New("identifiants invalides")
	}

	access, refresh, err := s.generateTokens(user, deviceName)
	return access, refresh, user, err
}

func (s *authService) RefreshToken(userID uint, rawTokenString, deviceName string) (string, string, error) {
	tokenModel, err := s.tokenRepo.FindByUserIDAndDevice(userID, deviceName)
	if err != nil {
		return "", "", errors.New("token invalide ou expiré")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(tokenModel.TokenHash), []byte(rawTokenString)); err != nil {
		s.tokenRepo.Revoke(tokenModel.ID) // Suspicieux, on révoque
		return "", "", errors.New("token compromis")
	}

	user, err := s.userRepo.FindByID(userID)
	if err != nil || !user.IsActive {
		return "", "", errors.New("utilisateur invalide")
	}

	return s.generateTokens(user, deviceName)
}

func (s *authService) Logout(userID uint) error {
	return s.tokenRepo.RevokeAllForUser(userID)
}
