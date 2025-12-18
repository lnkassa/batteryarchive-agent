/*
Name: Filters: NE Volume
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.835Z
Visualizations: [{'id': 29, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.862Z', 'created_at': '2025-11-05T22:01:34.862Z'}, {'id': 320, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.822Z', 'created_at': '2025-11-05T22:01:40.822Z'}, {'id': 321, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.835Z', 'created_at': '2025-11-05T22:01:40.835Z'}]
*/

select distinct ne_volume as a, count(*) from flow_cell_metadata group by a order by a