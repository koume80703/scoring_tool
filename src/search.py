import os

from directory import Directory
from process import Process
from status import Status


class Search:
    """
    テキスト上から特定の文字列を検索するクラス
    提出されたソースファイルから不正な出力が行われるのを防ぐ。
    また、ソースが課題の要求を満たすような文を含むか
    """

    def __init__(self):
        pass

    @classmethod
    def search_for_all_patterns(
        cls, path: str, pattern_path: str, option=None, inverse=0
    ) -> bool:
        # 文字列をソースコード中から探索し、要件を満たすソースとなっているか確認する。
        patterns = Directory.get_all_file(pattern_path)
        for pat in patterns:
            with open(os.path.join(pattern_path, pat), "r") as p:
                lines = p.read().splitlines()

            for line in lines:
                args = line.split(",")

                if len(args) == 2:
                    [option, pattern] = args
                    inverse = 0
                elif len(args) == 3:
                    [option, pattern, inverse] = args
                    inverse = int(inverse)

                if option == "":
                    option = None

                if not cls.search_text(path, pattern, option=option, inverse=inverse):
                    return Status.GREP_FAILURE

        return Status.SUCCESS

    @staticmethod
    def search_text(path: str, pattern: str, option: str = None, inverse=0) -> bool:
        """patternがソースコードに含まれているかどうか

        Args:
            path (str): 調べられる対象ソースの絶対パス
            pattern (str): 探したい文字列
            option (str, optional): grepコマンドにつけるオプション引数。 Defaults to None.
            inverse (int, optional): 文字列があることが要求されるのか、ないことが要求されるのかによって値が変わる。
                                     文字列があって欲しい場合、1。Defaults to 0.

        Returns:
            bool: 要件を満たさない場合、Falseを返す。
        """

        # grepコマンドの戻り値は、マッチした行があれば0、なければ1を返す。
        grep_status = Process.grep(path, pattern, option=option) - inverse

        if grep_status == 0:
            if inverse == 1:
                print("<< Required pattern was NOT discovered. >>")
            else:
                print("<< Illegal pattern was discovered. >>")
            return False
        else:
            return True
