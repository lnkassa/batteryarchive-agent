/*
Name: Filters: C charge Rate
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.279Z
Visualizations: [{'id': 8, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.415Z', 'created_at': '2025-11-05T22:01:34.415Z'}, {'id': 272, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.241Z', 'created_at': '2025-11-05T22:01:40.241Z'}, {'id': 273, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.254Z', 'created_at': '2025-11-05T22:01:40.254Z'}, {'id': 274, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.266Z', 'created_at': '2025-11-05T22:01:40.266Z'}, {'id': 275, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.279Z', 'created_at': '2025-11-05T22:01:40.279Z'}]
*/

select distinct crate_c as a, count(*) from cycle_metadata group by a order by a