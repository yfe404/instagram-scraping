import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://deskgram.org'
USER = 'trex'

start_url = BASE_URL + '/' + USER

img_url_all = list()
caption_all = list()

r = requests.get(start_url)
soup = BeautifulSoup(r.text, 'html.parser')
captions = soup.findAll("div", {"class": "post-caption"})
images = soup.findAll("div", {"class": "post-img"})

for image in images:
    img_url = image.img['src'].split('?')[0]
    img_url_all.append(img_url)

for caption in captions:
    caption_all.append(caption.text)

print ('Found {0} captions.'.format(len(captions)))
print ('Found {0} images.'.format(len(images)))

while True:
    links = soup.findAll('a')
    next_link = list(filter( lambda x: 'next_id' in x['href'], links))
    if len(next_link) == 0:
        break
    else:
        dest = next_link[0]['href']
        next_url = BASE_URL + dest
        print ('fetching {0}'.format(next_url))
        r = requests.get(next_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        captions = soup.findAll("div", {"class": "post-caption"})
        images = soup.findAll("div", {"class": "post-img"})

        for image in images:
            img_url = image.img['src'].split('?')[0]
            img_url_all.append(img_url)

        for caption in captions:
            caption_all.append(caption.text)


        print ('Found {0} captions.'.format(len(captions)))
        print ('Found {0} images.'.format(len(images)))

for idx, img_url in enumerate(img_url_all):
    img_data = requests.get(img_url).content
    filename = '{0}_{1}.jpg'.format(USER, idx)
    print('saving image {0}'.format(filename))
    with open(filename, 'wb') as handler:
        handler.write(img_data)
     
for idx, caption in enumerate(caption_all):
    filename = '{0}_{1}.txt'.format(USER, idx)
    print('saving caption {0}'.format(filename))
    text_file = open(filename, 'w')
    text_file.write(caption)
    text_file.close()
