# -*- mode: python -*-
#run: pyinstaller filename.spec

block_cipher = None

from kivy.deps import sdl2, glew, gstreamer
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

a = Analysis(['PlagueLyrics.py'],
             pathex=['C:\\repos\\bramvk38\\sw\\py-PlagueLyrics'],
             binaries=[],
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_all())
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PlagueLyrics',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('C:\\repos\\bramvk38\\sw\\py-PlagueLyrics'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
               strip=False,
               upx=True,
               name='PlagueLyrics')
