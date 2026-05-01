import json
import anthropic


def parse_json(text: str):
    """Strip markdown fences and extract the first complete JSON object or array."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    arr_start = text.find("[")
    obj_start = text.find("{")
    if arr_start != -1 and (obj_start == -1 or arr_start < obj_start):
        start, end = arr_start, text.rfind("]")
    else:
        start, end = obj_start, text.rfind("}")
    if start != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic()
