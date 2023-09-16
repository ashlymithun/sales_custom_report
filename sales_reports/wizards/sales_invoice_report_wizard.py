from odoo import fields, models


class SalesSummaryReport(models.TransientModel):
    _name = "sales.summary.wizard"
    _description = "Sales Invoice Report"

    from_date = fields.Date(string="Start Date")
    to_date = fields.Date(string="End Date")

    def get_report(self):
        domain = []
        sales = []
        if self.from_date:
            domain += [('invoice_date', '>=', self.from_date)]
        if self.to_date:
            domain += [('invoice_date', '<=', self.to_date)]
        invoices = self.env['account.move'].search(domain)
        print("result", invoices)
        for invoice in invoices.filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'out_invoice'):
            if invoice.name not in sales:
                sales.append(
                    {
                        'invoice_no': invoice.name,
                        'invoice_date': invoice.invoice_date,
                        'customer': invoice.partner_id.display_name,
                        'taxable_amount': invoice.amount_untaxed,
                        'taxes': invoice.amount_tax,
                        'net_amount':invoice.amount_total,
                    }
                )
        currency = self.env.user.company_id.currency_id.symbol
        data = {
            'sales': sales,
            'currency': currency,
        }
        return self.env.ref('sales_reports.sales_invoice_report_action').report_action(self, data=data)

