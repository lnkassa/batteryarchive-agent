/*
Name: module DD
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.732Z
Visualizations: [{'id': 17, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.607Z', 'created_at': '2025-11-05T22:01:34.607Z'}, {'id': 312, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.713Z', 'created_at': '2025-11-05T22:01:40.713Z'}, {'id': 313, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.732Z', 'created_at': '2025-11-05T22:01:40.732Z'}]
*/

select module_id from module_metadata where status = 'completed' order by module_id