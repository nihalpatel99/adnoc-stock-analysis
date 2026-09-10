# ADNOC Stock Analysis — Databricks Project
Link:- https://dbc-fc44f338-b1da.cloud.databricks.com/dashboardsv3/01f1ad2e2e5115579dd53d714276e28d/published?o=7474658030205253

## Dataset

Daily OHLCV data for ADNOC stock, 2018-01-02 to 2024-05-30 (1,288 trading days), with derived columns: `Price_Change`, `Percentage_Change`, `Average_Price`, `Range`.

Additional engineered features (see `cleaning.py`): `Daily_Return`, `MA_20/50/200`, `Volatility_20d`, `RSI_14`, `Bollinger_Upper/Lower`, `Volume_MA_20`, `Is_Green`, `Gap`, `Cumulative_Return`, `Drawdown`, `Year`, `Month`, `DayOfWeek`.

## Questions

1. **What were ADNOC's best and worst trading days/months/years by return?**
2. **How has daily volatility (using Range or Percentage_Change) evolved over time?**
3. **Is there any pattern around Ramadan/UAE holidays, given it's a Gulf market?**

## Notes

- Source CSV is sorted newest-first; sort ascending by `Date` before running any rolling/window calculations.
- Some numeric columns carry floating-point noise (e.g. `-0.010000000000000231`) — round early in the pipeline.
