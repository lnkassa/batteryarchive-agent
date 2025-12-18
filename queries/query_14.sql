/*
Name: Filters: SOC
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.557Z
Visualizations: [{'id': 14, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.542Z', 'created_at': '2025-11-05T22:01:34.542Z'}, {'id': 296, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.523Z', 'created_at': '2025-11-05T22:01:40.523Z'}, {'id': 297, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.535Z', 'created_at': '2025-11-05T22:01:40.535Z'}, {'id': 298, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.547Z', 'created_at': '2025-11-05T22:01:40.547Z'}, {'id': 299, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.557Z', 'created_at': '2025-11-05T22:01:40.557Z'}]
*/

select distinct soc as a, count(*) from abuse_metadata group by a order by a