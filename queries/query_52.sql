/*
Name: Filters: Initial Voltage
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:37.473Z
Visualizations: [{'id': 52, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:35.347Z', 'created_at': '2025-11-05T22:01:35.347Z'}, {'id': 165, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.438Z', 'created_at': '2025-11-05T22:01:37.438Z'}, {'id': 166, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.450Z', 'created_at': '2025-11-05T22:01:37.450Z'}, {'id': 167, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.460Z', 'created_at': '2025-11-05T22:01:37.460Z'}, {'id': 168, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:37.473Z', 'created_at': '2025-11-05T22:01:37.473Z'}]
*/

select distinct v_init as a, count(*) from abuse_metadata group by a order by a