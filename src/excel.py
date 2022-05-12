import openpyxl as px

from typing import Optional


class Excel:
    def __init__(self, wb_path):
        self.wb_path = wb_path
        self.workbook = px.load_workbook(wb_path)

        self.worksheet = self.workbook.worksheets[0]

    def write_score(self, scores: list[tuple[Optional[int]]]) -> None:
        for row in self.worksheet.iter_rows(min_row=2):
            grade = int(row[1].value)
            cls = int(row[2].value)
            num = int(row[3].value)

            student = (grade, cls, num)

            for sc in scores:
                if (sc[0], sc[1], sc[2]) == student:
                    if sc[3] is None:
                        row[7].value = "採点結果を入力。エラーあり。"
                    elif sc[3] == 10:
                        row[7].value = "10点: よくできています。"
                    scores.remove(sc)

        self.workbook.save(self.wb_path)
