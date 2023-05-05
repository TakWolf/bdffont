import os

import bdffont
from examples import assets_dir, build_dir


def test_encode_and_decode():
    bdf_file_path = os.path.join(assets_dir, 'example.bdf')
    with open(bdf_file_path, 'r', encoding='utf-8') as file:
        bdf_text = file.read()
    font = bdffont.decode_bdf_str(bdf_text)
    assert font.encode_str() == bdf_text


def test_load_and_save():
    bdf_file_path = os.path.join(assets_dir, 'unifont-15.0.01.bdf')
    output_path = os.path.join(build_dir, 'unifont-output.bdf')
    font = bdffont.load_bdf(bdf_file_path)
    font.save(output_path)
