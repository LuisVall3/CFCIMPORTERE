# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],  # 1. Punto de entrada corregido a main.py
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],  # 2. Empaqueta la carpeta assets completa
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
    a.binaries,
    a.datas,
    [],
    name='Carbon Free Importer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/favicon.ico'],  # 3. Asigna el icono al archivo .exe en Windows
)

app = BUNDLE(
    exe,
    name='Carbon Free Importer.app',
    icon='assets/favicon.ico',
    bundle_identifier=None,
)