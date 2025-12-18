/*
Name: Filters: Source cycle test
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.075Z
Visualizations: [{'id': 12, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.499Z', 'created_at': '2025-11-05T22:01:34.499Z'}, {'id': 256, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.039Z', 'created_at': '2025-11-05T22:01:40.039Z'}, {'id': 257, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.050Z', 'created_at': '2025-11-05T22:01:40.050Z'}, {'id': 258, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.062Z', 'created_at': '2025-11-05T22:01:40.062Z'}, {'id': 259, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.075Z', 'created_at': '2025-11-05T22:01:40.075Z'}]
*/

select distinct source as a, count(*) from cell_metadata where test = 'cycle' and source <> 'commercial' group by a order by a 