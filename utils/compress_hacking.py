import os
import zipfile
from pathlib import Path

def compress_hacking_folder():
    """Compresse le dossier hacking en un fichier zip sécurisé."""
    base_dir = Path(__file__).parent.parent.absolute()
    hacking_dir = base_dir / "hacking"
    assets_dir = base_dir / "assets"
    
    if not hacking_dir.exists():
        print("Le dossier 'hacking' est introuvable.")
        return
        
    assets_dir.mkdir(parents=True, exist_ok=True)
    zip_path = assets_dir / "hacking_payloads.zip"
    
    print(f"Compression de {hacking_dir} vers {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(hacking_dir):
            for file in files:
                file_path = Path(root) / file
                # Chemin relatif dans le zip
                arcname = file_path.relative_to(hacking_dir)
                zipf.write(file_path, arcname)
                
    print("Compression terminée avec succès !")

if __name__ == "__main__":
    compress_hacking_folder()
