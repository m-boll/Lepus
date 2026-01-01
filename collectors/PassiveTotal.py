import requests
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	PT = []

	print(colored("[*]-Searching PassiveTotal...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	PT_KEY = parser.get("PassiveTotal", "PT_KEY")
	PT_SECRET = parser.get("PassiveTotal", "PT_SECRET")

	if PT_KEY == "" or PT_SECRET == "":
		print(r"  \__", colored("No PassiveTotal API credentials configured", "red"))
		return []

	else:
		auth = (PT_KEY, PT_SECRET)
		url = "https://api.passivetotal.org/v2/enrichment/subdomains"
		data = {"query": domain}
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}

		try:
			response = requests.get(url, auth=auth, json=data, headers=headers)

			if response.status_code == 402:
				print(r"  \__", colored("Quota exceeded.", "red"))
				return []

			try:
				for subdomain in response.json()["subdomains"]:
					PT.append("%s.%s" % (subdomain, domain))

				PT = set(PT)

				print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(PT), "yellow")))
				return PT

			except KeyError as errk:
				print(r"  \__", colored(errk, "red"))
				return []

		except requests.exceptions.RequestException as err:
			print(r"  \__", colored(err, "red"))
			return []

		except requests.exceptions.HTTPError as errh:
			print(r"  \__", colored(errh, "red"))
			return []

		except requests.exceptions.ConnectionError as errc:
			print(r"  \__", colored(errc, "red"))
			return []

		except requests.exceptions.Timeout as errt:
			print(r"  \__", colored(errt, "red"))
			return []

		except Exception:
			print(r"  \__", colored("Something went wrong!", "red"))
			return []
