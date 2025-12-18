/*
Name: Filters: Abuse Cells Nominal Capacity (Ah)
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:36.456Z
Visualizations: [{'id': 38, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.052Z', 'created_at': '2025-11-05T22:01:35.052Z'}, {'id': 105, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.421Z', 'created_at': '2025-11-05T22:01:36.421Z'}, {'id': 106, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.433Z', 'created_at': '2025-11-05T22:01:36.433Z'}, {'id': 107, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.444Z', 'created_at': '2025-11-05T22:01:36.444Z'}, {'id': 108, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:36.456Z', 'created_at': '2025-11-05T22:01:36.456Z'}]
*/

select distinct ah as a, count(*) from cell_metadata where test = 'abuse' group by a order by a