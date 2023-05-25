from amplify.amplify import BinaryPoly, gen_symbols
from behave import *

import cost
import util

use_step_matcher("re")

route = [1, 2, 3, 4]
ncity = len(route)
binary_q = None
unary_q = None
distances = None
unary_cost = None
binary_cost = None


@given("a route encoded in unary and binary and a distance array")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    binary_q = gen_symbols(BinaryPoly, ncity, ncity)
    unary_q = gen_symbols(BinaryPoly, ncity, ncity - 1)
    _, distances = util.gen_test_tsp(ncity)


@when("the their cost functions are calculated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    #unary
    encoded_q = util.qdict_to_qvalues(util.route_to_unary_dict(route), unary_q)
    unary_cost = cost.cost_func_unary(distances, encoded_q, ncity)

    #binary
    encoded_q = util.qdict_to_qvalues(util.route_to_binary_dict(route), binary_q)
    binary_cost = cost.cost_func_binary(distances, encoded_q, ncity)


@then("the two cost functions equal the same number")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert unary_cost == binary_cost

