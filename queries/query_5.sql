/*
Name: Filters: Anode
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.419Z
Visualizations: [{'id': 5, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.350Z', 'created_at': '2025-11-05T22:01:34.350Z'}, {'id': 284, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.385Z', 'created_at': '2025-11-05T22:01:40.385Z'}, {'id': 285, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.397Z', 'created_at': '2025-11-05T22:01:40.397Z'}, {'id': 286, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.408Z', 'created_at': '2025-11-05T22:01:40.408Z'}, {'id': 287, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.419Z', 'created_at': '2025-11-05T22:01:40.419Z'}]
*/

select distinct anode as a, count(*) from cell_metadata group by a order by a