from subprocess import run


class Process:
    """
    ターミナルにて実行するコマンドをpython上で実行できるようにしたクラス
    処理に対応するターミナル上でのコマンドと概ね引数の取り方は同じ仕様とした。
    """

    def __init__(self):
        pass

    @staticmethod
    def make_directory(dir_path: str) -> int:
        # ディレクトリを作成するメソッド
        cmd = ["mkdir", dir_path]
        return run(args=cmd).returncode

    @staticmethod
    def touch_file(file_path: str) -> int:
        # ファイルを生成するコマンド
        cmd = ["touch", file_path]
        return run(args=cmd).returncode

    @staticmethod
    def move_file(file_path: str, dest_path: str) -> int:
        # ファイルを移動するメソッド
        cmd = ["mv", file_path, dest_path]
        return run(args=cmd).returncode

    @staticmethod
    def copy_file(file_path: str, dest_path: str) -> int:
        # 指定のパスにファイルをコピーするメソッド
        # 主に、事前配布のファイルを各パッケージにコピーするのに用いる
        cmd = [
            "cp",
            file_path,
            dest_path,
        ]
        return run(args=cmd).returncode

    @staticmethod
    def make_text(text: str, output_path: str) -> int:
        # テキストファイルを作成し、それを指定のディレクトリに出力するメソッド
        with open(output_path, "w") as txt:
            cmd = ["echo", text]
            return run(args=cmd, stdout=txt).returncode

    @staticmethod
    def rename_file(file_path: str, renamed_path: str) -> int:
        # ファイル名を書き換えるメソッド
        cmd = ["mv", file_path, renamed_path]
        return run(args=cmd).returncode

    @staticmethod
    def remove_file(path: str, option: str = None) -> int:
        # ファイルを削除するメソッド
        if option is None:
            cmd = ["rm", path]
        else:
            cmd = ["rm", option, path]

        return run(args=cmd).returncode

    @staticmethod
    def remove_dir(path: str, option: str = None) -> int:
        # ディレクトリを削除するメソッド
        if option is None:
            cmd = ["rm", "-r", path]
        else:
            cmd = ["rm", "-r", option, path]

        return run(args=cmd).returncode

    @staticmethod
    def grep(path: str, pattern: str, option: str = None) -> int:
        if option is None:
            cmd = ["grep", pattern, path]
        else:
            cmd = ["grep", option, pattern, path]

        for arg in cmd:
            print(arg, end=" ")
        else:
            print()

        return run(args=cmd).returncode

    @staticmethod
    def nkf(path, ctype: str = "utf-8") -> int:
        if ctype == "utf-8":
            cmd = ["nkf", "-w", "--overwrite", path]
        else:
            pass

        for arg in cmd:
            print(arg, end=" ")
        else:
            print()

        return run(args=cmd).returncode
