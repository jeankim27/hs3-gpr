"""The lunar scene: what the radar looks at (flowchart steps 9–11).

Q2 uses `flat_scene` (flat surface, regolith over basalt, one void).
Q3 replaces the flat surface with LOLA elevation data and adds realistic layering.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class Layer:
    """A material below `top_depth` (m below the local surface) until the next layer."""
    name: str
    top_depth: float
    eps: float
    tan_delta: float


@dataclass
class Void:
    """A lava tube cross-section: empty space between roof and floor, centered at x_center."""
    x_center: float          # along-track position of the tube axis, m
    width: float             # m
    roof_depth: float        # m below the surface
    height: float            # m (floor = roof_depth + height)


@dataclass
class PointTarget:
    """A small isolated reflector, used for verification (e.g. SAR resolution test V-03)."""
    x: float                 # along-track position, m
    depth: float             # m below the surface (0 = on the surface)
    amplitude: float = 1.0   # amplitude reflection, relative


@dataclass
class Scene:
    layers: list[Layer]
    voids: list[Void] = field(default_factory=list)
    points: list[PointTarget] = field(default_factory=list)
    surface_height: Callable[[np.ndarray], np.ndarray] = lambda x: np.zeros_like(np.asarray(x, float))
    include_surface: bool = True      # False → only buried reflectors (handy for tests)

    def layer_at(self, depth: float) -> Layer:
        """Material at `depth` below the surface."""
        current = self.layers[0]
        for layer in self.layers:
            if depth >= layer.top_depth:
                current = layer
        return current


def flat_scene(p, void_x=0.0, void_width=None, roof_depth=None, void_height=None) -> Scene:
    """Flat surface, regolith over basalt, one lava tube. Values default to the register:
    regolith_thickness, eps_*, tan_delta_*, roof_depth_max, tube_width_min, tube_height_min."""
    regolith = Layer("regolith", 0.0, p["eps_regolith"], p["tan_delta_regolith"])
    basalt = Layer("basalt", p["regolith_thickness"], p["eps_basalt"], p["tan_delta_basalt"])
    void = Void(
        x_center=void_x,
        width=void_width or p["tube_width_min"] or 300.0,
        roof_depth=roof_depth or p["roof_depth_max"],
        height=void_height or p["tube_height_min"] or 50.0,
    )
    return Scene(layers=[regolith, basalt], voids=[void])


def point_target_scene(x=0.0, depth=0.0) -> Scene:
    """A single point reflector in vacuum, for verification tests."""
    return Scene(layers=[Layer("vacuum", 0.0, 1.0, 0.0)], points=[PointTarget(x, depth)], include_surface=False)
