/*
Name: Filters: NE Active
Data source: 1
Created By: admin
Last Update At: 2025-11-05T22:01:40.930Z
Visualizations: [{'id': 25, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:34.776Z', 'created_at': '2025-11-05T22:01:34.776Z'}, {'id': 328, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.917Z', 'created_at': '2025-11-05T22:01:40.917Z'}, {'id': 329, 'type': 'TABLE', 'name': 'Table', 'description': '', 'options': {}, 'updated_at': '2025-11-05T22:01:40.930Z', 'created_at': '2025-11-05T22:01:40.930Z'}]
*/

select distinct ne_active as a, count(*) from flow_cell_metadata group by a order by a