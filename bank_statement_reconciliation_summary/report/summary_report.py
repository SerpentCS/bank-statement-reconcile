# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import time
from openerp import api, models


class SummaryReport(models.AbstractModel):
    _name = 'report.bank_statement_reconciliation_summary.summary_report'

    @api.model
    def plus_outstanding_payments(self, journal_record):
        account_id = journal_record.default_credit_account_id and\
            journal_record.default_credit_account_id.clearing_account_id and\
            journal_record.default_credit_account_id.clearing_account_id.id
        account_move_line_records = self.env['account.move.line'].search([
            ('account_id', '=', account_id),
            ('reconcile_id', '=', False),
            ('account_id.reconcile', '=', True),
            ('credit', '>', 0.00)
        ], order='date')
        return account_move_line_records

    @api.model
    def less_outstanding_receipts(self, journal_record):
        account_id = journal_record.default_credit_account_id and\
            journal_record.default_credit_account_id.clearing_account_id and\
            journal_record.default_credit_account_id.clearing_account_id.id
        account_move_line_records = self.env['account.move.line'].search([
            ('account_id', '=', account_id),
            ('reconcile_id', '=', False),
            ('account_id.reconcile', '=', True),
            ('debit', '>', 0.00)
        ], order='date')
        return account_move_line_records

    @api.multi
    def render_html(self, data=None):
        Report = self.env['report']
        report_name = 'bank_statement_reconciliation_summary.summary_report'
        report = Report._get_report_from_name(report_name)
        records = self.env['account.bank.statement'].browse(self.ids)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': report.model,
            'data': data,
            'docs': records,
            'time': time,
            'plus_outstanding_payments': self.plus_outstanding_payments,
            'less_outstanding_receipts': self.less_outstanding_receipts,
        }
        return self.env['report'].render(report_name, docargs)
