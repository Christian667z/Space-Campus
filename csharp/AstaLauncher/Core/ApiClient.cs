using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace AstaLauncher.Core
{
    public class ApiClient
    {
        private static readonly HttpClient _client = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };
        private const string API_URL = "http://127.0.0.1:8080/api/v1";
        private static string _token = "";

        public static async Task<bool> LoginAsync(string username, string password)
        {
            try
            {
                var payload = new { nom = username, password = password };
                var content = new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json");
                
                var response = await _client.PostAsync($"{API_URL}/auth/login", content);
                if (response.IsSuccessStatusCode)
                {
                    var responseStr = await response.Content.ReadAsStringAsync();
                    dynamic data = JsonConvert.DeserializeObject(responseStr);
                    _token = data.token;
                    return true;
                }
            }
            catch { }
            return false;
        }

        public static async Task<JArray> GetUsersAsync()
        {
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Get, $"{API_URL}/users");
                request.Headers.Add("Authorization", $"Bearer {_token}");
                var response = await _client.SendAsync(request);
                var content = await response.Content.ReadAsStringAsync();
                return JArray.Parse(content);
            }
            catch { return new JArray(); }
        }

        public static async Task<JObject> GetDashboardMetricsAsync()
        {
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Get, $"{API_URL}/dashboard");
                request.Headers.Add("Authorization", $"Bearer {_token}");
                var response = await _client.SendAsync(request);
                var content = await response.Content.ReadAsStringAsync();
                return JObject.Parse(content);
            }
            catch { return new JObject(); }
        }
    }
}
