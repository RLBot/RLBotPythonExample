from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"Ball",
"Car",
"ControlPoint",
"Curve",
"Field",
"Game",
"Goal",
"Input",
"Pad",
"obb",
"ray",
"sphere",
"tri",
"intersect"
]
class Ball():
    collision_radius = 93.1500015258789
    drag = -0.030500000342726707
    friction = 2.0
    mass = 30.0
    max_omega = 6.0
    max_speed = 4000.0
    moment_of_inertia = 99918.75
    radius = 91.25
    restitution = 0.6000000238418579

    @overload
    def __init__(self) -> None: 
        pass
    @overload
    def __init__(self, arg0: Ball) -> None: ...
    def hitbox(self) -> sphere: ...
    @overload
    def step(self, arg0: float) -> None: 
        pass
    @overload
    def step(self, arg0: float, arg1: Car) -> None: ...

    angular_velocity: vec3
    position: vec3
    time: float
    velocity: vec3
    pass
class Car():

    @overload
    def __init__(self) -> None: 
        pass
    @overload
    def __init__(self, arg0: Car) -> None: ...
    def extrapolate(self, arg0: float) -> None: ...
    def forward(self) -> vec3: ...
    def hitbox(self) -> obb: ...
    def left(self) -> vec3: ...
    def step(self, arg0: Input, arg1: float) -> None: ...
    def up(self) -> vec3: ...

    angular_velocity: vec3
    boost: int
    controls: Input
    demolished: bool
    dodge_rotation: mat2
    dodge_timer: float
    double_jumped: bool
    id: int
    jump_timer: float
    jumped: bool
    on_ground: bool
    orientation: mat3
    position: vec3
    quaternion: vec4
    rotator: vec3
    supersonic: bool
    team: int
    time: float
    velocity: vec3
    pass
class ControlPoint():

    @overload
    def __init__(self, arg0: vec3, arg1: vec3, arg2: vec3) -> None: 
        pass
    @overload
    def __init__(self) -> None: ...

    n: vec3
    p: vec3
    t: vec3
    pass
class Curve():

    @overload
    def __init__(self, arg0: List[ControlPoint]) -> None: 
        pass
    @overload
    def __init__(self, arg0: List[vec3]) -> None: ...
    def calculate_distances(self) -> None: ...
    def calculate_max_speeds(self, arg0: float, arg1: float) -> float: ...
    def calculate_tangents(self) -> None: ...
    def curvature_at(self, arg0: float) -> float: ...
    def find_nearest(self, arg0: vec3) -> float: ...
    def max_speed_at(self, arg0: float) -> float: ...
    def point_at(self, arg0: float) -> vec3: ...
    def pop_front(self) -> None: ...
    def tangent_at(self, arg0: float) -> vec3: ...
    def write_to_file(self, arg0: str) -> None: ...

    length: float
    points: List[vec3]
    pass
class Field():
    mode = 'Uninitialized'
    triangles = []
    walls = []

    @staticmethod
    @overload
    def collide(arg0: obb) -> ray: 
        pass
    @staticmethod
    @overload
    def collide(arg0: sphere) -> ray: ...
    @staticmethod
    def raycast_any(arg0: ray) -> ray: ...
    @staticmethod
    def snap(arg0: vec3) -> ray: ...

    pass
class Game():
    frametime = 0.008333333767950535
    gravity = -650.0
    map = 'map_not_set'

    def __init__(self, arg0: int) -> None: ...
    def read_game_information(self, arg0: object, arg1: object) -> None: ...
    @staticmethod
    def set_mode(arg0: str) -> None: ...

    ball: Ball
    cars: List[Car[8]]
    frame: int
    frame_delta: int
    kickoff_pause: bool
    match_ended: bool
    num_cars: int
    overtime: bool
    pads: List[Pad]
    round_active: bool
    team: int
    time: float
    time_delta: float
    time_remaining: float
    pass
class Goal():

    def __init__(self) -> None: ...

    direction: vec3
    location: vec3
    team: int
    pass
class Input():

    def __init__(self) -> None: ...

    boost: bool
    handbrake: bool
    jump: bool
    pitch: float
    roll: float
    steer: float
    throttle: float
    yaw: float
    pass
class Pad():

    def __init__(self) -> None: ...

    is_active: bool
    is_full_boost: bool
    position: vec3
    timer: float
    pass
class obb():

    def __init__(self) -> None: ...

    center: vec3
    half_width: vec3
    orientation: mat3
    pass
class ray():

    @overload
    def __init__(self) -> None: 
        pass
    @overload
    def __init__(self, arg0: vec3, arg1: vec3) -> None: ...

    direction: vec3
    start: vec3
    pass
class sphere():

    @overload
    def __init__(self, arg0: vec3, arg1: float) -> None: 
        pass
    @overload
    def __init__(self) -> None: ...

    center: vec3
    radius: float
    pass
class tri():

    def __getitem__(self, arg0: int) -> vec3: ...
    def __init__(self) -> None: ...
    def __setitem__(self, arg0: int, arg1: vec3) -> None: ...

    pass
@overload
def intersect(arg0: sphere, arg1: obb) -> bool:
    pass
@overload
def intersect(arg0: obb, arg1: sphere) -> bool:
    pass