/*
Name: Filters: PE Active
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.884Z
Visualizations: [{'id': 27, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.819Z', 'created_at': '2025-11-05T22:01:34.819Z'}, {'id': 324, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.871Z', 'created_at': '2025-11-05T22:01:40.871Z'}, {'id': 325, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.884Z', 'created_at': '2025-11-05T22:01:40.884Z'}]
*/

select distinct pe_active as a, count(*) from flow_cell_metadata group by a order by a