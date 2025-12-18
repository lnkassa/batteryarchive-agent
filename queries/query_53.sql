/*
Name: Filters: Nail speed
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.522Z
Visualizations: [{'id': 53, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.368Z', 'created_at': '2025-11-05T22:01:35.368Z'}, {'id': 170, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.497Z', 'created_at': '2025-11-05T22:01:37.497Z'}, {'id': 171, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.509Z', 'created_at': '2025-11-05T22:01:37.509Z'}, {'id': 172, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.522Z', 'created_at': '2025-11-05T22:01:37.522Z'}, {'id': 169, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.485Z', 'created_at': '2025-11-05T22:01:37.485Z'}]
*/

select distinct nail_speed as a, count(*) from abuse_metadata group by a order by a