/*
Name: Filters: NE Material
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:41.027Z
Visualizations: [{'id': 21, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.690Z', 'created_at': '2025-11-05T22:01:34.690Z'}, {'id': 336, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:41.013Z', 'created_at': '2025-11-05T22:01:41.013Z'}, {'id': 337, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:41.027Z', 'created_at': '2025-11-05T22:01:41.027Z'}]
*/

select distinct ne_material as a, count(*) from flow_cell_metadata group by a order by a