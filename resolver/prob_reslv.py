from reslv import Resolver
import itertools


def generate_binary_replacements(
    expr: str, letters: list[str]
) -> list[tuple[str, dict[str, str]]]:
    combinations = itertools.product("01", repeat=len(letters))
    return [
        ("".join(mapping[c] if c in mapping else c for c in expr), mapping.copy())
        for combo in combinations
        if (mapping := dict(zip(letters, combo)))
    ]


def main():
    props = {}
    props_n = int(input("请输入命题的数量: "))

    from string import ascii_lowercase

    start = ascii_lowercase.index("p")  # 从 p 开始
    symbols = ascii_lowercase[start:]
    if props_n > len(symbols):
        raise ValueError("命题数量超过可用的符号数量 (p-z)。")

    print(f"输入 {props_n} 个命题: ")
    for n in list(range(0, props_n)):
        inp = input(f"{symbols[n]} = ").strip()
        if inp:
            props[symbols[n]] = inp

    conds = []
    conds_n = int(input("\n现在你可以输入条件的数量: "))
    for n in list(range(conds_n)):
        inp = input("> ").strip()
        if inp:
            conds.append(inp)
    if not conds:
        raise ValueError("未输入条件。")

    cond_expressions = generate_binary_replacements(
        "&".join(conds), sorted(props.keys())
    )

    calc = Resolver()
    print("\n恭喜你：")
    count = 0
    for expr, truth_values in cond_expressions:
        if calc.parse(expr):
            true_props = [props[k] for k, v in truth_values.items() if v == "1"]
            if true_props:
                count += 1
                print(f"方案 {count} ：", end="")
                print("，".join(true_props))
    print(f"我们一共找到 {count} 个方案")
    if count == 0:
        print("没有任何组合满足条件，别灰心，起码这数学上无解。")


if __name__ == "__main__":
    main()
