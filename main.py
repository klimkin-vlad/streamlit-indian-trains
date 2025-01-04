import pandas as pd
import datetime as dt
import streamlit as st

st.header("Расписание индийских ПДС")
date_start = dt.date(2022, 1, 1)
date_end = dt.date(2022, 12, 31)
date_selector = st.date_input("Укажите день, на который нужно расписание",
		value = date_start, min_value = date_start, max_value = date_end, format = "DD-MM-YYYY")
train_class = st.multiselect("Укажите предпочитаемые классы мест", ["1A", "2A", "3A", "2S", "SL"])
no_changes = st.checkbox("Без пересадок")
submit = st.button("Выбрать")
trains = pd.read_csv("Scraped.csv")
trains["start_date"] = pd.to_datetime(trains["start_date"], format = "%b-%d").dt.date
trains["start_date"] = trains["start_date"].apply(lambda x: x.replace(year = 2022))
trains["start_time"] = pd.to_datetime(trains["start_time"], format = "%H:%M").dt.time
if submit:
	query = trains[trains["start_date"] == date_selector]
	query = query[query["class_types"].str.contains("|".join(train_class))]
	if no_changes:
		query = query[query["Change"] == "No TT Change"]
	st.table(trains)
