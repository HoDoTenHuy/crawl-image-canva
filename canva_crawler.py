import os
import csv
import datetime
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CanvaCrawler:
    def __init__(self, csv_name, name_folder):
        self.links = []
        self.max_index = 1000
        self.step_index = 50
        self.url = "https://www.canva.com/vi_vn/instagram-story/mau/"
        self.csv_file = f"csv_folder/{csv_name}.csv"
        self.chrome_driver = f"chromedriver.exe'"
        self.path_save = f"images/{name_folder}"

    def get_links(self):
        """
        Because Canva only displays 50 items at a time, you need to run it multiple times to retrieve more items.
        :return: list of link images
        """
        for i in range(0, self.max_index + 1, self.step_index):
            driver = webdriver.Chrome(executable_path=self.chrome_driver)

            url = f"{self.url}?continuation={i}"

            driver.get(url)

            # aiE6Dw.qN_0PQ: this is div class name
            elements = driver.find_elements_by_class_name("aiE6Dw.qN_0PQ")

            for element in elements:
                href = element.get_attribute("href")
                # Since the images in the template start with '/EA,' you need to filter out unnecessary images.
                if '/EA' in href:
                    self.links.append(href)

            driver.quit()

        # Remove duplicate item
        self.links = list(set(self.links))

    def write_csv(self):
        # Open the CSV file in write mode
        with open(self.csv_file, mode='w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write each URL to a separate row
            for url in self.links:
                writer.writerow([url])

    def load_csv(self):
        self.links = []
        # Open the CSV file in read mode
        with open(self.csv_file, mode='r') as file:
            # Create a CSV reader object
            reader = csv.reader(file)

            # Iterate through each row in the CSV file
            for row in reader:
                self.links.append(row[0])

    def download_image(self):
        if not os.path.exists(self.path_save):
            os.makedirs(self.path_save)
        for link in self.links:
            driver = webdriver.Chrome(
                executable_path=self.chrome_driver)

            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y_%m_%d_%H_%M_%S")

            driver.get(link)
            try:
                # E8DoAg: this is a class name cover image information
                downloadable_image = driver.find_element_by_css_selector(".E8DoAg")

                if downloadable_image:
                    # get URL of image
                    image_url = downloadable_image.get_attribute("src")
                    response = requests.get(image_url)
                    with open(f"{self.path_save}/{formatted_date}.png", 'wb') as f:
                        f.write(response.content)
            except NoSuchElementException:
                pass

            driver.quit()


if __name__ == '__main__':
    canva_crawler = CanvaCrawler(csv_name="data", name_folder="data_facebook")
    canva_crawler.get_links()
    canva_crawler.download_image()
