from __future__ import unicode_literals

import frappe

from frappe.utils import cstr, flt


def get_tax_amount(order):
    """
    Method to get the amount of the excise to be added
    """
    amount = 0
    for item_dict in order.get("items"):
        # This is a filter, returns a list, but we expect only
        # one element as we are searching by code
        # XXX: errors ignored here as they are handled by the framework
        item = frappe.db.sql(
            """
            SELECT excise_applied,excise_value,excise_weight
            FROM tabItem
            WHERE item_code="{}"
            """.format(item_dict.item_code), as_dict=1)[0]

        if item.excise_applied == 1:
            # Here is where the excise is applied
            amount += flt(item.excise_value) * flt(item.excise_weight) * flt(item_dict.qty)
    return amount


def tax_already_applied(order, excise_account, excise_cost_center):
    """
    If there are already taxes applied to this account_head, add the excise to the existing ones,
    otherwise create a new entry in the Sales Order manually
    """
    for tax_dict in order.get("taxes"):
        if tax_dict.account_head == company.excise_account and tax_dict.cost_center == company.excise_cost_center:
            if tax_dict.tax_amount != tax_amount:
                tax_dict.tax_amount = tax_amount
            return True


def sales_order_excise(sales_order, method):
    """
    Method called on Sales Order's pre_save to add excise tax amount to the item taxes
    """
    tax_amount = get_tax_amount(sales_order)

    if tax_amount > 0:
        company = frappe.db.sql(
            """
            SELECT excise_account,excise_cost_center
            FROM tabCompany
            WHERE name = "{}" """.format(sales_order.get("company")), as_dict=1)[0]
        if not tax_already_applied(sales_order, company.excise_account, company.excise_cost_center):
            new_tax = sales_order.append("taxes",{})
            new_tax.charge_type = "Actual"
            new_tax.account_head = company.excise_account
            new_tax.cost_center = company.excise_cost_center
            new_tax.description = "Excise"
            new_tax.tax_amount = tax_amount

    sales_order.calculate_taxes_and_totals()


def purchase_order_excise(purchase_order, method):
    """
    Method called on Purchase Order's pre_save to add excise tax amount to the item taxes
    """
    tax_amount = get_tax_amount(purchase_order)

    if tax_amount > 0:
        company = frappe.db.sql(
            """
            SELECT excise_account,excise_cost_center
            FROM tabCompany
            WHERE name = "{}" """.format(purchase_order.get("company")), as_dict=1)[0]

        if not tax_already_applied(sales_order, company.excise_account, company.excise_cost_center):
            new_tax = purchase_order.append("taxes",{})
            new_tax.charge_type = "Actual"
            new_tax.account_head = company.excise_account
            new_tax.cost_center = company.excise_cost_center
            new_tax.description = "Excise"
            new_tax.tax_amount = tax_amount
            new_tax.category = "Valuation and Total"
            new_tax.add_deduct_tax = "Add"
    purchase_order.calculate_taxes_and_totals()
