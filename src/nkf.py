from directory import Directory
from process import Process


class Nkf:
    """
    文字コードをutf-8に変更するクラス。
    utf-8以外に変更することも可能なはず。
    """

    def __init__(self, dir: Directory):
        pass

    @classmethod
    def encoding(cls, path: str) -> bool:
        Process.nkf(path)
