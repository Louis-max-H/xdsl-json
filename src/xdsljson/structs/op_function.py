from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import IntegerType
from xdsl.dialects.func import FuncOp
from xdsl.ir import Attribute, SSAValue
from xdsl.parser import IntegerAttr
from xdsl.rewriter import InsertPoint

from xdsljson.structs.base import BaseOp
from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import CodegenOp
from xdsljson.structs.op_var import VarOp


class ConstOp(CodegenOp):
    type: Literal["function"] = "function"
    name: str
    args: list[VarOp]
    body: list[BaseOp]

    def codegen(self, builder: Builder) -> SSAValue:

        # create arg_types
        arg_types: list[Attribute] = []
        for arg in self.args:
            if arg.varType is None:
                raise ValueError("Type is mendatory for function argument")
            arg_types.append(arg.varType.codegen())

        # Gen block
        block = codegenBlock(self.body, builder)
        yield_op = block.last_op
        assert yield_op is not None

        # Create function
        return_types = [result.type for result in yield_op.results]
        func = FuncOp(self.name, (arg_types, return_types))
        builder.insert(func)

        # Set args name
        for arg, var in zip(func.args, self.args):
            arg.name_hint = var.name

        # Set the builder insertion point inside the function.
        builder.insertion_point = InsertPoint.at_end(func.body.block)

        # Return 0
        return ConstantOp(IntegerAttr(0, IntegerType(1)))
