#!/usr/bin/env python3
"""初回セットアップ: 依存関係の確認とフォルダ作成"""

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"


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
        subprocess.run([sys.executable, "-m", "venv", str(PROJECT_ROOT / ".venv")], check=True)
    print("Pythonパッケージをインストール中...")
    subprocess.run(
        [str(VENV_PYTHON), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=PROJECT_ROOT,
        check=True,
    )
    print("✓ Pythonパッケージ")


def main() -> None:
    print("=== 納品書整理ツール セットアップ ===\n")

    errors = []

    if not check_command("python3"):
        errors.append("Python3 が見つかりません")
    else:
        print("✓ Python3")

    if not check_command("tesseract"):
        errors.append("Tesseract OCR が見つかりません → brew install tesseract")
    else:
        print("✓ Tesseract OCR")

    if not check_tesseract_lang("jpn"):
        errors.append("日本語OCRデータがありません → brew install tesseract-lang")
    else:
        print("✓ 日本語OCR (jpn)")

    if not check_command("pdftoppm"):
        errors.append("poppler が見つかりません → brew install poppler")
    else:
        print("✓ poppler (PDF→画像変換)")

    for folder in ("受け取り", "納品書", "処理済み", "エラー"):
        path = PROJECT_ROOT / folder
        path.mkdir(exist_ok=True)
        print(f"✓ フォルダ: {folder}/")

    print("\n--- 顧客フォルダ ---")
    print("  納品書/ に顧客名フォルダを作成してください。")
    print("  例: 納品書/○○株式会社/")

    if errors:
        print("\n⚠ 以下をインストールしてください:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    setup_venv()

    print("\nセットアップOK！")
    print("次のコマンドで起動できます:")
    print("  .venv/bin/python run.py")


if __name__ == "__main__":
    main()
