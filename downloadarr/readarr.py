import requests
import os
import time

import libgen
import functions

def create_author_dir(base_dir, author, title):
    author = functions.string_cleaner(author)
    title = functions.string_cleaner(title)
    author_dir = os.path.join(base_dir, "ebook", author, title)
    os.makedirs(author_dir, exist_ok=True)
    return author_dir

def create_readarr_dir(base_dir, author):
    author = functions.string_cleaner(author)
    author_dir = os.path.join(base_dir, "ebook", author)
    return author_dir

def create_file_name(folder_path, author, title):
    author = functions.string_cleaner(author)
    title = functions.string_cleaner(title)
    filename = author + " - " + title
    return os.path.join(folder_path, filename)

def process_book(readarr_url, api_key, folder_path):
    headers = {
        'X-Api-Key': api_key,
    }
    
    # Endpoint to initiate folder import scan in Readarr
    endpoint = f"{readarr_url}/api/v1/command"
    
    payload = {
        "name": "DownloadedBooksScan",
        "path": folder_path
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 201:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False

def get_wanted_books(readarr_url, api_key):
    params = {
        "apikey": api_key, 
        "pageSize": 250,
    }
    # Endpoint to get wanted books in Readarr
    endpoint = f"{readarr_url}/api/v1/wanted/missing"
    
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            wanted_books = response.json()
            return wanted_books["records"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

def libgen_download_missing_books(readarr_url, readarr_api_key, downloaddir, readarr_rootdir, importdelay):
    wanted_books = get_wanted_books(readarr_url, readarr_api_key)
    if wanted_books:
        print(f"Wanted Books ({len(wanted_books)}):")
        for book in wanted_books:
            title = book["title"]
            author_and_title = book["authorTitle"]
            author_reversed = author_and_title.replace(title, "")
            author_with_sep = author_reversed.split(", ")
            author = "".join(reversed(author_with_sep))
            book = (f"{author} -- {title}")
            
            print(f"Searching for {author} - {title}")

            search_result = libgen.search_libgen(book)
            if search_result:
                print (f"  Found {len(search_result)} links, attempt downloads")
                author_dir = create_author_dir(downloaddir, author_reversed, title)
                readarr_dir = create_readarr_dir(readarr_rootdir, author_reversed)
                full_filename = create_file_name(author_dir, author_reversed, title)
                for link in search_result:
                    print (f"    Downloading {link}: ", end='')
                    ret, full_filename = libgen.download_from_libgen(link,full_filename)
                    print(ret)
                    if ret == "Success":
                        print(f"      Importing {author} - {title} into readarr")
                        process_book(readarr_url, readarr_api_key, readarr_dir)
                        print(f"      Giving readarr {importdelay} seconds to process")
                        time.sleep(importdelay)
                        if functions.check_file_existence(full_filename):
                            print(f"      {full_filename} not imported")
                            print(f"      Try increasing the importdelay or try to manually import")
                        else:
                            print(f"      {full_filename} succesfully imported")
                        break
            else:
                print(f"  No matching links found")

