using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using AstaAcademieApp.Core;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Views
{
    public partial class NotesPage : Page
    {
        private string _currentId = "";
        private List<dynamic> _notes = new();

        public NotesPage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"NotesPage init: {ex.Message}"); return; }
            Loaded += async (_, _) => await LoadNotesAsync();
        }

        private async System.Threading.Tasks.Task LoadNotesAsync()
        {
            try
            {
                var data = await PythonBridge.Instance.GetNotesAsync();
                Dispatcher.Invoke(() =>
                {
                    _notes = data?["notes"] is JArray arr
                        ? arr.ToObject<List<dynamic>>() ?? new()
                        : new();
                    NotesList.ItemsSource = null;
                    NotesList.ItemsSource = _notes;
                    if (_notes.Count > 0) NotesList.SelectedIndex = 0;
                });
            }
            catch (Exception ex) { Console.WriteLine($"NotesPage load: {ex.Message}"); }
        }

        private void NotesList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (NotesList.SelectedItem is not JObject note) return;
            try
            {
                _currentId      = note["id"]?.ToString() ?? "";
                TxtTitre.Text   = note["titre"]?.ToString() ?? "";
                TxtContenu.Text = note["contenu"]?.ToString() ?? "";
                string cat      = note["categorie"]?.ToString() ?? "Général";
                foreach (ComboBoxItem item in CbCategorie.Items)
                    if (item.Content.ToString() == cat) { CbCategorie.SelectedItem = item; break; }
                TxtSaveStatus.Text = "";
            }
            catch { }
        }

        private void BtnNew_Click(object sender, RoutedEventArgs e)
        {
            _currentId      = "";
            TxtTitre.Text   = "";
            TxtContenu.Text = "";
            CbCategorie.SelectedIndex = 0;
            TxtSaveStatus.Text = "";
            NotesList.SelectedItem = null;
            TxtTitre.Focus();
        }

        private async void BtnSave_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(TxtTitre.Text)) return;
            try
            {
                string cat = (CbCategorie.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "Général";
                var result = await PythonBridge.Instance.SaveNoteAsync(
                    _currentId, TxtTitre.Text, TxtContenu.Text, cat);

                if (result?["status"]?.ToString() == "ok")
                {
                    _currentId = result["id"]?.ToString() ?? _currentId;
                    TxtSaveStatus.Text = "✅ Sauvegardé";
                    await LoadNotesAsync();
                }
                else
                {
                    TxtSaveStatus.Text = "⚠️ Erreur — backend hors ligne ?";
                }
            }
            catch (Exception ex)
            {
                TxtSaveStatus.Text = $"❌ {ex.Message}";
            }
        }

        private async void BtnDelete_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(_currentId)) return;
            var confirm = MessageBox.Show("Supprimer cette note ?", "Confirmer",
                MessageBoxButton.YesNo, MessageBoxImage.Question);
            if (confirm != MessageBoxResult.Yes) return;

            try
            {
                await PythonBridge.Instance.DeleteNoteAsync(_currentId);
                _currentId = "";
                TxtTitre.Text = "";
                TxtContenu.Text = "";
                await LoadNotesAsync();
            }
            catch (Exception ex) { Console.WriteLine($"DeleteNote error: {ex.Message}"); }
        }
    }
}
