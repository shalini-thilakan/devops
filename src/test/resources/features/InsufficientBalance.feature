Scenario: Customer tries to make an online payment with insufficient balance
  Given a customer with a debit card and insufficient balance
  When they attempt an online transaction
  Then the transaction should be declined

Scenario: Customer tries to make an online payment with sufficient balance
  Given a customer with a debit card and sufficient balance
  When they attempt an online transaction
  Then the transaction should be accepted
