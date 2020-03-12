# -*- coding: utf-8 -*-


from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class PeopleSoftReport(models.AbstractModel):
	_name = "account.peaplesoft.report"
	_description = "People Soft Report"
	_inherit = "account.report"


	filter_date = {'date_from': '', 'date_to': '', 'filter': 'today'}
	filter_all_entries = False
	filter_journals = False
	filter_analytic = False
	filter_unfold_all = False

	def _get_category(self):
		"""[summary]
		
		Returns:
			[type] -- [description]
		"""
		return [
			{'id':0, 'name': 'Customer Account BCI', 'value': 'customer_bci'},
			{'id':1, 'name': 'Customer Account STRI', 'value': 'customer_stri'},
			{'id':2, 'name': 'STRIFUND', 'value': 'strifund'}
		]


	def _get_templates(self):
		"""[summary]
		
		Returns:
			[type] -- [description]
		"""
		templates = super(PeopleSoftReport, self)._get_templates()
		templates['line_template'] = 'hs_custom_reports.line_template_peoplesoft_report'
		return templates


	def _get_columns_name(self, options):
		"""[summary]
		
		Arguments:
			options {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		return [{'name': ''},
				{'name': _("Ledger")},
				{'name': _("Account")},
				{'name': _("Entry Event")},
				{'name': _("Fund")},
				{'name': _("Dsgc")},
				{'name': _("Budget Ref")},
				{'name': _("Dept ID")},
				{'name': _("Amount"), 'class': 'number'},
				{'name': _("Currency")},
				{'name': _("Reference")},
				{'name': _("Program")},
				{'name': _("Class")},
				{'name': _("Project")},
				{'name': _("Proj Unit")},
				{'name': _("Activity")},
				{'name': _("Analysis")}]

	"""
	def _get_super_columns(self, options):
		return super(PeopleSoftReport, self)._get_super_columns(options)



	def registered_report(self, options, response):
		super_columns = self._get_super_columns(options)
		for column in super_columns.get('columns', []):
			_logger.info(str(column))


	def _do_filter_by_category(self, options):
		pass
	"""

	def _do_filter_by_journal(self, options):
		"""[summary]
		
		Arguments:
			options {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		journals = options['journals']
		if journals == None:
			return '' 

		indices = ''
		for journal in journals:
			journal_id = str(journal['id'])
			if journal_id == 'divider':
				# El primer registro del elemento  no es un diario
				continue

			if journal['selected'] == True:
				temp1 = ',' + journal_id
				temp = journal_id if indices == '' else temp1
				indices = indices + temp
		if indices == '':
			return ''
		return ' AND inv.journal_id in ({}) '.format(indices)



	def _do_filter_by_state(self, options):
		"""[summary]
		
		Arguments:
			options {[type]} -- [description]
		"""
		pass



	def _do_filter_by_documents(self, docs=None):
		"""[summary]
		
		Arguments:
			line_id {[type]} -- [description]
		"""
		if docs == None:
			return ''

		content = ''
		for item in docs:
			temp1 = ',' + str(item)
			temp = str(item) if content == '' else temp1
			content = content + temp
				
		if content == '':
			return ''
			
		return " AND inv.id in ({}) ".format(content)



	def _get_with_statement(self, options, documents=None):
		dt_from = options['date'].get('date_from')
		dt_to = options['date'].get('date_to')
		by_journal = self._do_filter_by_journal(options)
		by_documents = self._do_filter_by_documents(documents)
		sql = """
		WITH people_soft_data AS (
			SELECT(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) 
				THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
				ELSE (SELECT CASE WHEN partner.customer_type = 'fund' 
					THEN CONCAT(partner.stri_fund, ',', partner.stri_budget, ',', partner.stri_desig, ',', partner.stri_dept, ',', partner.stri_account, ',', partner.stri_class, ',', partner.stri_program, ',', partner.stri_project, ',', partner.stri_activity, ',', partner.stri_type)
					ELSE (SELECT CONCAT(a2.stri_fund, ',', a2.stri_budget, ',', a2.stri_desig, ',', a2.stri_dept, ',', a2.stri_account, ',', a2.stri_class, ',', a2.stri_program, ',', a2.stri_project, ',', a2.stri_activity, ',', a2.stri_type) as strifund
						FROM account_account as a2, account_journal as j
						WHERE a2.id = j.default_debit_account_id AND j.id = inv.journal_id LIMIT 1)	
					END)
				END) AS chartfield,
			line.partner_id,
			line.invoice_id as invoice,
			inv.number as reference, 
			(SELECT CASE WHEN inv.type = 'out_invoice' THEN 'invoice' ELSE 'refund' END) AS document,
			(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
			(SELECT (CASE WHEN credit > 0.00 THEN (credit * -1) WHEN debit > 0.00 THEN debit ELSE 0.00 END )) AS amount
			FROM account_move_line AS line, account_invoice AS inv, res_partner AS partner, account_account AS account, account_journal as j
			WHERE (line.date BETWEEN '{}' AND '{}') AND line.invoice_id IS NOT NULL AND line.partner_id = partner.id AND line.invoice_id = inv.id
			AND inv.journal_id = j.id AND line.account_id = account.id AND inv.type in ('out_invoice', 'out_refund') {} {}
			ORDER BY line.invoice_id DESC, line.id DESC)
		SELECT 'ACTUALS' Ledger, 
		split_part(chartfield, ',', 5) AS account,
		CONCAT('REIMB_', (SELECT CASE WHEN split_part(chartfield, ',', 5) = '6998' THEN '6998' ELSE '6999' END)) as entry_event,
		split_part(chartfield, ',', 1) AS fund,
		split_part(chartfield, ',', 3) AS dsgc,
		split_part(chartfield, ',', 2) AS budget_ref,
		split_part(chartfield, ',', 4) AS dept_id,
		ROUND(SUM(amount), 2) as amount,
		'USD' Currency,
		reference,
		split_part(chartfield, ',', 7) AS program,

		(SELECT CASE WHEN split_part(chartfield, ',', 6) != 'CLASSCODE' 
			THEN split_part(chartfield, ',', 6) 
			ELSE (SELECT cc.code FROM class_code AS cc, account_invoice AS ai WHERE ai.id = invoice AND ai.class_code = cc.id)
			END) AS class,

		split_part(chartfield, ',', 8) AS project,
		(SELECT CASE WHEN split_part(chartfield, ',', 8) = '' THEN '' ELSE 'SI000' END) AS proj_unit,
		split_part(chartfield, ',', 9) AS activity,
		split_part(chartfield, ',', 10) AS Analysis
		FROM people_soft_data
		GROUP BY Ledger, account, entry_event, fund, dsgc, budget_ref, dept_id, Currency, reference, program, class, project, proj_unit,activity, Analysis, invoice, sub_order
		ORDER BY invoice DESC, sub_order DESC;
		""".format(dt_from, dt_to, by_journal, by_documents)

		return sql


	def _do_query(self, options, documents=None):
		with_sql = self._get_with_statement(options, documents)
		self.env.cr.execute(with_sql)
		results = self.env.cr.fetchall()
		return results


	@api.model
	def _get_lines(self, options, line_id=None):
		_logger.info("El valor de options es: '" + str(options))
		_logger.info("El valor de line_id es: '" + str(line_id))
		lines = []
		docs = self.env.context['docs'] if 'docs' in self.env.context else None
		invoices = self._do_query(options, docs)
		count = 0
		for invoice in invoices:
			lines.append({
				'id': count,
				'name': count,
				'unfoldable': False,
				'level': 3,
				'columns': [{'name' : v} for v in invoice],
			})
			count+=1

		if len(invoices) == 0:
			lines.append({
				'id': '',
				'name': '',
				'unfoldable': False,
				'level': 3,
				'columns': [{'name' : v} for v in ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]],
			})
		
		return lines


	@api.model
	def _get_report_name(self):
		return _('People Soft')


	def _get_reports_buttons(self):
		buttons = super(PeopleSoftReport, self)._get_reports_buttons()
		buttons.append({'name': _('publish'), 'action': 'publish_report'})
		return buttons