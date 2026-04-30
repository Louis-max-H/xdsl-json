from xdsl.universe import Universe

from xdsljson.dialects import get_all_dialects
from xdsljson.transforms import get_all_passes

UNIVERSE = Universe(
    all_dialects=get_all_dialects(),
    all_passes=get_all_passes(),
)
