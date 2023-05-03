import pandas as pd
from datetime import datetime, time, timedelta
from random import randint

def jitter_time(input_datetime: datetime, max_jitter_minutes: int = 30) -> time:
    new_datetime = input_datetime + timedelta(minutes=randint(-max_jitter_minutes, max_jitter_minutes))
    return new_datetime.time()

def model(dbt, session) -> pd.DataFrame:
    borough_codes = dbt.ref("borough_codes")
    time_now = datetime.now()

    borough_best_times = borough_codes.copy()

    borough_best_times["best_time"] = time_now
    borough_best_times["best_time"] = borough_best_times["best_time"].apply(jitter_time)
    borough_best_times['best_time'] = borough_best_times['best_time'].apply(lambda t: t.strftime("%H:%M"))
    

    # df = pd.DataFrame.from_dict(
    #     {
    #         # 'bbl': [3, 2, 1, 0],
    #         # 'wkb_geometry': ['a', 'b', 'c', 'd'],
    #     }
    # )

    return borough_best_times