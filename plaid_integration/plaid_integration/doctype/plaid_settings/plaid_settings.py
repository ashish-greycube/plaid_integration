# -*- coding: utf-8 -*-
# Copyright (c) 2018, Drivedgevd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.utils import cstr
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.background_jobs import enqueue
from plaid_integration.plaid_integration.plaid_controller import PlaidController

class PlaidSettings(Document):
	
	def generate_access_token(self, public_token):
		plaid = PlaidController()
		access_token = plaid.get_access_token(public_token)
		return access_token

	def sync_transactions(self, bank, access_token):
		try:
			self.db_set("sync_status", "In Progress")
			frappe.msgprint(_("Queued for Syncing Plaid Transactions. It may take a few minutes."))
			method = "plaid_integration.plaid_integration.doctype.plaid_settings.plaid_settings.sync_plaid_data"
			enqueue(method, now=True)
		except Exception as e:
			print frappe.get_traceback()
			self.db_set("sync_status", "Failed")
			frappe.msgprint("Syncing is failed. Please check Sync log")

	def get_transactions(self, access_token):
		plaid = PlaidController(access_token)
		transactions = plaid.get_trasaction()
		return transactions

	def make_sync_data_entries(self, synced_data, bank):
		accounts = self.sync_accounts(synced_data.get('accounts'), bank)
		transactions = self.sync_plaid_transactions(synced_data.get('transactions'), bank)
		return {"accounts": accounts, "transactions": transactions}

	def sync_accounts(self, accounts, bank):
		try:
			acc_ids = []
			for acc in accounts:
				if not frappe.db.exists("Plaid Account", acc.get('account_id')):
					acc_ = frappe.new_doc("Plaid Account")
					acc_.account_id = acc.get('account_id')
					acc_.official_name = acc.get('official_name')
					acc_.insert()
					acc_ids.append(acc_.name)
			return acc_ids
		except Exception as e:
			raise e

	def sync_plaid_transactions(self, transactions, bank):
		try:
			transaction_ids = []
			for idx, row in enumerate(transactions):
				pt = self.make_plaid_transaction(row, bank)
				if pt: transaction_ids.append(pt)
			return transaction_ids
		except Exception as e:
			raise e

	def make_plaid_transaction(self, transaction, bank):
		try:
			if not frappe.db.get_value("Plaid Transaction",
				{"transaction_id": transaction.get('transaction_id')},"name"):
				fields = ['account_owner', 'category_id', 'account_id', 'pending_transaction_id'\
					'transaction_name', 'date', 'transaction_id', 'transaction_type', 'amount', 'pending']
				pt = frappe.new_doc("Plaid Transaction")
				doc_dict = {}
				for key, val in transaction.iteritems():
					if key in fields:
						doc_dict[key] = val
					elif key == "category":
						doc_dict[key] = ("-").join(val) if val else ""
					elif key == "location":
						doc_dict['location'] = (",\n").join([ key+"-"+str(val) for key, val in val.iteritems()])
					elif key == "payment_meta" and val:
						payment_meta = []
						for k, v in val.iteritems():
							payment_meta.append({
								"key": k,
								"value": v
							})
						doc_dict[key] = payment_meta
					elif key == "name":
						doc_dict["transaction_name"] = val
					else: pass
					doc_dict["bank"] = bank
					doc_dict['account_type'] = frappe.db.get_value("Plaid Account", {
						"account_id": doc_dict.get('account_id')}, "official_name")
				pt.update(doc_dict)
				pt.insert()
				return pt.name
		except Exception as e:
			raise e

	def make_sync_log(self, bank, sync_details, status):
		try:
			sync_log = frappe.new_doc("Plaid Sync Log")
			sync_log.date = frappe.utils.now()
			sync_log.sync_status = status
			sync_log.bank = bank
			sync_log.sync_log = cstr(sync_details)
			sync_log.save()
			frappe.db.commit()
		except Exception as e:
			print frappe.get_traceback()
			raise e

@frappe.whitelist()
def sync_plaid_data():
	plaid_settings = frappe.get_doc("Plaid Settings", "Plaid Settings")
	for bank in plaid_settings.banks:
		try:
			if bank.get('access_token'):
				sync_data = plaid_settings.get_transactions(bank.get('access_token'))
				sync_details = plaid_settings.make_sync_data_entries(sync_data, bank.get('bank_name'))
				plaid_settings.make_sync_log(bank.get('bank_name'), sync_details, "Successful")
		except Exception as e:
			err_msg = frappe.as_unicode(e)
			plaid_settings.make_sync_log(bank.get('bank_name'), err_msg, "Failed")
	plaid_settings.sync_status = "Successful"
	plaid_settings.last_sync = now_datetime()
	plaid_settings.save()
