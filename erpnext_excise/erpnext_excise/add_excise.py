from __future__ import unicode_literals

import frappe
import frappe.utils

from frappe.model.document import Document
from frappe.utils import cstr, flt


def sales_order_excise(sales_order,method):
	tax = 0
	for d in sales_order.get("items"):
		item = frappe.db.sql("""select excise_applied,excise_value,excise_weight from tabItem where item_code="{}" """.format(d.item_code), as_dict=1)
		if item[0].excise_applied == 1:
			tax += (flt(item[0].excise_value) * flt(item[0].excise_weight) * flt(d.qty))
	if tax > 0:
		company = frappe.db.sql("""select excise_account,excise_cost_center from tabCompany where name = "{}" """.format(sales_order.get("company")), as_dict=1)
		found = 0
		for td in sales_order.get("taxes"):
			if td.account_head == company[0].excise_account and td.cost_center == company[0].excise_cost_center:
				found = 1
				if td.tax_amount != tax:
					td.tax_amount = tax
		if found == 0:
			new_tax = sales_order.append("taxes",{})
			new_tax.charge_type = "Actual"
			new_tax.account_head = company[0].excise_account
			new_tax.cost_center = company[0].excise_cost_center
			new_tax.description = "Excise"
			new_tax.tax_amount = tax
	sales_order.calculate_taxes_and_totals()
