"""
Configuration for docs
"""

source_link = "https://github.com/ashish-greycube/plaid_integration"
docs_base_url = "https://ashish-greycube.github.io/plaid_integration"
headline = "Integration between ERPNext journal entry and plaid transactions"
sub_heading = "Documentation"

def get_context(context):
	context.brand_html = "Plaid Integration"
    context.top_bar_items = [
      {"label": "About", "url": context.docs_base_url + "/about"},
    ]