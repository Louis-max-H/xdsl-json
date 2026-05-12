from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.func import FuncOp, ReturnOp
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.base import BaseValue
from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import Codegen
from xdsljson.structs.op_var import VarOp, populate_block_heap, variablesHeap


class FunctionOp(Codegen):
    type: Literal["function"] = "function"
    name: str
    args: list[VarOp]
    body: list[BaseValue]

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        variablesHeap.clear()

        # create arg_types
        arg_types: list[Attribute] = []
        for arg in self.args:
            arg_types.append(arg.get_type())

        # create function
        func = FuncOp(self.name, (arg_types, []))
        builder.insert(func)

        # set args name
        for arg, var in zip(func.args, self.args):
            arg.name_hint = var.name

        # codegen into function block
        populate_block_heap(func)
        body_block, last_value = codegenBlock(self.body, func.body.block)

        # add ReturnOp
        if last_value is not None:
            body_block.add_op(ReturnOp(*last_value))
        else:
            body_block.add_op(ReturnOp())
        func.update_function_type()

        # Return
        return func.results
