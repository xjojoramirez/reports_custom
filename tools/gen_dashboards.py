import json
from pathlib import Path

SAMPLE = '/usr/lib/python3/dist-packages/odoo/addons/spreadsheet_dashboard_sale/data/files/product_dashboard.json'
OUT_DIR = Path('/mnt/custom_addons/reports_custom/data/files')
DATE_FILTER_ID = 'f1a2b3c4-1111-4222-8333-444444444444'

DOMAIN = [["state", "not in", ["draft", "sent", "cancel"]]]


def base_spreadsheet():
    with open(SAMPLE) as f:
        sample = json.load(f)
    return {
        'version': 21,
        'sheets': [],
        'styles': {
            '1': {'bold': True, 'fontSize': 16, 'textColor': '#01666b'},
            '2': {'bold': True, 'fontSize': 11, 'textColor': '#434343'},
            '3': {'bold': True},
        },
        'formats': {},
        'borders': {},
        'revisionId': 'START_REVISION',
        'uniqueFigureIds': True,
        'settings': sample.get('settings', {}),
        'pivots': {},
        'pivotNextId': 2,
        'customTableStyles': {},
        'odooVersion': 12,
        'globalFilters': [
            {
                'id': DATE_FILTER_ID,
                'type': 'date',
                'label': 'Period',
                'defaultValue': 'this_month',
                'rangeType': 'relative',
            },
        ],
        'lists': {},
        'listNextId': 1,
        'chartOdooMenusReferences': {},
    }


def make_pivot(dim_field, name):
    return {
        'type': 'ODOO',
        'context': {'group_by': []},
        'domain': DOMAIN,
        'id': '1',
        'measures': [
            {'id': 'product_uom_qty', 'fieldName': 'product_uom_qty'},
            {'id': 'price_subtotal', 'fieldName': 'price_subtotal'},
        ],
        'model': 'sale.report',
        'name': name,
        'sortedColumn': {
            'groupId': [[], []],
            'measure': 'price_subtotal',
            'order': 'desc',
        },
        'formulaId': '1',
        'columns': [],
        'rows': [{'fieldName': dim_field}],
        'fieldMatching': {
            DATE_FILTER_ID: {'chain': 'date', 'type': 'datetime'},
        },
    }


def cell(content):
    return {'content': content}


def make_sheet(title, dim_field, dim_label, pivot_name):
    cells = {}
    cells['A1'] = cell(title)
    cells['A3'] = cell(f'={dim_label}')
    cells['B3'] = cell('=_t("Qty Ordered")')
    cells['C3'] = cell('=_t("Untaxed Total")')
    for n in range(1, 11):
        row = n + 3
        cells[f'A{row}'] = cell(f'=PIVOT.HEADER(1,"#{dim_field}",{n})')
        cells[f'B{row}'] = cell(
            f'=PIVOT.VALUE(1,"product_uom_qty","#{dim_field}",{n})'
        )
        cells[f'C{row}'] = cell(
            f'=PIVOT.VALUE(1,"price_subtotal","#{dim_field}",{n})'
        )
    cells['A15'] = cell('=_t("Total")')
    cells['B15'] = cell('=PIVOT.VALUE(1,"product_uom_qty")')
    cells['C15'] = cell('=PIVOT.VALUE(1,"price_subtotal")')
    return {
        'id': 'sheet1',
        'name': 'Dashboard',
        'colNumber': 10,
        'rowNumber': 20,
        'rows': {},
        'cols': {},
        'merges': [],
        'cells': cells,
        'styles': {'A1': 1, 'A3:C3': 2, 'A15:C15': 3},
        'formats': {},
        'borders': {},
        'conditionalFormats': [],
        'figures': [],
        'tables': [],
        'areGridLinesVisible': False,
        'isVisible': True,
        'headerGroups': {},
        'dataValidationRules': [],
        'comments': {},
    }


def build_dashboard(title, dim_field, dim_label, pivot_name):
    data = base_spreadsheet()
    data['pivots']['1'] = make_pivot(dim_field, pivot_name)
    data['sheets'] = [make_sheet(title, dim_field, dim_label, pivot_name)]
    return data


DASHBOARDS = [
    ('Sales by Item', 'product_id', '_t("Item")', 'Sales Analysis by Item', 'sales_by_item.json'),
    ('Sales by Customer', 'partner_id', '_t("Customer")', 'Sales Analysis by Customer', 'sales_by_customer.json'),
    ('Sales by Category', 'categ_id', '_t("Category")', 'Sales Analysis by Category', 'sales_by_category.json'),
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for title, dim, label, pivot_name, filename in DASHBOARDS:
        data = build_dashboard(title, dim, label, pivot_name)
        path = OUT_DIR / filename
        with open(path, 'w') as f:
            json.dump(data, f, indent=1)
        print('wrote', path)


if __name__ == '__main__':
    main()
