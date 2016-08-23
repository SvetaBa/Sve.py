from bs4 import BeautifulSoup
import re
import requests


soup = BeautifulSoup(open("bab.html"))
#print(soup.prettify())


# for link in soup.find_all('a'):
#     print("http://slovari.ru/"+link.get('href'))


for link in soup.find_all('a'):
	result = requests.get("http://slovari.ru/"+link.get('href'))
	soup = BeautifulSoup(result.text)
	#print(soup)
s = string (soup)

res = re.findall(r'<p>')
print (res)



