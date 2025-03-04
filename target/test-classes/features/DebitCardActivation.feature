Scenario: Customer activates debit card via net banking
  Given a customer with an inactive debit card
  When they activate the card via net banking
  Then the card should be activated successfully
