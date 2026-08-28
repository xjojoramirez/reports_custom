{
    'name': 'Reports Custom',
    'version': '18.0.1.0.0',
    'category': 'Custom',
    'summary': 'Management report dashboards: sales, profit, vendor spend, customers, past due, dormant items',
    'description': """
Reports Custom
==============

Adds a "Management Reports" group to the Dashboards app with live report
dashboards:

* Sales by item, customer, and product category.
* Profit by item, customer, and product category.
* Vendor spend by vendor, item, and category.
* Customer lists by salesperson, area, and name.
* Past due accounts with aging buckets.
* Dormant items with 30/60/90/180 day presets.
""",
    'depends': ['spreadsheet_dashboard', 'sale', 'account'],
    'data': [
        'data/dashboard_group.xml',
        'data/dashboards.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
