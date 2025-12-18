/*
Name: Filters: Indentor
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.572Z
Visualizations: [{'id': 54, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.389Z', 'created_at': '2025-11-05T22:01:35.389Z'}, {'id': 173, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.535Z', 'created_at': '2025-11-05T22:01:37.535Z'}, {'id': 174, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.546Z', 'created_at': '2025-11-05T22:01:37.546Z'}, {'id': 175, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.559Z', 'created_at': '2025-11-05T22:01:37.559Z'}, {'id': 176, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.572Z', 'created_at': '2025-11-05T22:01:37.572Z'}]
*/

select distinct indentor as a, count(*) from abuse_metadata group by a order by a