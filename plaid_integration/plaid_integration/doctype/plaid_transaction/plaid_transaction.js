// Copyright (c) 2018, Drivedgevd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Plaid Transaction", {
	refresh: function(frm) {
		frm.add_custom_button("Journal Entry", function() {
			var doc = frappe.model.get_new_doc("Journal Entry");
			doc.posting_date = frm.doc.date
			doc.voucher_type = "Journal Entry"
			doc.naming_series = "JV-"
			doc.cheque_no = frm.doc.name
			doc.company = frappe.defaults.get_default('company')
			var row = frappe.model.add_child(doc, "Journal Entry Account", "accounts");
			if (frm.doc.amount < 0)
				row.debit_in_account_currency = frm.doc.amount
			else
				row.credit_in_account_currency = frm.doc.amount
			frappe.set_route("Form", doc.doctype, doc.name);
		})
	}
});