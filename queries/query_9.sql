/*
Name: Filters: C Discharge Rate
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.227Z
Visualizations: [{'id': 9, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.436Z', 'created_at': '2025-11-05T22:01:34.436Z'}, {'id': 268, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.191Z', 'created_at': '2025-11-05T22:01:40.191Z'}, {'id': 269, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.203Z', 'created_at': '2025-11-05T22:01:40.203Z'}, {'id': 270, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.215Z', 'created_at': '2025-11-05T22:01:40.215Z'}, {'id': 271, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.227Z', 'created_at': '2025-11-05T22:01:40.227Z'}]
*/

select distinct crate_d as a, count(*) from cycle_metadata group by a order by a