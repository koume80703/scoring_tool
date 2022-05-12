import difflib
import os
import sys

from typing import Optional

from directory import Directory
from excel import Excel
from test import Test


class Scoring:
    """
    学生が提出したファイルを実行し、得られた出力を正しい出力結果と比較し、採点を行うクラス。
    """

    # root_pathはsrcディレクトリの親ディレクトリを指定する。
    # lecture_nameは採点対象の講義名を"javalecXX"の形で指定する。
    # correct_result_dirは正しい出力結果のおいてあるディレクトリ名を指定する。

    # TODO コンストラクタの引数にDirectory型の変数を取ることで、余計な変数の生成を防ぎたい。
    # self.main_file_dirなどはすでにDirectoryクラスのインスタンスで生成された変数であるので、わざわざ、このTestクラスでも同じ変数を用意する必要はない。
    def __init__(
        self,
        workspace_path: str,
        lecture_name: str,
        etc_dir: str = "etc",
        correct_result_dir: str = "correct_result",
        diff_result: str = "diff_result",
        xls_dir: str = "xls_file",
    ):
        self.root_path = os.path.join(workspace_path, lecture_name)
        self.lecture_name = lecture_name
        self.etc_dir = etc_dir
        self.correct_result_dir = os.path.join(self.etc_dir, correct_result_dir)
        self.diff_result = os.path.join(self.etc_dir, diff_result)
        self.xls_dir = os.path.join(self.etc_dir, xls_dir)

        xls_file = Directory.get_all_file(os.path.join(self.root_path, self.xls_dir))[1]
        self.excel = Excel(os.path.join(self.root_path, self.xls_dir, xls_file))

    def comp_all_result(self) -> None:
        """
        全ての出力結果に対して、正しい出力結果との比較を行うメソッド
        """

        # 学生番号以下のパッケージ名を用いて探索しているので、変数名がややこしくならないようにpackage_nameという変数にしている。
        # self.lecture_nameを用いても問題はない
        package_name = self.lecture_name
        result_file_name = "result.txt"
        for pathname, dirnames, filenames in os.walk(self.root_path):
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

        # result_pathは正しい結果に対して比較したいテキストファイルのパス
        # identity_numは比較対象のファイルがどの学生のものかを示す番号。学年_クラス_番号という形式で与えられる。

        diff = difflib.Differ()

        output_file = "diff_" + identity_num
        output_path = os.path.join(
            os.path.join(self.root_path, self.diff_result, output_file),
        )

        with open(result_path, "r") as result_text:
            result_text_lines = result_text.readlines()
        if len(result_text_lines) > 0 and result_text_lines[0] == "error":
            with open(output_path, "w") as f:
                print(identity_num, "error")
                f.writelines(["error"])
        else:
            # 比較した結果、出力結果が一致していなければ、htmlDiffを用いて比較結果のファイルをhtml形式で出力する。
            # TODO 比較結果が一致不一致によって出力ファイルの形式がテキストかhtmlか変わっており、統一性がないのをなんとかしたい。
            correct_result_text_list = Directory.get_all_file(
                os.path.join(self.root_path, self.correct_result_dir)
            )

            for correct_result_text in correct_result_text_list:
                with open(
                    os.path.join(
                        self.root_path, self.correct_result_dir, correct_result_text
                    ),
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
        # TODO 比較結果をdiff_resultに保存することができたので、次はその比較結果ファイルをもとに各学生に対して採点を行う。
        self.comp_all_result()

        diff_result_names = Directory.get_all_file(
            os.path.join(self.root_path, self.diff_result)
        )
        scores = []
        for dr in diff_result_names:
            _, grade, cls, num = dr.split("_")
            grade, cls, num = int(grade), int(cls), int(num)
            with open(os.path.join(self.root_path, self.diff_result, dr), "r") as f:
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
    workspace_dir = os.path.dirname(os.getcwd())

    if len(sys.argv) != 1:
        if sys.argv[1] == "-t":
            student_num = sys.argv[2]
            test = Test(workspace_dir, lecture_name)
            elapsed_files = Directory.get_all_file(
                os.path.join(test.root_path, test.main_file_dir)
            )
            test.test_file(os.path.join(test.root_path, student_num), elapsed_files[0])
    else:
        dir = Directory(workspace_dir, lecture_name)
        dir.tidy_dir()

        test = Test(workspace_dir, lecture_name)
        test.test_all_file()

        Directory.remove_classes(dir.root_path)

        scoring = Scoring(workspace_dir, lecture_name)
        scoring.scoring()


if __name__ == "__main__":
    main()
