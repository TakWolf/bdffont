import hashlib
from pathlib import Path

from bdffont import BdfFont

project_root_dir = Path(__file__).parent.joinpath('..').resolve()


def _file_sha256(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'unifont', 'unifont-15.1.05.bdf')
    save_file_path = tmp_path.joinpath('unifont-15.1.05.bdf')
    font = BdfFont.load(load_file_path)
    save_file_path.write_text(font.dump().replace('\nBITMAP\n', '\nBITMAP \n'), 'utf-8')
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_galmuri9(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'galmuri', 'galmuri9.bdf')
    save_file_path = tmp_path.joinpath('galmuri9.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_gothic(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'misaki', 'misaki_gothic.bdf')
    save_file_path = tmp_path.joinpath('misaki_gothic.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_gothic_2nd(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'misaki', 'misaki_gothic_2nd.bdf')
    save_file_path = tmp_path.joinpath('misaki_gothic_2nd.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_misaki_mincho(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'misaki', 'misaki_mincho.bdf')
    save_file_path = tmp_path.joinpath('misaki_mincho.bdf')
    font = BdfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
