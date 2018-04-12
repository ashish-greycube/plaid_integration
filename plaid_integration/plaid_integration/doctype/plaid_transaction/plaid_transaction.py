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
	if (self.cheque_no!=None):
		if  ("PT-" in self.cheque_no):
			if not frappe.db.exists('Plaid Transaction', self.cheque_no):
				return
			else:
				doc = frappe.get_doc('Plaid Transaction', self.cheque_no)
				doc.linked_jv=self.name
				doc.save()