// Copyright (c) 2018, Drivedgevd and contributors
// For license information, please see license.txt

frappe.provide("plaid.generate_tokens");

frappe.ui.form.on('Plaid Settings', {
	onload: function(frm) {
		if(frm.doc.sync_status) {
			stuas_map = {
				"In Progress": "Syncing is in progress, Please wait.",
				"Successful": "Successfully Synced Plaid Transactions.",
				"Failed": "Syncing failed, Check Sync Log"
			}
			frm.set_intro(stuas_map[frm.doc.sync_status])
		}
		
	},
	sync_categories: function(frm,access_token){
		frappe.call({
			method: "get_categories",
			doc: frm.doc
		}).then((r) => {
			if (r.message) {
				console.log(r.message)
				frappe.call({
					method: "import_category",
					doc: frm.doc
				})

			} else {
				//console.log(r)
			}
		});

	},
	sync_transactions: function(frm, bank, access_token) {
		if(frm.doc.sync_status != "In Progress"){
			frm.call({
				method: "sync_transactions",
				doc: frm.doc,
				args: {
					"bank": bank,
					"access_token": access_token
				}
			})
		}
		else
			frappe.msgprint("Syncing is in process, please wait..")
	}
});

frappe.ui.form.on("Plaid Bank Detail", {
	get_access_token: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if(!row.bank_name)
			frappe.msgprint(__("Please enter bank name first."))
		if(row.access_token)
			frappe.msgprint(__("Access Token already generated. Please save the form."))
		else
			plaid.generate_tokens.get_public_token(frm, cdt, cdn);
	}
})

plaid.generate_tokens.get_public_token = function(frm, cdt, cdn) {
	var handler = Plaid.create({
		apiVersion: 'v2',
		clientName: 'Plaid Walkthrough Demo',
		env: 'sandbox',
		product: ['transactions'],
		key: frm.doc.public_key,
		onSuccess: function(public_token) {
			plaid.generate_tokens.get_access_token(frm, cdt, cdn, public_token)
		},
	});
	handler.open();
}

plaid.generate_tokens.get_access_token = function(frm, cdt, cdn, public_token) {
	frm.call({
		method: "generate_access_token",
		doc: frm.doc,
		args: {"public_token": public_token},
		callback: function(r) {
			if(!r.exc && r.message) {
				frappe.model.set_value(cdt, cdn, "access_token", r.message);
			}
			else frappe.msgprint("Failed to generate Access Token. Try again ...")
		}
	})
}
