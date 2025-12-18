/*
Name: Filters: Min State of Charge
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.128Z
Visualizations: [{'id': 11, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.479Z', 'created_at': '2025-11-05T22:01:34.479Z'}, {'id': 260, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.089Z', 'created_at': '2025-11-05T22:01:40.089Z'}, {'id': 261, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.103Z', 'created_at': '2025-11-05T22:01:40.103Z'}, {'id': 262, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.116Z', 'created_at': '2025-11-05T22:01:40.116Z'}, {'id': 263, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.128Z', 'created_at': '2025-11-05T22:01:40.128Z'}]
*/

select distinct soc_min as a, count(*) from cycle_metadata group by a order by a