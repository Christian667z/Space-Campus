from PIL import Image
import shutil
import sys

try:
    logo_path = r"C:\Users\DELL\.gemini\antigravity\brain\82aed3d6-6b54-4614-a2f2-da81015040fd\asta_logo_main_1777753848181.png"
    splash_path = r"C:\Users\DELL\.gemini\antigravity\brain\82aed3d6-6b54-4614-a2f2-da81015040fd\asta_splash_screen_1777753878958.png"

    # Replace splash screen (which is called Space_logo_256.png in the project for the splash, or actually I should just resize the splash)
    # The current Space_logo_256.png is probably the splash background or the logo itself. Let's make it the splash background.
    # Wait, in main.py, _show_splash uses Space_logo_256.png. Let's look at it. If it's a square logo, I should use logo_path.
    
    # Save the logo as .png and .ico
    img_logo = Image.open(logo_path)
    img_logo = img_logo.resize((256, 256), Image.Resampling.LANCZOS)
    img_logo.save("Space_logo_256.png", format="PNG")
    
    # Generate ICO from logo
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img_logo.save("Space_logo.ico", format="ICO", sizes=icon_sizes)

    print("Images traitées avec succès !")
except Exception as e:
    print(f"Erreur : {e}")
    sys.exit(1)
