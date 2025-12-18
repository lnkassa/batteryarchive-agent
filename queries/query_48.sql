/*
Name: Cycle Quantities by step
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.211Z
Visualizations: [{'id': 48, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.266Z', 'created_at': '2025-11-05T22:01:35.266Z'}, {'id': 146, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.164Z', 'created_at': '2025-11-05T22:01:37.164Z'}, {'id': 147, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.176Z', 'created_at': '2025-11-05T22:01:37.176Z'}, {'id': 148, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.188Z', 'created_at': '2025-11-05T22:01:37.188Z'}, {'id': 149, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.199Z', 'created_at': '2025-11-05T22:01:37.199Z'}, {'id': 150, 'type': 'CHART', 'name': 'Chart', 'description': '', 'options': {'globalSeriesType': 'line', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Cycle Time (s)'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Voltage (V)'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': False, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'cycle_time': 'x', 'v': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:37.211Z', 'created_at': '2025-11-05T22:01:37.211Z'}]
*/

select * from 
(SELECT
	cycle_time,
	v,  
	cycle_index,  
	case 
	    when i>0 then
	        ah_c  
	    when i<0 then
	        ah_d
	    end ah,
	case 
	    when i>0 then
	        cell_id || ' c: ' || cycle_index   
	    when i<0 then
	        cell_id || ' d: ' || cycle_index
	    end series
FROM cycle_timeseries
where 
    cell_id IN ({{cell_id}}) and
    MOD(cycle_index,{{Step}})=0 
order by cycle_index, series) as foo where series is not null;