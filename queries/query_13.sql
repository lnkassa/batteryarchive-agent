/*
Name: Filters: Form Factor
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.027Z
Visualizations: [{'id': 13, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.520Z', 'created_at': '2025-11-05T22:01:34.520Z'}, {'id': 252, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:39.991Z', 'created_at': '2025-11-05T22:01:39.991Z'}, {'id': 253, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.002Z', 'created_at': '2025-11-05T22:01:40.002Z'}, {'id': 254, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.015Z', 'created_at': '2025-11-05T22:01:40.015Z'}, {'id': 255, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.027Z', 'created_at': '2025-11-05T22:01:40.027Z'}]
*/

select distinct form_factor as a, count(*) from cell_metadata group by a order by a