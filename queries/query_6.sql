/*
Name: Filters: Cycle Cells Nominal Capacity (Ah)
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.373Z
Visualizations: [{'id': 6, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.372Z', 'created_at': '2025-11-05T22:01:34.372Z'}, {'id': 283, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.373Z', 'created_at': '2025-11-05T22:01:40.373Z'}, {'id': 280, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.338Z', 'created_at': '2025-11-05T22:01:40.338Z'}, {'id': 281, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.350Z', 'created_at': '2025-11-05T22:01:40.350Z'}, {'id': 282, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.362Z', 'created_at': '2025-11-05T22:01:40.362Z'}]
*/

select distinct ah as a, count(*) from cell_metadata where test = 'cycle' group by a order by a