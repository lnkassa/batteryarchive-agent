/*
Name: Disruptive Test DD
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.607Z
Visualizations: [{'id': 3, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.307Z', 'created_at': '2025-11-05T22:01:34.307Z'}, {'id': 300, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.570Z', 'created_at': '2025-11-05T22:01:40.570Z'}, {'id': 301, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.582Z', 'created_at': '2025-11-05T22:01:40.582Z'}, {'id': 302, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.595Z', 'created_at': '2025-11-05T22:01:40.595Z'}, {'id': 303, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.607Z', 'created_at': '2025-11-05T22:01:40.607Z'}]
*/


select cell_id from cell_metadata where test = 'abuse' and status ='completed' order by cell_id