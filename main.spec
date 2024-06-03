# -*- mode: python ; coding: utf-8 -*-

SETUP_DIR = 'F:\\1A研究生\\实验\\for_graduation_pyqt\\'

a = Analysis(
    ['main.py', 'change_IR_bkg_thread.py', 'img_concat_thread.py','recog_thread.py','ui_thread.py',
    'F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\model.py','F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\utils.py',
    'F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_bkg_set.py','F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_bkg_set_instance.py',
    'F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_releated_subwidget.py','F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_releated_subwidget_instance.py',
    'F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\main_widght.py','F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\main_widght.py',
    'F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\recog_subwidget_instance.py'],
    pathex=['F:\\1A研究生\\实验\\for_graduation_pyqt'],
    binaries=[],
    datas=[(SETUP_DIR+'model/*.*','model'),(SETUP_DIR+'ui/*.*','ui'),(SETUP_DIR+'utils/*.*','utils'),
    (SETUP_DIR+'model/model/INFRAD/DENSENET121/model_epoch26_ACC0.9882_LOSS0.7570.pth','model/model/INFRAD/DENSENET121'),
    (SETUP_DIR+'model/model/OPT/DENSENET121/model_epoch172_ACC0.9732_LOSS2.3807.pth','model/model/OPT/DENSENET121'),
    (SETUP_DIR+'model/model/OPT/REGNETY16GF/model_epoch147_ACC0.9647_LOSS2.3621.pth','model/model/OPT/REGNETY16GF'),
    (SETUP_DIR+'model/model/OPT/RESNEXT50/model_epoch71_ACC0.9796_LOSS2.3478.pth','model/model/OPT/RESNEXT50'),
    (SETUP_DIR+'model/model/SAR/DENSENET121/model_epoch90_ACC0.8259_LOSS1.9448.pth','model/model/SAR/DENSENET121'),
    (SETUP_DIR+'model/model/SAR/REGNETY16GF/model_epoch69_ACC0.8935_LOSS1.9001.pth','model/model/SAR/REGNETY16GF'),
    (SETUP_DIR+'model/model/SAR/RESNEXT50/model_epoch42_ACC0.6960_LOSS2.0931.pth','model/model/SAR/RESNEXT50')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
