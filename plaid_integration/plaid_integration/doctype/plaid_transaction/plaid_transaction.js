// Copyright (c) 2018, Drivedgevd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Plaid Transaction", {
	refresh: function(frm) {
		frm.add_custom_button("Journal Entry", function() {
			console.log(frm.doc.category_id)

			console.log(frm.doc.account_id)
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Plaid Category Account Mapping",
					filters: [
						["plaid_category_id", "=", frm.doc.category_id],
					],
					fields: ["account"]
				},
				callback: function(r) {
					if (r.message) {
						console.log(r.message)
					}
				}
			})

			linked_category_account=frappe.model.get_list('Plaid Category Account Mapping',filters={'plaid_category_id':frm.doc.category_id}, fields=['name','account'])
			linked_bank_account=frappe.model.get_list('Plaid Bank Account Mapping',filters={'plaid_account_id':frm.doc.account_id}, fields=['bank_account'])

			console.log(linked_category_account)
			console.log(linked_bank_account)

			var doc = frappe.model.get_new_doc("Journal Entry");
			doc.posting_date = frm.doc.date
			doc.voucher_type = "Journal Entry"
			doc.naming_series = "JV-"
			doc.cheque_no = frm.doc.name
			doc.company = frappe.defaults.get_default('company')
			var row = frappe.model.add_child(doc, "Journal Entry Account", "accounts");
			row.account=linked_category_account[0]
			if (frm.doc.amount < 0)
				row.debit_in_account_currency = frm.doc.amount
			else
				row.credit_in_account_currency = frm.doc.amount
			
			var row = frappe.model.add_child(doc, "Journal Entry Account", "accounts");
			row.account=linked_bank_account[0]
			if (frm.doc.amount < 0)
				row.debit_in_account_currency = frm.doc.amount
			else
				row.credit_in_account_currency = frm.doc.amount
				
				
			frappe.set_route("Form", doc.doctype, doc.name);
		})
	}
});