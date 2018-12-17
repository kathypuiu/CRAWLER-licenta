from insta_dld import *
import face_recognition
import sys
import os


kapi1 = face_recognition.load_image_file("photos/k1.jpg")
kapi2 = face_recognition.load_image_file("photos/k2.jpg")
kapi3 = face_recognition.load_image_file("photos/k3.jpg")
kapi4 = face_recognition.load_image_file("photos/k4.jpg")
kapi5 = face_recognition.load_image_file("photos/grup.jpg")

encoding1 = face_recognition.face_encodings(kapi1)[0]
encoding2 = face_recognition.face_encodings(kapi2)[0]
encoding3 = face_recognition.face_encodings(kapi3)[0]
encoding4 = face_recognition.face_encodings(kapi4)[0]
encoding5 = face_recognition.face_encodings(kapi5)[0]

encoding = [encoding1, encoding2, encoding3, encoding4, encoding5]


browser = webdriver.Firefox()
username = 'paunstefan'
#username = 'cati.puiu'
browser.get('https://www.instagram.com/' + username)
urls = []

insta_scroll_to_bottom(browser, urls)
img_urls = list_insta_images(browser, urls)

try:
	os.makedirs(username)
except OSError:
	pass
os.chdir(username)
name = 0

for url in img_urls:
	fname = str(name) + '.jpg'
	f = open(fname, 'wb')
	f.write(requests.get(url).content)
	f.close()

	unk_picture = face_recognition.load_image_file(fname)
	try:
		unk_face_encoding = face_recognition.face_encodings(unk_picture)[0]
	except Exception as e:
		print("exception")
		os.remove(fname)
		continue

	not_ok = 1
	for e in encoding:
		results = face_recognition.compare_faces([e], unk_face_encoding)

		if results[0] == False:
			os.remove(fname)
			print("file removed")
			break
		else:
			name += 1
			print("match found")
			break

	


