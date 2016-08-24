# Cleaning steps

- Apply underscore-case to names, e.g. `pd_id` for `PdId`
- Rename columns for clarity, e.g. `incident_num` for `IncidntNum`
  in particular, `longitude` for `X` and `latitude` for `Y`
- Drop redundant `Location`
- Keep `DayOfWeek` as `day_of_week`, but trim data from `Monday` to `Mon`. Prefer abbreviations to 0-6/1-7 numbering so that end-user doesn't also have to wonder if data is in PST or UTC (it's the former!)
- Concatenate `Date` and `Time` to `datetime, and convert to UTC
- 
