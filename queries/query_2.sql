/*
Name: Validate Cycle Test DD
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:39.980Z
Visualizations: [{'id': 2, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.285Z', 'created_at': '2025-11-05T22:01:34.285Z'}, {'id': 248, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.945Z', 'created_at': '2025-11-05T22:01:39.945Z'}, {'id': 249, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.957Z', 'created_at': '2025-11-05T22:01:39.957Z'}, {'id': 250, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.968Z', 'created_at': '2025-11-05T22:01:39.968Z'}, {'id': 251, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.980Z', 'created_at': '2025-11-05T22:01:39.980Z'}]
*/


select cell_id from cell_metadata where status = 'validate' and test = 'cycle' order by cell_id