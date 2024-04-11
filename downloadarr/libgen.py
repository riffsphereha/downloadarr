import re
from bs4 import BeautifulSoup
import requests
import os

def search_libgen(book):
    try:
        item = book
        found_links = []
        non_standard_chars_pattern = r"[^a-zA-Z0-9\s.]"
        item = item.replace("ø", "o")
        cleaned_string = re.sub(non_standard_chars_pattern, "", item)
        search_item = cleaned_string.replace(" ", "+")
        url = "http://libgen.is/fiction/?q=" + search_item
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.find_all(class_="record_mirrors_compact")

            for element in elements:
                links = element.find_all("a", href=True)
                for link in links:
                    href = link["href"]
                    if href.startswith("http://") or href.startswith("https://"):
                        found_links.append(href)
        else:
            ret = {"Status": "Error", "Code": "Libgen Connection Error"}
            print("Libgen Connection Error: " + str(response.status_code) + "Data: " + response.text)

    except Exception as e:
        print(str(e))
        raise Exception("Error Searching libgen: " + str(e))

    finally:
        return found_links

def download_from_libgen(link, full_filename):
    response = requests.get(link, timeout=120)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        download_div = soup.find("div", id="download")

        if download_div:
            download_link = download_div.find("a")
            if download_link:
                link_url = download_link.get("href")
            else:
                return "Dead Link"
        else:
            elements_with_get = soup.find_all(string=lambda text: "GET" in text)

            for element_text in elements_with_get:
                parent_element = element_text.parent
                download_link = parent_element.find("a") if parent_element else None
                if download_link:
                    link_url = download_link.get("href")
                    break
            else:
                return "Dead Link"

        dl_resp = requests.get(link_url, stream=True)

        if dl_resp.status_code == 200:
            file_type = os.path.splitext(link_url)[1]
            valid_book_extensions = [".pdf", ".epub", ".mobi", ".azw", ".djvu"]
            if file_type not in valid_book_extensions:
                return "Wrong File Type"

            # Download file
            full_filename += file_type
            with open(full_filename, "wb") as f:
                for chunk in dl_resp.iter_content(chunk_size=1024):
                    f.write(chunk)
            return "Success", full_filename
        else:
            return str(dl_resp.status_code) + " : " + dl_resp.text, full_filename
    else:
        return str(response.status_code) + " : " + response.text, full_filename