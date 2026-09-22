using System;
using System.Windows;
using AstaInterop;

namespace AstaAcademieLauncher
{
    public static class NativeExample
    {
        public static int Add(int a, int b)
        {
            try
            {
                return NativeInterop.Add(a, b);
            }
            catch (System.DllNotFoundException)
            {
                return -1;
            }
        }
    }
}
