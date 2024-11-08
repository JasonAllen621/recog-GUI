# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(10000)

SETUP_DIR = 'F:\\1A研究生\\实验\\for_graduation_pyqt\\'

a = Analysis(
    ["F:\\1A研究生\\实验\\for_graduation_pyqt\\change_IR_bkg_thread.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\img_concat_thread.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\main.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\recog_thread.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui_test.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui_thread.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\detect_thread.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\benchmarks.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\export.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\hubconf.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\common.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\experimental.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\tf.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\yolo.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__init__.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\activations.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\augmentations.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\autoanchor.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\autobatch.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\callbacks.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\dataloaders.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\downloads.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\general.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\loss.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\metrics.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\plots.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\torch_utils.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\triton.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__init__.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\dataloaders.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\general.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\__init__.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\detect_subwidget.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\detect_subwidget_indtance.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_bkg_set.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_bkg_set_instance.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_releated_subwidget.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_releated_subwidget_instance.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\main_widght.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\recog_subwidget.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\recog_subwidget_instance.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\model.py",
        "F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\utils.py"
        ],
    pathex=['F:\\1A研究生\\实验\\for_graduation_pyqt'],
    binaries=[],
    datas=[
    (SETUP_DIR+'model/*.*','model'),(SETUP_DIR+'ui/*.*','ui'),(SETUP_DIR+'utils/*.*','utils'),
    (SETUP_DIR+'model/model/*.*','model/model'),
    (SETUP_DIR+'model/model/yolov5/*.*','model/model/yolov5'),
    (SETUP_DIR+'model/model/yolov5/models/*.*','model/model/yolov5/models'),
    (SETUP_DIR+'model/model/yolov5/utils/*.*','model/model/yolov5/utils'),
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\detect_set.ui', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_bkg_set.ui', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\IR_releated_layout_widget.ui', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\object_recog_demo.ui', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\recog_set.ui', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\logo.png', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\logo.jpg', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\logo_gray.jpeg', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\weights\\8ship_best_v1.pt', 'model\\model\\yolov5\\weights') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\weights\\8ship_v2.pt', 'model\\model\\yolov5\\weights') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\weights\\vl_best.pt', 'model\\model\\yolov5\\weights') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\INFRAD\\DENSENET121\\model_epoch26_ACC0.9882_LOSS0.7570.pth', 'model\\model\\INFRAD\\DENSENET121') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\OPT\\DENSENET121\\model_epoch172_ACC0.9732_LOSS2.3807.pth', 'model\\model\\OPT\\DENSENET121') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\OPT\\REGNETY16GF\\model_epoch147_ACC0.9647_LOSS2.3621.pth', 'model\\model\\OPT\\REGNETY16GF') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\OPT\\RESNEXT50\\model_epoch71_ACC0.9796_LOSS2.3478.pth', 'model\\model\\OPT\\RESNEXT50') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\SAR\\DENSENET121\\model_epoch90_ACC0.8259_LOSS1.9448.pth', 'model\\model\\SAR\\DENSENET121') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\SAR\\REGNETY16GF\\model_epoch69_ACC0.8935_LOSS1.9001.pth', 'model\\model\\SAR\\REGNETY16GF') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\SAR\\RESNEXT50\\model_epoch42_ACC0.6960_LOSS2.0931.pth', 'model\\model\\SAR\\RESNEXT50') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\logo.ico', 'ui') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\common.cpython-37.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\common.cpython-39.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\experimental.cpython-37.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\experimental.cpython-39.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\yolo.cpython-37.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\yolo.cpython-39.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\__init__.cpython-37.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\models\\__pycache__\\__init__.cpython-39.pyc', 'model\\model\\yolov5\\models\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\general.pyc', 'model\\model\\yolov5\\utils') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\__pycache__\\general.cpython-37.pyc', 'model\\model\\yolov5\\utils\\segment\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\__pycache__\\general.cpython-39.pyc', 'model\\model\\yolov5\\utils\\segment\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\__pycache__\\__init__.cpython-37.pyc', 'model\\model\\yolov5\\utils\\segment\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\segment\\__pycache__\\__init__.cpython-39.pyc', 'model\\model\\yolov5\\utils\\segment\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\augmentations.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\augmentations.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\autoanchor.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\autoanchor.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\autobatch.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\callbacks.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\dataloaders.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\dataloaders.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\downloads.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\downloads.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\general.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\general.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\loss.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\metrics.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\metrics.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\plots.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\plots.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\torch_utils.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\torch_utils.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\__init__.cpython-37.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\utils\\__pycache__\\__init__.cpython-39.pyc', 'model\\model\\yolov5\\utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\__pycache__\\export.cpython-37.pyc', 'model\\model\\yolov5\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\yolov5\\__pycache__\\export.cpython-39.pyc', 'model\\model\\yolov5\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\model\\__pycache__\\detect_thread.cpython-39.pyc', 'model\\model\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\model\\__pycache__\\model.cpython-39.pyc', 'model\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\detect_subwidget.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\detect_subwidget_indtance.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\IR_bkg_set.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\IR_bkg_set_instance.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\IR_releated_subwidget.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\IR_releated_subwidget_instance.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\main_widght.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\object_recog_demo_v1_5.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\object_recog_demo_v1_6.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\recog_subwidget.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\recog_subwidget_instance.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\ui1.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\ui2.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\ui_object_recog_demo.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\__pycache__\\ui_object_recog_demo_record.cpython-39.pyc', 'ui\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\__pycache__\\model.cpython-39.pyc', 'utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\utils\\__pycache__\\utils.cpython-39.pyc', 'utils\\__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\__pycache__\\change_IR_bkg_thread.cpython-39.pyc', '__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\__pycache__\\detect_thread.cpython-39.pyc', '__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\__pycache__\\img_concat_thread.cpython-39.pyc', '__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\__pycache__\\recog_thread.cpython-39.pyc', '__pycache__') ,
    ('F:\\1A研究生\\实验\\for_graduation_pyqt\\__pycache__\\ui_thread.cpython-39.pyc', '__pycache__') ,
    ],
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
    name='demo',
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
    icon='F:\\1A研究生\\实验\\for_graduation_pyqt\\ui\\logo.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='demo',
)
