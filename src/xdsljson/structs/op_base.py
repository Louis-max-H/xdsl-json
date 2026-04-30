from pydantic import Field
from xdsljson.structs.op_binary import BinaryOp
from xdsljson.structs.op_constant import ConstOp
from typing import Annotated, Union

BaseOp = Annotated[
    Union[BinaryOp, ConstOp],
    Field(discriminator='type')
]