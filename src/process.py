from subprocess import run


class Process:
    """
    ターミナルにて実行するコマンドをpython上で実行できるようにしたクラス
    処理に対応するターミナル上でのコマンドと概ね引数の取り方は同じ仕様とした。
    """

    def __init__(self):
        pass

    @classmethod
    def make_directory(cls, dir_path: str) -> int:
        # ディレクトリを作成するメソッド
        cmd = ["mkdir", dir_path]
        return run(args=cmd).returncode

    @classmethod
    def move_file(cls, file_path: str, dest_path: str) -> int:
        # ファイルを移動するメソッド
        cmd = ["mv", file_path, dest_path]
        return run(args=cmd).returncode

    @classmethod
    def copy_file(cls, file_path: str, dest_path: str) -> int:
        # 指定のパスにファイルをコピーするメソッド
        # 主に、事前配布のファイルを各パッケージにコピーするのに用いる
        cmd = [
            "cp",
            file_path,
            dest_path,
        ]
        return run(args=cmd).returncode

    @classmethod
    def make_text(cls, text: str, output_path: str) -> int:
        # テキストファイルを作成し、それを指定のディレクトリに出力するメソッド
        with open(output_path, "w") as txt:
            cmd = ["echo", text]
            return run(args=cmd, stdout=txt).returncode

    @classmethod
    def rename_file(cls, file_path: str, renamed_path: str) -> int:
        # ファイル名を書き換えるメソッド
        cmd = ["mv", file_path, renamed_path]
        return run(args=cmd).returncode

    @classmethod
    def remove_file(cls, path: str, option: str = None) -> int:
        # ファイルを削除するメソッド
        if option is None:
            cmd = ["rm", path]
        else:
            cmd = ["rm", option, path]

        return run(args=cmd).returncode

    @classmethod
    def grep(cls, path: str, pattern: str, option: str = None) -> int:
        if option is None:
            cmd = ["grep", pattern, path]
        else:
            cmd = ["grep", option, pattern, path]

        return run(args=cmd).returncode

    @classmethod
    def grep_pipe(cls, path, patterns: list[str]) -> int:
        cmd = "grep"
        cmd += " " + patterns[0] + " " + path
        for i in range(1, len(patterns)):
            cmd += " | grep " + patterns[i]

        print(cmd)

        return run(args=cmd, shell=True).returncode
