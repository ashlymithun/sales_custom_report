{
    'name': 'Sales Reports',
    'version': '1.0',
    'category': 'uncategorized',
    'summary': 'Sales_reports',
    'description': """
This module contains all the reports of  sales.
    """,
    'depends': ['base','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'wizards/sales_summary_report_wizard.xml',
        'reports/sales_invoice_reports.xml',
        'wizards/daywise_invoice_report_wizard.xml',
        'reports/daywise_invoice_report.xml',
        'reports/monthwise_invoice_report.xml',
        'reports/daywise_summary_report.xml',
        'reports/monthwise_summary_report.xml',
        
    ],

    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'sequence': '2',
}
# this is a report of sale invoice withe account_move module.it is just an whole month report.in daywise
