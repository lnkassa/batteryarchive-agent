/*
Name: Filters: Membrane Size
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.953Z
Visualizations: [{'id': 24, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.751Z', 'created_at': '2025-11-05T22:01:34.751Z'}, {'id': 330, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.942Z', 'created_at': '2025-11-05T22:01:40.942Z'}, {'id': 331, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.953Z', 'created_at': '2025-11-05T22:01:40.953Z'}]
*/

select distinct membrane_size as a, count(*) from flow_cell_metadata group by a order by a