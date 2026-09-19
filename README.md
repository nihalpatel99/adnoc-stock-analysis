# ADNOC Stock Analysis — Databricks Project
Link:- https://dbc-fc44f338-b1da.cloud.databricks.com/dashboardsv3/01f1ad2e2e5115579dd53d714276e28d/published?o=7474658030205253

## Dataset

Daily OHLCV data for ADNOC stock, 2018-01-02 to 2024-05-30 (1,288 trading days), with derived columns: `Price_Change`, `Percentage_Change`, `Average_Price`, `Range`.

Additional engineered features (see `cleaning.py`): `Daily_Return`, `MA_20/50/200`, `Volatility_20d`, `RSI_14`, `Bollinger_Upper/Lower`, `Volume_MA_20`, `Is_Green`, `Gap`, `Cumulative_Return`, `Drawdown`, `Year`, `Month`, `DayOfWeek`.

## ADNOC Trading Performance Summary
Record Single Days
Best Day: Jan 4, 2021 → +35.99% return
Worst Day: Mar 9, 2020 → -13.0% (COVID-19 market crash)
Top Performing Months
Jan 2021: +34.47% cumulative (+2.15% avg daily)
Apr 2019: +15.57% cumulative
Nov 2023: +12.88% cumulative
Yearly Summary
Best Year: 2021 → +46.75%
Worst Year: 2023 → -15.20%

## Questions

1. **What were ADNOC's best and worst trading days/months/years by return?**

<img width="1220" height="501" alt="image" src="https://github.com/user-attachments/assets/850e9429-547b-4191-abeb-b24564886eb0" />
<img width="1247" height="521" alt="image" src="https://github.com/user-attachments/assets/ea8542a8-82e2-4dbc-9bed-674a5e5cc0e2" />

2. **How has daily volatility evolved over time?**

<img width="962" height="470" alt="image" src="https://github.com/user-attachments/assets/36836a11-d999-4c51-ade6-e2406ba02344" />


3. **Is there any pattern around Ramadan/UAE holidays, given it's a Gulf market?**

<img width="1373" height="552" alt="image" src="https://github.com/user-attachments/assets/a14350d4-427c-4eeb-837c-8876d44522e6" />


## Notes

- Source CSV is sorted newest-first; sort ascending by `Date` before running any rolling/window calculations.
- Some numeric columns carry floating-point noise (e.g. `-0.010000000000000231`) — round early in the pipeline.
