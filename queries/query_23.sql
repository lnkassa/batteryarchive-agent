/*
Name: Filters: Membrane
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.979Z
Visualizations: [{'id': 23, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.731Z', 'created_at': '2025-11-05T22:01:34.731Z'}, {'id': 332, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.965Z', 'created_at': '2025-11-05T22:01:40.965Z'}, {'id': 333, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.979Z', 'created_at': '2025-11-05T22:01:40.979Z'}]
*/

select distinct membrane as a, count(*) from flow_cell_metadata group by a order by a