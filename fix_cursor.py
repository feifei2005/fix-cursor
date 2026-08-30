# -*- coding: utf-8 -*-
"""
修复 Windows 鼠标指针"正常选择"无法修改的问题。
原理: 系统从注册表加载 OCR_NORMAL 的机制被内核驱动干扰, 导致加载失败回退传统白色。
       本脚本绕过系统加载, 直接用 SetSystemCursor API 把注册表中的光标方案应用到系统。
由 WorkBuddy 生成于 2026-08-22。可安全删除。
"""
import ctypes
import ctypes.wintypes as wt
import winreg
import sys
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.LoadCursorFromFileW.argtypes = [wt.LPCWSTR]
user32.LoadCursorFromFileW.restype = ctypes.c_void_p
user32.SetSystemCursor.argtypes = [ctypes.c_void_p, ctypes.c_uint]
user32.SetSystemCursor.restype = ctypes.c_int

# OCR_* 系统光标常量 -> HKCU\Control Panel\Cursors 注册表值名
OCR_MAP = {
    'Arrow': 32512, 'IBeam': 32513, 'Wait': 32514, 'Crosshair': 32515,
    'No': 32516, 'SizeNS': 32517, 'SizeWE': 32518, 'SizeNWSE': 32519,
    'SizeNESW': 32520, 'SizeAll': 32521, 'UpArrow': 32522,
    'Hand': 32649, 'AppStarting': 32650, 'Help': 32651, 'NWPen': 32652,
    'Pin': 32653, 'Person': 32654,
}


def read_cursor_paths():
    """从注册表读取当前光标方案的全部路径"""
    paths = {}
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\Cursors')
    except FileNotFoundError:
        return paths
    i = 0
    while True:
        try:
            name, value, vtype = winreg.EnumValue(k, i)
            if isinstance(value, str) and value and name in OCR_MAP:
                paths[name] = value
            i += 1
        except OSError:
            break
    winreg.CloseKey(k)
    return paths


def main():
    paths = read_cursor_paths()
    if not paths:
        print('[fix_cursor] 未读取到光标配置')
        return 1

    ok = 0
    for name, path in paths.items():
        # 确保路径为绝对路径（展开环境变量）
        if '%' in path:
            try:
                path = winreg.ExpandEnvironmentStrings(path)
            except Exception:
                pass
        h = user32.LoadCursorFromFileW(path)
        if h:
            r = user32.SetSystemCursor(h, OCR_MAP[name])
            if r:
                ok += 1
    print(f'[fix_cursor] 已应用 {ok}/{len(paths)} 个光标')
    return 0 if ok else 1


if __name__ == '__main__':
    time.sleep(1)
    sys.exit(main())
