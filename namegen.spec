# -*- mode: python -*-

block_cipher = None

import platform
system = platform.system()
if system == 'Windows':
    folderslash = '\\'
else:
    folderslash = '/'
string = "%s" + folderslash + "*"

a = Analysis(['namegen.py', 'namegen.spec'],
             pathex=['/home/jack/Documents/non-work/DnD/mynamegen'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob(string % d, files)
    files = []
    rec_glob(string % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

a.datas += extra_datas('namedb/')
#a.datas += [("namedb/","/home/jack/Documents/non-work/DnD/mynamegen/namedb/","DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='namegen',
          debug=False,
          strip=False,
          upx=True,
          console=True )
