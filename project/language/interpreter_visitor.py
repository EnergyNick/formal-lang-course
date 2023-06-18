from collections.abc import Iterable

import networkx as nx
from pyformlang.finite_automaton import *

import project.automath as fau
import project.utilities as gu
from project.language.GraphLangParser import GraphLangParser
from project.language.GraphLangVisitor import GraphLangVisitor
from project.language.exceptions import *
from project.language.interpreter_types import *


class LangVisitor(GraphLangVisitor):
    def __init__(self):
        self.context = MemoryContext()

    def clone(self):
        res = LangVisitor()
        res.context = self.context.clone()
        return res

    def clone_with_bind(self, *newValues: tuple[str, object]):
        res = self.clone()
        for key, val in newValues:
            res.context[key] = val
        return res

    def _get_value_from_ctx(self, expr):
        if expr is None:
            return None
        result = expr.accept(self)
        if isinstance(result, ArgName):
            if result.value not in self.context:
                raise IncorrectVariableException(result.value)
            return self.context[result.value]
        else:
            return result

    def _get_parts_of_double_expr(self, ctx):
        val1 = self._get_value_from_ctx(ctx.expr(0))
        val2 = self._get_value_from_ctx(ctx.expr(1))
        return val1, val2

    # Arguments

    def visitNameArg(self, ctx: GraphLangParser.NameArgContext):
        return ArgName(ctx.getText())

    def visitEmptyArg(self, ctx: GraphLangParser.EmptyArgContext):
        return EmptyArg

    # Values

    def visitIntegerVal(self, ctx: GraphLangParser.IntegerValContext):
        return int(ctx.INT().getText())

    def visitStringVal(self, ctx: GraphLangParser.StringValContext):
        return ctx.getText()[1:-1]

    def visitBooleanVal(self, ctx: GraphLangParser.BooleanValContext):
        return bool(ctx.BOOL().getText())

    def visitSetBodyElements(self, ctx: GraphLangParser.SetBodyElementsContext):
        values = ctx.expr()
        result = set()
        for item in values:
            result.add(item.accept(self))
        return result

    def visitSetBodyRange(self, ctx: GraphLangParser.SetBodyRangeContext):
        start = int(ctx.INT(0).getText())
        end = int(ctx.INT(1).getText())
        return set(range(start, end + 1))

    def visitSetVal(self, ctx: GraphLangParser.SetValContext):
        return ctx.setBody().accept(self)

    # Structures

    def visitBind(self, ctx: GraphLangParser.BindContext):
        name = ctx.arg().accept(self).value
        self.context[name] = self._get_value_from_ctx(ctx.expr())

    def visitPrint(self, ctx: GraphLangParser.PrintContext):
        result = self._get_value_from_ctx(ctx.expr())

        if isinstance(result, EpsilonNFA):
            result = fau.convert_nfa_to_str(result)

        print(result)

    def visitLambdaBody(self, ctx: GraphLangParser.LambdaBodyContext):
        name = ctx.arg().accept(self).value
        body = ctx.expr()

        def invoker(value):
            vis = self.clone_with_bind((name, value))
            return body.accept(vis)

        return invoker

    def visitLambdaBrackets(self, ctx: GraphLangParser.LambdaBracketsContext):
        return ctx.lambda_().accept(self)

    # Operations Block:

    # - Common Operations

    def visitBracketExp(self, ctx: GraphLangParser.BracketExpContext):
        return ctx.expr().accept(self)

    def visitLoadExp(self, ctx: GraphLangParser.LoadExpContext):
        nameCtx = ctx.expr()
        nameStr = nameCtx.accept(self)
        return fau.build_nfa_from_graph(gu.get_graph_from_dataset(nameStr))

    def visitMapExp(self, ctx: GraphLangParser.MapExpContext):
        expr_res = self._get_value_from_ctx(ctx.expr())

        if not isinstance(expr_res, Iterable):
            raise InvalidOperationStateException(expr_res, "Converter")

        converter: callable = ctx.lambda_().accept(self)
        result = set()
        for val in expr_res:
            res = converter(val)
            result.add(res)
        return result

    def visitFilterExp(self, ctx: GraphLangParser.FilterExpContext):
        expr_res = self._get_value_from_ctx(ctx.expr())

        if not isinstance(expr_res, Iterable):
            raise InvalidOperationStateException(expr_res, "Filter")

        predicate: callable = ctx.lambda_().accept(self)
        result = set()
        for val in expr_res:
            if predicate(val):
                result.add(val)
        return result

    # - Operations with Starts and Finals

    def visitGetStartExp(self, ctx: GraphLangParser.GetStartExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get starts")

        return set(value.start_states)

    def visitGetFinalExp(self, ctx: GraphLangParser.GetFinalExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get finals")

        return set(value.final_states)

    def visitAddStartExp(self, ctx: GraphLangParser.AddStartExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        operationType = "add starts"
        if not isinstance(val1, EpsilonNFA):
            raise InvalidOperationStateException(val1, operationType)
        if not isinstance(val2, set):
            raise InvalidOperationStateException(val2, operationType)

        val1 = val1.copy()
        val1.start_states.update(val2)
        return val1

    def visitAddFinalExp(self, ctx: GraphLangParser.AddFinalExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        operationType = "add finals"
        if not isinstance(val1, EpsilonNFA):
            raise InvalidOperationStateException(val1, operationType)
        if not isinstance(val2, set):
            raise InvalidOperationStateException(val2, operationType)

        val1 = val1.copy()
        val1.final_states.update(val2)
        return val1

    def visitSetStartExp(self, ctx: GraphLangParser.SetStartExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        operationType = "set starts"
        if not isinstance(val1, EpsilonNFA):
            raise InvalidOperationStateException(val1, operationType)
        if not isinstance(val2, set):
            raise InvalidOperationStateException(val2, operationType)

        val1 = val1.copy()
        val1.start_states.clear()
        val1.start_states.update(val2)
        return val1

    def visitSetFinalExp(self, ctx: GraphLangParser.SetFinalExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        operationType = "set finals"
        if not isinstance(val1, EpsilonNFA):
            raise InvalidOperationStateException(val1, operationType)
        if not isinstance(val2, set):
            raise InvalidOperationStateException(val2, operationType)

        val1 = val1.copy()
        val1.final_states.clear()
        val1.final_states.update(val2)
        return val1

    # - Operations with properties

    def visitEdgeExp(self, ctx: GraphLangParser.EdgeExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get edge")

        return set(value)

    def visitVertsExp(self, ctx: GraphLangParser.VertsExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get edge")

        return set(value.states)

    def visitLabelExp(self, ctx: GraphLangParser.LabelExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get edge")

        return set(value.symbols)

    def visitReachExp(self, ctx: GraphLangParser.ReachExpContext):
        value = self._get_value_from_ctx(ctx.expr())

        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "get edge")

        temp: nx.MultiDiGraph = nx.transitive_closure(nx.DiGraph(value.to_networkx()))
        return temp.edges

    # - Group and utils operations

    def visitConcatExp(self, ctx: GraphLangParser.ConcatExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, EpsilonNFA) and isinstance(val2, EpsilonNFA):
            return val1.concatenate(val2)
        elif isinstance(val1, str) and isinstance(val2, str):
            return val1 + val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Concat")

    def visitContainExp(self, ctx: GraphLangParser.ContainExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, EpsilonNFA) and isinstance(val2, set):
            return val1.accepts(val2)
        elif isinstance(val1, set) and isinstance(val2, set):
            return val2 in val2
        elif isinstance(val1, str) and isinstance(val2, str):
            return val2 in val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Contains")

    def visitUnionExp(self, ctx: GraphLangParser.UnionExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, EpsilonNFA) and isinstance(val2, EpsilonNFA):
            return val1.union(val2)
        elif isinstance(val1, set) and isinstance(val2, set):
            return val1 | val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Union")

    def visitInterExp(self, ctx: GraphLangParser.InterExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, EpsilonNFA) and isinstance(val2, EpsilonNFA):
            return val1.get_intersection(val2)
        elif isinstance(val1, set) and isinstance(val2, set):
            return val1 & val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Intersect")

    def visitStarExp(self, ctx: GraphLangParser.StarExpContext):
        value = self._get_value_from_ctx(ctx.expr())
        if not isinstance(value, EpsilonNFA):
            raise InvalidOperationStateException(value, "Star")

        return value.kleene_star()

    def visitSumExp(self, ctx: GraphLangParser.SumExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, int) and isinstance(val2, int):
            return val1 + val2
        elif isinstance(val1, str) and isinstance(val2, str):
            return val1 + val2
        elif isinstance(val1, bool) and isinstance(val2, bool):
            return val1 + val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Sum")

    def visitMultExp(self, ctx: GraphLangParser.MultExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, int) and isinstance(val2, int):
            return val1 * val2
        elif isinstance(val1, bool) and isinstance(val2, bool):
            return val1 * val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Multiply")

    def visitSubExp(self, ctx: GraphLangParser.SubExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, int) and isinstance(val2, int):
            return val1 - val2
        elif isinstance(val1, set) and isinstance(val2, set):
            return val1 - val2
        elif isinstance(val1, bool) and isinstance(val2, bool):
            return val1 - val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Subtract")

    def visitModExp(self, ctx: GraphLangParser.ModExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, int) and isinstance(val2, int):
            return val1 % val2
        elif isinstance(val1, bool) and isinstance(val2, bool):
            return val1 % val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Module")

    def visitEqualExp(self, ctx: GraphLangParser.EqualExpContext):
        val1, val2 = self._get_parts_of_double_expr(ctx)

        if isinstance(val1, int) and isinstance(val2, int):
            return val1 == val2
        elif isinstance(val1, bool) and isinstance(val2, bool):
            return val1 == val2
        elif isinstance(val1, str) and isinstance(val2, str):
            return val1 == val2
        elif isinstance(val1, set) and isinstance(val2, set):
            return val1 == val2
        elif isinstance(val1, EpsilonNFA) and isinstance(val2, EpsilonNFA):
            return val1 == val2
        else:
            raise InvalidGroupOperationException(val1, val2, "Equals")
