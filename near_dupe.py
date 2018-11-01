from PIL import Image
import imagehash
import os
import sqlite3

ADS_DIRECTORY = "../OpenWPM/images/ads"
DB_FILE = "../crawl_data/crawl-data.sqlite"



def find_similar_images():
    images = {}
    for host in os.listdir(ADS_DIRECTORY):
        for img_file in os.listdir(os.path.join(ADS_DIRECTORY, host)):
            hash = imagehash.average_hash(Image.open(os.path.join(ADS_DIRECTORY, host, img_file)))
            if hash in images:
                print '{} is a dupe with {}'.format(img_file, images[hash])
            else:
                images[hash] = []
            images[hash].append(img_file)
    conn = sqlite3.connect(DB_FILE)
    for k, imgs in images.iteritems():
        u_id = imgs[0][:-4]
        for img in imgs:
            conn.execute('UPDATE ads_found SET uid=? WHERE frame_id=?',
                         (u_id, img[:-4]))
            conn.commit()


# the plan is to go through every image, load them up
# fingerprint them, and de-dup if distance is below a threshold
# we can then add a unique id to each ad in the ads_found db table
if __name__ == "__main__":
    find_similar_images()