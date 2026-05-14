class Validator:
    def __init__(self, question_type, checker):
        self.question_type = question_type
        self.checker = checker

def is_integer(s: str):
    return s and s[(s[0] in ["+", "-"]) :].isdigit()

def is_float(s: str):
    if not s:
        return False
    s = s.strip()
    if s[0] in ["+", "-"]:
        s = s[1:]
    if "." not in s:
        return is_integer(s)
    before, after = s.split(".", 1)
    return ((before.isdigit() or before == "") and (after.isdigit() or after == ""))
