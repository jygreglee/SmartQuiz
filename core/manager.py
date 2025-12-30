import random

class ProblemManager:
    """문제 목록을 기반으로 랜덤/차례/검색 기능 지원"""

    def __init__(self, problems):
        self.problems = problems
        self.index = 0  # 차례 모드용

    # 차례 모드
    def current(self):
        return self.problems[self.index]

    def next(self):
        if self.index < len(self.problems) - 1:
            self.index += 1
        return self.current()

    def prev(self):
        if self.index > 0:
            self.index -= 1
        return self.current()

    # 랜덤 모드
    def random_problem(self):
        return random.choice(self.problems)

    # 검색 기능
    def search(self, keyword):
        key = keyword.lower()
        results = []
        for p in self.problems:
            text = f"{p.topic} {p.description} {p.mnemonic}".lower()
            if key in text:
                results.append(p)
        return results
