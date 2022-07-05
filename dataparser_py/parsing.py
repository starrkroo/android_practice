import requests
import os
import sqlite3
import unicodedata
from tqdm import tqdm
from bs4 import BeautifulSoup as bs


core_url = 'https://visagehall.ru/'
url_parse = 'https://visagehall.ru/catalog/vh-new/'
html_from_page = requests.get(url_parse).text


def save_image(url: str, pathname: str, filename: str) -> str:
    """Method that saves image on lc (local machine)


    @param: url Page image url
    @param: pathname Local relative directory
    @param filename Name of current saving file

    """
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    # filename = os.path.join(pathname, url.split("/")[-1])
    filename = os.path.join(pathname, filename + '.' + url.split('.')[-1])
    progress = tqdm(response.iter_content(1024),
                    f"Downloading {filename}",
                    total=file_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024
    )

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))

    return filename

def parse_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    command = """CREATE TABLE IF NOT EXISTS vhdata (
                        merch_preview_title VARCHAR(127),
                        merch_preview_description VARCHAR(255),
                        merch_preview_price INT,
                        merch_preview_image_path VARCHAR(255)
    )"""
    cursor.execute(command)
    soup = bs(html_from_page, 'lxml')
    posts = soup.find('div', class_='catalog-block__products-list').find_all('a', class_='merch-preview')

    for index_post, post in enumerate(posts):
        command = """
            INSERT INTO vhdata (
                merch_preview_title,
                merch_preview_description,
                merch_preview_price,
                merch_preview_image_path
            ) VALUES (?, ?, ?, ?)
        """

        image_url = post.find('img').get('data-src')

        product_local_path_url = os.getcwd().replace('\\', '/') + '/' + save_image(
            url=core_url + image_url,
            pathname='images/',
            filename=f'post_{index_post}'
        )

        product_title = post.find('div', class_='merch-preview__title').text
        product_description = post.find('div', class_='merch-preview__description').text
        product_price = post.find('div', class_='merch-preview__price').text.strip()

        # for something like \xa1 that means space in normalized localization
        normal_product_price = unicodedata.normalize("NFKD", product_price)

        values = ((product_title, product_description, normal_product_price, product_local_path_url), )

        cursor.executemany(command, values)

    conn.commit()
    cursor.close()
    conn.close()


parse_data()
    