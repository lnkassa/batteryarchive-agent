/*
Name: Filters: PE Material
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:41.001Z
Visualizations: [{'id': 22, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.711Z', 'created_at': '2025-11-05T22:01:34.711Z'}, {'id': 334, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.990Z', 'created_at': '2025-11-05T22:01:40.990Z'}, {'id': 335, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:41.001Z', 'created_at': '2025-11-05T22:01:41.001Z'}]
*/

select distinct pe_material as a, count(*) from flow_cell_metadata group by a order by a