import os

urls = []

for file_name in os.listdir(os.getcwd()):
	if file_name.endswith('.txt'):
		with open(file_name, 'r') as file:
			urls.extend(file.readlines())
			
url_set = sorted(list(set(urls)))

with open('UrlSet.txt', 'w') as file:
	for url in url_set:
		file.write(url)
		

