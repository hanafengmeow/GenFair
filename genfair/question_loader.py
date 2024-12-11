from __future__ import annotations

import json
import random
from collections import defaultdict
from typing import Literal


class QuestionLoader:
    
    type QuestionType = Literal['SAM', 'GPD', 'SCS', 'ORR', 'CRA']
    
    registry: dict[QuestionType, list[tuple[str, str]]]
        
    def __init__(self, file: str = 'resources/questions.json') -> None:
        questions = json.load(open(file))
        self.registry = defaultdict(list)
        for question in questions:
            self.registry[question['evaluation_dimension']].append(tuple(question['sample_question_pair']))
        
    def load_question_pairs(self, type: QuestionType, n: int = 1) -> list[tuple[str, str]]:
        all_question_pairs = self.registry[type]
        return random.choices(all_question_pairs, k=n)