from reslv import Resolver
import itertools
import re


def generate_binary_replacements(expr) -> list[str]:
    letters = sorted(set(re.findall(r"[a-zA-Z]", expr)))
    combinations = itertools.product("01", repeat=len(letters))
    return [
        "".join(mapping[c] if c in mapping else c for c in expr)
        for combo in combinations
        if (mapping := dict(zip(letters, combo)))
    ]


def repl():
    calc = Resolver()
    while True:
        line = input("> ")
        if line == "BYE":
            print("< bye!")
            exit()
        lines = generate_binary_replacements(line)
        for line in lines:
            try:
                print(f"< {line}", calc.parse(line))
            except SyntaxError as e:
                print(f"Syntax Error: {e.msg}")


if __name__ == "__main__":
    repl()
