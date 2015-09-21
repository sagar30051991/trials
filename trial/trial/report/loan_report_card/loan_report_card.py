# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import get_columns,get_data

def execute(filters=None):
	if not filters: filters ={}
	data = []
	conditions = get_columns(filters, "Loan Installment")
	data = get_data(filters, conditions)

	return conditions["columns"], data
	
def get_columns(filters, trans):
	validate_filters(filters)

	# get conditions for based_on filter cond
	based_on_details = based_wise_columns_query(filters.get("based_on"), trans)
	# get conditions for periodic filter cond
	period_cols, period_select = period_wise_columns_query(filters, trans)
	# get conditions for grouping filter cond
	group_by_cols = group_wise_column(filters.get("group_by"))

	columns = based_on_details["based_on_cols"] + period_cols + [_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]
	if group_by_cols:
		columns = based_on_details["based_on_cols"] + group_by_cols + period_cols + \
			[_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]

	conditions = {"based_on_select": based_on_details["based_on_select"], "period_wise_select": period_select,
		"columns": columns, "group_by": based_on_details["based_on_group_by"], "grbc": group_by_cols, "trans": trans,
		"addl_tables": based_on_details["addl_tables"], "addl_tables_relational_cond": based_on_details.get("addl_tables_relational_cond", "")}

	return conditions