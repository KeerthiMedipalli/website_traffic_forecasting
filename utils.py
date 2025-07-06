import numpy as np
import pandas as pd
from datetime import timedelta, datetime

def generate_sample_data(url: str, days: int = 90):
    """Simulate traffic data based on URL type"""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days-1)
    dates = pd.date_range(start=start_date, end=end_date)

    # simulate traffic patterns based on URL
    if 'blog' in url or 'news' in url:
        base = 500
    elif 'shop' in url or 'store' in url:
        base = 1200
    else:
        base = 800

    trend = np.linspace(0, 50, days)
    weekly_pattern = np.tile([1.0, 1.1, 0.9, 0.95, 1.2, 1.5, 1.8], days // 7 + 1)[:days]
    noise = np.random.normal(0, 30, days)

    traffic = np.maximum(base + trend * weekly_pattern + noise, 0).astype(int)
    return dates, traffic
