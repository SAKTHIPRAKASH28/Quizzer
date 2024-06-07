import json
import regex as re
def extract_json(text_response):
    pattern = r'\{\s*"questionNumber"\s*:\s*\d+\s*,\s*"question"\s*:\s*".*?"\s*,\s*"options"\s*:\s*\{(?:\s*".*?"\s*:\s*".*?"\s*,?\s*)+\}\s*,\s*"correctOption"\s*:\s*".*?"\s*\}'

    matches = re.finditer(pattern, text_response)
    json_objects = []
    for match in matches:
        json_str = match.group(0)
        try:
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            extended_json_str = extend_search(text_response, match.span())
            try:
                json_obj = json.loads(extended_json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                continue
    if json_objects:
        return json_objects
    else:
        return None  
    
def extend_search(text, span):

    start, end = span
    nest_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            nest_count += 1
        elif text[i] == '}':
            nest_count -= 1
            if nest_count == 0:
                return text[start:i+1]
    return text[start:end]