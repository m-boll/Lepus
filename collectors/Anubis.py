import requests
from json import loads
from termcolor import colored


def init(domain):
	ANUBIS = []

	print(colored("[*]-Searching Anubis...", "yellow"))

	url = "https://anubisdb.com/anubis/subdomains/{0}".format(domain)
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}

	try:
		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			subdomains = loads(response.text)

			if isinstance(subdomains, list):
				ANUBIS.extend(subdomains)

		ANUBIS = set(ANUBIS)

		print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(ANUBIS), "yellow")))
		return ANUBIS

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
