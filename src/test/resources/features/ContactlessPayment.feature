Scenario: Contactless payment below limit
  Given a customer with a debit card enabled for contactless payments
  When they make a transaction below the limit
  Then the transaction should be approved without a PIN
