/*
Name: Filters: PE Volume
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.809Z
Visualizations: [{'id': 30, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.883Z', 'created_at': '2025-11-05T22:01:34.883Z'}, {'id': 318, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.797Z', 'created_at': '2025-11-05T22:01:40.797Z'}, {'id': 319, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.809Z', 'created_at': '2025-11-05T22:01:40.809Z'}]
*/

select distinct pe_volume as a, count(*) from flow_cell_metadata group by a order by a