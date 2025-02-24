# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

block_cipher = None
added_files = [
    ( 'templates/*', 'templates' ),
    ( 'assets/*', 'assets' ),
    ( 'modules/*', 'modules' ),
    ( 'modules/reports/*', 'modules/reports' ),
    ( 'VERSION', '.')
    ]
added_files += copy_metadata("laceworksdk")

block_cipher = None
a = Analysis(
    ['lw_report_gen.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['./pyinstaller_runtime_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='lw_report_gen_win',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
