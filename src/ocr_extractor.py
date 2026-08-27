"""スキャンPDFからOCRで情報を読み取る"""

import re
from datetime import datetime
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


DATE_PATTERNS = [
    re.compile(r"(\d{4})[./\-年](\d{1,2})[./\-月](\d{1,2})"),
]


def ocr_pdf_page(pdf_path: Path, language: str = "jpn", dpi: int = 300) -> str:
    """PDFの1ページを画像に変換してOCRテキストを返す"""
    images = convert_from_path(str(pdf_path), dpi=dpi, first_page=1, last_page=1)
    if not images:
        return ""
    return pytesseract.image_to_string(images[0], lang=language)


def extract_value_after_label(text: str, label: str) -> str | None:
    """ラベル（例: 届け先）の直後にある値を取り出す"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if label in line:
            # 同じ行に値がある場合（例: 届け先: 田中）
            after_label = line.split(label, 1)[-1]
            after_label = re.sub(r"^[：:\s]+", "", after_label).strip()
            if after_label:
                return after_label
            # 次の行が値の場合
            if index + 1 < len(lines):
                return lines[index + 1].strip()
    return None


def parse_date(text: str) -> datetime | None:
    """テキストから日付を探して datetime に変換する"""
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        year, month, day = map(int, match.groups())
        try:
            return datetime(year, month, day)
        except ValueError:
            continue
    return None


def format_delivery_name(raw_name: str, suffix: str = "家") -> str:
    """届け先の苗字に「家」を付けたファイル名用の文字列を作る"""
    name = raw_name.strip()
    # 敬称や空白を除去
    name = re.sub(r"\s*(様|さん|殿)\s*$", "", name)
    name = name.strip()
    if not name:
        return ""
    if not name.endswith(suffix):
        name = f"{name}{suffix}"
    return name


def extract_slip_info(
    pdf_path: Path,
    delivery_label: str,
    customer_label: str,
    language: str = "jpn",
    dpi: int = 300,
    delivery_suffix: str = "家",
) -> dict:
    """1枚の納品書PDFから日付・届け先・顧客名を読み取る"""
    text = ocr_pdf_page(pdf_path, language=language, dpi=dpi)
    delivery_raw = extract_value_after_label(text, delivery_label)
    customer_name = extract_value_after_label(text, customer_label)
    date_value = parse_date(text)

    return {
        "text": text,
        "date": date_value,
        "delivery_raw": delivery_raw,
        "delivery_name": format_delivery_name(delivery_raw or "", delivery_suffix),
        "customer_name": (customer_name or "").strip(),
    }
