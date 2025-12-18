/*
Name: stackDD
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.761Z
Visualizations: [{'id': 19, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.649Z', 'created_at': '2025-11-05T22:01:34.649Z'}, {'id': 314, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.748Z', 'created_at': '2025-11-05T22:01:40.748Z'}, {'id': 315, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.761Z', 'created_at': '2025-11-05T22:01:40.761Z'}]
*/

select stack_id from stack_metadata where status = 'completed' order by stack_id