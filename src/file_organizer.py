"""ファイルのリネームとフォルダへの移動"""

import shutil
from datetime import datetime
from pathlib import Path


def list_customer_folders(customers_root: Path) -> list[Path]:
    """納品書フォルダ内の顧客フォルダ一覧を返す"""
    if not customers_root.exists():
        return []
    return sorted([p for p in customers_root.iterdir() if p.is_dir()])


def find_matching_customer_folder(customer_name: str, customers_root: Path) -> Path | None:
    """OCRで読み取った顧客名と一致する既存フォルダを探す"""
    if not customer_name:
        return None

    normalized = customer_name.strip()
    folders = list_customer_folders(customers_root)

    # 完全一致
    for folder in folders:
        if folder.name == normalized:
            return folder

    # 部分一致（OCRの誤読を許容）
    for folder in folders:
        if folder.name in normalized or normalized in folder.name:
            return folder

    return None


def build_destination_folder(customer_folder: Path, date_value: datetime) -> Path:
    """顧客フォルダ / 年 / 月 のパスを作る"""
    return customer_folder / str(date_value.year) / f"{date_value.month:02d}"


def build_filename(date_value: datetime, delivery_name: str, date_format: str) -> str:
    """リネーム後のファイル名を作る"""
    date_str = date_value.strftime(date_format)
    safe_delivery = delivery_name.replace("/", "_").replace("\\", "_")
    return f"{date_str}_{safe_delivery}.pdf"


def move_to_unique_path(source: Path, destination: Path) -> Path:
    """同名ファイルがある場合は連番を付けて移動する"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.move(str(source), str(destination))
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 2
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            shutil.move(str(source), str(candidate))
            return candidate
        counter += 1


def move_to_error(error_root: Path, source: Path, reason: str) -> Path:
    """エラーフォルダにファイルを移動する"""
    error_root.mkdir(parents=True, exist_ok=True)
    destination = error_root / source.name
    moved = move_to_unique_path(source, destination)
    log_path = error_root / "error.log"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{source.name}\t{reason}\n")
    return moved
