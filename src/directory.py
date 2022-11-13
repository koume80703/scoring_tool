import os
import sys

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
        patterns_dir: str = "patterns",
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
        self.patterns_path = os.path.join(self.etc_path, patterns_dir)
        self.xls_path = os.path.join(self.etc_path, xls_dir)

        self.check_dir_structure()

    def check_dir_structure(self):
        """
        ディレクトリ構造をチェックするメソッド。
        ディレクトリetc以下に必要なディレクトリが存在するか確認し、なければそれを生成する。
        なお、etcがそもそも存在しない場合、etcも生成する。
        """

        # etcディレクトリがない場合、ディレクトリを作成してプログラム終了する。
        # 再度、プログラムを実行することで必要なディレクトリを作成するので、プログラムの再実行を要求する。
        if self.is_exist_dir(self.etc_path):
            pass
        else:
            Process.make_directory(self.etc_path)
            print('make directory "etc"')

        # サブファイルのディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.necessary_path):
            Process.make_directory(self.necessary_path)
            print('make directory "necessary_files"')

        # grep用のパターンディレクトリが無い場合、作成する。
        if not self.is_exist_dir(self.patterns_path):
            Process.make_directory(self.patterns_path)
            print('make directory "patterns"')

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

        # 実行ファイル名（メインクラスのあるファイル名)を保存する。
        files = Directory.get_all_file(self.main_file_path)
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        if not files:
            print('Place the main file in "main_file" directory.')
            sys.exit(1)
        if len(files) == 1:
            self.main_file = files[0]

        # 比較対象の正しい出力結果がない場合、プログラム終了。
        if not Directory.get_all_file(self.correct_result_path):
            print('Place the correct result file in "correct_result" directory.')
            sys.exit(1)

        # xlsファイルがない場合、プログラム終了。
        if not Directory.get_all_file(self.xls_path):
            print('Place the excel file in "xls_file" directory.')
            sys.exit(1)

    def generate_tmp_dir(self) -> None:
        """
        javacにてコンパイルするにあたって、ディレクトリ構造を整理する必要があるので、一時的なディレクトリtmpを生成し、それをプロジェクトパスとして、tmp配下でコンパイル及び実行を行う。
        """

        self.tmp_path = os.path.join(self.root_path, "tmp")
        Process.make_directory(self.tmp_path)

        self.package_path = os.path.join(self.tmp_path, self.package_name)
        Process.make_directory(self.package_path)

        necessary_files = Directory.get_all_file(self.necessary_path)
        for nf in necessary_files:
            Process.copy_file(
                os.path.join(self.necessary_path, nf),
                os.path.join(self.tmp_path, self.package_name),
            )

        self.tmp_result_path = os.path.join(self.tmp_path, "result.txt")
        Process.touch_file(self.tmp_result_path)

        self.tmp_original_name_path = os.path.join(
            self.tmp_path, "original_file_name.txt"
        )
        Process.touch_file(self.tmp_original_name_path)

    def move_main_file(self, target_path: str) -> None:
        """
        テスト対象のソースをプロジェクトディレクトリ配下に配置し、適切なファイル名に変更する。

        Args:
            target_path (str): テスト対象のソースの絶対パス。
        """

        target_file_name = os.path.basename(target_path)

        Process.make_text(target_file_name, self.tmp_original_name_path)

        Process.move_file(target_path, self.package_path)

        Process.rename_file(
            os.path.join(self.package_path, target_file_name),
            os.path.join(self.package_path, self.main_file),
        )

    def replace_main_file(self) -> None:
        """
        採点終了後、メインファイルを元に戻すメソッド。ファイル名も元に戻す。
        """
        with open(self.tmp_original_name_path) as f:
            original_file_name = f.read().splitlines()[0]

        Process.rename_file(
            os.path.join(self.package_path, self.main_file),
            os.path.join(self.package_path, original_file_name),
        )

        Process.move_file(
            os.path.join(self.package_path, original_file_name), self.root_path
        )

    def remove_tmp_dir(self) -> None:
        """
        tmpディレクトリを削除するメソッド
        """
        Process.remove_dir(self.tmp_path)

        del self.tmp_path
        del self.package_path
        del self.tmp_result_path
        del self.tmp_original_name_path

    def is_exist_dir(self, path) -> bool:
        """
        与えられたpathが存在するか返すメソッド
        """
        return os.path.isdir(path)

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
