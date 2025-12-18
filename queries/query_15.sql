/*
Name: Filters: testers abuse test
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.512Z
Visualizations: [{'id': 15, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.563Z', 'created_at': '2025-11-05T22:01:34.563Z'}, {'id': 292, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.477Z', 'created_at': '2025-11-05T22:01:40.477Z'}, {'id': 293, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.488Z', 'created_at': '2025-11-05T22:01:40.488Z'}, {'id': 294, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.498Z', 'created_at': '2025-11-05T22:01:40.498Z'}, {'id': 295, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.512Z', 'created_at': '2025-11-05T22:01:40.512Z'}]
*/

select distinct tester as a, count(*) from cell_metadata where test = 'abuse' group by a order by a