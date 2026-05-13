from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.func import FuncOp, ReturnOp
from xdsl.ir import Attribute, OpResult, SSAValues
from xdsl.rewriter import InsertPoint

from xdsljson.structs.base import BaseValue
from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import Codegen
from xdsljson.structs.op_var import VarOp, variables_heap
from xdsljson.types_interface.any_value_type import AnyValueType


class FunctionOp(Codegen):
    op: Literal["function"] = "function"
    name: str
    args: list[tuple[str, AnyValueType]]
    body: list[BaseValue]

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        variables_heap.clear()

        # create arg_types
        arg_types: list[Attribute] = []
        for _name, type in self.args:
            arg_types.append(type.get_type())

        # create function
        func = FuncOp(self.name, (arg_types, []))
        builder.insert(func)

        # set args name
        for arg, (name, _type) in zip(func.args, self.args):
            arg.name_hint = name

        # Block Init
        """Instanciate one memref variable per SSA argument of the function"""
        init_builder = Builder(InsertPoint.at_end(func.body.block))
        for (name, type), arg in zip(self.args, func.args):
            VarOp(name=name, type=type).codegenSet(arg, init_builder)

        # Block codegen
        body_block, last_value = codegenBlock(self.body, func.body.block)

        # Block return
        if last_value is not None:
            body_block.add_op(ReturnOp(*last_value))
        else:
            body_block.add_op(ReturnOp())
        func.update_function_type()

        # Return
        return func.results
