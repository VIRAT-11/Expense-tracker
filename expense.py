import json
from pathlib import Path


# -------------------- CLASS --------------------

class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = float(amount)
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category
        }


# -------------------- LOAD DATA --------------------

def load_expenses():
    expenses = []

    if Path("expenses.json").exists():
        with open("expenses.json", "r") as f:
            data = json.load(f)

        expenses = [
            Expense(
                item["name"],
                item["amount"],
                item["category"]
            )
            for item in data
        ]

    return expenses


# -------------------- SAVE DATA --------------------

def save_expenses(expenses):
    expense_dicts = [
        expense.to_dict()
        for expense in expenses
    ]

    with open("expenses.json", "w") as f:
        json.dump(
            expense_dicts,
            f,
            indent=4
        )