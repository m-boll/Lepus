import shodan
from re import findall
from json import dumps
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	SD = []

	print(colored("[*]-Searching Shodan...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	SHODAN_API_KEY = parser.get("Shodan", "SHODAN_API_KEY")
	api = shodan.Shodan(SHODAN_API_KEY)

	if SHODAN_API_KEY == "":
		print(r"  \__", colored("No Shodan API key configured", "red"))
		return []

	else:
		try:
			try:
				for res in api.search_cursor("hostname:.{0}".format(domain)):
					SD.extend([hostname for hostname in res["hostnames"] if ".{0}".format(domain) in hostname])

				for res in api.search_cursor("ssl:.{0}".format(domain)):
					SD.extend(findall(r"([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", r"\.")), dumps(res)))

			except KeyError as errk:
				print(r"  \__", colored(errk, "red"))
				return []

			SD = set(SD)

			print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(SD), "yellow")))
			return SD

		except shodan.exception.APIError as err:
			print(r"  \__", colored(err, "red"))
			return []

		except Exception:
			print(r"  \__", colored("Something went wrong!", "red"))
			return []
