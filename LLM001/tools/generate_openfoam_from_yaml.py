#!/usr/bin/env python3
"""Generate OpenFOAM dictionaries from config/LLM001.yaml."""

from __future__ import annotations

import math
import os
import sys

from config_io import load_config


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE_DIR = os.path.join(ROOT_DIR, "case")


def _mkdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _write(path: str, text: str) -> None:
    _mkdir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _flow_m3_s(pump: dict) -> float:
    return float(pump.get("flow_L_min", 0.0)) / 60.0 / 1000.0


def _inlet_pumps(config: dict) -> list[dict]:
    return [p for p in config["pumps"] if p["role"] == "inlet"]


def _outlet_pumps(config: dict) -> list[dict]:
    return [p for p in config["pumps"] if p["role"] == "outlet"]


def _wall_patches(config: dict) -> list[str]:
    patches = config["patches"]
    return [
        patches["pump_wall"],
        patches["top_wall"],
        patches["bottom_wall"],
        patches["side_wall"],
        patches["front_wall"],
    ]


def _all_boundary_patches(config: dict) -> list[str]:
    return [p["patch"] for p in config["pumps"]] + _wall_patches(config)


def generate_u(config: dict) -> str:
    lines = [
        "FoamFile",
        "{",
        "    version     2.0;",
        "    format      ascii;",
        "    class       volVectorField;",
        "    object      U;",
        "}",
        "",
        "dimensions      [0 1 -1 0 0 0 0];",
        "",
        "internalField   uniform (0 0 0);",
        "",
        "boundaryField",
        "{",
    ]

    for pump in config["pumps"]:
        patch = pump["patch"]
        if pump["role"] == "inlet":
            flow_l_min = float(pump.get("flow_L_min", 0.0))
            lines += [
                f"    {patch}",
                "    {",
                "        type                flowRateInletVelocity;",
                f"        volumetricFlowRate  constant {_flow_m3_s(pump):.10g}; // {flow_l_min:g} L/min",
                "        value               uniform (0 0 0);",
                "    }",
                "",
            ]
        elif pump["role"] == "outlet":
            lines += [
                f"    {patch}",
                "    {",
                "        type        pressureInletOutletVelocity;",
                "        value       uniform (0 0 0);",
                "    }",
                "",
            ]
        else:
            raise ValueError(f"Unknown pump role: {pump['role']}")

    for patch in _wall_patches(config):
        lines += [f"    {patch}", "    {", "        type        noSlip;", "    }", ""]

    lines += ["}", ""]
    return "\n".join(lines)


def generate_p(config: dict) -> str:
    lines = [
        "FoamFile",
        "{",
        "    version     2.0;",
        "    format      ascii;",
        "    class       volScalarField;",
        "    object      p;",
        "}",
        "",
        "dimensions      [0 2 -2 0 0 0 0];",
        "",
        "internalField   uniform 0;",
        "",
        "boundaryField",
        "{",
    ]

    for pump in config["pumps"]:
        patch = pump["patch"]
        if pump["role"] == "outlet":
            lines += [
                f"    {patch}",
                "    {",
                "        type        fixedValue;",
                "        value       uniform 0;",
                "    }",
                "",
            ]
        else:
            lines += [f"    {patch}", "    {", "        type        zeroGradient;", "    }", ""]

    for patch in _wall_patches(config):
        lines += [f"    {patch}", "    {", "        type        zeroGradient;", "    }", ""]

    lines += ["}", ""]
    return "\n".join(lines)


def generate_k(config: dict) -> str:
    value = 0.0066
    lines = _scalar_header("k", "[0 2 -2 0 0 0 0]", value)
    for pump in config["pumps"]:
        patch = pump["patch"]
        if pump["role"] == "inlet":
            lines += _fixed_value_patch(patch, value)
        else:
            lines += _inlet_outlet_patch(patch, value)
    for patch in _wall_patches(config):
        lines += [f"    {patch}", "    {", "        type        kqRWallFunction;", f"        value       uniform {value};", "    }", ""]
    lines += ["}", ""]
    return "\n".join(lines)


def generate_omega(config: dict) -> str:
    value = 53
    lines = _scalar_header("omega", "[0 0 -1 0 0 0 0]", value)
    for pump in config["pumps"]:
        patch = pump["patch"]
        if pump["role"] == "inlet":
            lines += _fixed_value_patch(patch, value)
        else:
            lines += _inlet_outlet_patch(patch, value)
    for patch in _wall_patches(config):
        lines += [f"    {patch}", "    {", "        type        omegaWallFunction;", f"        value       uniform {value};", "    }", ""]
    lines += ["}", ""]
    return "\n".join(lines)


def generate_nut(config: dict) -> str:
    lines = _scalar_header("nut", "[0 2 -1 0 0 0 0]", 0)
    for pump in config["pumps"]:
        lines += _calculated_patch(pump["patch"], 0)
    for patch in _wall_patches(config):
        lines += [f"    {patch}", "    {", "        type        nutkWallFunction;", "        value       uniform 0;", "    }", ""]
    lines += ["}", ""]
    return "\n".join(lines)


