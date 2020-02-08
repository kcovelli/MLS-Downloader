from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

# use this image scraper from the location that 
#you want to save scraped images to

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "html.parser")

def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.find_all(class_ = "gallery-image thumbnail ")]
    print (str(len(images)) + " images found.")
    print ('Downloading images...')
    image_links = [each['href'] for each in images]
    for i, each in enumerate(image_links, 1):
        filename=str(i) + ".jpg"
        urlretrieve(each, filename)
    print('Finished')
    return image_links

get_images("http://tours.bizzimage.com/ub/79596")
raw_input("...")
