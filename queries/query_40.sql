/*
Name: Charge voltage by step
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:36.541Z
Visualizations: [{'id': 40, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.094Z', 'created_at': '2025-11-05T22:01:35.094Z'}, {'id': 112, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.541Z', 'created_at': '2025-11-05T22:01:36.541Z'}, {'id': 111, 'type': 'CHART', 'name': 'Chart', 'description': '', 'options': {'globalSeriesType': 'line', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Cycle Time (s)'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Voltage (V)'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': False, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'cycle_time': 'x', 'v': 'y', 'label': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.399Z', 'created_at': '2025-11-05T22:01:36.528Z'}]
*/

SELECT t.*
FROM (
  SELECT 
    cell_id, 
    cycle_time, 
    v, 
    count(*) as row_m, 
    cell_id  || ' ' || cycle_index as label, 
    row_number() OVER(ORDER BY min(test_time)) AS row
  FROM cycle_timeseries 
  where cell_id IN ({{cell_id}}) and (cycle_index = {{cycle_1}} or cycle_index = {{cycle_2}} or cycle_index = {{cycle_3}}) and i>0
  group by 
    cell_id,
    cycle_time,
    v,
    cycle_index
) t
WHERE MOD(t.row,
    case 
        when t.row_m > 1000000 then 1000
        when t.row_m > 100000 then 100
        when t.row_m > 10000 then 10
        else 1
    end) =0;
    
