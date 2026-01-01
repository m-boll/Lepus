import requests
from termcolor import colored


def init(domain):
	THC = []

	print(colored("[*]-Searching THC...", "yellow"))

	url = "https://ip.thc.org/api/v1/subdomains/download"
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}
	params = {"domain": domain, "limit": 50000, "hide_header": "true"}

	try:
		response = requests.get(url, params=params, headers=headers)

		if response.status_code == 200:
			subdomains = response.text.strip().split("\n")
			for subdomain in subdomains:
				if subdomain:
					THC.append(subdomain)

		THC = set(THC)

		print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(THC), "yellow")))
		return THC

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
