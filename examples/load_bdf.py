import os

import bdffont
from examples import path_define


def main():
    font = bdffont.load_bdf(os.path.join(path_define.assets_dir, 'unifont-15.0.01.bdf'))


if __name__ == '__main__':
    main()
