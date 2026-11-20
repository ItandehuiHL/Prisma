import pandas as pd

def status(state, condition, yld):
    if pd.isna(state) or pd.isna(condition) or pd.isna(yld):
        return pd.NA
    if state != 0:
        return 3  if yld == 0.0 else 2 if condition == 1.0 else 1  # DUT NOK
    if yld == 0.0:
        return 4 if condition < 1.0 else 3  # sin material
    if yld == 1.0:
        return 2 if condition < 1.0 else 3  # yield bajo
    return 1  # DUT OK

df1 = pd.read_csv("cycleData.csv", parse_dates=["_time"])
df1.sort_values("_time", inplace=True)

df2 = pd.read_csv("machineState.csv", parse_dates=["_time"])
df2.sort_values("_time", inplace=True) 

merge = pd.merge(df1, df2, on=["_time", "Fixture", "asset_name"], how="left")

states_unicos = df2[
    ~df2["_time"].isin(df1["_time"])
]

combinado = pd.concat([merge, states_unicos], ignore_index=True)
combinado = combinado.sort_values("_time").reset_index(drop=True)

results = (combinado.cycle_result / combinado.cycle_result)
combinado["results"] = results
combinado["results"] = combinado["results"].fillna(0)

combinado.to_csv("dutState.csv", index=False)

dut_1 = combinado[combinado['Fixture'] == 1]
dut_1 = dut_1.ffill()
mean_results = dut_1["mean_results"] = (
    dut_1["results"]
    .rolling(5)
    .mean()
)
total =  dut_1["cycle_result"].rolling(20).count()
passed = dut_1["cycle_result"].rolling(20).apply(lambda x: (x == 0.0).sum())
dut_1["yield_pct"] = (passed / total)
#dut_1["yield_pct"] = dut_1["yield_pct"].bfill()
dut_1["yield_state"] = dut_1["yield_pct"].apply(lambda x: 2 if x > 0.5 else 1 if x <= 0.5 and x > 0.0 else 0)
dut_1["status"] = dut_1.apply(lambda row: status(row["machine_state"], row["mean_results"], row["yield_state"]),axis=1,)

dut_1.to_csv("dut1.csv", index=False)

dut_2 = combinado[combinado['Fixture'] == 2]
dut_2 = dut_2.ffill()
mean_results = dut_2["mean_results"] = (
    dut_2["results"]
    .rolling(5)
    .mean()
)
total =  dut_2["cycle_result"].rolling(20).count()
passed = dut_2["cycle_result"].rolling(20).apply(lambda x: (x == 0.0).sum())
dut_2["yield_pct"] = (passed / total)
#dut_2["yield_pct"] = dut_2["yield_pct"].bfill()
dut_2["yield_state"] = dut_2["yield_pct"].apply(lambda x: 2 if x > 0.5 else 1 if x <= 0.5 and x > 0.0 else 0)
dut_2["status"] = dut_2.apply(lambda row: status(row["machine_state"], row["mean_results"], row["yield_state"]),axis=1,)

dut_2.to_csv("dut2.csv", index=False)

dut_3 = combinado[combinado['Fixture'] == 3]
dut_3 = dut_3.ffill()
mean_results = dut_3["mean_results"] = (
    dut_3["results"]
    .rolling(5)
    .mean()
)
total =  dut_3["cycle_result"].rolling(20).count()
passed = dut_3["cycle_result"].rolling(20).apply(lambda x: (x == 0.0).sum())
dut_3["yield_pct"] = (passed / total)
#dut_3["yield_pct"] = dut_3["yield_pct"].bfill()
dut_3["yield_state"] = dut_3["yield_pct"].apply(lambda x: 2 if x > 0.5 else 1 if x <= 0.5 and x > 0.0 else 0)
dut_3["status"] = dut_3.apply(lambda row: status(row["machine_state"], row["mean_results"], row["yield_state"]),axis=1,)

dut_3.to_csv("dut3.csv", index=False)

dut_4 = combinado[combinado['Fixture'] == 4]
dut_4 = dut_4.ffill()
mean_results = dut_4["mean_results"] = (
    dut_4["results"]
    .rolling(5)
    .mean()
)
total =  dut_4["cycle_result"].rolling(20).count()
passed = dut_4["cycle_result"].rolling(20).apply(lambda x: (x == 0.0).sum())
dut_4["yield_pct"] = (passed / total)
#dut_4["yield_pct"] = dut_4["yield_pct"].bfill()
dut_4["yield_state"] = dut_4["yield_pct"].apply(lambda x: 2 if x > 0.5 else 1 if x <= 0.5 and x > 0.0 else 0)
dut_4["status"] = dut_4.apply(lambda row: status(row["machine_state"], row["mean_results"], row["yield_state"]),axis=1,)

dut_4.to_csv("dut4.csv", index=False)