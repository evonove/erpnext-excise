frappe.ui.form.on("Sales Order", "taxes_and_charges", function(frm) {
  frappe.call({
    method: "erpnext_excise.erpnext_excise.add_excise.sales_order_excise",
    args: {
      sales_order: cur_frm.doc
    },
    callback: function(r) {
      if (typeof r.message !== "undefined") {
        var excise = cur_frm.add_child("taxes", {});
        excise.charge_type = r.message.charge_type;
        excise.description = r.message.description;
        excise.tax_amount = r.message.tax_amount;
        excise.account_head = r.message.excise_account;
        excise.cost_center = r.message.excise_cost_center;
        cur_frm.cscript.calculate_taxes_and_totals();
        cur_frm.refresh_field("taxes");
      }
    }
  });
});
