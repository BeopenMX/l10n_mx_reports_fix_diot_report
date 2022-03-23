# Copyright 2022 Munin
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'L10n Mx Reports Fix Diot Report',
    'description': """
        Fix the https://github.com/odoo/enterprise/pull/20110/commits/a875c5c01f089e3bd1a81d9c225f661d2c7e4055 commit""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Munin',
    'depends': [
        'l10n_mx_reports'
    ],
    'data': [
    ],
    'demo': [
    ],
    'post_load': 'post_load',
}
