# Created by thomasmattsson at 23/05/2023
Feature: Calculate unary cost function
  # Enter feature description here

  Scenario: Unary cost function should equal the binary equivalent
    Given a route encoded in unary and binary and a distance array
    When the their cost functions are calculated
    Then the two cost functions equal the same number