from directory import Directory
from process import Process

import os


class Nkf:
    """
    文字コードをutf-8に変更するクラス。
    utf-8以外に変更することも可能なはず。
    """

    def __init__(self, dir: Directory):
        self.dir = dir

    def encoding_all_file(self) -> None:
        print()
        print("***** encoding all files *****")

        for pathname, dirnames, filenames in os.walk(self.dir.root_path):
            if len(dirnames) == 1 and self.dir.package_name in dirnames:
                self.encoding(
                    os.path.join(pathname, self.dir.package_name, self.dir.main_file[0])
                )

    def encoding(self, path: str) -> bool:
        Process.nkf(path)