def _scalar_header(name: str, dims: str, internal: float) -> list[str]:
    return [
        "FoamFile",
        "{",
        "    version     2.0;",
        "    format      ascii;",
        "    class       volScalarField;",
        f"    object      {name};",
        "}",
        "",
        f"dimensions      {dims};",
        "",
        f"internalField   uniform {internal};",
        "",
        "boundaryField",
        "{",
    ]


def _fixed_value_patch(patch: str, value: float) -> list[str]:
    return [f"    {patch}", "    {", "        type        fixedValue;", f"        value       uniform {value};", "    }", ""]


def _inlet_outlet_patch(patch: str, value: float) -> list[str]:
    return [
        f"    {patch}",
        "    {",
        "        type        inletOutlet;",
        f"        inletValue  uniform {value};",
        f"        value       uniform {value};",
        "    }",
        "",
    ]


def _calculated_patch(patch: str, value: float) -> list[str]:
    return [f"    {patch}", "    {", "        type        calculated;", f"        value       uniform {value};", "    }", ""]


def generate_transport_properties(config: dict) -> str:
    nu = float(config["fluid"]["nu_m2_s"])
    return f"""FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}}

transportModel  Newtonian;
nu              [0 2 -1 0 0 0 0] {nu:.10g};
"""


def generate_turbulence_properties(config: dict) -> str:
    model = config["simulation"]["turbulence_model"]
    return f"""FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      turbulenceProperties;
}}

simulationType  RAS;

RAS
{{
    RASModel        {model};
    turbulence      on;
    printCoeffs     on;
}}
"""


def generate_change_dictionary(config: dict) -> str:
    lines = [
        "FoamFile",
        "{",
        "    version     2.0;",
        "    format      ascii;",
        "    class       dictionary;",
        "    object      changeDictionaryDict;",
        "}",
        "",
        "boundary",
        "{",
    ]
    for pump in config["pumps"]:
        lines += [
            f"    {pump['patch']}",
            "    {",
            "        type         patch;",
            "        physicalType patch;",
            "    }",
            "",
        ]
    for patch in _wall_patches(config):
        lines += [
            f"    {patch}",
            "    {",
            "        type         wall;",
            "        physicalType wall;",
            "    }",
            "",
        ]
    lines += ["}", ""]
    return "\n".join(lines)


def generate_control_dict(config: dict) -> str:
    sim = config["simulation"]
    fields = "(p U k omega)"
    functions: list[str] = [
        "    residuals",
        "    {",
        "        type            residuals;",
        '        libs            ("libutilityFunctionObjects.so");',
        "        writeControl    timeStep;",
        "        writeInterval   1;",
        f"        fields          {fields};",
        "    }",
        "",
    ]
    for pump in config["pumps"]:
        name = f"{pump['id']}FlowRate"
        functions += [
            f"    {name}",
            "    {",
            "        type            surfaceFieldValue;",
            '        libs            ("libfieldFunctionObjects.so");',
            "        writeControl    timeStep;",
            "        writeInterval   10;",
            "        log             true;",
            "        writeFields     false;",
            "        regionType      patch;",
            f"        name            {pump['patch']};",
            "        operation       sum;",
            "        fields          (phi);",
            "    }",
            "",
        ]
    return f"""FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}}

application     {sim["solver"]};

startFrom       startTime;
startTime       0;

stopAt          endTime;
endTime         {sim["end_time"]};

deltaT          1;

writeControl    timeStep;
writeInterval   {sim["write_interval"]};

purgeWrite      0;

writeFormat     ascii;
writePrecision  6;
writeCompression off;

timeFormat      general;
timePrecision   6;

runTimeModifiable true;

functions
{{
{os.linesep.join(functions)}}}
"""


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    config = load_config(config_path)

    _write(os.path.join(CASE_DIR, "0", "U"), generate_u(config))
    _write(os.path.join(CASE_DIR, "0", "p"), generate_p(config))
    _write(os.path.join(CASE_DIR, "0", "k"), generate_k(config))
    _write(os.path.join(CASE_DIR, "0", "omega"), generate_omega(config))
    _write(os.path.join(CASE_DIR, "0", "nut"), generate_nut(config))
    _write(os.path.join(CASE_DIR, "constant", "transportProperties"), generate_transport_properties(config))
    _write(os.path.join(CASE_DIR, "constant", "turbulenceProperties"), generate_turbulence_properties(config))
    _write(os.path.join(CASE_DIR, "system", "controlDict"), generate_control_dict(config))
    _write(os.path.join(CASE_DIR, "system", "changeDictionaryDict"), generate_change_dictionary(config))

    print("Generated OpenFOAM dictionaries from YAML config.")


if __name__ == "__main__":
    main()
