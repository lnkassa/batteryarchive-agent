/*
Name: stackEnergyandCapDecay
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:38.986Z
Visualizations: [{'id': 69, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.706Z', 'created_at': '2025-11-05T22:01:35.706Z'}, {'id': 226, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:38.892Z', 'created_at': '2025-11-05T22:01:38.892Z'}, {'id': 227, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:38.919Z', 'created_at': '2025-11-05T22:01:38.919Z'}, {'id': 228, 'type': 'CHART', 'name': 'Timeseries Data', 'description': '', 'options': {'globalSeriesType': 'scatter', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Time (s)'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Wh/Ah'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': False, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'test_time': 'x', 'value': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.742Z', 'created_at': '2025-11-05T22:01:38.945Z'}, {'id': 229, 'type': 'CHART', 'name': 'Cycle Data', 'description': '', 'options': {'globalSeriesType': 'line', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Cycle Index'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Wh/Ah'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': False, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'cycle_index': 'x', 'value': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.822Z', 'created_at': '2025-11-05T22:01:38.986Z'}]
*/

SELECT
   key || ': ' || r.cell_id as series,
   r.cycle_index,
   r.test_time,
   value
FROM (SELECT cell_id, trunc(cycle_index,0) as cycle_index, test_time, json_build_object('e_d', e_d, 'ah_d', ah_d, 'e_c', e_c, 'ah_c', ah_c ) AS line 
FROM flow_cycle_stats
where cell_id IN ({{stack_id}}) and ah_eff<1.1) as r
JOIN LATERAL json_each_text(r.line) ON (key ~ '[e,ah]_[d,c]')
where cast(value as numeric)!=0
GROUP by r.cell_id, r.cycle_index,  r.test_time, json_each_text.key, json_each_text.value      
order by r.cell_id,r.cycle_index, key    