import os
from subprocess import run

from status import Status


class Test:
    """
    コンパイルおよび実行を行うクラス
    """

    COMPILE_COMMAND = "javac"
    EXE_COMMAND = "java"
    ENCODING = "UTF8"
    COMMAND_DETAIL = True

    RESULT_FILE = "result.txt"  # Directoryクラスで生成するtmp/result.txtに一致させる

    def __init__(self):
        pass

    @classmethod
    def test_file(
        cls,
        path: str,
        package_name: str,
        main_file: str,
        stdout: bool = True,
    ) -> Status:
        """コンパイルと実行を行うメソッド

        Args:
            path (str): tmpディレクトリの絶対パスが入る
            package_name (str): 指定されたパッケージ名が入る。パスではないことに注意
            main_file (str): メインファイル名が入る。パスではないことに注意
            stdout (bool): 実行時に出力を標準出力にするか、ファイルへの出力へするか定めるフラグ

        Returns:
            Status: _description_
        """

        compile_status = cls.compile_file(
            os.path.join(path, package_name, main_file), path
        )

        if compile_status == 1:
            print("<javac> was failed. Compile Error.")
            return Status.COMPILE_FAILURE

        output_path = None if stdout else os.path.join(path, Test.RESULT_FILE)

        exe_status = cls.execute_file(
            os.path.join(package_name, os.path.splitext(main_file)[0]),
            classpath=path,
            output_path=output_path,
        )

        if exe_status == 1:
            print("<java> was failed. Execution Error.")
            return Status.EXECUTION_FAILURE

        return Status.SUCCESS

    @classmethod
    def compile_file(cls, path: str, classpath: str) -> int:
        # .javaファイルをコンパイルするメソッド
        cmd = [
            Test.COMPILE_COMMAND,
            "-classpath",
            classpath,
            "-J-Dfile.encoging=" + Test.ENCODING,
            path,
        ]

        if Test.COMMAND_DETAIL:
            for arg in cmd:
                print(arg, end=" ")
            print()
        return run(args=cmd).returncode

    @classmethod
    def execute_file(
        cls, classname: str, classpath: str, output_path: str = None
    ) -> int:
        # .classファイルを実行するメソッド。
        # 引数に出力に関連するものがあるが、これらはメソッド呼び出し時に指定されなかった場合、標準出力で実行されるものとなる。

        cmd = [
            Test.EXE_COMMAND,
            "-classpath",
            classpath,
            "-Dfile.encoding=" + Test.ENCODING,
            classname,
        ]

        if Test.COMMAND_DETAIL:
            for arg in cmd:
                print(arg, end=" ")
            print()
        if output_path is None:
            return run(args=cmd).returncode
        else:
            with open(output_path, "w") as txt:
                return run(args=cmd, stdout=txt).returncode
