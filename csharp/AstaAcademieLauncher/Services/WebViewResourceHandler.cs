using System;
using System.IO;
using System.Reflection;
using System.Threading.Tasks;
using Microsoft.Web.WebView2.Core;

namespace AstaAcademieLauncher.Services
{
    public static class WebViewResourceHandler
    {
        // Call this once after WebView2 is initialized
        public static void Register(CoreWebView2 webview)
        {
            webview.SetVirtualHostNameToFolderMapping("app.local", "wwwroot", CoreWebView2HostResourceAccessKind.Allow);
            webview.WebResourceRequested += Webview_WebResourceRequested;
        }

        private static void Webview_WebResourceRequested(object? sender, CoreWebView2WebResourceRequestedEventArgs e)
        {
            try
            {
                var uri = new Uri(e.Request.Uri);
                // Expecting requests like https://app.local/index.html or /assets/js/app.js
                var path = uri.AbsolutePath.TrimStart('/').Replace('/', '.');
                var asm = Assembly.GetExecutingAssembly();
                var resourceName = "AstaAcademieLauncher.frontend.dist." + path;
                Stream? s = asm.GetManifestResourceStream(resourceName);
                if (s != null)
                {
                    var stream = new CoreWebView2WebResourceResponse(s, 200, "OK", "Content-Type: application/octet-stream");
                    e.Response = stream;
                }
            }
            catch
            {
                // silent fallback — let WebView2 continue
            }
        }
    }
}
