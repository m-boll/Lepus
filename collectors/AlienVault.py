import requests
from json import loads
from termcolor import colored


def init(domain):
	AV = []

	print(colored("[*]-Searching AlienVault OTX...", "yellow"))

	url = "https://otx.alienvault.com/api/v1/indicators/domain/{0}/url_list".format(domain)
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}
	page = 1
	limit = 500

	try:
		while True:
			params = {"limit": limit, "page": page}
			response = requests.get(url, params=params, headers=headers)

			if response.status_code == 200:
				try:
					data = loads(response.text)

					if not data.get("url_list"):
						break

					for item in data["url_list"]:
						hostname = item.get("hostname", "")
						if hostname and domain in hostname:
							AV.append(hostname)

					# Check if we should continue to next page
					if len(data["url_list"]) < limit:
						break

					page += 1

				except ValueError:
					break

			else:
				break

		AV = set(AV)

		print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(AV), "yellow")))
		return AV

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
