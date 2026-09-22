using System.Windows.Controls;

namespace AstaAcademieApp.Views
{
    public partial class PlaceholderPage : Page
    {
        public PlaceholderPage(string title)
        {
            InitializeComponent();
            TxtTitle.Text = $"⚙️ Module « {title} » en construction...";
        }
    }
}
