#!/usr/bin/env python3
"""初回セットアップ: 依存関係の確認とフォルダ作成"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
IS_WINDOWS = os.name == "nt"
VENV_DIR = PROJECT_ROOT / ".venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")

# OSごとの入れ直し案内
HINTS = {
    "tesseract": (
        "Tesseract OCR が見つかりません → https://github.com/UB-Mannheim/tesseract/wiki からインストール"
        if IS_WINDOWS
        else "Tesseract OCR が見つかりません → brew install tesseract"
    ),
    "jpn": (
        "日本語OCRデータがありません → Tesseractを入れ直し、Japanese にチェックを入れる"
        if IS_WINDOWS
        else "日本語OCRデータがありません → brew install tesseract-lang"
    ),
    "poppler": (
        "poppler が見つかりません → https://github.com/oschwartz10612/poppler-windows/releases から入れ、"
        "Library\\bin をPATHに追加"
        if IS_WINDOWS
        else "poppler が見つかりません → brew install poppler"
    ),
}


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def check_tesseract_lang(lang: str = "jpn") -> bool:
    try:
        result = subprocess.run(
            ["tesseract", "--list-langs"],
            capture_output=True,
            text=True,
            check=False,
        )
        return lang in result.stdout
    except OSError:
        return False


def setup_venv() -> None:
    """Python仮想環境を作成して依存関係をインストールする"""
    if not VENV_PYTHON.exists():
        print("仮想環境を作成中...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print("Pythonパッケージをインストール中...")
    subprocess.run(
        [str(VENV_PYTHON), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=PROJECT_ROOT,
        check=True,
    )
    print("✓ Pythonパッケージ")


def run_command_hint() -> str:
    return ".venv\\Scripts\\python run.py" if IS_WINDOWS else ".venv/bin/python run.py"


def main() -> None:
    print("=== 納品書整理ツール セットアップ ===\n")

    errors = []

    # 実行中のPython自身を確認する（Windowsには python3 コマンドが無いため）
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    if sys.version_info < (3, 9):
        errors.append("Python 3.9 以上が必要です → https://www.python.org/downloads/ から入れ直す")

    if not check_command("tesseract"):
        errors.append(HINTS["tesseract"])
    else:
        print("✓ Tesseract OCR")

    if not check_tesseract_lang("jpn"):
        errors.append(HINTS["jpn"])
    else:
        print("✓ 日本語OCR (jpn)")

    if not check_command("pdftoppm"):
        errors.append(HINTS["poppler"])
    else:
        print("✓ poppler (PDF→画像変換)")

    for folder in ("受け取り", "納品書", "処理済み", "エラー"):
        path = PROJECT_ROOT / folder
        path.mkdir(exist_ok=True)
        print(f"✓ フォルダ: {folder}/")

    if errors:
        print("\n⚠ 以下をインストールしてください:")
        for err in errors:
            print(f"  - {err}")
        print("\n入れ直したら、パソコンを再起動してからもう一度 setup を実行してください。")
        sys.exit(1)

    setup_venv()

    print("\n--- 顧客フォルダ ---")
    print("  納品書/ に顧客名フォルダを作成してください。")
    print("  例: 納品書/○○株式会社/")

    print("\nセットアップOK！")
    print("次のコマンドで起動できます:")
    print(f"  {run_command_hint()}")


if __name__ == "__main__":
    main()
