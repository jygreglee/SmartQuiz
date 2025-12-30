import pandas as pd
from core.model import ProblemItem

class ProblemBankLoader:
    def __init__(self, excel_path):
        self.path = excel_path

    def load(self):
        xls = pd.ExcelFile(self.path)
        sheet = xls.sheet_names[0]

        df = pd.read_excel(self.path, sheet_name=sheet)

        problems = []
        for _, row in df.iterrows():

            topic = row.get("중토픽")
            importance = row.get("중요도")
            desc = row.get("키워드 특징 및 설명")
            mnemonic = row.get("암기법")

            # 문제(topic)가 없으면 스킵
            if pd.isna(topic):
                continue

            problems.append(
                ProblemItem(topic, importance, desc, mnemonic)
            )

        return problems
