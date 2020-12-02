# 事前課題
厚生労働省が提供してるデータ（COVID-19関連）をBigQueryに取り込み、AppEngie（python3）でグラフ化する

 * 使用するデータ​

https://www.mhlw.go.jp/stf/covid-19/open-data.html

## 注意事項
 * 各サービスを利用する際にAPIを有効化する必要があります。
 * Cloud Shellで操作を行います。
 * 以下のコマンドでプロジェクトを指定してください。
 ```shell
 gcloud config set project [PROJECT_ID]
 ```

## BigQueryにテーブルを作成する

### 事前準備

 * PCR検査陽性者数ファイルのダウンロード

 ```shell
 curl -O https://www.mhlw.go.jp/content/pcr_positive_daily.csv
 ```

  * PCR検査実施人数別ファイルのダウンロード

 ```shell
 curl -O https://www.mhlw.go.jp/content/pcr_tested_daily.csv
 ```

   * 入院治療等を要する者の数別ファイルのダウンロード

 ```shell
 curl -O https://www.mhlw.go.jp/content/cases_total.csv
 ```

   * 死亡者数ファイルのダウンロード

 ```shell
 curl -O https://www.mhlw.go.jp/content/death_total.csv
 ```

   * 各ファイルの改行を削除

 ```shell
 tr -d "\r" <pcr_positive_daily.csv > lf_positive_daily.csv
 tr -d "\r" <pcr_tested_daily.csv > lf_tested_daily.csv
 tr -d "\r" <cases_total.csv > lf_cases_total.csv
 tr -d "\r" <death_total.csv > lf_death_total.csv
 ```


 * ファイルを結合する

 ```shell
 join -t, -a 1 -a 2 -1 1 -2 1 -o 0 1.2 2.2 -e '0' --header lf_positive_daily.csv lf_tested_daily.csv > temp.csv
 join -t, -a 1 -a 2 -1 1 -2 1 -o 0 1.2 1.3 2.2 -e '0' --header temp.csv  lf_cases_total.csv > temp2.csv
 join -t, -a 1 -a 2 -1 1 -2 1 -o 0 1.2 1.3 1.4 2.2 -e '0' --header temp2.csv lf_death_total.csv > data.csv
 rm temp*.csv
 ```

 * 日付のフォーマットを整える

 ```shell
 sed "s/\//\-/g" data.csv > data2.csv
 mv data2.csv data.csv
 ```

  * ファイルの確認をする
   ```shell
 head data.csv
 ```

 ### テーブルの作成
  
  * データセットの作成

 ```shell
 bq mk COVID19
 ```

   * テーブルの作成

 ```shell
 bq load --skip_leading_rows=1 --source_format=CSV COVID19.MHLW_JAPAN data.csv mhlw_japan_schema.json
 ```


   * データの確認

 ```shell
 bq show COVID19.MHLW_JAPAN
 ```

 ## アプリケーションをデプロイする

 ### ディレクトリの移動


 ```shell
 cd app
 ```

