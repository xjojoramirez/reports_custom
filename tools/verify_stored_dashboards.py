import base64
import json

for d in env['spreadsheet.dashboard'].browse([7, 8, 9]):
    data = json.loads(base64.b64decode(d.spreadsheet_binary_data))
    sh = data['sheets'][0]
    print('dashboard', d.id, d.name,
          '| figures:', type(sh['figures']).__name__,
          '| headerGroups:', type(sh['headerGroups']).__name__,
          '| cells:', len(sh['cells']),
          '| pivots:', sorted(data['pivots']))
