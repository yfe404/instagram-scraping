import os

import click

import requests
from bs4 import BeautifulSoup


def save_captions(prefix, user, caption_all):
    for idx, caption in enumerate(caption_all):
        filename = '{0}_{1}.txt'.format(user, idx)
        filename = os.path.join(prefix, filename)
        print('saving caption {0}'.format(filename))
        text_file = open(filename, 'w')
        text_file.write(caption)
        text_file.close()

def download_and_save_images(prefix, user, img_url_all):        
    for idx, img_url in enumerate(img_url_all):
        img_data = requests.get(img_url).content
        filename = '{0}_{1}.jpg'.format(user, idx)
        filename = os.path.join(prefix, filename)
        print('saving image {0}'.format(filename))
        with open(filename, 'wb') as handler:
            handler.write(img_data)


@click.command()
@click.option('--images/--no-images', default=True,
              help='Scrap also images.')
@click.option('--captions/--no-captions', default=True,
              help='Scrap also captions.')
@click.option('--user', '-u', required=True,
              help='The account to scrap (all photos and all captions).')
def scrap(images, captions, user):
    """ Scrap photos and captions from posts of a single user """
    BASE_URL = 'https://deskgram.org'
    USER = user

    url = BASE_URL + '/' + USER
    
    dest_folder = './{0}'.format(USER)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    pattern_for_images = {'name':"div", 'attrs':{"class": "post-img"}}
    pattern_for_captions = {'name':"div", 'attrs':{"class": "post-caption"}}

    while True:
        print ('fetching {0}'.format(url))
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        if images:
            img_url_all = list()
            images = soup.findAll(**pattern_for_images)
            for image in images:
                img_url = image.img['src'].split('?')[0]
                img_url_all.append(img_url)
            print ('Found {0} images.'.format(len(images)))

        if captions:
            caption_all = list()
            captions = soup.findAll(**pattern_for_captions)
            for caption in captions:
                caption_all.append(caption.text)
            print ('Found {0} captions.'.format(len(captions)))


        links = soup.findAll('a')
        next_link = list(filter( lambda x: 'next_id' in x['href'], links))
        if len(next_link) == 0:
            break
        else:
            dest = next_link[0]['href']
            url = BASE_URL + dest
        
    if images:
        download_and_save_images(dest_folder, USER, img_url_all)
    
    if captions:
        save_captions(dest_folder, USER, caption_all)


if __name__ == '__main__':
    scrap()
