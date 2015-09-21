from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr
from frappe import msgprint, _
import frappe.defaults


class Controller_monthly(objects):
    def __init__(self, doc):
		self.doc = doc
		self.calculate()

    def _calculate(self):
		self.calculate_item_values()
		self.initialize_taxes()
		self.determine_exclusive_rate()
		self.calculate_net_total()
		self.calculate_taxes()
		self.manipulate_grand_total_for_inclusive_tax()
		self.calculate_totals()
		self._cleanup()
	def calculate(self):
		self.discount_amount_applied = False
		self._calculate()

		if self.doc.meta.get_field("loan_amount"):
			self.apply_discount_amount()

		if self.doc.doctype in ["Sales Invoice", "Purchase Invoice"]:
			self.calculate_total_advance()

	def calculate_item_values(self):
		if not self.discount_amount_applied:
			for item in self.doc.get("items"):
				self.doc.round_floats_in(item)

				if item.discount_percentage == 100:
					item.rate = 0.0
				elif not item.rate:
					item.rate = flt(item.price_list_rate *
						(1.0 - (item.discount_percentage / 100.0)), item.precision("rate"))

				item.net_rate = item.rate
				item.amount = flt(item.rate * item.qty,	item.precision("amount"))
				item.net_amount = item.amount

				self._set_in_company_currency(item, ["price_list_rate", "rate", "net_rate", "amount", "net_amount"])

				item.item_tax_
    def calculate_net_total(self):
		self.doc.total = self.doc.base_total = self.doc.net_total = self.doc.base_net_total = 0.0

		for item in self.doc.get("items"):
			self.doc.total += item.amount
			self.doc.base_total += item.base_amount
			self.doc.net_total += item.net_amount
			self.doc.base_net_total += item.base_net_amount

		