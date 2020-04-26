from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"mat2",
"mat3",
"vec2",
"vec3",
"vec4",
"angle_between",
"axis_to_rotation",
"clip",
"cross",
"dot",
"euler_to_rotation",
"inv",
"look_at",
"norm",
"normalize",
"rotation",
"rotation_to_axis",
"rotation_to_euler",
"sgn",
"transpose",
"xy"
]
class mat2():

    def __getitem__(self, arg0: Tuple[int, int]) -> float: ...
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float) -> None: ...
    def __setitem__(self, arg0: Tuple[int, int], arg1: float) -> None: ...
    def __str__(self) -> str: ...

    pass
class mat3():

    def __getitem__(self, arg0: Tuple[int, int]) -> float: ...
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float, arg8: float) -> None: ...
    def __setitem__(self, arg0: Tuple[int, int], arg1: float) -> None: ...
    def __str__(self) -> str: ...

    pass
class vec2():

    def __add__(self, arg0: vec2) -> vec2: ...
    def __getitem__(self, arg0: int) -> float: ...
    def __iadd__(self, arg0: vec2) -> vec2: ...
    def __imul__(self, arg0: float) -> vec2: ...
    @overload
    def __init__(self, arg0: vec2) -> None: 
        pass
    @overload
    def __init__(self, arg0: vec3) -> None: ...
    @overload
    def __init__(self, arg0: float, arg1: float) -> None: ...
    def __isub__(self, arg0: vec2) -> vec2: ...
    def __itruediv__(self, arg0: float) -> vec2: ...
    def __mul__(self, arg0: float) -> vec2: ...
    def __rmul__(self, arg0: float) -> vec2: ...
    def __setitem__(self, arg0: int, arg1: float) -> None: ...
    def __str__(self) -> str: ...
    def __sub__(self, arg0: vec2) -> vec2: ...
    def __truediv__(self, arg0: float) -> vec2: ...

    pass
class vec3():

    def __add__(self, arg0: vec3) -> vec3: ...
    def __getitem__(self, arg0: int) -> float: ...
    def __iadd__(self, arg0: vec3) -> vec3: ...
    def __imul__(self, arg0: float) -> vec3: ...
    @overload
    def __init__(self, arg0: vec3) -> None: 
        pass
    @overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None: ...
    @overload
    def __init__(self, arg0: vec2) -> None: ...
    def __isub__(self, arg0: vec3) -> vec3: ...
    def __itruediv__(self, arg0: float) -> vec3: ...
    def __mul__(self, arg0: float) -> vec3: ...
    def __rmul__(self, arg0: float) -> vec3: ...
    def __setitem__(self, arg0: int, arg1: float) -> None: ...
    def __str__(self) -> str: ...
    def __sub__(self, arg0: vec3) -> vec3: ...
    def __truediv__(self, arg0: float) -> vec3: ...

    pass
class vec4():

    def __add__(self, arg0: vec4) -> vec4: ...
    def __getitem__(self, arg0: int) -> float: ...
    def __iadd__(self, arg0: vec4) -> vec4: ...
    def __imul__(self, arg0: float) -> vec4: ...
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float) -> None: ...
    def __isub__(self, arg0: vec4) -> vec4: ...
    def __itruediv__(self, arg0: float) -> vec4: ...
    def __mul__(self, arg0: float) -> vec4: ...
    def __rmul__(self, arg0: float) -> vec4: ...
    def __setitem__(self, arg0: int, arg1: float) -> None: ...
    def __str__(self) -> str: ...
    def __sub__(self, arg0: vec4) -> vec4: ...
    def __truediv__(self, arg0: float) -> vec4: ...

    pass
@overload
def angle_between(arg0: mat3, arg1: mat3) -> float:
    pass
@overload
def angle_between(arg0: vec3, arg1: vec3) -> float:
    pass
@overload
def angle_between(arg0: vec2, arg1: vec2) -> float:
    pass
def axis_to_rotation(arg0: vec3) -> mat3:
    pass
@overload
def clip(arg0: int, arg1: int, arg2: int) -> int:
    pass
@overload
def clip(arg0: float, arg1: float, arg2: float) -> float:
    pass
@overload
def cross(arg0: vec3, arg1: vec3) -> vec3:
    pass
@overload
def cross(arg0: vec3) -> vec3:
    pass
@overload
def cross(arg0: vec2) -> vec2:
    pass
@overload
def dot(arg0: vec2, arg1: mat2) -> vec2:
    pass
@overload
def dot(arg0: vec4, arg1: vec4) -> float:
    pass
@overload
def dot(arg0: vec2, arg1: vec2) -> float:
    pass
@overload
def dot(arg0: vec3, arg1: mat3) -> vec3:
    pass
@overload
def dot(arg0: mat3, arg1: mat3) -> mat3:
    pass
@overload
def dot(arg0: vec3, arg1: vec3) -> float:
    pass
@overload
def dot(arg0: mat2, arg1: mat2) -> mat2:
    pass
@overload
def dot(arg0: mat2, arg1: vec2) -> vec2:
    pass
@overload
def dot(arg0: mat3, arg1: vec3) -> vec3:
    pass
def euler_to_rotation(arg0: vec3) -> mat3:
    pass
@overload
def inv(arg0: mat3) -> mat3:
    pass
@overload
def inv(arg0: mat2) -> mat2:
    pass
def look_at(arg0: vec3, arg1: vec3) -> mat3:
    pass
@overload
def norm(arg0: vec2) -> float:
    pass
@overload
def norm(arg0: vec3) -> float:
    pass
@overload
def normalize(arg0: vec3) -> vec3:
    pass
@overload
def normalize(arg0: vec2) -> vec2:
    pass
def rotation(arg0: float) -> mat2:
    pass
def rotation_to_axis(arg0: mat3) -> vec3:
    pass
def rotation_to_euler(arg0: mat3) -> vec3:
    pass
def sgn(arg0: float) -> float:
    pass
@overload
def transpose(arg0: mat2) -> mat2:
    pass
@overload
def transpose(arg0: mat3) -> mat3:
    pass
def xy(arg0: vec3) -> vec3:
    pass