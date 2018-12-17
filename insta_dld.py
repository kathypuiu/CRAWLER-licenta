import time
import requests
import os
import sys
from selenium import webdriver
from bs4 import BeautifulSoup


def get_insta_urls(browser, urls):
	''' Create a list of the particular image pages'''
	content = browser.page_source								# Download the HTML source
	soup = BeautifulSoup(content, features="html.parser")		# Create the BS object

	mydivs = soup.findAll("div", {"class": "v1Nh3"})

	for div in mydivs:											# Put all unique URLs in the list
		link = div.find('a', href=True)['href']
		if link not in urls:
			urls.append(link)


def insta_scroll_to_bottom(browser, urls):
	''' Scroll to the bottom of an infinite scrolling page'''
	SCROLL_PAUSE_TIME = 0.7										# Can be changed

	last_height = browser.execute_script("return document.body.scrollHeight")

	while True:
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		get_insta_urls(browser, urls)							# Get the URLs from the currently loaded part of the page

		time.sleep(SCROLL_PAUSE_TIME)							# Wait for next section to load

		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


def list_insta_images(browser, urls):
	''' Create a list with all the image URLs from the Instagram page'''
	img_urls = []

	for url in urls:
		browser.get('https://www.instagram.com/' + url)
		content = browser.page_source
		soup = BeautifulSoup(content, features="html.parser")
		time.sleep(0.2)

		if soup.find("button", {"class": "_6CZji"}):			# If it is a multiple photo post
			button_exists = 1

			while button_exists:
				content = browser.page_source					# Load the current source
				soup = BeautifulSoup(content, features="html.parser")
				# if soup.find("img", {"class": "FFVAD"}):
				img_group = soup.findAll("img", {"class": "FFVAD"})		# Find all images
				for img in img_group:
					image = img['src']
					if image not in img_urls:
						img_urls.append(image)					# Add URL if not already present
				try:
					button = browser.find_element_by_class_name('_6CZji')
					button.click()								# Click the 'next' button until it no longer exists
				except Exception as e:
					button_exists = 0

		elif soup.find("img", {"class": "FFVAD"}):				# If it is a normal page and not a video
			img_url = soup.find("img", {"class": "FFVAD"})['src']
			img_urls.append(img_url)

		else:
			continue

	return img_urls


def download_images(url_list, username):
	try:
		os.makedirs(username)								# Create directory if not already present
	except OSError:
		pass
	os.chdir(username)
	name = 0
	for url in url_list:
		f = open(str(name) + '.jpg', 'wb')					# Create a file
		f.write(requests.get(url).content)					# WWrite to it the jpg data
		f.close()

		name += 1


def main():
	if len(sys.argv) != 2:
		print('Usage: py insta_dld.py [username]')
		sys.exit(1)
	browser = webdriver.Firefox()
	user = sys.argv[1]
	browser.get('https://www.instagram.com/' + user)
	urls = []

	insta_scroll_to_bottom(browser, urls)
	img_urls = list_insta_images(browser, urls)
	download_images(img_urls, user)

	# print(len(img_urls))
	# for url in img_urls:
	# 	print(url)


if __name__ == '__main__':
	main()
