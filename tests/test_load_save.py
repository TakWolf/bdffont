import hashlib
import os
from pathlib import Path

from bdffont import BdfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _file_sha256(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.bdf')
    save_file_path = os.path.join(tmp_path, 'unifont-15.1.05.bdf')
    font = BdfFont.load(load_file_path)
    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(font.dump().replace('\nBITMAP\n', '\nBITMAP \n'))
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_galmuri9(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'galmuri', 'galmuri9.bdf')
    save_file_path = os.path.join(tmp_path, 'galmuri9.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_gothic(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'misaki', 'misaki_gothic.bdf')
    save_file_path = os.path.join(tmp_path, 'misaki_gothic.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_gothic_2nd(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'misaki', 'misaki_gothic_2nd.bdf')
    save_file_path = os.path.join(tmp_path, 'misaki_gothic_2nd.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_mincho(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'misaki', 'misaki_mincho.bdf')
    save_file_path = os.path.join(tmp_path, 'misaki_mincho.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
