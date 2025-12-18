/*
Name: Filters: Flow Pattern
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:41.054Z
Visualizations: [{'id': 20, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.669Z', 'created_at': '2025-11-05T22:01:34.669Z'}, {'id': 338, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:41.041Z', 'created_at': '2025-11-05T22:01:41.041Z'}, {'id': 339, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:41.054Z', 'created_at': '2025-11-05T22:01:41.054Z'}]
*/

select distinct flow_pattern as a, count(*) from flow_cell_metadata group by a order by a