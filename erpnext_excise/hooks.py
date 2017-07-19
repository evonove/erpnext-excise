# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_excise"
app_title = "Erpnext Excise"
app_publisher = "Evonove"
app_description = "Excise module for erpnext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dev@evonove.it"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_excise/css/erpnext_excise.css"
# app_include_js = "/assets/erpnext_excise/js/erpnext_excise.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_excise/css/erpnext_excise.css"
# web_include_js = "/assets/erpnext_excise/js/erpnext_excise.js"

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
# get_website_user_home_page = "erpnext_excise.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_excise.install.before_install"
# after_install = "erpnext_excise.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_excise.notifications.get_notification_config"

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

fixtures = ["Custom Field"]
doc_events = {
	("Sales Order", "Sales Invoice", "Quotation"): {
		"before_save": "erpnext_excise.erpnext_excise.add_excise.sales_order_excise"
	},
	("Purchase Order", "Purchase Invoice"): {
		"before_save": "erpnext_excise.erpnext_excise.add_excise.purchase_order_excise"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_excise.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_excise.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_excise.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_excise.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_excise.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_excise.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_excise.event.get_events"
# }

