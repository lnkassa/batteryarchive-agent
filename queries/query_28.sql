/*
Name: Filters: Initial PE Active
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.860Z
Visualizations: [{'id': 28, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.840Z', 'created_at': '2025-11-05T22:01:34.840Z'}, {'id': 322, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.848Z', 'created_at': '2025-11-05T22:01:40.848Z'}, {'id': 323, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.860Z', 'created_at': '2025-11-05T22:01:40.860Z'}]
*/

select distinct initial_pe_active as a, count(*) from flow_cell_metadata group by a order by a