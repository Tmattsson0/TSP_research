from amplify.amplify import BinaryPoly, gen_symbols
from behave import *

import cost
import util

use_step_matcher("re")


@given("a valid route encoded in unary and binary and a distance array")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.route = [1, 2, 3, 4]
    context.ncity = len(context.route)

    context.binary_q = gen_symbols(BinaryPoly, context.ncity, context.ncity)
    context.unary_q = gen_symbols(BinaryPoly, context.ncity, context.ncity - 1)
    context._, context.distances = util.gen_test_tsp(context.ncity)


@when("the their cost functions are calculated")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    #unary
    context.encoded_q = util.qdict_to_qvalues(util.route_to_unary_dict(context.route), context.unary_q)
    context.unary_cost = cost.cost_func_unary(context.distances, context.encoded_q, context.ncity)

    #binary
    context.encoded_q = util.qdict_to_qvalues(util.route_to_binary_dict(context.route), context.binary_q)
    context.binary_cost = cost.cost_func_binary(context.distances, context.encoded_q, context.ncity)


@then("the two cost functions equal the same number")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.unary_cost == context.binary_cost


@when("their column constraints are calculated with explicit variables")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    #Binary
    q_with_val_binary = util.qdict_to_qvalues(util.route_to_binary_dict(context.route), context.binary_q)
    context.col_constraint_binary = cost.col_constraint_binary(q_with_val_binary, context.ncity)

    # context.col_constraint_binary = cost.col_constraint_binary(context.binary_q, context.ncity)

    #Unary
    q_with_val_unary = util.qdict_to_qvalues(util.route_to_unary_dict(context.route), context.unary_q)
    context.col_constraint_unary = cost.col_constraint_unary(q_with_val_unary, context.ncity)

    # context.col_constraint_unary = cost.col_constraint_unary(context.unary_q, context.ncity)


@then("the two column constraints should equal the same number")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print(context.col_constraint_binary)
    print(context.col_constraint_unary)

    assert (context.col_constraint_binary[i] == 1 for i in range(len(context.col_constraint_binary)))
    assert (context.col_constraint_unary[i] == 1 for i in range(len(context.col_constraint_unary)))
