using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace AstaAcademieApp.Views
{
    public partial class SpaceAiPage : Page
    {
        public SpaceAiPage()
        {
            InitializeComponent();
        }

        private async void BtnSend_Click(object sender, RoutedEventArgs e)
        {
            await SendMessage();
        }

        private async void TxtInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                await SendMessage();
            }
        }

        private async Task SendMessage()
        {
            string message = TxtInput.Text.Trim();
            if (string.IsNullOrEmpty(message)) return;

            // Ajouter le message Utilisateur
            AddUserMessage(message);
            TxtInput.Text = "";

            // Désactiver l'entrée pendant le chargement
            TxtInput.IsEnabled = false;
            BtnSend.IsEnabled = false;

            try
            {
                // Appeler le script Python en arrière-plan
                string response = await Core.PythonBridge.Instance.ChatAsync(message);
                AddBotMessage(response);
            }
            finally
            {
                TxtInput.IsEnabled = true;
                BtnSend.IsEnabled = true;
                TxtInput.Focus();
            }
        }

        private void AddUserMessage(string text)
        {
            Border bubble = new Border
            {
                Background = (Brush)Application.Current.Resources["BrushPrimary"], // Emeraude pour l'utilisateur
                CornerRadius = new CornerRadius(12, 12, 0, 12),
                Padding = new Thickness(15),
                Margin = new Thickness(50, 0, 0, 15),
                HorizontalAlignment = HorizontalAlignment.Right
            };

            TextBlock textBlock = new TextBlock
            {
                Text = text,
                Foreground = Brushes.White,
                TextWrapping = TextWrapping.Wrap
            };

            bubble.Child = textBlock;
            ChatHistory.Children.Add(bubble);
            ScrollToBottom();
        }

        private void AddBotMessage(string text)
        {
            Border bubble = new Border
            {
                Background = (Brush)Application.Current.Resources["BrushBgCard"],
                BorderBrush = (Brush)Application.Current.Resources["BrushBorder"],
                BorderThickness = new Thickness(1),
                CornerRadius = new CornerRadius(12, 12, 12, 0),
                Padding = new Thickness(15),
                Margin = new Thickness(0, 0, 50, 15),
                HorizontalAlignment = HorizontalAlignment.Left
            };

            StackPanel panel = new StackPanel();
            
            TextBlock nameBlock = new TextBlock
            {
                Text = "Space AI",
                FontSize = 11,
                FontWeight = FontWeights.Bold,
                Foreground = (Brush)Application.Current.Resources["BrushAccent"],
                Margin = new Thickness(0, 0, 0, 5)
            };

            TextBlock textBlock = new TextBlock
            {
                Text = text,
                Foreground = (Brush)Application.Current.Resources["BrushTextWhite"],
                TextWrapping = TextWrapping.Wrap
            };

            panel.Children.Add(nameBlock);
            panel.Children.Add(textBlock);
            bubble.Child = panel;

            ChatHistory.Children.Add(bubble);
            ScrollToBottom();
        }

        private void ScrollToBottom()
        {
            ChatScroll.ScrollToBottom();
        }
    }
}
