import sys
from unittest.mock import patch

import pytest

from rasa_chinese_service.nlu.tokenizers.lm_tokenizer import (
    language_model_tokenizer_service,
)


@pytest.mark.parametrize(
    "text, expected_tokens, expected_indices",
    [
        (
            "我想去吃兰州拉面",  # easy/normal case
            ["我", "想", "去", "吃", "兰", "州", "拉", "面"],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)],
        ),
        (
            "从东畈村走了。",  # OOV case: `畈` is a OOV word
            ["从", "东", "[UNK]", "村", "走", "了", "。"],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)],
        ),
        (
            "Micheal 你好吗？",  # Chinese mixed up with English
            ["[UNK]", "你", "好", "吗", "？"],
            [
                (0, 7),
                (8, 9),
                (9, 10),
                (10, 11),
                (11, 12),
            ],
        ),
        (
            "我想买 iPhone 12 🤭",  # Chinese mixed up with English, numbers, and emoji
            ["我", "想", "买", "[UNK]", "12", "[UNK]"],
            [(0, 1), (1, 2), (2, 3), (4, 10), (11, 13), (14, 15)],
        ),
    ],
)
def test_tokenizer_for_chinese(text, expected_tokens, expected_indices):
    with patch.object(
        sys,
        "argv",
        ["rasa_chinese_service.nlu.tokenizers.lm_tokenizer", "bert-base-chinese"],
    ):
        app = language_model_tokenizer_service()

        _, response = app.test_client.get("/", params={"q": text})
        tokens = response.json

        assert [t[0] for t in tokens] == expected_tokens
        assert [t[1] for t in tokens] == [i[0] for i in expected_indices]
        assert [t[2] for t in tokens] == [i[1] for i in expected_indices]
