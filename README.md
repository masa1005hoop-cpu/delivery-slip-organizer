# delivery-slip-organizer — 納品書整理ツール

スキャンした納品書PDFを自動で分割・リネーム・振り分けするツール。
1ページ＝1枚の納品書として処理し、OCRで日付・届け先・顧客名を読み取る。

## コマンド一覧

```bash
python3 setup.py                        # 初回セットアップ（環境チェック＋パッケージ導入）
.venv/bin/python run.py                 # 監視モードで起動（常時）
.venv/bin/python run.py --once          # 受け取りフォルダ内を1回だけ処理
```

## 使い方

1. `納品書/` に顧客名フォルダを作成する（例: `納品書/○○株式会社/`）
2. `python3 run.py` でツールを起動する
3. 複数枚入りのPDFを `受け取り/` フォルダに入れる
4. 自動で分割・リネーム・振り分けされる

## ファイル名のルール

- 形式: `2026.08.20_田中家.pdf`
- 届け先の苗字に「家」を付ける（例: 田中 → 田中家）

## 保存先

```
納品書 / 顧客名 / 年 / 月 / ファイル名.pdf
```

## プロジェクト構成

```
delivery-slip-organizer/
├── CLAUDE.md           ← プロジェクト定義
├── README.md           ← このファイル
├── config.yaml         ← 設定（ラベル名・フォルダパス）
├── setup.py            ← 初回セットアップ
├── run.py              ← 起動スクリプト
├── requirements.txt
├── src/
│   ├── main.py         ← 監視・起動
│   ├── processor.py    ← 処理パイプライン
│   ├── pdf_splitter.py ← PDF分割
│   ├── ocr_extractor.py← 文字認識
│   └── file_organizer.py ← リネーム・移動
├── 受け取り/           ← PDFを入れる
├── 納品書/             ← 顧客フォルダ
├── 処理済み/           ← 処理済みの元PDF
└── エラー/             ← 読み取れなかったPDF
```

## 必要なソフト

**すべて無料です。** 有料契約やクレジットカード登録は不要です。

### Mac

```bash
brew install tesseract tesseract-lang poppler
python3 setup.py
```

### Windows

詳しくは **[SETUP-WINDOWS.md](SETUP-WINDOWS.md)** を参照してください。

```cmd
python setup.py
.venv\Scripts\python run.py
```

## よくあるエラーと対処法

| エラー | 原因 | 対処 |
|--------|------|------|
| 日付を読み取れませんでした | OCR精度・レイアウト | スキャン解像度を上げる。`config.yaml` のラベルを確認 |
| 顧客名フォルダが見つかりません | フォルダ名とPDF内の顧客名が一致しない | `納品書/` に正しい顧客名フォルダを作成 |
| jpn not found | 日本語OCR未インストール | `brew install tesseract-lang` |
| pdftoppm not found | poppler未インストール | `brew install poppler` |

## 設定のカスタマイズ

`config.yaml` で以下を変更できます:

- `labels.delivery_to` — 届け先のラベル名（デフォルト: 届け先）
- `labels.customer` — 顧客名のラベル名（デフォルト: 顧客名）
- `ocr.dpi` — スキャン解像度（高いほど精度UP、処理は遅くなる）
