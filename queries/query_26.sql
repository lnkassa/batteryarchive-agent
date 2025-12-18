/*
Name: Filters: Initial NE Active
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.906Z
Visualizations: [{'id': 26, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.797Z', 'created_at': '2025-11-05T22:01:34.797Z'}, {'id': 326, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.895Z', 'created_at': '2025-11-05T22:01:40.895Z'}, {'id': 327, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.906Z', 'created_at': '2025-11-05T22:01:40.906Z'}]
*/

select distinct initial_ne_active as a, count(*) from flow_cell_metadata group by a order by a