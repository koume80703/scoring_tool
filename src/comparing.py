from status import Status
from directory import Directory

import os


class Compare:
    def __init__(self):
        pass

    @classmethod
    def compare_to_all_answer(cls, target_path: str, cr_path: str) -> Status:
        """正答パターンが1つとは限らないので、正答パターンそれぞれに対して比較を行う。

        Args:
            target_path (str): 比較対象の出力結果ファイルの絶対パス。
            cr_path (str): 正答ファイルのあるディレクトリの絶対パス。

        Returns:
            Status: 正答パターンどれかに一致していれば Status.SUCCESS を返す。
                    どれにも一致しなければ Status.COMPARING_FAILURE を返す。
        """

        cr_list = Directory.get_all_file(cr_path)

        for answer in cr_list:
            if cls.compare(target_path, os.path.join(cr_path, answer)):
                return Status.SUCCESS
        else:
            return Status.COMPARING_FAILURE

    @staticmethod
    def compare(target_path: str, answer_path: str) -> bool:
        """出力結果と正答の比較結果を返すメソッド。

        Args:
            target_path (str): 比較対象の出力結果ファイルの絶対パス。
            answer_path (str): 正答ファイルの絶対パス。

        Returns:
            bool: 比較結果が一致していれば True, 異なっていれば False。
        """

        with open(target_path, "r") as f:
            target_text = f.read().splitlines(keepends=False)
            if target_text == []:
                return False

        with open(answer_path, "r") as f:
            answer_text = f.read().splitlines(keepends=False)

        for i, answer_line in enumerate(answer_text):
            target_line = target_text[i]
            if answer_line != target_line:
                return False
        else:
            return True
