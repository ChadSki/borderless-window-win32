import win32api
import win32con
import win32gui

from ctypes import windll, pointer
from ctypes.wintypes import MSG


class MainWindow:

    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)
        className = 'MyWndClass'
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
        wc.lpszClassName = className
        win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPEDWINDOW
        self.hwnd = win32gui.CreateWindow(
            className,
            'My win32api app',
            style,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            300,
            300,
            0,
            0,
            self.hinst,
            None
        )
        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def OnDestroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True


win = None


def main():
    global win
    win = MainWindow()

    msg = MSG()
    lpmsg = pointer(msg)

    print('Entering message loop')
    while windll.user32.GetMessageA(lpmsg, 0, 0, 0) != 0:
        windll.user32.TranslateMessage(lpmsg)
        windll.user32.DispatchMessageA(lpmsg)

    print('done.')


if __name__ == "__main__":
    main()
