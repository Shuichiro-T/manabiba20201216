import os

from flask import Flask, render_template, request
from google.cloud import bigquery

app = Flask(__name__)
bigquery_client = bigquery.Client()

# リクエストを受け付ける関数
@app.route('/', methods=['GET'])
def diplay():

    #BigQueryにクエリを投げる(地域別に新規感染者数と累計死者数を取得)
    query_job = bigquery_client.query(
        """
        SELECT
            DATE_REPORTED AS DATE,
            WHO_REGION AS REGION,
            SUM(NEW_CASES) AS NEW_CASES,
            SUM(CUMULATIVE_DEATHS) AS CUMULATIVE_DEATHS
        FROM
            COVID19.WHO_WORLD
        GROUP BY
            WHO_REGION, DATE_REPORTED
        ORDER BY
            DATE
        """
    )

    # クエリの実行結果をデータフレームに取得する
    df = query_job.to_dataframe()

    labels = df["DATE"]

    dfAFRO = df.query('REGION == "AFRO"')
    dfAMRO = df.query('REGION == "AMRO"')
    dfSEARO = df.query('REGION == "SEARO"')
    dfEURO = df.query('REGION == "EURO"')
    dfEMRO = df.query('REGION == "EMRO"')
    dfWPRO = df.query('REGION == "WPRO"')

    labels = dfAFRO["DATE"]

    datas = {
        "AFRO" : [dfAFRO["NEW_CASES"], dfAFRO["CUMULATIVE_DEATHS"]],
        "AMRO" : [dfAMRO["NEW_CASES"], dfAMRO["CUMULATIVE_DEATHS"]],
        "SEARO" : [dfSEARO["NEW_CASES"], dfSEARO["CUMULATIVE_DEATHS"]],
        "EURO" : [dfEURO["NEW_CASES"], dfEURO["CUMULATIVE_DEATHS"]],
        "EMRO" : [dfEMRO["NEW_CASES"], dfEMRO["CUMULATIVE_DEATHS"]],
        "WPRO" : [dfWPRO["NEW_CASES"], dfWPRO["CUMULATIVE_DEATHS"]]
    }
    
    return render_template('chart.html', datas=datas, labels=labels)


if __name__ == '__main__':
    #ローカル実行時はCloud Shell推奨の8080ポートを使用する
    app.run(host='0.0.0.0', port=8080)