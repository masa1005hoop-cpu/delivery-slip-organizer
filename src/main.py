"""納品書整理ツール — エントリーポイント"""

import argparse
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.config_loader import PROJECT_ROOT, get_folder_path, load_config
from src.processor import process_pdf


class PdfHandler(FileSystemEventHandler):
    """受け取りフォルダにPDFが追加されたら処理する"""

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() != ".pdf":
            return
        # ファイルの書き込み完了を待つ
        time.sleep(1)
        handle_pdf(path)


def handle_pdf(pdf_path: Path) -> None:
    """1つのPDFを処理して結果を表示する"""
    print(f"\n処理開始: {pdf_path.name}")
    try:
        result = process_pdf(pdf_path)
        print(f"  成功: {result['success']}件 / 失敗: {result['failed']}件")
        for detail in result["details"]:
            status = "OK" if detail["ok"] else "NG"
            print(f"  [{status}] {detail['page']} → {detail['message']}")
    except Exception as exc:
        print(f"  エラー: {exc}", file=sys.stderr)


def ensure_folders() -> None:
    """必要なフォルダが無ければ作成する"""
    config = load_config()
    for key in ("inbox", "customers", "processed", "error"):
        folder = get_folder_path(config, key)
        folder.mkdir(parents=True, exist_ok=True)


def process_existing_pdfs() -> None:
    """受け取りフォルダ内の既存PDFをすべて処理する"""
    config = load_config()
    inbox = get_folder_path(config, "inbox")
    pdfs = sorted(inbox.glob("*.pdf"))
    if not pdfs:
        print("受け取りフォルダにPDFがありません。")
        return
    for pdf in pdfs:
        handle_pdf(pdf)


def watch_inbox() -> None:
    """受け取りフォルダを監視し続ける"""
    config = load_config()
    inbox = get_folder_path(config, "inbox")
    print("納品書整理ツールを起動しました。")
    print(f"監視中: {inbox}")
    print("PDFを「受け取り」フォルダに入れると自動で処理します。")
    print("停止するには Ctrl+C を押してください。\n")

    handler = PdfHandler()
    observer = Observer()
    observer.schedule(handler, str(inbox), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n停止しました。")
    observer.join()


def main() -> None:
    parser = argparse.ArgumentParser(description="納品書PDFの分割・リネーム・振り分け")
    parser.add_argument(
        "--once",
        action="store_true",
        help="受け取りフォルダ内のPDFを1回だけ処理する",
    )
    args = parser.parse_args()

    ensure_folders()

    if args.once:
        process_existing_pdfs()
    else:
        process_existing_pdfs()
        watch_inbox()


if __name__ == "__main__":
    main()
