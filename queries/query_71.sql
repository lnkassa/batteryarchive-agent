/*
Name: stackEfficiencies
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:39.231Z
Visualizations: [{'id': 71, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.749Z', 'created_at': '2025-11-05T22:01:35.749Z'}, {'id': 233, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.174Z', 'created_at': '2025-11-05T22:01:39.174Z'}, {'id': 234, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.202Z', 'created_at': '2025-11-05T22:01:39.202Z'}, {'id': 235, 'type': 'CHART', 'name': 'Chart', 'description': '', 'options': {'globalSeriesType': 'line', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Cycle Index'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Energy and Coulombic Efficiencies'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': False, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'cycle_index': 'x', 'value': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.758Z', 'created_at': '2025-11-05T22:01:39.231Z'}]
*/

SELECT
   key || ': ' || r.cell_id as series,
   r.cycle_index,
   value
FROM (SELECT cell_id, trunc(cycle_index,0) as cycle_index, json_build_object('e_eff', e_eff, 'ah_eff', ah_eff) AS line 
FROM flow_cycle_stats
where cell_id IN ({{stack_id}})) as r
JOIN LATERAL json_each_text(r.line) ON (key ~ '[e,ah]_[eff]')
where cast(value as numeric)>0 
GROUP by r.cell_id, r.cycle_index, json_each_text.key, json_each_text.value
order by r.cell_id,r.cycle_index, key     