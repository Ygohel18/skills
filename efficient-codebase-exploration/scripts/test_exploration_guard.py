#!/usr/bin/env python3
"""
Exploration & Package Manager Guard Tests

Verifies that the exploration logic strictly blocks vendor/dependency directories,
flags prohibited package manager commands, and correctly groups candidate files.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_explore import BANNED_DIRS, scan_directory

class TestExplorationGuard(unittest.TestCase):

    def test_banned_directories_present(self):
        """Ensure all critical package directories are included in the banlist."""
        required_bans = {"node_modules", "vendor", ".git", ".venv", "dist", "build"}
        for b in required_bans:
            self.assertIn(b, BANNED_DIRS, f"Missing banned directory: {b}")

    def test_prohibited_package_commands(self):
        """Simulate command validation for package manager operations."""
        prohibited_commands = [
            "npm install",
            "npm i express",
            "npm update",
            "yarn add lodash",
            "pnpm install",
            "composer install",
            "composer update",
            "pip install requests",
            "poetry install"
        ]

        # Guard heuristic
        def is_command_allowed(cmd: str, user_explicitly_requested: bool = False) -> bool:
            if user_explicitly_requested:
                return True
            banned_verbs = [
                "npm install", "npm i ", "npm update", "yarn add", "yarn install",
                "pnpm install", "pnpm add", "composer install", "composer update",
                "composer require", "pip install", "poetry install"
            ]
            return not any(verb in cmd for verb in banned_verbs)

        for cmd in prohibited_commands:
            self.assertFalse(
                is_command_allowed(cmd, user_explicitly_requested=False),
                f"Command should be blocked: {cmd}"
            )

        # Allowed when user explicitly asks
        for cmd in prohibited_commands:
            self.assertTrue(
                is_command_allowed(cmd, user_explicitly_requested=True),
                f"Command should be allowed when explicitly instructed: {cmd}"
            )

    def test_fast_explore_scanner(self):
        """Ensure fast_explore accurately scans current repository without crashing."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        res = scan_directory(base_dir, max_depth=2)
        self.assertGreater(res["total_source_files"], 0)
        self.assertIn("layers", res)

if __name__ == "__main__":
    unittest.main()
