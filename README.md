# My expenses service

Serviço de gestão de despesas

## Requisitos

- Capacidade de adicionar uma **`Expense`** (Despesa)
- Tem uma valor total agregado
- Possui descrição (O que também é o título)
  - Pode ser descrita em varios detalhes
    - Esses detalhes também possuem valores agregados, os quais somam ao valor agregado da despesa
  - Seriam então `SubExpenses`, ou seja, funcionariam em nodes?
    - talvez, pois:
      - Caso sim, é como uma despesa dentro da outra, com a diferença de que essa `SubExpense` só descreve as partes da atual
      - Caso não, isso gera uma espécie de recursão onde uma Expense tem uma Expense que também, em tese poderia ter uma Expense.

## Requisitos Não funcionais

- Expenses não podem ter valores negativos, pois isso seria considerado `receita`
- Um detalhamento pode ter ser dos seguintes tipos:
  - Detalhamento Complementar
    - O valor total de uma Expense é representado pelo seu valor agregado, somado aos seus detalhamentos
      - Exemplo: Se eu tenho um Expense de R$ 25,00 e um detalhamento de R$ 5,00. No total eu tenho R$ 30,00 em despesas
  - Detalhamento Imbutido
    - O valor do detalhamento inbutido já faz parte do valor inserido no `Expense`.
      - **O valor embutido na Expense não pode ser menor que a soma de os detalhamentos do tipo Embutido**

```python
class ExpenseDetailType(Enum):
    INJECTED = "INJECTED"
    COMPLEMENTARY = "COMPLEMENTARY"

class ExpenseDetail:
    description: str
    type: ExpenseDetailType
    value: Decimal


class Expense:
    description: str
    value: Decimal
    
    details: List[ExpenseDetails]
```
