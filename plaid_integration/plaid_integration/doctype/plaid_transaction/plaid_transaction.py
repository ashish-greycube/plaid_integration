# -*- coding: utf-8 -*-
# Copyright (c) 2018, Drivedgevd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PlaidTransaction(Document):
	pass

@frappe.whitelist()
def insert_JVid_in_plaidtransaction(self,method):
    doc = frappe.get_doc('Plaid Transaction', self.cheque_no)
    if doc:
		doc.linked_jv=self.name
		doc.save()
		#frappe.reload_doc("plaid_integration", "doctype", doc.name)