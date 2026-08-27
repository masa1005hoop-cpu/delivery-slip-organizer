"""PDFを1ページずつ分割する"""

from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def split_pdf_by_page(pdf_path: Path, output_dir: Path) -> list[Path]:
    """PDFを1ページ1ファイルに分割して保存する"""
    output_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf_path))
    output_files: list[Path] = []

    for index, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = output_dir / f"{pdf_path.stem}_page{index:03d}.pdf"
        with output_path.open("wb") as f:
            writer.write(f)
        output_files.append(output_path)

    return output_files
