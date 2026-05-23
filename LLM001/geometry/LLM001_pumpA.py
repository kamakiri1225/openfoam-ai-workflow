#!/usr/bin/env python3
"""Create the LLM001 gmsh model from config/LLM001.yaml."""

from __future__ import annotations

import argparse
import math
import os
import sys

import gmsh

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from config_io import load_config


def _pump_radius(pump: dict) -> float:
    return float(pump["outer_diameter_m"]) / 2.0


def _pump_top(pump: dict, tank_z: float) -> float:
    top = pump.get("top", "tankTop")
    if top == "tankTop":
        return tank_z
    return float(top)


def _patch_groups(config: dict) -> dict[str, list[int]]:
    patches = config["patches"]
    groups = {
        patches["pump_wall"]: [],
        patches["top_wall"]: [],
        patches["bottom_wall"]: [],
        patches["side_wall"]: [],
        patches["front_wall"]: [],
    }
    for pump in config["pumps"]:
        groups[pump["patch"]] = []
    return groups


def create_geometry_and_mesh(config_path: str | None = None):
    config = load_config(config_path)

    case_name = config["case"]["name"]
    tank_x, tank_y, tank_z = [float(v) for v in config["tank"]["size_m"]]
    mesh_cfg = config["mesh"]
    patches = config["patches"]
    pumps = config["pumps"]

    gmsh.initialize()
    gmsh.model.add(case_name)
    occ = gmsh.model.occ

    tank = occ.addBox(0, 0, 0, tank_x, tank_y, tank_z)
    pump_bodies: list[tuple[int, int]] = []

    for pump in pumps:
        cx, cy = [float(v) for v in pump["center_m"]]
        radius = _pump_radius(pump)
        bottom = float(pump["bottom_offset_m"])
        top = _pump_top(pump, tank_z)
        height = top - bottom
        if height <= 0:
            raise ValueError(f"{pump['id']}: top must be higher than bottom_offset_m")
        tag = occ.addCylinder(cx, cy, bottom, 0, 0, height, radius)
        pump_bodies.append((3, tag))

    fluid_out, _ = occ.cut(
        [(3, tank)],
        pump_bodies,
        removeObject=True,
        removeTool=True,
    )
    if not fluid_out:
        raise RuntimeError("Failed to create the fluid volume by CAD subtraction.")

    occ.synchronize()

    tol = 1e-4
    groups = _patch_groups(config)

    def matching_pump(fcx: float, fcy: float, fcz: float, horizontal: bool):
        for pump in pumps:
            cx, cy = [float(v) for v in pump["center_m"]]
            radius = _pump_radius(pump)
            bottom = float(pump["bottom_offset_m"])
            top = _pump_top(pump, tank_z)
            if math.hypot(fcx - cx, fcy - cy) > radius + tol:
                continue
            if horizontal and (abs(fcz - top) < tol or abs(fcz - bottom) < tol):
                return pump
            if not horizontal and bottom - tol <= fcz <= top + tol:
                return pump
        return None

    for _, surface_tag in gmsh.model.getEntities(2):
        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(2, surface_tag)
        fcx = (xmin + xmax) / 2.0
        fcy = (ymin + ymax) / 2.0
        fcz = (zmin + zmax) / 2.0

        is_flat_z = abs(zmax - zmin) < tol
        is_flat_x = abs(xmax - xmin) < tol
        is_flat_y = abs(ymax - ymin) < tol

        if is_flat_z and abs(fcz) < tol:
            groups[patches["bottom_wall"]].append(surface_tag)
        elif is_flat_z:
            pump = matching_pump(fcx, fcy, fcz, horizontal=True)
            if pump is not None:
                groups[pump["patch"]].append(surface_tag)
            elif abs(fcz - tank_z) < tol:
                groups[patches["top_wall"]].append(surface_tag)
            else:
                groups[patches["pump_wall"]].append(surface_tag)
        elif is_flat_x and (abs(fcx) < tol or abs(fcx - tank_x) < tol):
            groups[patches["side_wall"]].append(surface_tag)
        elif is_flat_y and (abs(fcy) < tol or abs(fcy - tank_y) < tol):
            groups[patches["front_wall"]].append(surface_tag)
        else:
            groups[patches["pump_wall"]].append(surface_tag)

    fluid_vols = [tag for _, tag in fluid_out]
    gmsh.model.addPhysicalGroup(3, fluid_vols, name="fluid")

    for patch_name, tags in groups.items():
        if tags:
            gmsh.model.addPhysicalGroup(2, tags, name=patch_name)
        else:
            print(f"WARNING: no surfaces found for patch {patch_name}")

    ms_global = float(mesh_cfg["global_size_m"])
    ms_pump = float(mesh_cfg["pump_size_m"])
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", ms_pump)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", ms_global)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 1)

    pump_surfs: list[int] = []
    pump_surfs.extend(groups[patches["pump_wall"]])
    for pump in pumps:
        pump_surfs.extend(groups[pump["patch"]])

    if pump_surfs:
        fid_dist = gmsh.model.mesh.field.add("Distance")
        gmsh.model.mesh.field.setNumbers(fid_dist, "SurfacesList", pump_surfs)

        fid_thr = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(fid_thr, "InField", fid_dist)
        gmsh.model.mesh.field.setNumber(fid_thr, "SizeMin", ms_pump)
        gmsh.model.mesh.field.setNumber(fid_thr, "SizeMax", ms_global)
        gmsh.model.mesh.field.setNumber(fid_thr, "DistMin", float(mesh_cfg["refine_dist_min_m"]))
        gmsh.model.mesh.field.setNumber(fid_thr, "DistMax", float(mesh_cfg["refine_dist_max_m"]))
        gmsh.model.mesh.field.setAsBackgroundMesh(fid_thr)

    gmsh.option.setNumber("Mesh.Algorithm3D", 1)
    gmsh.option.setNumber("Mesh.Optimize", 1)
    gmsh.option.setNumber("General.Verbosity", 5)

    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.optimize("Netgen")

    out_path = os.path.normpath(os.path.join(os.path.dirname(__file__), mesh_cfg["output"]))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    gmsh.option.setNumber("Mesh.MshFileVersion", float(mesh_cfg["msh_version"]))
    gmsh.write(out_path)

    print("\n" + "=" * 62)
    print(f"  {case_name}: gmsh model and mesh generated")
    print("=" * 62)
    print(f"  config : {config_path or os.path.join(ROOT_DIR, 'config', 'LLM001.yaml')}")
    print(f"  output : {out_path}")
    print(f"  tank   : {tank_x*1000:.0f} x {tank_y*1000:.0f} x {tank_z*1000:.0f} mm")
    for pump in pumps:
        cx, cy = [float(v) for v in pump["center_m"]]
        print(
            f"  {pump['id']:6s}: {pump['role']:6s}, patch={pump['patch']}, "
            f"center=({cx*1000:.0f},{cy*1000:.0f}) mm, "
            f"OD={float(pump['outer_diameter_m'])*1000:.0f} mm, "
            f"flow={float(pump['flow_L_min']):.1f} L/min"
        )
    print("  patches:")
    for name, tags in groups.items():
        print(f"    {name:15s}: {len(tags)} surfaces")
    print("=" * 62)

    return groups, fluid_vols


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-gui", action="store_true", help="open gmsh GUI after mesh generation")
    parser.add_argument("--config", default=None, help="YAML configuration file")
    args = parser.parse_args()

    create_geometry_and_mesh(args.config)
    if args.gui:
        gmsh.fltk.run()
    gmsh.finalize()


if __name__ == "__main__":
    main()
