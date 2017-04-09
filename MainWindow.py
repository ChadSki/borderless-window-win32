from ctypes import windll, pointer, Structure, c_int
from ctypes.wintypes import MSG
import win32api
import win32con
from win32con import (
    WS_CAPTION, WS_THICKFRAME, WS_MINIMIZE, WS_MAXIMIZE, WS_SYSMENU)
import win32gui

border_style_flags = (
    WS_CAPTION | WS_THICKFRAME | WS_MINIMIZE | WS_MAXIMIZE | WS_SYSMENU)


class MARGINS(Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)]


class MainWindow:

    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)

        # Define window class
        className = 'MyWndClass'
        windowName = 'My Window'
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = {
            win32con.WM_COMMAND: self.on_command,
            win32con.WM_DESTROY: self.on_destroy,
            win32con.WM_GETMINMAXINFO: self.on_minmaxinfo,
            win32con.WM_NCHITTEST: self.on_hittest,
            win32con.WM_NCCALCSIZE: self.on_calcsize,
            win32con.WM_SIZE: self.on_size,
        }
        wc.lpszClassName = className
        win32gui.RegisterClass(wc)

        # Instantiate window
        self.hwnd = win32gui.CreateWindow(
            className, windowName,
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            300, 300, 0, 0,
            self.hinst, None
        )

        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

        # Make borderless
        style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_STYLE,
            style & ~border_style_flags)

        # Extend dwm frame. In other words, have the Windows compositor handle
        # a 1px transparent border. This is an easy way to enable Aero snap
        # functionality.
        margins = MARGINS(1, 1, 1, 1)
        windll.dwmapi.DwmExtendFrameIntoClientArea(self.hwnd, margins)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def on_calcsize(self, hwnd, message, wparam, lparam):
        return 0

    def on_command(self, hwnd, message, wparam, lparam):
        win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, wparam, lparam)

    def on_destroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

    def on_hittest(self, hwnd, message, wparam, lparam):
        border_width = 8
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        x = win32api.LOWORD(lparam)
        y = win32api.HIWORD(lparam)

        is_left = x >= left and x < left + border_width
        is_top = y >= top and y < top + border_width
        is_right = x < right and x >= right - border_width
        is_bottom = y < bottom and y >= bottom - border_width

        if is_left:
            if is_top:
                return win32con.HTTOPLEFT
            if is_bottom:
                return win32con.HTBOTTOMLEFT

            return win32con.HTLEFT

        if is_right:
            if is_top:
                return win32con.HTTOPRIGHT
            if is_bottom:
                return win32con.HTBOTTOMRIGHT

            return win32con.HTRIGHT

        if is_top:
            return win32con.HTTOP
        if is_bottom:
            return win32con.HTBOTTOM

        # HTCAPTION: draggable
        # HTNOWHERE: not draggable
        return win32con.HTCAPTION

    def on_minmaxinfo(self, hwnd, message, wparam, lparam):
        return 0

    def on_size(self, hwnd, message, wparam, lparam):
        return win32gui.DefWindowProc(hwnd, message, wparam, lparam)


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
