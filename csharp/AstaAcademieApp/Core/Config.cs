using System;
using System.IO;

namespace AstaAcademieApp.Core
{
    public static class Config
    {
        public static string BasePath { get; private set; }
        public static string DataDir { get; private set; }
        public static string DbPath { get; private set; }
        public static string ProfilesPath { get; private set; }
        
        static Config()
        {
            // Trouver le chemin racine (un dossier au-dessus de csharp, ou dans le même dossier si compilé en prod)
            string currentDir = AppDomain.CurrentDomain.BaseDirectory;
            
            // Si on est dans bin/Debug/net8.0-windows, on remonte
            if (currentDir.Contains("bin") || currentDir.Contains("csharp"))
            {
                BasePath = Path.GetFullPath(Path.Combine(currentDir, @"..\..\..\..\..\"));
            }
            else
            {
                BasePath = currentDir;
            }

            DataDir = Path.Combine(BasePath, "data");
            DbPath = Path.Combine(DataDir, "asta_database.db");
            ProfilesPath = Path.Combine(DataDir, "profiles.json");
            
            if (!Directory.Exists(DataDir))
            {
                Directory.CreateDirectory(DataDir);
            }
        }
    }
}
