/*
Name: Filters: Number of Cycles
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.070Z
Visualizations: [{'id': 46, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.222Z', 'created_at': '2025-11-05T22:01:35.222Z'}, {'id': 138, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.035Z', 'created_at': '2025-11-05T22:01:37.035Z'}, {'id': 139, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.047Z', 'created_at': '2025-11-05T22:01:37.047Z'}, {'id': 140, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.058Z', 'created_at': '2025-11-05T22:01:37.058Z'}, {'id': 141, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.070Z', 'created_at': '2025-11-05T22:01:37.070Z'}]
*/

select distinct cycle_index from cycle_stats where cycle_index%10 = 0 order by cycle_index