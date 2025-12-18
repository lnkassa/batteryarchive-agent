/*
Name: Disruptive Test: Force
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.286Z
Visualizations: [{'id': 49, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.287Z', 'created_at': '2025-11-05T22:01:35.287Z'}, {'id': 151, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.240Z', 'created_at': '2025-11-05T22:01:37.240Z'}, {'id': 152, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.252Z', 'created_at': '2025-11-05T22:01:37.252Z'}, {'id': 153, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.264Z', 'created_at': '2025-11-05T22:01:37.264Z'}, {'id': 154, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.275Z', 'created_at': '2025-11-05T22:01:37.275Z'}, {'id': 155, 'type': 'CHART', 'name': 'Force', 'description': '', 'options': {'globalSeriesType': 'scatter', 'sortX': True, 'legend': {'enabled': True, 'placement': 'auto', 'traceorder': 'normal'}, 'xAxis': {'type': '-', 'labels': {'enabled': True}, 'title': {'text': 'Time (s)'}}, 'yAxis': [{'type': 'linear', 'title': {'text': 'Force (N)'}}, {'type': 'linear', 'opposite': True}], 'alignYAxesAtZero': True, 'error_y': {'type': 'data', 'visible': True}, 'series': {'stacking': None, 'error_y': {'type': 'data', 'visible': True}}, 'seriesOptions': {}, 'valuesOptions': {}, 'columnMapping': {'test_time': 'x', 'value': 'y', 'series': 'series'}, 'direction': {'type': 'counterclockwise'}, 'sizemode': 'diameter', 'coefficient': 1, 'numberFormat': '0,0[.]00000', 'percentFormat': '0[.]00%', 'textFormat': '', 'missingValuesAsZero': True, 'showDataLabels': False, 'dateTimeFormat': 'DD/MM/YY HH:mm', 'swappedAxes': False}, 'updated_at': '2025-11-05T22:01:41.266Z', 'created_at': '2025-11-05T22:01:37.286Z'}]
*/

SELECT KEY || ': ' || r.cell_id AS series,
              r.test_time,
              value
FROM
  (SELECT abuse_timeseries.cell_id,
          test_time,
          json_build_object(
            'F', axial_f,
            'D', axial_d
        ) AS line
   FROM abuse_timeseries TABLESAMPLE BERNOULLI (10)
   WHERE cell_id IN ({{cell_id}})) AS r
JOIN LATERAL json_each_text(r.line) ON (KEY ~ '[F,D]')
where cast(value as decimal) <> '0' 
ORDER BY r.cell_id,
         r.test_time,
         KEY