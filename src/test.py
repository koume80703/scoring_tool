import os
from subprocess import run
from directory import Directory


class Test:
    """
    コンパイルおよび実行を行うクラス
    """

    def __init__(
        self,
        dir: Directory,
        # javacでのコンパイル時やjavaでの実行時にどんな引数で実行したのか表示するかどうか
        OUTPUT_COMMAND_DETAIL: bool = True,
    ):
        self.dir = dir
        self.COMPILE_COMMAND = "javac"
        self.EXE_COMMAND = "java"
        self.ENCODING = "UTF8"
        self.OUTPUT_DETAIL_COMMAND = OUTPUT_COMMAND_DETAIL

    def test_all_file(self) -> None:
        print()
        print("***** Testing all files *****")
        for pathname, dirnames, filenames in os.walk(self.dir.root_path):
            if len(dirnames) == 1 and self.dir.package_name in dirnames:
                self.test_file(
                    pathname, self.dir.main_file[0], output_file="result.txt"
                )

    def test_file(self, pathname: str, elapsed_file: str, output_file=None) -> None:
        compile_status = self.compile_file(
            os.path.join(pathname, self.dir.package_name, elapsed_file),
            classpath=pathname,
        )

        if compile_status == 1:
            print("<javac> was failed. Compile Error.")
            if output_file is not None:
                with open(os.path.join(pathname, output_file), "w") as txt:
                    txt.writelines(["compile error"])
            return

        exe_status = self.execute_file(
            os.path.join(self.dir.package_name, os.path.splitext(elapsed_file)[0]),
            classpath=pathname,
            output_dir=pathname,
            output_file=output_file,
        )

        if exe_status == 1:
            print("<java> was failed. Execution Error.")
            if output_file is not None:
                with open(os.path.join(pathname, output_file), "w") as txt:
                    txt.writelines(["execution error"])
            return

    def compile_file(self, path: str, classpath: str) -> int:
        # .javaファイルをコンパイルするメソッド
        cmd = [
            self.COMPILE_COMMAND,
            "-classpath",
            classpath,
            "-J-Dfile.encoding=" + self.ENCODING,
            path,
        ]
        if self.OUTPUT_DETAIL_COMMAND:
            for arg in cmd:
                print(arg, end=" ")
            print()
        return run(args=cmd).returncode

    def execute_file(
        self,
        class_name: str,
        classpath: str,
        output_dir: str = None,
        output_file: str = None,
    ) -> int:
        # .classファイルを実行するメソッド。
        # 引数に出力に関連するものがあるが、これらはメソッド呼び出し時に指定されなかった場合、標準出力で実行されるものとなる。指定された場合、"result.txt"というファイルにその実行結果が出力される。
        cmd = [
            self.EXE_COMMAND,
            "-classpath",
            classpath,
            "-Dfile.encoding=" + self.ENCODING,
            class_name,
        ]
        if self.OUTPUT_DETAIL_COMMAND:
            for arg in cmd:
                print(arg, end=" ")
            print()
        if output_file is None:
            return run(args=cmd).returncode
        else:
            with open(os.path.join(output_dir, output_file), "w") as txt:
                return run(args=cmd, stdout=txt).returncode
