from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd
from utils import generate_sample_data
from forecast import forecast_traffic, analyze_patterns

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    # Run forecast & insights
    url = request.args.get('url', 'https://example.com')
    dates, traffic = generate_sample_data(url)
    series = pd.Series(traffic, index=dates)
    future_dates, forecast, conf_int = forecast_traffic(series)
    insights = analyze_patterns(dates, traffic)

    # Build HTML table
    table_rows = "".join(
        f"<tr><td>{d.strftime('%Y-%m-%d')}</td><td>{int(p)}</td><td>{int(ci[0])}</td><td>{int(ci[1])}</td></tr>"
        for d,p,ci in zip(future_dates, forecast, conf_int.values)
    )

    insights_html = "".join(
        f"<li><b>{item['title']}</b>: {item['value']}</li>" for item in insights
    )

    html = f"""
    <html>
    <head>
        <title>Website Traffic Forecast</title>
    </head>
    <body style="font-family:Arial; margin:30px;">
        <h1>Traffic Forecast for next 30 days</h1>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Date</th><th>Prediction</th><th>Lower</th><th>Upper</th></tr>
            {table_rows}
        </table>
        <h2>Insights</h2>
        <ul>{insights_html}</ul>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    dates, traffic = generate_sample_data(url)
    series = pd.Series(traffic, index=dates)
    future_dates, forecast, conf_int = forecast_traffic(series)
    results = {
        "history": [{"date": d.strftime("%Y-%m-%d"), "traffic": int(t)} for d,t in zip(dates,traffic)],
        "forecast": [
            {"date": d.strftime("%Y-%m-%d"), "prediction": int(p), "lower": int(ci[0]), "upper": int(ci[1])}
            for d,p,ci in zip(future_dates, forecast, conf_int.values)
        ]
    }
    return jsonify(results)

@app.route('/insights', methods=['POST'])
def insights():
    data = request.get_json()
    url = data.get('url')
    dates, traffic = generate_sample_data(url)
    insights_data = analyze_patterns(dates, traffic)
    return jsonify(insights_data)

if __name__ == '__main__':
    app.run(debug=True)
