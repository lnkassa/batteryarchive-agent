/*
Name: Disruptive Test: Displacement
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:36.235Z
Visualizations: [{'id': 34, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.968Z', 'created_at': '2025-11-05T22:01:34.968Z'}, {'id': 87, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.186Z', 'created_at': '2025-11-05T22:01:36.186Z'}, {'id': 88, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.199Z', 'created_at': '2025-11-05T22:01:36.199Z'}, {'id': 89, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.211Z', 'created_at': '2025-11-05T22:01:36.211Z'}, {'id': 90, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.223Z', 'created_at': '2025-11-05T22:01:36.223Z'}, {'id': 91, 'type': 'CHART', 'name': 'Displacement', 'description': '', 'options': {'globalSeriesType': 'scatter', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Time (s)'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Displacement (mm)'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': True, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'test_time': 'x', 'value': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.283Z', 'created_at': '2025-11-05T22:01:36.235Z'}]
*/

SELECT KEY || ': ' || r.cell_id AS series,
              r.test_time,
              value
FROM
  (SELECT abuse_timeseries.cell_id,
          test_time,
          json_build_object(
            'D', axial_d
        ) AS line
   FROM abuse_timeseries TABLESAMPLE BERNOULLI (10)
   WHERE cell_id IN ({{cell_id}})) AS r
JOIN LATERAL json_each_text(r.line) ON (KEY ~ '[F,D]')
where cast(value as decimal) <> '0' 
ORDER BY r.cell_id,
         r.test_time,
         KEY