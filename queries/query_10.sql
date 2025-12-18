/*
Name: Filters: Max State of Charge
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.177Z
Visualizations: [{'id': 10, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.457Z', 'created_at': '2025-11-05T22:01:34.457Z'}, {'id': 264, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.141Z', 'created_at': '2025-11-05T22:01:40.141Z'}, {'id': 265, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.151Z', 'created_at': '2025-11-05T22:01:40.151Z'}, {'id': 266, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.163Z', 'created_at': '2025-11-05T22:01:40.163Z'}, {'id': 267, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.177Z', 'created_at': '2025-11-05T22:01:40.177Z'}]
*/

select distinct soc_max as a, count(*) from cycle_metadata group by a order by a