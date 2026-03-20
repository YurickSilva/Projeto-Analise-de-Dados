# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('navigation.py', '.'),
        ('router.py', '.'),
        ('requirements.txt', '.'),
        ('auth', 'auth'),
        ('components', 'components'),
        ('datasets', 'datasets'),
        ('metrics', 'metrics'),
        ('workspaces', 'workspaces'),
        ('services', 'services'),
        ('utils', 'utils'),
        ('Mock/gerar_mock.py', 'Mock'),
        ('Mock/mockuser.py', 'Mock'),
        ('.streamlit', '.streamlit'),
    ],
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
    name='Iniciar_Dashboard',
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
