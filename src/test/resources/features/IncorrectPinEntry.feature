Scenario: Customer enters incorrect PIN three times
  Given a customer with an active debit card
  When they enter an incorrect PIN three times
  Then the card should be temporarily blocked
