# delivery-slip-organizer — 納品書整理ツール

スキャンした納品書PDFを自動で分割・リネーム・振り分けするツール。

## コマンド一覧

```bash
python3 setup.py                   # 初回セットアップ
pip3 install -r requirements.txt   # 依存関係インストール
python3 run.py                     # 監視モード起動
python3 run.py --once              # 1回だけ処理
```

## 共通ルール

- ユーザーはプログラミング未経験者の場合がある。1ステップずつ案内する
- エラーが起きたら、何が起きたか・次に何をすればいいかを平易に伝える

---

## トリガー

| ユーザーの発話 | 発動するスキル |
|--------------|-------------|
| 「開始」「処理して」 | 納品書整理スキル |
| 「セットアップして」 | セットアップスキル |

---

## セットアップスキル

### 完了の定義

- Tesseract OCR + 日本語データ (jpn) がインストール済み
- poppler がインストール済み
- `pip3 install -r requirements.txt` 完了
- `納品書/` に顧客名フォルダが作成済み

### 初回に必要なコマンド

**Mac:**

```bash
brew install tesseract tesseract-lang poppler
python3 setup.py
```

**Windows:** `SETUP-WINDOWS.md` を参照

```cmd
python setup.py
```

---

## 納品書整理スキル（メイン）

### 使い方

1. `python3 run.py` で起動
2. PDFを `受け取り/` に入れる
3. 自動で処理される

### 処理内容

1. PDFを1ページずつ分割
2. OCRで日付・届け先・顧客名を読み取り
3. `YYYY.MM.DD_届け先家.pdf` にリネーム
4. `納品書/顧客名/年/月/` に保存

### エラー時

- 読み取れなかったPDFは `エラー/` に移動
- `エラー/error.log` に理由が記録される

---

## よくあるエラーと対処法

- **日付/届け先/顧客名を読み取れない** → スキャン品質を確認。`config.yaml` のラベル名を納品書の表記に合わせる
- **顧客名フォルダが見つからない** → `納品書/` にPDF内の顧客名と同じフォルダ名を作成
- **jpn not found** → `brew install tesseract-lang`
