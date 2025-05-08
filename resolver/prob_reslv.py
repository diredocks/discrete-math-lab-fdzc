from reslv import Resolver
import itertools


def generate_binary_replacements(
    expr: str, letters: list[str]
) -> list[tuple[str, dict[str, str]]]:
    combinations = itertools.product("01", repeat=len(letters))
    results = []
    for combo in combinations:
        mapping = dict(zip(letters, combo))
        replaced = "".join(mapping[c] if c in mapping else c for c in expr)
        results.append((replaced, mapping.copy()))
    return results


def prop_mapper(props: list[str]) -> dict[str, str]:
    from string import ascii_lowercase

    start = ascii_lowercase.index("p")  # Start from 'p'
    symbols = ascii_lowercase[start:]
    if len(props) > len(symbols):
        raise ValueError("命题数量超过可用的符号数量 (p-z)。")
    return {symbols[i]: prop for i, prop in enumerate(props)}


def condition_merger(conditions: list[str]) -> str:
    return "&".join(conditions)


def main():
    props = []
    print("输入任意个命题，要结束对命题的输入，输入 'END' :")
    while True:
        inp = input("> ").strip()
        if inp.upper() == "END":
            break
        if inp:
            props.append(inp)

    symbol_map = prop_mapper(props)
    print("\n--- 命题映射 ---")
    for k, v in symbol_map.items():
        print(f"{k}: {v}")
    print("---\n")

    conds = []
    print("输入任意个条件（例如 p&q），要结束对条件的输入，输入 'END' :")
    while True:
        inp = input("> ").strip()
        if inp.upper() == "END":
            break
        if inp:
            conds.append(inp)

    if not conds:
        print("未输入条件。")
        return

    cond_expr = condition_merger(conds)
    letters = sorted(symbol_map.keys())
    cond_expressions = generate_binary_replacements(cond_expr, letters)

    calc = Resolver()
    print("\n满足条件时为真的命题：\n-----------------------")
    count = 0
    for expr, truth_values in cond_expressions:
        if calc.parse(expr):
            count += 1
            print(f"方案 {count} ：", end="")
            true_props = [symbol_map[k] for k, v in truth_values.items() if v == "1"]
            if true_props:
                print("，".join(true_props))
    print(f"共 {count} 个方案")
    if count == 0:
        print("没有任何组合满足条件。")
    print("-----------------------")


if __name__ == "__main__":
    main()
