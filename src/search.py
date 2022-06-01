import os

from directory import Directory
from process import Process


class Search:
    """
    テキスト上から特定の文字列を検索するクラス
    提出されたソースファイルから不正な出力が行われるのを防ぐ
    """

    def __init__(self, dir: Directory):
        self.dir = dir

    def search_all_file(self) -> None:
        print()
        print("***** Searching illegal patterns *****")
        for pathname, dirnames, filenames in os.walk(self.dir.root_path):
            if len(dirnames) == 1 and self.dir.package_name in dirnames:
                for pattern_file in self.dir.illegal_patterns:
                    with open(
                        os.path.join(self.dir.illegal_patterns_path, pattern_file), "r"
                    ) as p:
                        lines = p.read().splitlines()
                        [option, pattern] = lines[0].split(",")
                        self.search_text(
                            os.path.join(
                                pathname, self.dir.package_name, self.dir.main_file[0]
                            ),
                            [pattern],
                            output_file="result.txt",
                            option=option,
                        )

    def search_text(
        self, path: str, patterns: list[str], output_file=None, option=None
    ) -> None:
        if len(patterns) == 1:
            pattern = patterns[0]
            grep_status = Process.grep(path, pattern, option=option)
        else:
            grep_status = Process.grep_pipe(path, patterns)

        if grep_status == 0:
            print("Illegal pattern was discovered.")
            if output_file is not None:
                with open(os.path.join(os.path.dirname(path), output_file), "w") as txt:
                    txt.writelines(["error"])
            return
