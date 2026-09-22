using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using AstaAcademieApp.Core;
using Newtonsoft.Json.Linq;

namespace AstaAcademieApp.Views
{
    public partial class QuizPage : Page
    {
        // ── État du quiz ──────────────────────────────────────────────────────
        private List<dynamic>  _questions  = new();
        private dynamic?       _current    = null;
        private bool           _answered   = false;
        private int            _score      = 0;
        private int            _total      = 0;
        private readonly Button[] _optBtns;

        // Couleurs
        private static readonly SolidColorBrush BrushCorrect = new(Color.FromRgb(16, 185, 129));
        private static readonly SolidColorBrush BrushWrong   = new(Color.FromRgb(239, 68, 68));
        private static readonly SolidColorBrush BrushNeutral = new(Color.FromRgb(20, 40, 70));

        public QuizPage()
        {
            try { InitializeComponent(); }
            catch (Exception ex) { Console.WriteLine($"QuizPage init: {ex.Message}"); return; }

            _optBtns = new[] { BtnA, BtnB, BtnC, BtnD };
            Loaded += async (_, _) => await LoadQuestionsAsync();
        }

        // ── Chargement des questions ──────────────────────────────────────────
        private async System.Threading.Tasks.Task LoadQuestionsAsync(string matiere = "")
        {
            try
            {
                var data = await PythonBridge.Instance.GetQuizQuestionsAsync(matiere);
                if (data == null) return;

                Dispatcher.Invoke(() =>
                {
                    if (data["questions"] is JArray qs)
                        _questions = qs.ToObject<List<dynamic>>() ?? new();

                    if (data["matieres"] is JArray mat)
                    {
                        CbMatiere.Items.Clear();
                        CbMatiere.Items.Add("Toutes");
                        foreach (var m in mat) CbMatiere.Items.Add(m.ToString());
                        CbMatiere.SelectedIndex = 0;
                    }

                    NextQuestion();
                });
            }
            catch (Exception ex) { Console.WriteLine($"QuizPage load: {ex.Message}"); }
        }

        // ── Question suivante ─────────────────────────────────────────────────
        private void NextQuestion()
        {
            if (_questions.Count == 0)
            {
                TxtQuestion.Text = "Aucune question disponible. Vérifie que api_bridge.py tourne.";
                return;
            }

            var rnd = new Random();
            _current  = _questions[rnd.Next(_questions.Count)];
            _answered = false;

            string question = _current.question?.ToString() ?? "";
            string matiere  = _current.matiere?.ToString() ?? "";
            string niveau   = _current.niveau?.ToString()  ?? "";
            TxtQuestion.Text = question;
            TxtMatiere.Text  = $"Matière : {matiere}  |  Niveau : {niveau}";
            TxtResult.Text   = "";
            TxtExplication.Text = "";

            JArray? opts = _current.options is JArray ja ? ja : null;
            for (int i = 0; i < 4; i++)
            {
                if (opts != null && i < opts.Count)
                {
                    _optBtns[i].Content    = $"  {(char)('A' + i)}. {opts[i]}";
                    _optBtns[i].Visibility = Visibility.Visible;
                    _optBtns[i].IsEnabled  = true;
                    _optBtns[i].Background = BrushNeutral;
                }
                else
                {
                    _optBtns[i].Visibility = Visibility.Collapsed;
                }
            }
        }

        // ── Répondre ─────────────────────────────────────────────────────────
        private void BtnOption_Click(object sender, RoutedEventArgs e)
        {
            if (_answered || _current == null) return;
            _answered = true;
            _total++;

            int idx = int.Parse(((Button)sender).Tag.ToString()!);
            int correct = (int)(_current.correct ?? 0);

            foreach (var btn in _optBtns) btn.IsEnabled = false;

            _optBtns[correct].Background = BrushCorrect;
            if (idx != correct) _optBtns[idx].Background = BrushWrong;

            if (idx == correct)
            {
                _score++;
                TxtResult.Text      = "✅ Correct ! Bien joué.";
                TxtResult.Foreground = BrushCorrect;
            }
            else
            {
                string correctText = (_current.options as JArray)?[correct]?.ToString() ?? "";
                TxtResult.Text      = $"❌ Incorrect. Bonne réponse : {correctText}";
                TxtResult.Foreground = BrushWrong;
            }

            string expl = _current.explication?.ToString() ?? "";
            TxtExplication.Text = string.IsNullOrEmpty(expl) ? "" : $"💡 {expl}";

            UpdateScore();
        }

        private void BtnNext_Click(object sender, RoutedEventArgs e) => NextQuestion();

        private async void CbMatiere_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (CbMatiere.SelectedItem == null) return;
            string sel = CbMatiere.SelectedItem.ToString()!;
            string matiere = sel == "Toutes" ? "" : sel;
            await LoadQuestionsAsync(matiere);
        }

        private void BtnReset_Click(object sender, RoutedEventArgs e)
        {
            _score = 0; _total = 0;
            UpdateScore();
            TxtResult.Text = "";
            TxtExplication.Text = "";
            NextQuestion();
        }

        private void UpdateScore()
        {
            TxtScore.Text = $"✅ Score : {_score} / {_total}";
            int pct = _total > 0 ? (int)(_score * 100.0 / _total) : 0;
            TxtPct.Text  = $"  ({pct}%)";
        }
    }
}
