from decimal import Decimal
from enum import Enum
from typing import Iterable, List

import pytest


class ExpenseDetailType(Enum):
    INJECTED = "INJECTED"
    COMPLEMENTARY = "COMPLEMENTARY"


class ExpenseDetail:
    def __init__(self, description: str, value: Decimal, type: ExpenseDetailType):
        self.description = description
        self.value = value
        self.type = type


class Expense:
    """Represents an expense"""

    def __init__(self, description: str) -> None:
        self.description = description
        self.value = Decimal(0)
        self.__details: List[ExpenseDetail] = []

    def update_value(self, value: Decimal) -> None:
        if value < 0:
            raise ValueError("Value must be greater than 0")

        self.value = value

    def add_detail(
        self, description: str, value: Decimal, type: ExpenseDetailType
    ) -> None:
        if value < 0:
            raise ValueError("Value must be greater than 0")

        detail = ExpenseDetail(description=description, value=value, type=type)
        self.__details.append(detail)

    @property
    def details(self) -> Iterable[ExpenseDetail]:
        return self.__details

    @property
    def total(self) -> Decimal:
        iterator = (
            detail.value
            for detail in self.__details
            if detail.type != ExpenseDetailType.INJECTED
        )
        return sum(iterator, self.value)


class TestExpenses:
    def test_create_expense(self):
        Expense(description="Fatura de luz")

    def test_update_value(self):
        expense = Expense(description="Fatura de luz")
        expense.update_value(Decimal(100.0))

    def test_iterate_expense_details(self):
        expense = Expense(description="Fatura de luz")
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.COMPLEMENTARY,
        )

        assert len(list(expense.details)) == 1

    def test_add_detail(self):
        expense = Expense(description="Fatura de luz")
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.COMPLEMENTARY,
        )

    def test_value_error_when_receive_negative_value(self):
        expense = Expense(description="Fatura de luz")
        with pytest.raises(ValueError):
            expense.update_value(Decimal(-100))

    def test_value_error_when_receive_negative_detail_value(self):
        expense = Expense(description="Fatura de luz")
        with pytest.raises(ValueError):
            expense.add_detail(
                description="Detalhe",
                value=Decimal(-100),
                type=ExpenseDetailType.COMPLEMENTARY,
            )

    def test_returns_total_value(self):
        expense = Expense(description="Fatura de luz")
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.COMPLEMENTARY,
        )
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.COMPLEMENTARY,
        )

        assert expense.total == Decimal(200)

    def test_total_should_not_sum_details_when_type_is_injected(self):
        expense = Expense(description="Fatura de luz")
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.INJECTED,
        )
        expense.add_detail(
            description="Detalhe",
            value=Decimal(100),
            type=ExpenseDetailType.COMPLEMENTARY,
        )

        assert expense.total == Decimal(100)
