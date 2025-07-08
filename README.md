# 戦闘シーン抽出アプリケーション

このリポジトリは、VALORANT戦闘シーン抽出アプリケーションのコードを含んでいます。このアプリケーションは、ユーザーがアップロードした動画から戦闘シーンを抽出します。

## 機能概要

- 動画アップロード機能
- 戦闘シーン抽出機能
- 抽出結果のプレビュー機能

## 使用技術

- Python
- Flask
- OpenCLIP
- Torch
- MoviePy
- Bootstrap

## セットアップ方法

### 必要な環境
- Python 3.8以上
- CUDA対応GPU（推奨）

### インストール手順
1. リポジトリをクローンします:
    ```
    git clone https://github.com/yourusername/battle-scene-extraction.git
    cd battle-scene-extraction
    ```

2. 必要な依存関係をインストールします:
    ```
    pip install -r requirements.txt
    ```

3. モデルファイルを準備します:
    - `finetuned_openclip.pth`を`app.py`で指定されたパスに配置してください。

4. アプリケーションを起動します:
    ```
    python app.py
    ```

5. ブラウザで`http://127.0.0.1:5000/`にアクセスしてください。

## ファイル構成

```
├── app.py                # Flaskアプリケーションのメインスクリプト
├── requirements.txt      # 必要なPython依存関係
├── templates/            # HTMLテンプレート
│   ├── index.html        # 動画アップロード画面
│   └── result.html       # 抽出結果画面
├── static/               # 静的ファイル
│   ├── uploads/          # アップロードされた動画
│   └── output/           # 戦闘シーン抽出後の動画
└── README.md             # プロジェクト概要
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。