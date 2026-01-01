import requests
from json import loads
from termcolor import colored


def init(domain):
	TC = []

	print(colored("[*]-Searching ThreatCrowd...", "yellow"))

	url = "http://ci-www.threatcrowd.org/searchApi/v2/domain/report/"
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}

	try:
		response = requests.get(url, params={"domain": domain}, headers=headers)

		try:
			RES = loads(response.text)
			resp_code = int(RES["response_code"])

			if resp_code == 1:
				for sd in RES["subdomains"]:
					TC.append(sd)

			TC = set(TC)

			print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(TC), "yellow")))
			return TC

		except ValueError as errv:
			print(r"  \__", colored(errv, "red"))
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
