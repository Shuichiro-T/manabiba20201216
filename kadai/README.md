# 当日課題
WHOが提供してるデータ（COVID-19関連）をBigQueryに取り込み、AppEngie（python3）でグラフ化する

 * 使用するデータ​

  https://covid19.who.int/WHO-COVID-19-global-data.csv

## 注意事項
 * 各サービスを利用する際にAPIを有効化する必要があります。
 * Cloud Shellで操作を行います。
 * 以下のコマンドでプロジェクトを指定してください。
 ```shell
 gcloud config set project [PROJECT_ID]
 ```

## BigQueryにテーブルを作成する

### 事前準備

 * COVID-19感染者数・死亡者数ファイルのダウンロード

 ```shell
 curl -O https://covid19.who.int/WHO-COVID-19-global-data.csv
 ```

  
 ### テーブルの作成
  
  * データセットの作成（事前課題で作成している場合は不要）

 ```shell
 bq mk COVID19
 ```

   * テーブルの作成

 ```shell
 bq load --skip_leading_rows=1 --source_format=CSV COVID19.WHO_WORLD WHO-COVID-19-global-data.csv who_world_schema.json
 ```


   * データの確認

 ```shell
 bq show COVID19.WHO_WORLD
 ```

 ## アプリケーションをデプロイする

 ### ディレクトリの移動

 ```shell
 cd app
 ```

 ### デプロイする

 ```shell
 gcloud app deploy
 ```
