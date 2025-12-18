/*
Name: Cycle Test DD
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.656Z
Visualizations: [{'id': 1, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.204Z', 'created_at': '2025-11-05T22:01:34.204Z'}, {'id': 304, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.620Z', 'created_at': '2025-11-05T22:01:40.620Z'}, {'id': 305, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.632Z', 'created_at': '2025-11-05T22:01:40.632Z'}, {'id': 306, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.644Z', 'created_at': '2025-11-05T22:01:40.644Z'}, {'id': 307, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.656Z', 'created_at': '2025-11-05T22:01:40.656Z'}]
*/


select cell_id from cell_metadata where status = 'completed' and test = 'cycle' order by cell_id