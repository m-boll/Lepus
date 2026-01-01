import requests
from json import loads
from datetime import datetime
from urllib.parse import urlparse
from termcolor import colored


def init(domain):
	CC = []

	print(colored("[*]-Searching CommonCrawl...", "yellow"))

	try:
		# Fetch collection info
		collinfo_url = "https://index.commoncrawl.org/collinfo.json"
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Chrome/142.0"}

		response = requests.get(collinfo_url, headers=headers)
		collections = loads(response.text)

		# Filter collections from the last 5 years (2020-2025)
		current_year = datetime.now().year
		target_collections = []

		for collection in collections:
			# Extract year from the id (e.g., "CC-MAIN-2025-51" -> 2025)
			try:
				collection_year = int(collection["id"].split("-")[2])
				if collection_year >= current_year - 5:
					target_collections.append(collection["cdx-api"])
			except (IndexError, ValueError):
				continue

		print(r"  \__ {0}: {1}".format(colored("Searching indexes", "cyan"), colored(len(target_collections), "yellow")))

		# Search each collection
		for index_url in target_collections:
			try:
				search_url = "{0}?url=*.{1}&output=json".format(index_url, domain)
				response = requests.get(search_url, headers=headers)

				if response.status_code == 200:
					lines = response.text.strip().split("\n")
					for line in lines:
						try:
							data = loads(line)
							url = data.get("url", "")
							if url:
								# Extract hostname from URL
								parsed = urlparse(url)
								hostname = parsed.netloc
								if hostname and domain in hostname:
									CC.append(hostname)
						except Exception:
							continue

			except Exception:
				continue

		CC = set(CC)

		print(r"  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(CC), "yellow")))
		return CC

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
