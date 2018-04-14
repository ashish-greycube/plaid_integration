# -*- coding: utf-8 -*-
# Copyright (c) 2018, Drivedgevd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PlaidCategory(Document):
	
	def validate(self):
		if(self.category_3):
			self.title=self.category_1+" - "+self.category_2+" - "+self.category_3
		elif(self.category_2):
			self.title=self.category_1+" - "+self.category_2
		else:
			self.title=self.category_1