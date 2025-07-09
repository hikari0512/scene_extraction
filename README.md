# VALORANT シーン自動抽出アプリケーション

このアプリケーションは、チーム対戦型FPSゲーム「VALORANT」のプレイ動画から特定のシーンを自動抽出する機能を提供します。OpenCLIPモデルを活用し、さまざまなシーンへの柔軟な対応が可能です。

## 機能概要

### 主な機能
- 動画のアップロード
- 検出確信度の閾値調整
- シーンの自動抽出
- 抽出結果のプレビュー

### モデル学習に関する機能
- OpenCLIPモデルのファインチューニング
- カスタムデータセットを用いた学習プロセス
- 最適なモデルの保存と運用

## 使用言語/フレームワーク等

- **Python**: ロジック構築と機械学習モデルの操作
- **Flask**: Webフレームワーク
- **OpenCLIP**: CLIPモデルの利用と学習
- **PyTorch**: モデル学習と推論
- **MoviePy**: 動画編集ツール
- **Bootstrap**: フロントエンドデザインの構築

## セットアップ手順

### 必要な環境
- Python 3.8以上
- CUDA対応GPU（推奨）

### インストール方法
1. リポジトリをクローンします:
    ```
    git clone https://github.com/hikari0512/VALORANT_scene_extraction.git
    cd VALORANT_scene_extraction
    ```

2. 必要な依存関係をインストールします:
    ```
    pip install -r requirements.txt
    ```

3. モデルファイルを準備します:
    - `finetuned_openclip.pth`を`app.py`で指定されたパスに配置してください。

4. サーバーを起動します:
    ```
    python app.py
    ```

5. ブラウザで`http://127.0.0.1:5000/`にアクセスしてください。

### モデル学習を行う場合
1. トレーニング用のCSVファイルを準備します:
    - ファイルには画像ファイルのパス（相対パス）と、各画像に対応するテキストラベル（プロンプト）を含める必要があります。
    - 画像はdata/0（非戦闘シーン）、data/1（戦闘シーン）など、クラスごとにフォルダ分けして保存されます。
    - 学習データの例（train_clip.csv）：
      ```
        image_path,text
        data/0/train_000.png,"holding weapon not shooting at enemy"
        data/0/train_001.png,"preparing during buy phase"
        data/0/train_002.png,"using skill not in combat"
        data/1/train_000.png,"shooting at enemy"
        data/1/train_001.png,"killed an enemy"
        data/1/train_002.png,"killed by enemy"
      ```
   - 各行が画像とそれに対応する自然言語プロンプトを紐づけており、CLIPモデルのファインチューニングに利用されます。

2. 学習を開始します:
    ```
    python train_openCLIP.py
    ```

## システム画面

### 入力画面
![入力画面へ移動](images/start_screen.png)

### 抽出プロセス画面
![抽出プロセス画面へ移動](images/extraction_screen.png)

### 抽出結果画面
![抽出結果画面へ移動](images/result_screen.png)

## ファイル構成

```
|── data/
    ├── 0/ #非戦闘シーン
        ├── train_000.png 
        ├── train_001.png
        ├── train_002.png 
    ├── 1/ #戦闘シーン
        ├── train_000.png
        ├── train_001.png
        ├── train_002.png
│── images/   # システムの画面画像
    ├── extraction_screen.png  # 抽出途中の画像
    ├── result_screen.png   # 抽出結果の画像
    ├── start_screen.png  # 入力画面の画像
├── templates/            # HTMLテンプレート
    ├── index.html        # 動画アップロード画面
    └── result.html       # 抽出結果画面
├── README.md             # プロジェクト概要
├── app.py                # 主なサーバースクリプト
├── requirements.txt      # 必要なPython依存関係
├── train_openCLIP.py     # モデル学習用スクリプト
```

### 今後の展望
1. ユーザがプロンプトを設定し、より多様なシーンに対応。
2. 学習データセットの拡充。
3. プロンプトの精度向上。
4. モデル選定の最適化。

### 留意事項
本プロジェクトのコードおよびドキュメントは、OpenAIのChatGPTをはじめとする生成AIツールを活用しながら作成しています。
生成AIを通じてアイデアの整理や実装の支援を受けつつ、自身でも構成や実行・検証・改善を繰り返すことで完成させました。
