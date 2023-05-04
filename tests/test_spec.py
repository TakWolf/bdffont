import os
import shutil

import bdffont
from tests import path_define

if os.path.exists(path_define.build_dir):
    shutil.rmtree(path_define.build_dir)
os.makedirs(path_define.build_dir)


def test_encode_and_decode():
    bdf_file_path = os.path.join(path_define.assets_dir, 'example.bdf')
    with open(bdf_file_path, 'r', encoding='utf-8') as file:
        bdf_text = file.read()
    font = bdffont.decode_bdf(bdf_text)
    assert font.encode() == bdf_text


def test_load_and_save():
    bdf_file_path = os.path.join(path_define.assets_dir, 'unifont-15.0.01.bdf')
    output_path = os.path.join(path_define.build_dir, 'unifont-output.bdf')
    font = bdffont.load_bdf(bdf_file_path)
    font.save(output_path)
