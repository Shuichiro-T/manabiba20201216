# 事前課題
厚生労働省が提供してるデータ（COVID-19関連）をBigQueryに取り込み、AppEngie（python3）でグラフ化する

 * 使用するデータ​

https://www.mhlw.go.jp/stf/covid-19/open-data.html


## BigQueryにテーブルを作成する

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


  * ファイルの確認をする
   ```shell
 head data.csv
 ```