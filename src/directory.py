import os
import sys
import re

from process import Process


class Directory:
    """
    ディレクトリ構造を整えるクラス。取得した提出ファイルをもとにjavaパッケージとなるディレクトリを生成し、対応するjavaファイルを格納する。
    """

    def __init__(
        self,
        workspace_path: str,
        lecture_name: str,
        etc_dir: str = "etc",
        necessary_dir: str = "necessary_files",
        main_file_dir: str = "main_file",
        correct_result_dir: str = "correct_result",
        diff_result_dir: str = "diff_result",
        illegal_patterns_dir: str = "illegal_patterns",
        xls_dir: str = "xls_file",
    ):
        self.workspace_path = workspace_path
        self.lecture_name = lecture_name
        self.package_name = lecture_name

        # root_pathは提出されたファイルのあるディレクトリの絶対パスとしている。javalec1というディレクトリに提出ファイルがある場合、"/workspace/javalec1"がroot_pathになる。
        self.root_path = os.path.join(self.workspace_path, self.lecture_name)

        self.etc_path = os.path.join(self.root_path, etc_dir)

        self.necessary_path = os.path.join(self.etc_path, necessary_dir)
        self.main_file_path = os.path.join(self.etc_path, main_file_dir)
        self.correct_result_path = os.path.join(self.etc_path, correct_result_dir)
        self.diff_result_path = os.path.join(self.etc_path, diff_result_dir)
        self.illegal_patterns_path = os.path.join(self.etc_path, illegal_patterns_dir)
        self.xls_path = os.path.join(self.etc_path, xls_dir)

    def tidy_dir(self) -> None:
        """
        ディレクトリ構造を整理するメソッドで、これを行うことでJavaコンパイルおよび実行を可能としている。
        project_path以下に提出されたファイルを全て配置することでそれらを対応するパッケージに移動させる。
        また、課題をやるにあたって事前に与えられたファイルについてはパッケージをプログラム実行前に作成することで自動で各パッケージに配置させることができる。パッケージ名は"necessary_files"とする。
        """

        # etcディレクトリがない場合、ディレクトリを作成してプログラム終了する。
        # 再度、プログラムを実行することで必要なディレクトリを作成するので、プログラムの再実行を要求する。
        if self.is_exist_dir(self.etc_path):
            pass
        else:
            Process.make_directory(self.etc_path)
            print("Run this program again.")
            sys.exit(1)

        # サブファイルのディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.necessary_path):
            Process.make_directory(self.necessary_path)
            print('make directory "necessary_files"')

        # 比較結果の出力先ディレクトリがない場合、作成する。
        if not self.is_exist_dir(self.diff_result_path):
            Process.make_directory(self.diff_result_path)
            print('make directory "diff_result"')

        # grep用のパターンディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.illegal_patterns_path):
            Process.make_directory(self.illegal_patterns_path)
            print('make directory "illegal_patterns"')

        # 実行ファイル名のあるディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.main_file_path):
            Process.make_directory(self.main_file_path)
            print('make directory "main_file"')

        # 正しい出力のディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.correct_result_path):
            Process.make_directory(self.correct_result_path)
            print('make directory "correct_result_dir"')

        # xlsファイルのあるディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.xls_path):
            Process.make_directory(self.xls_path)
            print('make directory "xls_file"')

        # 実行に必要な他ファイル名を保存する。
        self.necessary_files = Directory.get_all_file(self.necessary_path)

        # grepにて検出したいパターンを保存する。
        self.illegal_patterns = Directory.get_all_file(self.illegal_patterns_path)

        # 実行ファイル名（メインクラスのあるファイル名)を保存する。
        # リストで保存する必要はないかもしれない。
        self.main_file = Directory.get_all_file(self.main_file_path)
        if not self.main_file:
            print('Place the main file in "main_file" directory.')
            sys.exit(1)

        # 比較対象の正しい出力結果がない場合、プログラム終了。
        if not Directory.get_all_file(self.correct_result_path):
            print('Place the correct result file in "correct_result" directory.')
            sys.exit(1)

        # xlsファイルがない場合、プログラム終了。
        if not Directory.get_all_file(self.xls_path):
            print('Place the excel file in "xls_file" directory.')
            sys.exit(1)

        if self.is_exist_dir(self.root_path):
            java_files = Directory.get_all_file(self.root_path)
            for f in java_files:
                file_name = os.path.splitext(os.path.basename(f))[0]

                # macにおいて.DS_Storeというファイルが生成されることがあり、これを処理の対象外とするための処理
                extension = os.path.splitext(os.path.basename(f))[1]
                if extension != ".java":
                    print("Illegal file type:", os.path.basename(f))
                    continue

                # パッケージ上部のディレクトリ名を"学年_組_番号"とした
                # このディレクトリは学生の名前を示すテキストファイルを含む
                identify_num = "_".join(re.findall(r"\d+", file_name)[1:4])
                student_name = file_name.split("_")[3]

                # パッケージ名を.javaファイル上で指定されたものにする必要があるが、各学生ごとに実行すべきファイル群が違うので一旦各学生ごとに異なるディレクトリを生成し、その中に指定されたパッケージ名のディレクトリを生成することで.javaファイルの実行を可能としている。
                Process.make_directory(os.path.join(self.root_path, identify_num))
                Process.make_directory(
                    os.path.join(self.root_path, identify_num, self.package_name)
                )
                Process.make_text(
                    student_name,
                    os.path.join(self.root_path, identify_num, "student_name.txt"),
                )
                Process.make_text(
                    os.path.basename(f),
                    os.path.join(
                        self.root_path, identify_num, "original_file_name.txt"
                    ),
                )
                if len(self.main_file) >= 1:
                    Process.rename_file(
                        os.path.join(self.root_path, f), self.main_file[0]
                    )
                    Process.move_file(
                        self.main_file[0],
                        os.path.join(self.root_path, identify_num, self.package_name),
                    )

                if self.necessary_files:
                    for nf in self.necessary_files:
                        Process.copy_file(
                            os.path.join(self.root_path, self.necessary_path, nf),
                            os.path.join(
                                self.root_path, identify_num, self.package_name
                            )
                            + "/",
                        )
        else:
            print(self.root_path, "was not existed. Input correct path.")
            sys.exit(1)

    def is_exist_dir(self, path) -> bool:
        """
        与えられたpathが存在するか返すメソッド
        """
        return os.path.isdir(path)

    def reset_directory(self) -> None:
        """
        root_path以下の全てのディレクトリを削除し、全てのファイルをroot_path以下に配置する。
        主にデバック時に用いるメソッド。
        """

        for pathname, dirnames, filenames in os.walk(self.root_path):
            if not self.is_student_dir(pathname):
                continue
            print(pathname)
            for f in filenames:
                if f.endswith(".java"):
                    if f == self.main_file[0]:
                        with open(
                            os.path.join(
                                os.path.dirname(pathname), "original_file_name.txt"
                            ),
                            "r",
                        ) as txt:
                            original_file_name = txt.readline().replace("\n", "")
                            Process.rename_file(
                                os.path.join(pathname, self.main_file[0]),
                                os.path.join(pathname, original_file_name),
                            )
                            Process.move_file(
                                os.path.join(pathname, original_file_name),
                                self.root_path,
                            )

        for pathname, dirnames, filenames in os.walk(self.root_path):
            for d in dirnames:
                if not self.is_student_dir(os.path.join(pathname, d)):
                    continue
                Process.remove_file(os.path.join(self.root_path, d), option="-r")
            else:
                break

        sys.exit(0)

    def is_student_dir(self, path: str) -> bool:
        """
        デバッグ用のメソッドreset_directoryに用いるメソッド。
        各学生ディレクトリ以外のディレクトリに対して、処理を行わないためのメソッド。
        与えられたpathが学生用ディレクトリかどうか判断するメソッド。
        """
        if path == self.necessary_path:
            return False
        if path == self.necessary_path:
            return False
        if path == self.correct_result_path:
            return False
        if path == self.diff_result_path:
            return False
        if path == self.xls_path:
            return False
        if path == self.etc_path:
            return False
        if path == self.main_file_path:
            return False
        if path == self.illegal_patterns_path:
            return False

        return True

    @classmethod
    def remove_classes(cls, path: str) -> list:
        """
        path以下にある.classファイルを全て削除するメソッド
        """
        for pathname, dirnames, filenames in os.walk(path):
            for f in filenames:
                if f.endswith(".class"):
                    Process.remove_file(os.path.join(pathname, f))

    @classmethod
    def get_all_file(cls, path: str) -> list[str]:
        """
        path以下の全てのファイル名を取得し、それらをlistとして返すメソッド
        """
        file_and_dir = os.listdir(path)
        files = [f for f in file_and_dir if os.path.isfile(os.path.join(path, f))]

        return files
