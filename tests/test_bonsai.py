import unittest
import os
from typing import Dict
from pathlib import Path

from aind_behavior_services.utils import run_bonsai_process

import test_examples

class BonsaiTests(unittest.TestCase):

    def test_deserialization(self):

        tested_modules = [
            "aind_manipulator",
            "load_cells",
            "olfactometer",
            "water_valve",
        ]

        JSON_ROOT = Path("./local").resolve()

        workflow_props: Dict[str, str] = {}

        for module in tested_modules:
            workflow_props[f"{module}.RigPath"] = JSON_ROOT / f"{module}_rig.json"
            workflow_props[f"{module}.TaskLogicPath"] = JSON_ROOT / f"{module}_calibration_logic.json"
            workflow_props[f"{module}.SessionPath"] = JSON_ROOT / f"{module}_session.json"

        for _, file in workflow_props.items():
            if not os.path.exists(file):
                raise FileNotFoundError(f"File {file} does not exist")

        completed_proc = run_bonsai_process(
            workflow_file=Path("./src/unit_tests.bonsai").resolve(),
            is_editor_mode=False,
            layout=None,
            additional_properties=workflow_props,
        )

        self.assertEqual(completed_proc.stderr.decode(), "")
        self.assertEqual(completed_proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
