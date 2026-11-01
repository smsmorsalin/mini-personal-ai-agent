import ast
import operator
from datetime import datetime


# -------------------------------
# TOOL 1: Calculator
# -------------------------------

def calculator(expression):

    # Allow only basic mathematical operations.
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def calculate(node):

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are allowed.")
            return node.value

        if isinstance(node, ast.BinOp):
            operation = operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(
                calculate(node.left),
                calculate(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            operation = operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(calculate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")

        return str(calculate(tree.body))

    except Exception as error:
        return f"Calculation error: {error}"


# -------------------------------
# TOOL 2: Current Date and Time
# -------------------------------

def get_datetime():

    now = datetime.now()

    return now.strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------
# TOOL 3: Read a Text File
# -------------------------------

def read_notes():

    try:
        with open("notes.txt", "r", encoding="utf-8") as file:
            return file.read(10000)

    except FileNotFoundError:
        return "notes.txt does not exist."