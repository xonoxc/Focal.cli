class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 3,
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
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit():
                values.append(int(token))
            elif token in self.operators:
                operators.append(token)
            elif token == "(":  # Add support for parentheses
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":  # Evaluate until matching '('
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    result = self.operators[op](val1, val2)
                    values.append(result)
                operators.pop()  # Remove the '('
            i += 1

        while operators:
            op = operators.pop()
            val2 = values.pop()
            val1 = values.pop()
            result = self.operators[op](val1, val2)
            values.append(result)

        return values[0]

