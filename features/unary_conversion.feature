# Created by thomasmattsson at 23/05/2023
Feature: Unary conversion
  # Enter feature description here

  Scenario: Unary cost function should equal the binary equivalent
    Given a valid route encoded in unary and binary and a distance array
    When the their cost functions are calculated
    Then the two cost functions equal the same number

#  Scenario: Unary and binary row constraint should be numerically equivalent
#    Given a route encoded in unary and binary and a distance array
#    When the their row constraints are calculated with explicit variables
#    Then the two row constraints should equal the same number

  Scenario: Unary and binary column constraint should be numerically equivalent
    Given a valid route encoded in unary and binary and a distance array
    When their column constraints are calculated with explicit variables
    Then the two column constraints should equal the same number

  Scenario: Unary cost function should equal the binary equivalent for all permutations of valid route
    Given a list of different cities and a tsp
    When the cost function is calculated for all route-permutations in unary and binary
    Then all cost binary cost functions are equal to their unary counterpart