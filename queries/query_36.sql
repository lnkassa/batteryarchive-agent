/*
Name: Filters: Source abuse test
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:36.363Z
Visualizations: [{'id': 36, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.009Z', 'created_at': '2025-11-05T22:01:35.009Z'}, {'id': 97, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.325Z', 'created_at': '2025-11-05T22:01:36.325Z'}, {'id': 98, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.337Z', 'created_at': '2025-11-05T22:01:36.337Z'}, {'id': 99, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.351Z', 'created_at': '2025-11-05T22:01:36.351Z'}, {'id': 100, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.363Z', 'created_at': '2025-11-05T22:01:36.363Z'}]
*/

select distinct source as a, count(*) from cell_metadata where test = 'abuse' group by a order by a 