# WARN: this is the test project the agent was is to be tested nothing related to the agent code
class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            elif token.isdigit():
                values.append(float(token))
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                operators.pop()  # Remove '('
            else:
                raise ValueError(f"Invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        return values[0]

    def _apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        result = self.operators[operator](left, right)
        values.append(result)
