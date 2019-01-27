from bs4 import BeautifulSoup
import requests
import urllib2
import sys

def page_size(url):
	response = urllib2.urlopen(url)
	# Get all data contains headers,server etc.
	html = response.read()
	# Get only the length
	page_size = len(html)
	return page_size

def no_of_links(page,  url):
	try:
		cookie_field_tokens = page.headers['Set-Cookie'].split(';')
		for entry in cookie_field_tokens:
			entry = entry.lower().strip()
			if entry[:6:]=='domain':
				url_domain = entry[8::].split(',')[0]
				break
		# Getting domain from header is needed for url like fb.com
		# that url actually locates to fachttp://www.learningaboutelectronics.comebook.com
	except:
		url_domain = url.split('/')[2]
		
	content = BeautifulSoup(page.text, 'html.parser')
	links_with_same_domain = []

	for link in content.find_all('a'):
		if link.has_attr('href'):
			link_url = link.attrs['href']
		try:
			link_url_domain = link_url.split('/')[2] #removing http and locating domain

			# we need to check for www. as a prefix also
			if url_domain in link_url_domain:
				links_with_same_domain.append(link_url)
		except:
			pass
			#These links don't contain a domain therefore neglecting these links

	return len(links_with_same_domain)

if __name__ == "__main__":
    url = sys.argv[1]
    print sys.argv[1]
page = requests.get(url)
link_count = no_of_links(page, url)
page_size = page_size(url)
print 'Size :', page_size , ' bytes'
print 'Links to same domain : ', link_count