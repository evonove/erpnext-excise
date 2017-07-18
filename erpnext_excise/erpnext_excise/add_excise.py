from __future__ import unicode_literals

import frappe

from frappe.model.document import Document
from frappe.utils import cstr, flt


def order_excise(sales_order, method):
    """
    Method called on Sales and Purchase Order's pre_save to add excise tax amount to the item taxes
    """
    tax_amount = 0
    for item_dict in sales_order.get("items"):
        # This is a filter, returns a list, but we expect only
        # one element as we are searching by code
        # XXX: Should errors be handled here, or is this done somewhere else?
        item = frappe.db.sql(
            """
            SELECT excise_applied,excise_value,net_weight
            FROM tabItem
            WHERE item_code="{}"
            """.format(item_dict.item_code), as_dict=1)[0]

        if item.excise_applied == 1:
            # Here is where the excise is applied
            tax_amount += flt(item.excise_value) * flt(item.net_weight) * flt(item_dict.qty)

    if tax_amount > 0:
        company = frappe.db.sql(
            """
            SELECT excise_account,excise_cost_center
            FROM tabCompany
            WHERE name = "{}" """.format(sales_order.get("company")), as_dict=1)[0]

        # If there are already taxes applied to this account_head, add the excise to the existing ones,
        # otherwise create a new entry in the Sales Order manually
        found = 0
        for tax_dict in sales_order.get("taxes"):
            if tax_dict.account_head == company.excise_account and tax_dict.cost_center == company.excise_cost_center:
                found = 1
                if tax_dict.tax_amount != tax_amount:
                    tax_dict.tax_amount = tax_amount
        if found == 0:
            new_tax = sales_order.append("taxes",{})
            new_tax.charge_type = "Actual"
            new_tax.account_head = company.excise_account
            new_tax.cost_center = company.excise_cost_center
            new_tax.description = "Excise"
            new_tax.tax_amount = tax_amount
    sales_order.calculate_taxes_and_totals()
