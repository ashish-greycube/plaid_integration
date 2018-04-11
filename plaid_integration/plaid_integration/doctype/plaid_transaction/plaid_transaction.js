// Copyright (c) 2018, Drivedgevd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Plaid Transaction", {

	refresh: function (frm) {
		frm.add_custom_button("Journal Entry", function () {

			let category = new Promise(resolve => {
				console.log(frm.doc.category_id)
			if (frm.doc.category_id!=undefined)	{
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Plaid Category Account Mapping",
						filters: [
							["plaid_category_id", "=", frm.doc.category_id],
						],
						fields: ["account"]
					}
				}).then((r) => {
					if (r.message) {						
					}
					resolve(r.message[0].account);
				});}
			});

			let bank = new Promise(resolve => {
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Plaid Bank Account Mapping",
						filters: [
							["plaid_account_id", "=", frm.doc.account_id],
						],
						fields: ["bank_account"]
					}
				}).then((r) => {
					if (r.message) {						
					}
					resolve(r.message[0].bank_account);
				});
			});


			Promise.all([category, bank]).then((r) => {
				linked_category_account = r[0]
				linked_bank_account = r[1]
			
				var doc = frappe.model.get_new_doc("Journal Entry");
				doc.posting_date = frm.doc.date;
				doc.voucher_type = "Journal Entry";
				doc.naming_series = "JV-";
				//doc.cheque_no = frm.doc.name
				doc.company = frappe.defaults.get_default('company');
				
				if (frm.doc.location != "")
					locationLabel="[Location Details] --\n"
				else
					locationLabel=""

				if (linked_category_account != "")
					categoryLabel="[Category] --\n"
				else
					categoryLabel=""

				if (frm.doc.bank!="")
					bankLabel="[Bank] -- "
				else
					bankLabel=""
	
				plaidIDLabel="[Plaid ID] -- "
				
				doc.user_remark=categoryLabel+linked_category_account+'\n' +'\n'+locationLabel+frm.doc.location +'\n' +'\n'+ bankLabel+frm.doc.bank+'\n'+'\n'+plaidIDLabel+frm.doc.name
				doc.title=frm.doc.transaction_name+'-'+linked_category_account

				doc.cheque_no = frm.doc.transaction_id;
				doc.cheque_date=frm.doc.date;

				var row = frappe.model.add_child(doc, "Journal Entry Account", "accounts");
				row.account = linked_category_account
				if (frm.doc.amount < 0)
					row.credit_in_account_currency = frm.doc.amount
				else
					row.debit_in_account_currency = frm.doc.amount
				
					
				var row = frappe.model.add_child(doc, "Journal Entry Account", "accounts");
				row.account = linked_bank_account
				if (frm.doc.amount < 0)
					row.debit_in_account_currency = frm.doc.amount
				else
					row.credit_in_account_currency = frm.doc.amount

				frappe.set_route("Form", doc.doctype, doc.name);

			})





		});
	}
});