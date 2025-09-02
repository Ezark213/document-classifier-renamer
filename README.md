# 文書分類・リネームシステム

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

**OCR機能を備えたインテリジェント文書分類・リネームシステム**

OCRテキスト認識と事前定義されたルールを使用してPDFやCSV文書を自動分類し、構造化された命名規則でファイル名を変更します。

## 🚀 主な機能

- **自動文書分類**: 内容分析に基づく文書の自動分類
- **OCRテキスト認識**: PDF文書からのテキスト抽出と分析
- **スマートリネーム**: 分類に基づく構造化ファイル名の生成
- **バッチ処理**: 複数ファイルの一括処理
- **GUI インターフェース**: 使いやすいドラッグ&ドロップインターフェース
- **PDF分割**: 必要に応じた複数ページPDFの自動分割
- **カスタマイズ可能なルール**: 文書タイプと分類ルールの簡単追加

## 📋 対応文書タイプ

| カテゴリ | コード | 文書タイプ | 出力例 |
|----------|------|------------|--------|
| **財務書類** | 1001 | 財務諸表 | `1001_財務諸表_2024.pdf` |
| | 1002 | 損益計算書 | `1002_損益計算書_2024.pdf` |
| | 1003 | 貸借対照表 | `1003_貸借対照表_2024.pdf` |
| **法的文書** | 2001 | 契約書 | `2001_契約書_2024.pdf` |
| | 2002 | 合意書 | `2002_合意書_2024.pdf` |
| **報告書** | 3001 | 年次報告書 | `3001_年次報告書_2024.pdf` |
| | 3002 | 月次報告書 | `3002_月次報告書_2024.pdf` |
| **請求書類** | 4001 | 請求書 | `4001_請求書_2024.pdf` |
| | 4002 | 領収書 | `4002_領収書_2024.pdf` |

## 🛠️ インストール

### 必要な環境
- Python 3.8 以上
- Tesseract OCR（PDF テキスト抽出用）

### クイックスタート

1. **リポジトリのクローン**
```bash
git clone https://github.com/Ezark213/document-classifier-renamer.git
cd document-classifier-renamer
```

2. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

3. **Tesseract OCRのインストール**
   - **Windows**: [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki) からダウンロード
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **アプリケーションの実行**
```bash
python main.py
```

## 📁 プロジェクト構成

```
document-classifier-renamer/
├── main.py                    # メインアプリケーション
├── requirements.txt           # Python依存関係
├── core/                      # コアモジュール
│   ├── __init__.py
│   ├── classifier.py          # 文書分類エンジン
│   ├── ocr_engine.py          # OCR処理
│   ├── pdf_processor.py       # PDF処理
│   └── csv_processor.py       # CSV処理
├── ui/                        # ユーザーインターフェース
│   ├── __init__.py
│   └── drag_drop.py           # ドラッグ&ドロップGUI
├── config/                    # 設定ファイル
│   └── classification_rules.py
└── examples/                  # サンプル文書
    ├── sample_invoice.pdf
    ├── sample_contract.pdf
    └── sample_report.pdf
```

## 🎯 使用方法

### GUI モード（推奨）

1. **アプリケーションの起動**
   ```bash
   python main.py
   ```

2. **文書の追加**
   - アプリケーションウィンドウにファイルをドラッグ&ドロップ
   - または「ファイル選択」ボタンで参照

3. **設定の構成**
   - 出力日付形式の設定（YYYY、YYMM など）
   - 出力ディレクトリの選択
   - 自動PDF分割の有効/無効

4. **文書の処理**
   - 「分類・リネーム」ボタンで処理開始
   - 結果タブで処理結果を確認

### コマンドラインモード

```bash
python main.py --input /path/to/documents --output /path/to/output --batch
```

## 🔧 設定

### 新しい文書タイプの追加

`config/classification_rules.py` を編集して新しい文書タイプを追加：

```python
CLASSIFICATION_RULES = {
    "5001": {
        "name": "発注書",
        "keywords": ["発注書", "注文書", "purchase order"],
        "priority": 100,
        "category": "procurement"
    }
}
```

### ファイル名命名規則のカスタマイズ

設定で命名パターンを変更：

```python
NAMING_PATTERN = "{code}_{document_type}_{date}.{extension}"
```

## 🧪 サンプル

### サンプル入力文書
`examples/` ディレクトリにはシステムテスト用のサンプル文書が含まれています：
- 業務契約書
- 財務諸表
- 請求書
- 報告書

### 期待される出力
処理後、文書は以下のパターンでリネームされます：
- `input_contract.pdf` → `2001_契約書_2024.pdf`
- `financial_doc.pdf` → `1001_財務諸表_2024.pdf`

## 🤝 貢献

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🆘 サポート

- **Issues**: バグ報告や機能要求は [GitHub Issues](https://github.com/Ezark213/document-classifier-renamer/issues) まで
- **ドキュメント**: 詳細なドキュメントは [Wiki](https://github.com/Ezark213/document-classifier-renamer/wiki) を確認

## 🔗 関連プロジェクト

- [OCR Text Recognition](https://github.com/tesseract-ocr/tesseract)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF処理ライブラリ
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUIフレームワーク

---

**文書管理自動化への ❤️ を込めて開発**