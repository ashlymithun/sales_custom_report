from odoo import fields, models


class SalesSummaryReport(models.TransientModel):
    _name = "sale.invoice.wizard"
    _description = "Sales Invoice Report"

    from_date = fields.Date(string="Start Date:")
    to_date = fields.Date(string="End Date:")
    # check box
    show_daywise_report = fields.Boolean(string='Daywise Report:')
    show_monthwise_report = fields.Boolean(string='Monthwise Report:')
    daywise_summary_report = fields.Boolean(string='Daywise Summary Report:')
    monthwise_summary_report = fields.Boolean(string='Monthwise Summary Report:')
    show_report = fields.Boolean(string='Summary Report:')
    # radio button
    # option = fields.Selection(
    #     [('sales', 'Sales Invoice'), ('daywise', 'Day Wise'),('monthwise', 'Month Wise')],
    #     string='Select a Report',
    #     required=True
    # )

    def get_report(self):
        domain = []
        record = []
        if self.from_date:
            domain += [('invoice_date', '>=', self.from_date)]
        if self.to_date:
            domain += [('invoice_date', '<=', self.to_date)]
        record.append(self.from_date)
        record.append(self.to_date)
        print("record", record)
        invoices = self.env['account.move'].search(domain)
        dates = {}  # Dictionary to hold invoice dates
        sales = []  # List to hold sales data for each invoice date
        for invoice in invoices.filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'out_invoice'):
            invoice_date = invoice.invoice_date
            if invoice_date not in dates:
                dates[invoice_date] = {
                    'id': invoice.id,
                    'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
                    'taxable_amount_total': 0.0,
                    'tax_total': 0.0,
                    'net_amount_total': 0.0,
                }
            dates[invoice_date]['taxable_amount_total'] += invoice.amount_untaxed
            dates[invoice_date]['tax_total'] += invoice.amount_tax
            dates[invoice_date]['net_amount_total'] += invoice.amount_total

            sales.append(
                {
                    'invoice_no': invoice.name,
                    'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
                    'customer': invoice.partner_id.display_name,
                    'taxable_amount': invoice.amount_untaxed,
                    'taxes': invoice.amount_tax,
                    'net_amount': invoice.amount_total,
                }
            )

        currency = self.env.user.company_id.currency_id.symbol
        sorted_sales = sorted(sales, key=lambda x: x['invoice_date'])

        data = {
            'dates': list(dates.values()),  # Convert dictionary values to a list
            'sales': sorted_sales,
            'currency': currency,
            'record': record,
        }
        # check box wise report
        if self.show_daywise_report:
            report_name = 'sales_reports.daywise_invoice_report_action'
        elif self.show_monthwise_report:
            report_name = 'sales_reports.month_wise_invoice_report_action'
        elif self.daywise_summary_report:
            report_name = 'sales_reports.daywise_summary_report_action'
        elif self.monthwise_summary_report:
            report_name = 'sales_reports.month_wise_summary_report_action'
        elif self.show_report:
            report_name = 'sales_reports.sale_report_action'
        else:
            report_name = 'sales_reports.sales_invoice_report_action'

        # if self.option == 'sales':
        #     report_name = 'sales_reports.sales_invoice_report_action'
        # elif self.option == 'daywise':
        #     report_name = 'sales_reports.daywise_invoice_report_action'
        # else:
        #     report_name = 'sales_reports.month_wise_invoice_report_action'
        return self.env.ref(report_name).report_action(self, data=data)


