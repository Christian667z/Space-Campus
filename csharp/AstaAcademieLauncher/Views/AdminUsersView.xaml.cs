using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace AstaAcademieLauncher.Views
{
    public partial class AdminUsersView : UserControl
    {
        private readonly HttpClient _http = new HttpClient { BaseAddress = new Uri("http://127.0.0.1:5000/") };
        private string _adminKey = "local-admin-key"; // fallback header
        private string _jwtToken = null;

        public AdminUsersView()
        {
            InitializeComponent();
            _ = RefreshUsersAsync();
        }

        private async Task RefreshUsersAsync()
        {
            try
            {
                var req = new HttpRequestMessage(HttpMethod.Get, "api/admin/users");
                if (!string.IsNullOrEmpty(_jwtToken))
                    req.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _jwtToken);
                else
                    req.Headers.Add("X-ADMIN-KEY", _adminKey);
                var res = await _http.SendAsync(req);
                if (res.IsSuccessStatusCode)
                {
                    var payload = await res.Content.ReadFromJsonAsync<Dictionary<string, object>>();
                    if (payload != null && payload.TryGetValue("users", out var users))
                    {
                        LvUsers.ItemsSource = (System.Collections.IEnumerable)users;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Erreur: " + ex.Message);
            }
        }

        private async void BtnAdd_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var username = TxtNewUser.Text.Trim();
                var pwd = PwdNew.Password;
                var isAdmin = ChkAdmin.IsChecked == true;
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(pwd)) return;
                var payload = new { username = username, password = pwd, is_admin = isAdmin };
                var req = new HttpRequestMessage(HttpMethod.Post, "api/admin/users") { Content = JsonContent.Create(payload) };
                if (!string.IsNullOrEmpty(_jwtToken))
                    req.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _jwtToken);
                else
                    req.Headers.Add("X-ADMIN-KEY", _adminKey);
                var res = await _http.SendAsync(req);
                if (res.IsSuccessStatusCode)
                {
                    await RefreshUsersAsync();
                }
                else
                {
                    var txt = await res.Content.ReadAsStringAsync();
                    MessageBox.Show("Erreur: " + txt);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private async void BtnLogin_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var username = TxtLoginUser.Text.Trim();
                var pwd = PwdLogin.Password;
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(pwd)) return;
                var payload = new { username = username, password = pwd };
                var res = await _http.PostAsJsonAsync("api/admin/login", payload);
                if (res.IsSuccessStatusCode)
                {
                    var doc = await res.Content.ReadFromJsonAsync<Dictionary<string, string>>();
                    if (doc != null && doc.TryGetValue("token", out var token))
                    {
                        _jwtToken = token;
                        MessageBox.Show("Authentification réussie");
                        await RefreshUsersAsync();
                    }
                }
                else
                {
                    var txt = await res.Content.ReadAsStringAsync();
                    MessageBox.Show("Erreur login: " + txt);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void BtnLogout_Click(object sender, RoutedEventArgs e)
        {
            _jwtToken = null;
            MessageBox.Show("Déconnecté");
        }
    }
}
