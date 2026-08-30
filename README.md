# fix-cursor

修复 Windows 鼠标指针"正常选择"无法修改的问题。

## 原理

系统从注册表加载 `OCR_NORMAL` 的机制被内核驱动干扰，导致加载失败回退传统白色。
本工具绕过系统加载，直接用 `SetSystemCursor` API 把注册表中的光标方案应用到系统。

## 使用

- **FixCursor.exe**（Windows 10/11 64 位，无需安装任何运行时）：双击运行即可。
- **fix_cursor.py**（源码）：需要 Python 3 环境，`python fix_cursor.py`。

## 构建

```bat
pip install pyinstaller
pyinstaller --onefile --noconsole --name FixCursor fix_cursor.py
```