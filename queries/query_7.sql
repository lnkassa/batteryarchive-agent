/*
Name: Filters: Temperature
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.327Z
Visualizations: [{'id': 7, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.393Z', 'created_at': '2025-11-05T22:01:34.393Z'}, {'id': 276, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.291Z', 'created_at': '2025-11-05T22:01:40.291Z'}, {'id': 277, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.303Z', 'created_at': '2025-11-05T22:01:40.303Z'}, {'id': 278, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.315Z', 'created_at': '2025-11-05T22:01:40.315Z'}, {'id': 279, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.327Z', 'created_at': '2025-11-05T22:01:40.327Z'}]
*/

select distinct temperature as a, count(*) from cycle_metadata group by a order by a