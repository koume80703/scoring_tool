import os
import sys
import re

from search import Search
from directory import Directory
from excel import Excel
from test import Test
from nkf import Nkf
from comparing import Compare
from status import Status


class Scoring:
    """
    学生が提出したファイルを実行し、得られた出力を正しい出力結果と比較し、採点を行うクラス。
    """

    LECTURE_KIND = ["javalec", "oolec"]

    # この採点ツールがどの講義におけるものなのか指定する。
    CHOOSED_LECTURE = LECTURE_KIND[0]

    def __init__(self, exe_stdout: bool = False):
        # lecture_nameはjavalec(oolec)の何回目にあたるのかを入れれば良い
        # 入力としては"javalecXX(oolecXX)"となるような値を期待している

        if self.CHOOSED_LECTURE == self.LECTURE_KIND[0]:
            lecture_num = input("Choose number of java lecture: ")
        elif self.CHOOSED_LECTURE == self.LECTURE_KIND[1]:
            lecture_num = input("Choose number of object oriented lecture: ")
        if not lecture_num.isdecimal():
            print("Invalid input. Not Decimal. Input was '" + lecture_num + "'")
            sys.exit(1)

        # 採点対象の実行時に出力を標準出力にするか、ファイルに出力するかのフラグ変数
        # Trueの場合、ファイル出力がないので、正答との比較が行われない。
        self.EXE_STDOUT = exe_stdout

        lecture_name = self.CHOOSED_LECTURE + lecture_num
        workspace_path = os.path.dirname(os.getcwd())

        self.dir = Directory(workspace_path, lecture_name)

        xls_files = Directory.get_all_file(self.dir.xls_path)
        for xf in xls_files:
            if os.path.splitext(os.path.basename(xf))[1] == ".xlsx":
                xls_file = xf
                break

        self.excel = Excel(os.path.join(self.dir.xls_path, xls_file))

    def get_status(self, path: str) -> Status:
        """採点結果のステータスを返すメソッド。

        Args:
            path (str): 採点対象の絶対パス。

        Returns:
            Status: 採点する上で、文句のないソースであれば、Status.SUCCESSを返す。
                    要件を満たしていない場合は、満たしていない要件に応じて返す値が変わる。
        """
        status = Search.search_for_all_patterns(path, self.dir.patterns_path)

        if status == Status.GREP_FAILURE:
            print("***** Detected grep error *****")
            return Status.GREP_FAILURE

        self.dir.generate_tmp_dir()
        self.dir.move_main_file(path)

        status = Test.test_file(
            self.dir.tmp_path,
            self.dir.package_name,
            self.dir.main_file,
            self.EXE_STDOUT,
        )

        if status == Status.COMPILE_FAILURE:
            print("***** Detected compile error *****")
            self.dir.replace_main_file()
            self.dir.remove_tmp_dir()
            return Status.COMPILE_FAILURE
        elif status == Status.EXECUTION_FAILURE:
            print("***** Detected execution error *****")
            self.dir.replace_main_file()
            self.dir.remove_tmp_dir()
            return Status.EXECUTION_FAILURE

        # Testクラスにおける出力がファイル出力ではない場合、出力と正答の比較ができないため、比較ステップは飛ばす。
        if self.EXE_STDOUT:
            pass
        else:
            status = Compare.compare_to_all_answer(
                self.dir.tmp_result_path, self.dir.correct_result_path
            )

        self.dir.replace_main_file()
        self.dir.remove_tmp_dir()

        if status == Status.COMPARING_FAILURE:
            print("***** Detected comparing error *****")
            return Status.COMPARING_FAILURE

        print("***** Correct submitted file *****")
        return Status.SUCCESS

    def scoring_all(self, write_excel: bool = True):
        all_files = Directory.get_all_file(self.dir.root_path)
        for file in all_files:
            if os.path.splitext(file)[1] == ".java":
                print("#" * 7, file, "#" * 7)
                self.scoring(os.path.join(self.dir.root_path, file), write_excel)
            else:
                print("#" * 7, "Illegal file was detected:", file, "#" * 7)
            print()

    def scoring(self, path: str, write_excel: bool = False) -> None:
        """採点メソッド。

        Args:
            path (str): 採点対象の絶対パス
            write_excel (bool, optional): エクセルに採点結果を出力するかどうかのフラグ。 Defaults to False.
        """

        # UTF-8に変更
        Nkf.encoding(path)

        status = self.get_status(path)

        if write_excel:
            filename = os.path.splitext(os.path.basename(path))[0]
            [grade, cls, num] = re.findall(r"\d+", filename.split("_")[2])

            grade, cls, num = int(grade), int(cls), int(num)

            if status == Status.SUCCESS:
                self.excel.write_score(grade, cls, num, 10, "よくできています。")
            elif status == Status.GREP_FAILURE:
                self.excel.write_score(
                    grade, cls, num, 99, "想定したパターンが見つかりません。もしくは、不適切なパターンがあります。要確認。"
                )
            elif status == Status.COMPILE_FAILURE or status == Status.EXECUTION_FAILURE:
                self.excel.write_score(grade, cls, num, 0, "実行できませんでした。")
            elif status == Status.COMPARING_FAILURE:
                self.excel.write_score(grade, cls, num, 99, "出力結果が間違っています。要確認。")
            else:
                print("Error: Illegal value in variable <status>")
                sys.exit(1)
            self.excel.save_workbook()
        else:
            print(status)


def main():
    if len(sys.argv) != 1:
        if sys.argv[1] == "-s":
            scoring = Scoring()
            [grade, cls, num] = sys.argv[2].split("_")
            all_files = Directory.get_all_file(scoring.dir.root_path)
            for f in all_files:
                if str(grade) + "年" + str(cls) + "組" + str(num) + "番" in f:
                    scoring.scoring(os.path.join(scoring.dir.root_path, f))
        if sys.argv[1] == "-t":
            scoring = Scoring(exe_stdout=True)
            [grade, cls, num] = sys.argv[2].split("_")
            all_files = Directory.get_all_file(scoring.dir.root_path)
            for f in all_files:
                if str(grade) + "年" + str(cls) + "組" + str(num) + "番" in f:
                    # vscodeにて採点対象ファイルへクリックでアクセスするための出力
                    print(os.path.join(scoring.dir.root_path, f))

                    scoring.dir.generate_tmp_dir()
                    scoring.dir.move_main_file(os.path.join(scoring.dir.root_path, f))

                    Test.test_file(
                        scoring.dir.tmp_path,
                        scoring.dir.package_name,
                        scoring.dir.main_file,
                        scoring.EXE_STDOUT,
                    )

                    scoring.dir.replace_main_file()
                    scoring.dir.remove_tmp_dir()
        if sys.argv[1] == "--debug":
            scoring.dir.generate_tmp_dir()
            scoring.dir.replace_main_file()
            scoring.dir.remove_tmp_dir()
    else:
        scoring = Scoring()
        scoring.scoring_all(write_excel=True)


if __name__ == "__main__":
    main()
