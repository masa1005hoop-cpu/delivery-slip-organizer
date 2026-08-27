"""設定ファイルの読み込み"""

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config() -> dict:
    """config.yaml を読み込んで辞書として返す"""
    config_path = PROJECT_ROOT / "config.yaml"
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_folder_path(config: dict, key: str) -> Path:
    """設定からフォルダの絶対パスを取得する"""
    relative = config["folders"][key]
    return PROJECT_ROOT / relative
