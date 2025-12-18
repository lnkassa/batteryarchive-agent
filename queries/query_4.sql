/*
Name: Filters: Cathode cycle test
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.465Z
Visualizations: [{'id': 4, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.328Z', 'created_at': '2025-11-05T22:01:34.328Z'}, {'id': 288, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.431Z', 'created_at': '2025-11-05T22:01:40.431Z'}, {'id': 289, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.441Z', 'created_at': '2025-11-05T22:01:40.441Z'}, {'id': 290, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.454Z', 'created_at': '2025-11-05T22:01:40.454Z'}, {'id': 291, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.465Z', 'created_at': '2025-11-05T22:01:40.465Z'}]
*/

select distinct cathode as a, count(*) from cell_metadata where test = 'cycle' group by a order by a