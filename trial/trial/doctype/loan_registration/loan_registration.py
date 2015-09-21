# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cstr, flt, getdate, comma_and

class LoamonthlynRegistration(Document):
	pass

	def validate(self):
		self.validate_lamt()
		

	def validate_lamt(self):
		if self.loan_amount:
			try:
				val = int(self.loan_amount)
				pass
			except ValueError:
				frappe.throw(_("Enter Number Only "))
	

	def on_update(self):
		d = frappe.get_doc("Monthly Installment",)
		d = frappe.new_doc("")
		d.loan_amounts = self.amount
		d.save()

		