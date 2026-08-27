#!/usr/bin/env python3
"""納品書整理ツールの起動スクリプト"""

import sys
from pathlib import Path

# 仮想環境の Python で実行することを推奨
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.main import main

if __name__ == "__main__":
    main()
