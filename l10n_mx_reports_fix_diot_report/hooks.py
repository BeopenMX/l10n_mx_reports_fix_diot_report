# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_load():
    can_patch = True
    try:
        from odoo.addons.l10n_mx_reports.models.account_diot import MxReportPartnerLedger
    except ImportError:
        can_patch = False

    def _do_query_group_by_account(self, options, line_id):
        select = ',\"account_move_line_account_tax_rel\".account_tax_id, SUM(\"account_move_line\".debit - \"account_move_line\".credit)'  # noqa
        sql = "SELECT \"account_move_line\".partner_id%s FROM %s WHERE %s%s AND \"account_move_line_account_tax_rel\".account_move_line_id = \"account_move_line\".id GROUP BY \"account_move_line\".partner_id, \"account_move_line_account_tax_rel\".account_tax_id"  # noqa
        journal_ids = []
        for company in self.env.companies.filtered('tax_cash_basis_journal_id'):
            journal_ids.append(company.tax_cash_basis_journal_id.id)
        tax_ids = self.env['account.tax'].with_context(active_test=False).search([
            ('type_tax_use', '=', 'purchase'),
            ('tax_exigibility', '=', 'on_payment')])
        account_tax_ids = tax_ids.mapped('invoice_repartition_line_ids.account_id')
        domain = [
            ('journal_id', 'in', journal_ids),
            ('account_id', 'not in', account_tax_ids.ids),
            ('tax_ids', 'in', tax_ids.ids),
            ('date', '>=', options['date']['date_from']),
            ('date', '<=', options['date']['date_to']),
            ('move_id.state', '=', 'posted'),
        ]

        test = 1
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get(domain)
        tables += ',"account_move_line_account_tax_rel"'
        line_clause = line_id and\
            ' AND \"account_move_line\".partner_id = ' + str(line_id) or ''
        query = sql % (select, tables, where_clause, line_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        result = {}
        for res in results:
            result.setdefault(res[0], {}).setdefault(res[1], res[2])
        return result

    if can_patch:
        MxReportPartnerLedger._do_query_group_by_account = _do_query_group_by_account
