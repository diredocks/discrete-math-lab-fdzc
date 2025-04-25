import re


class Resolver:
    def __init__(self):
        self.line: str = ""
        self.current: str = ""

    def parse(self, expr: str) -> bool:
        self.line = expr
        result = self._exp()
        if self.line != "":
            raise SyntaxError(
                f"Unexpected character after expression: '{self.line[0]}'"
            )
        return result

    def _exp(self) -> bool:
        result = self._term()
        while self._is_next("[&|]"):
            match self.current:
                case "&":
                    result = self._term() and result
                case "|":
                    result = self._term() or result
        return result

    def _term(self) -> bool:
        result = self._factor()
        while self._is_next("[+-]"):
            match self.current:
                case "+":
                    result = result == self._factor()
                case "-":
                    result = self._factor() or (not result)
        return result

    def _factor(self) -> bool:
        if self._is_next(r"[0-1]*\.?[0-1]+"):
            return bool(int(self.current))
        if self._is_next("!"):
            return not self._factor()
        if self._is_next("[(]"):
            result = self._exp()
            if not self._is_next("[)]"):
                raise SyntaxError(
                    f"Expected ')' but got '{'<EOL>' if not self.line else self.line[0]}'"
                )
            return result
        raise SyntaxError(
            f"Expected operand or '-' or '(' but got '{'<EOL>' if not self.line else self.line[0]}'"
        )

    def _is_next(self, regexp: str) -> bool:
        m = re.match(r"\s*" + regexp + r"\s*", self.line)
        if m:
            self.current = m.group().strip()
            self.line = self.line[m.end() :]
            return True
        return False
