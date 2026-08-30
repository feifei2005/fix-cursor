# fix-cursor

Fix Windows mouse cursor **Normal Select** that can't be changed, by bypassing the broken system loader and applying the registry cursor scheme directly via `SetSystemCursor`.

Windows 鼠标指针 **正常选择**（Normal Select）无法修改的修复工具。绕过损坏的系统加载机制，直接用 `SetSystemCursor` API 将注册表中的光标方案应用到系统。

[中文说明](#中文说明) | [English](#english)

---

## English

### Why this happens

On some Windows systems (especially with third-party kernel drivers or desktop tweak tools installed), the system fails to load the `OCR_NORMAL` cursor from the registry and silently falls back to the classic white arrow. As a result, changing the cursor scheme in **Settings → Personalization → Themes → Mouse Cursors** has no visible effect.

### How it works

Instead of relying on the OS's cursor-loading mechanism, this tool reads every cursor path from `HKCU\Control Panel\Cursors` and applies them directly through the Win32 API `SetSystemCursor`. It covers all 17 cursor roles (Arrow, IBeam, Wait, Hand, etc.).

### Usage

- **FixCursor.exe** (Windows 10/11, x64, standalone — no Python or runtime needed): double-click to run. It applies the current registry scheme instantly.
- **fix_cursor.py** (source): requires Python 3, run with `python fix_cursor.py`.

> Runs from the current user session; no administrator rights are required.

### Build from source

```bat
pip install pyinstaller
pyinstaller --onefile --noconsole --name FixCursor fix_cursor.py
```

### Files

| File            | Description                                        |
|-----------------|----------------------------------------------------|
| `FixCursor.exe` | Pre-built standalone executable (~6 MB)           |
| `fix_cursor.py` | Source script (std-lib only: ctypes, winreg)      |
| `README.md`     | This document                                     |

---

## 中文说明

### 问题原因

部分 Windows 系统（尤其是安装过第三方内核驱动或桌面美化工具后），系统从注册表加载 `OCR_NORMAL`（正常选择）光标时失败，静默回退到经典白色箭头。因此，在 **设置 → 个性化 → 主题 → 鼠标光标** 中修改光标方案看不到任何效果。

### 工作原理

本工具不依赖系统的光标加载机制，而是直接读取 `HKCU\Control Panel\Cursors` 中全部光标路径，通过 Win32 API `SetSystemCursor` 应用到系统，覆盖全部 17 种光标角色（箭头、文本选择、忙碌、手型等）。

### 使用方法

- **FixCursor.exe**（Windows 10/11 x64，单文件免安装，无需任何运行时）：双击即可，立即应用当前注册表光标方案。
- **fix_cursor.py**（源码）：需要 Python 3，执行 `python fix_cursor.py`。

> 以当前用户会话运行，无需管理员权限。

### 从源码构建

```bat
pip install pyinstaller
pyinstaller --onefile --noconsole --name FixCursor fix_cursor.py
```

### 文件说明

| 文件            | 说明                                            |
|-----------------|--------------------------------------------------|
| `FixCursor.exe` | 预编译的独立可执行文件（约 6 MB）                 |
| `fix_cursor.py` | 源码脚本（仅标准库：ctypes、winreg）               |
| `README.md`     | 本说明文档                                        |