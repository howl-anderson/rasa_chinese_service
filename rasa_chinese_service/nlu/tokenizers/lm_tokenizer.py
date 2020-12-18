import argparse
from transformers import AutoTokenizer
from sanic import Sanic
from sanic.response import json
from functools import partial
from json import dumps

json_dumps = partial(dumps, separators=(",", ":"))


def language_model_tokenizer_service():
    parser = argparse.ArgumentParser(description='HuggingFace transformers tokenizer service')
    parser.add_argument('model_weights', type=str, help='Pre-Trained weights to be loaded')
    parser.add_argument("--cache_dir", type=str, default=None, required=False,
                        help='an optional path to a specific directory to download and cache the pre-trained model weights.')
    args = parser.parse_args()

    model_weights = args.model_weights
    cache_dir = args.cache_dir

    tokenizer = AutoTokenizer.from_pretrained(
        model_weights, cache_dir=cache_dir, use_fast=True
    )

    app = Sanic()

    @app.route('/')
    async def portal(request):
        text = request.args["q"][0]

        print(text)

        encoded_input = tokenizer(
            text, return_offsets_mapping=True, add_special_tokens=False
        )
        tokens_text_in = tokenizer.convert_ids_to_tokens(
            encoded_input["input_ids"]
        )

        tokens = []
        for token_text, position in zip(
                tokens_text_in, encoded_input["offset_mapping"]
        ):
            tokens.append([token_text, position[0], position[1]])

        return json(tokens, dumps=json_dumps, ensure_ascii=False)

    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    language_model_tokenizer_service()
