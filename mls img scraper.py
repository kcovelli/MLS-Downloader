import os, urllib, re
from urllib.request import urlopen, urlretrieve

# use this image scraper from the location that 
# you want to save scraped images to

# MLS regex
p = "\A[CEWXcewx][0-9]{7}\Z"

def get_image(url, i):
    dl_url = url + str(i)
    filename= str(i) + ".jpg"
    fullfilename = os.path.join(MLS, filename)

    try:
        urlretrieve(dl_url, fullfilename)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            if i == 1:
                print("MLS listing not found. Stopping...")
            else:
                print("Image " + str(i) + " not found. Stopping...")
        else:
            print("Error reaching Stratus, exiting...")
        return -1
    
    print('image ' + str(i) + ' downloaded')
    return 0

print("This program will download all the images from a given MLS listing to a single folder\n")

while True:
    MLS = input("Enter MLS number: ")
    if re.search(p, MLS) is not None:
        break
    else:
        print("Not a valid MLS number\n")
img_url = "http://trebphotos.stratusdata.com/Live/Default.ashx?type=ListingPhoto&entityName=Listing&entityID=" + MLS + "&index="

print ('\nDownloading images...')
if not os.path.exists(MLS):
    os.mkdir(MLS)
for i in range(1, 21):
    if get_image(img_url, i) == -1:
            break
print("Done!")
input("\nPress enter key to exit...")

