"""
Pytest configuration for the project.

Adds the project root to sys.path so tests can import `app.*` modules
without installing the package.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
