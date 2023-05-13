# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
added_files = [
    ( 'templates/*', 'templates' ),
    ( 'assets/*', 'assets' ),
    ( 'modules/*', 'modules' ),
    ( 'modules/reports/*', 'modules/reports' ),
    ( 'VERSION', '.')
    ]

a = Analysis(
    ['lw_report_gen.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['jinja2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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
    name='lw_report_gen_mac_arm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)
