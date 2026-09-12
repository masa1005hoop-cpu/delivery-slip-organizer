# delivery-slip-organizer — 納品書整理ツール

スキャンした納品書PDFを自動で分割・リネーム・振り分けするツール。
1ページ＝1枚の納品書として処理し、OCRで日付・届け先・顧客名を読み取る。

> **はじめて設定する方へ。**
> Windowsの手順は [SETUP-WINDOWS.md](SETUP-WINDOWS.md) に全部書いてあります。
> 配布用パッケージには、同じ内容を絵入りにしたPDFを同梱しています。

## コマンド一覧

| | Mac | Windows |
|---|---|---|
| 初回セットアップ | `python3 setup.py` | `python setup.py` |
| 監視モードで起動 | `.venv/bin/python run.py` | `.venv\Scripts\python run.py` |
| 1回だけ処理 | `.venv/bin/python run.py --once` | `.venv\Scripts\python run.py --once` |

`setup.py` は実行するOSを見て、仮想環境の場所と案内を切り替える。
起動は**必ず仮想環境のPython**を使う（`python3 run.py` では依存パッケージが見つからない）。

## 使い方

1. `納品書/` に顧客名フォルダを作成する（例: `納品書/○○株式会社/`）
2. 上の表の「監視モードで起動」を実行する
3. 複数枚入りのPDFを `受け取り/` フォルダに入れる
4. 自動で分割・リネーム・振り分けされる
5. **保存されたファイル名を目で確認する**（「気をつけること」を参照）

## ファイル名のルール

- 形式: `2026.08.20_田中家.pdf`
- 届け先の苗字に「家」を付ける（例: 田中 → 田中家）

## 保存先

```
納品書 / 顧客名 / 年 / 月 / ファイル名.pdf
```

## 気をつけること

OCRは読み間違える。**読み間違えても、そのままの名前で保存する。警告は出ない。**
実際のテストで `鈴木様` が `印木様` と読まれた。字形が似ていると機械には見分けがつかない。

運用では、1日の終わりに保存されたファイル名を目で確認する。
顧客名フォルダの照合は部分一致も許容するため、似た名前のフォルダがあると別の顧客に入ることがある。

なお日付については、OCRが数字の間に空白を入れる読み方（`2026年9月1 1日`）で
日付が手前で切れる不具合があった。`ocr_extractor.py` の `normalize_digit_gaps()` で
数字間の空白だけを除去してから解析するよう修正済み（改行はまたがない）。

## プロジェクト構成

```
（ツールのフォルダ）
├── かんたん設定ガイド（まずこれを読む）.pdf  ← 絵入り手順書（配布用のみ）
├── はじめに読んでください.txt               ← 配布用の入口（配布用のみ）
├── README.md           ← このファイル
├── SETUP-WINDOWS.md    ← Windows手順書（文字版）
├── CLAUDE.md           ← プロジェクト定義
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
└── エラー/             ← 読み取れなかったPDF（error.log に理由）
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
| jpn not found | 日本語OCR未インストール | Mac: `brew install tesseract-lang` ／ Windows: Tesseractを入れ直しJapaneseにチェック |
| pdftoppm not found | poppler未インストール | Mac: `brew install poppler` ／ Windows: `C:\poppler\Library\bin` をPATHへ |
| PDFを入れても何も起きない | 監視プロセスが止まっている | 起動コマンドを実行し直す |

## 設定のカスタマイズ

`config.yaml` で以下を変更できます:

- `labels.delivery_to` — 届け先のラベル名（デフォルト: 届け先）
- `labels.customer` — 顧客名のラベル名（デフォルト: 顧客名）
- `filename.delivery_suffix` — 届け先の末尾（デフォルト: 家）
- `ocr.dpi` — スキャン解像度（高いほど精度UP、処理は遅くなる）
