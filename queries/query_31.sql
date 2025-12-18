/*
Name: Filters: Flow Rate
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.785Z
Visualizations: [{'id': 31, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.906Z', 'created_at': '2025-11-05T22:01:34.906Z'}, {'id': 316, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.773Z', 'created_at': '2025-11-05T22:01:40.773Z'}, {'id': 317, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.785Z', 'created_at': '2025-11-05T22:01:40.785Z'}]
*/

select distinct flow_rate as a, count(*) from flow_cell_metadata group by a order by a