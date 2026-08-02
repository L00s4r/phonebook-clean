# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\BotPro261\\hello\\lessons\\Mathproject\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\BotPro261\\hello\\lessons\\Mathproject\\Sounds', 'Sounds'), ('C:\\Users\\BotPro261\\hello\\lessons\\Mathproject\\images', 'images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MathProject',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\BotPro261\\hello\\lessons\\Mathproject\\images\\icon_for_per.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MathProject',
)
