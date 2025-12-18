/*
Name: Filters: Cathode Abuse Test
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:36.409Z
Visualizations: [{'id': 37, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.029Z', 'created_at': '2025-11-05T22:01:35.029Z'}, {'id': 101, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.375Z', 'created_at': '2025-11-05T22:01:36.375Z'}, {'id': 102, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.386Z', 'created_at': '2025-11-05T22:01:36.386Z'}, {'id': 103, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.398Z', 'created_at': '2025-11-05T22:01:36.398Z'}, {'id': 104, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.409Z', 'created_at': '2025-11-05T22:01:36.409Z'}]
*/

select distinct cathode as a, count(*) from cell_metadata where test = 'abuse' group by a order by a