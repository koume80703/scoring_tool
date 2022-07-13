import difflib
import os
import sys

from typing import Optional

from search import Search
from directory import Directory
from excel import Excel
from test import Test
from nkf import Nkf


class Scoring:
    """
    学生が提出したファイルを実行し、得られた出力を正しい出力結果と比較し、採点を行うクラス。
    """

    def __init__(
        self,
        dir: Directory,
    ):
        self.dir = dir

        xls_files = Directory.get_all_file(self.dir.xls_path)
        for xf in xls_files:
            if os.path.splitext(os.path.basename(xf))[1] == ".xlsx":
                xls_file = xf

        self.excel = Excel(os.path.join(self.dir.xls_path, xls_file))

    def comp_all_result(self) -> None:
        """
        全ての出力結果に対して、正しい出力結果との比較を行うメソッド
        """

        # 学生番号以下のパッケージ名を用いて探索しているので、変数名がややこしくならないようにpackage_nameという変数にしている。
        # self.dir.lecture_nameを用いても問題はない
        package_name = self.dir.lecture_name
        result_file_name = "result.txt"
        print()
        print("***** Comparing all files *****")
        for pathname, dirnames, filenames in os.walk(self.dir.root_path):
            if len(dirnames) == 1 and package_name in dirnames:
                self.comp_result(
                    os.path.basename(pathname),
                    os.path.join(pathname, result_file_name),
                )

    def comp_result(self, identity_num: str, result_path: str) -> None:
        """
        出力結果と正しいものを比較する。
        比較した結果、一致したものに関しては何もしないが、一致しなかった場合、htmlファイルを生成し、何が異なっているのか検証できるようにした。
        """

        # TODO このメソッド外でresult.txtをチェックして出力結果がerrorでないものだけをこのメソッドに通すようにしたい。
        # 比較以外の処理を含んでいるので、それらをメソッド外に記述すべき。

        # result_pathは正しい結果に対して比較したいテキストファイルのパス
        # identity_numは比較対象のファイルがどの学生のものかを示す番号。学年_クラス_番号という形式で与えられる。

        diff = difflib.Differ()

        output_file = "diff_" + identity_num
        output_path = os.path.join(
            os.path.join(self.dir.diff_result_path, output_file),
        )

        ek = ["compile error", "execution error", "grep error"]

        with open(result_path, "r") as result_text:
            result_text_lines = result_text.readlines()
        if result_text_lines[0] in ek:
            for i in range(len(ek)):
                if result_text_lines[0] == ek[i]:
                    with open(output_path, "w") as f:
                        print(identity_num, ek[i])
                        f.writelines(ek[i])
        else:
            correct_result_text_list = Directory.get_all_file(
                self.dir.correct_result_path
            )

            for correct_result_text in correct_result_text_list:
                with open(
                    os.path.join(self.dir.correct_result_path, correct_result_text),
                    "r",
                ) as crt:
                    crt_lines = crt.readlines()
                    output_diff = diff.compare(crt_lines, result_text_lines)
                for i in output_diff:
                    if i[0] in ["+", "-"]:
                        break
                else:
                    break

            for i in output_diff:
                if i[0] in ["+", "-"]:
                    with open(output_path, "w") as f:
                        print(identity_num, "diff")
                        f.writelines(["diff"])
                    break
            else:
                with open(output_path, "w") as f:
                    print(identity_num, "ok")
                    f.writelines(["ok"])

    def scoring(self):
        self.comp_all_result()

        diff_result_names = Directory.get_all_file(self.dir.diff_result_path)
        scores = []
        for dr in diff_result_names:
            _, grade, cls, num = dr.split("_")
            grade, cls, num = int(grade), int(cls), int(num)
            with open(os.path.join(self.dir.diff_result_path, dr), "r") as f:
                if f.readline() == "ok":
                    scores.append((grade, cls, num, 10))
                else:
                    scores.append((grade, cls, num, None))

        self.write_score(scores)

    def write_score(self, scores: list[(int, int, int, Optional[int])]) -> None:
        self.excel.write_score(scores)


def main():
    # lecture_nameはjavalecの何回目にあたるのかを入れれば良い
    # 入力としては"javalecXX"となるような値を期待している
    # このlecture_nameという変数が各学生プロジェクト(ex. 2_14_001)に付随するパッケージ名になる
    lecture_num = input("Choose number of java lecture: ")
    lecture_name = "javalec" + lecture_num

    # 実行場所によってこの変数への代入値が異なってしまうので、実行場所はsrcにする必要がある。
    # TODO src以外の場所において実行したとしてもうまく実行できるようにしたい。
    workspace_path = os.path.dirname(os.getcwd())

    dir = Directory(workspace_path, lecture_name)
    dir.tidy_dir()

    if len(sys.argv) != 1:
        if sys.argv[1] == "-t":
            student_num = sys.argv[2]

            search = Search(dir)
            for pattern_file in dir.illegal_patterns:
                with open(
                    os.path.join(dir.illegal_patterns_path, pattern_file), "r"
                ) as p:
                    lines = p.read().splitlines()

                opi = lines[0].split(",")
                if len(opi) == 2:
                    [option, pattern] = opi
                    inverse = 0
                elif len(opi) == 3:
                    [option, pattern, inverse] = opi
                    inverse = int(inverse)

                search.search_text(
                    os.path.join(
                        dir.root_path,
                        student_num,
                        dir.package_name,
                        dir.main_file[0],
                    ),
                    pattern,
                    option=option,
                    inverse=inverse,
                )

            test = Test(dir)
            test.test_file(
                os.path.join(test.dir.root_path, student_num), dir.main_file[0]
            )
    else:
        Nkf(dir).encoding_all_file()

        Search(dir).search_all_file()

        Test(dir).test_all_file()

        Directory.remove_classes(dir.root_path)

        Scoring(dir).scoring()


if __name__ == "__main__":
    main()
