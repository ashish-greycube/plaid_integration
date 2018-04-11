# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "plaid_integration"
app_title = "Plaid Integration"
app_publisher = "GreyCube Technologies"
app_description = "Plaid Integration"
app_icon = "fa fa-money"
app_color = "#0e304b"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/plaid_integration/css/plaid_integration.css"
# app_include_js = "/assets/js/plaid.desk.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/plaid_integration/css/plaid_integration.css"
# web_include_js = "/assets/plaid_integration/js/plaid_integration.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "plaid_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "plaid_integration.install.before_install"
# after_install = "plaid_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "plaid_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Journal Entry":{
        "after_insert": "plaid_integration.plaid_integration.doctype.plaid_transaction.plaid_transaction.insert_JVid_in_plaidtransaction",
    }
}



# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"plaid_integration.tasks.all"
# 	],
# 	"daily": [
# 		"plaid_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"plaid_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"plaid_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"plaid_integration.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "plaid_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "plaid_integration.event.get_events"
# }

