import requests
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	C = []

	print(colored("[*]-Searching Censys...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	API_URL = "https://search.censys.io/api/v1"
	UID = parser.get("Censys", "CENSYS_UID")
	SECRET = parser.get("Censys", "CENSYS_SECRET")

	if UID == "" or SECRET == "":
		print(r"  \__", colored("No Censys API credentials configured", "red"))
		return []

	else:
		payload = {"query": domain}

		try:
			res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET))

			if res.status_code == 429:
				print(r"  \__", colored("Rate limit exceeded. See https://www.censys.io/account for rate limit details.", "red"))
				return C

			C = findall(r"CN=([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", r"\.")), str(res.content))
			numberOfPages = findall(r"pages\":\s(\d+)?}", str(res.content))

			for page in range(2, int(numberOfPages[0]) + 1):
				payload = {"query": domain, "page": page}
				res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET))

				if res.status_code != 200:
					if loads(res.text)["error_type"] == "max_results":
						print(r"  \__", colored("Search result limit reached. See https://www.censys.io/account for search results limit details.", "red"))
						break

					else:
						print(r"  \__ {0} {1} {2}".format(colored("An error occured on page", "red"), colored("{0}:".format(page), "red"), colored(loads(res.text)["error_type"], "red")))

				else:
					tempC = findall(r"CN=([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", r"\.")), str(res.content))
					C = C + tempC

			C = set(C)

			print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(C), "yellow")))
			return C

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
