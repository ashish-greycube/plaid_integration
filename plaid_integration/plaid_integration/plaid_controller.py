import os
import plaid
import frappe
import requests
import datetime
import json

class PlaidController():

	def __init__(self, access_token=None):
		self.access_token = access_token
		self.settings = self.get_plaid_settings()
		self.client = plaid.Client(client_id=self.settings.get('client_id') ,
			secret=self.settings.get('secret'), 
			public_key=self.settings.get('public_key'), 
			environment=self.settings.get('environment'))

	def get_plaid_settings(self):
		fields = ['client_id', 'secret', 'public_key']
		settings = frappe.db.get_value('Plaid Settings', 'Plaid Settings', fields, as_dict=True)
		if settings: settings['environment'] = 'sandbox'
		return settings

	def authenticate(self):
		try:
			if not self.settings:
				frappe.throw("Please setup Plaid Settings")
			self.client.Auth.get(self.access_token)
			print "Authentication Successful....."
		except Exception as e:
			print frappe.get_traceback()
			frappe.msgprint("Authentication Failed ...")

	def get_trasaction(self):
		try:
			self.authenticate()
			start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
			end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
			response = self.client.Transactions.get(self.access_token, start_date=start_date, end_date=end_date)
			transactions = response['transactions']
			while len(transactions) < response['total_transactions']:
				response = self.client.Transactions.get(self.access_token, start_date=start_date, end_date=end_date, offset=len(transactions))
				transactions.extend(response['transactions'])
			return response
		except Exception as e:
			raise e

	def get_access_token(self, public_token):
		try:
			exchange_response = self.client.Item.public_token.exchange(public_token)
			access_token = exchange_response['access_token']
			return access_token
		except Exception as e:
			print frappe.get_traceback()
			raise e