"""納品書PDFの処理パイプライン"""

import tempfile
from pathlib import Path

from src.config_loader import get_folder_path, load_config
from src.file_organizer import (
    build_destination_folder,
    build_filename,
    find_matching_customer_folder,
    move_to_error,
    move_to_unique_path,
)
from src.ocr_extractor import extract_slip_info
from src.pdf_splitter import split_pdf_by_page


def process_single_page(
    page_pdf: Path,
    config: dict,
    customers_root: Path,
    error_root: Path,
) -> tuple[bool, str]:
    """分割された1ページ分のPDFを処理する"""
    labels = config["labels"]
    ocr_cfg = config["ocr"]
    filename_cfg = config["filename"]

    info = extract_slip_info(
        page_pdf,
        delivery_label=labels["delivery_to"],
        customer_label=labels["customer"],
        language=ocr_cfg["language"],
        dpi=ocr_cfg["dpi"],
        delivery_suffix=filename_cfg["delivery_suffix"],
    )

    if not info["date"]:
        move_to_error(error_root, page_pdf, "日付を読み取れませんでした")
        return False, "日付を読み取れませんでした"

    if not info["delivery_name"]:
        move_to_error(error_root, page_pdf, "届け先を読み取れませんでした")
        return False, "届け先を読み取れませんでした"

    if not info["customer_name"]:
        move_to_error(error_root, page_pdf, "顧客名を読み取れませんでした")
        return False, "顧客名を読み取れませんでした"

    customer_folder = find_matching_customer_folder(info["customer_name"], customers_root)
    if not customer_folder:
        reason = f"顧客名フォルダが見つかりません: {info['customer_name']}"
        move_to_error(error_root, page_pdf, reason)
        return False, reason

    destination_dir = build_destination_folder(customer_folder, info["date"])
    filename = build_filename(info["date"], info["delivery_name"], filename_cfg["date_format"])
    destination = destination_dir / filename
    move_to_unique_path(page_pdf, destination)
    return True, str(destination)


def process_pdf(pdf_path: Path) -> dict:
    """受け取りフォルダに入ったPDFを処理する"""
    config = load_config()
    inbox_root = get_folder_path(config, "inbox")
    customers_root = get_folder_path(config, "customers")
    processed_root = get_folder_path(config, "processed")
    error_root = get_folder_path(config, "error")

    if pdf_path.parent.resolve() != inbox_root.resolve():
        raise ValueError(f"受け取りフォルダ以外のファイルです: {pdf_path}")

    results = {
        "source": str(pdf_path),
        "success": 0,
        "failed": 0,
        "details": [],
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        page_files = split_pdf_by_page(pdf_path, temp_path)

        for page_pdf in page_files:
            ok, message = process_single_page(page_pdf, config, customers_root, error_root)
            if ok:
                results["success"] += 1
            else:
                results["failed"] += 1
            results["details"].append({"page": page_pdf.name, "ok": ok, "message": message})

    processed_root.mkdir(parents=True, exist_ok=True)
    move_to_unique_path(pdf_path, processed_root / pdf_path.name)
    return results
