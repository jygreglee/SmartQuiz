class ProblemItem:
    """D행 = 문제, C행 = 중요도, E행 = 설명, G행 = 암기법"""

    def __init__(self, topic, importance, description, mnemonic):
        self.topic = topic              # D열
        self.importance = importance    # C열
        self.description = description  # E열
        self.mnemonic = mnemonic        # G열

    def get_answer(self):
        """정답(설명 + 암기법)"""
        return (
            "[키워드 설명]\n"
            f"{self.description}\n\n"
            "[암기법]\n"
            f"{self.mnemonic}"
        )
