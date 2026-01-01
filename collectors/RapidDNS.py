import requests
from re import findall
from termcolor import colored


def init(domain):
	RD = []

	print(colored("[*]-Searching RapidDNS...", "yellow"))

	base_url = "https://rapiddns.io/subdomain/{0}?page={1}"
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}

	try:
		# First request to get total pages
		response = requests.get(base_url.format(domain, 1), headers=headers)

		if response.status_code == 200:
			# Extract domains from table - domains are in <td> tags in the table body
			domains = findall(r'<td>([a-zA-Z0-9\-\.]+\.{0})</td>'.format(domain.replace(".", r"\.")), response.text)
			RD.extend(domains)

			# Find total pages from pagination
			pagination_match = findall(r'<a class="page-link" href="/subdomain/{0}\?page=(\d+)">{1}</a>'.format(
				domain.replace(".", r"\."), r"\1"), response.text)

			if pagination_match:
				total_pages = max([int(page) for page in pagination_match])
			else:
				total_pages = 1

			# Fetch remaining pages
			for page in range(2, total_pages + 1):
				try:
					response = requests.get(base_url.format(domain, page), headers=headers)

					if response.status_code == 200:
						domains = findall(r'<td>([a-zA-Z0-9\-\.]+\.{0})</td>'.format(domain.replace(".", r"\.")), response.text)
						RD.extend(domains)

				except Exception:
					continue

		RD = set(RD)

		print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(RD), "yellow")))
		return RD

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
