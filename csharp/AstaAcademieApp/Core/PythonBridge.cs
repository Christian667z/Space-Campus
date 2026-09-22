using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Core
{
    /// <summary>
    /// Pont HTTP singleton vers le backend Python (api_bridge.py sur localhost:5005).
    /// Toutes les méthodes retournent une valeur de fallback si le serveur est hors ligne.
    /// </summary>
    public sealed class PythonBridge
    {
        private static readonly Lazy<PythonBridge> _instance = new(() => new PythonBridge());
        public static PythonBridge Instance => _instance.Value;

        private readonly HttpClient _http;
        private const string BaseUrl = "http://localhost:5005";

        private PythonBridge()
        {
            _http = new HttpClient { Timeout = TimeSpan.FromSeconds(8) };
        }

        // ── Utilitaires ───────────────────────────────────────────────────────

        public async Task<bool> IsOnlineAsync()
        {
            try
            {
                var r = await _http.GetAsync($"{BaseUrl}/api/ping");
                return r.IsSuccessStatusCode;
            }
            catch { return false; }
        }

        private async Task<JObject?> GetJsonAsync(string path)
        {
            try
            {
                string json = await _http.GetStringAsync($"{BaseUrl}{path}");
                return JObject.Parse(json);
            }
            catch { return null; }
        }

        private async Task<JObject?> PostJsonAsync(string path, object payload)
        {
            try
            {
                string body = JsonConvert.SerializeObject(payload);
                var content = new StringContent(body, Encoding.UTF8, "application/json");
                var resp = await _http.PostAsync($"{BaseUrl}{path}", content);
                return JObject.Parse(await resp.Content.ReadAsStringAsync());
            }
            catch { return null; }
        }

        // ── Space AI ──────────────────────────────────────────────────────────

        public async Task<string> ChatAsync(string message)
        {
            var result = await PostJsonAsync("/api/spaceai/chat", new { message });
            return result?["response"]?.ToString()
                ?? "⚠️ Space AI hors ligne. Lance `api_bridge.py` d'abord.";
        }

        // ── Oracle ────────────────────────────────────────────────────────────

        public async Task<string> GetOracleTipAsync()
        {
            var r = await GetJsonAsync("/api/oracle/tip");
            return r?["tip"]?.ToString() ?? "Lancez api_bridge.py pour les données Oracle.";
        }

        public async Task<string> GetOracleFactAsync()
        {
            var r = await GetJsonAsync("/api/oracle/fact");
            return r?["fact"]?.ToString() ?? "Le premier bug était un vrai papillon de nuit.";
        }

        public async Task<(string Citation, string Auteur, string Role)> GetOracleQuoteAsync()
        {
            var r = await GetJsonAsync("/api/oracle/quote");
            if (r == null) return ("Talk is cheap. Show me the code.", "Linus Torvalds", "Créateur de Linux");
            return (r["citation"]?.ToString() ?? "", r["auteur"]?.ToString() ?? "", r["role"]?.ToString() ?? "");
        }

        public async Task<JObject?> GetOracleTimelineAsync()
            => await GetJsonAsync("/api/oracle/timeline");

        // ── Raccourcis ────────────────────────────────────────────────────────

        public async Task<JObject?> GetShortcutsExcelAsync()
            => await GetJsonAsync("/api/shortcuts/excel");

        public async Task<JObject?> GetShortcutsTrapsAsync()
            => await GetJsonAsync("/api/shortcuts/traps");

        public async Task<JObject?> GetShortcutsLinuxAsync()
            => await GetJsonAsync("/api/shortcuts/linux");

        public async Task<JObject?> GetShortcutsOsiAsync()
            => await GetJsonAsync("/api/shortcuts/osi");

        public async Task<JObject?> GetShortcutsProtocolsAsync()
            => await GetJsonAsync("/api/shortcuts/protocols");

        // ── Quiz ──────────────────────────────────────────────────────────────

        public async Task<JObject?> GetQuizQuestionsAsync(string matiere = "")
        {
            string path = string.IsNullOrEmpty(matiere)
                ? "/api/quiz/questions"
                : $"/api/quiz/questions?matiere={Uri.EscapeDataString(matiere)}";
            return await GetJsonAsync(path);
        }

        // ── Cours ─────────────────────────────────────────────────────────────

        public async Task<JObject?> GetCoursesAsync()
            => await GetJsonAsync("/api/courses");

        // ── Notes ─────────────────────────────────────────────────────────────

        public async Task<JObject?> GetNotesAsync()
            => await GetJsonAsync("/api/notes");

        public async Task<JObject?> SaveNoteAsync(string id, string titre, string contenu, string categorie)
            => await PostJsonAsync("/api/notes/save", new { id, titre, contenu, categorie,
                date = DateTime.Now.ToString("yyyy-MM-dd HH:mm") });

        public async Task<JObject?> DeleteNoteAsync(string id)
            => await PostJsonAsync("/api/notes/delete", new { id });

        // ── Profil ────────────────────────────────────────────────────────────

        public async Task<JObject?> GetProfileAsync()
            => await GetJsonAsync("/api/profile");
    }
}
