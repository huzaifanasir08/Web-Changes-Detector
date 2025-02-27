from django.shortcuts import render, redirect
from .models import Check
from manage_web.models import Web
import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crawl4ai import AsyncWebCrawler
from asgiref.sync import sync_to_async
from datetime import datetime
import time
import asyncio

def fetch_web_list():
    try:
        return list(Web.objects.all())  # Convert QuerySet to a list
    except Exception as e:
        return []


def fetch_old_checks():
    try:
        return list(Check.objects.all())  # Convert QuerySet to a list
    except Exception as e:
        return []


async def get_hash_code(url):
    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
    # Create an instance of AsyncWebCrawler
            result = await crawler.arun(url=url)
            # Access different formats
            raw_html = result.html
            # Get the hash value of the HTML content
            hash_value = hashlib.sha256(raw_html.encode('utf-8')).hexdigest()
            return hash_value
    except requests.RequestException as e:
        return None


def get_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            cleaned_content = response.content.decode('utf-8').replace('\r\n', '')
            return cleaned_content
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None



def get_check_by_id(id):
    # Use filter instead of get_object_or_404 to avoid the exception and handle cases where no match is found
    return Check.objects.filter(pk=id).first()  # Returns None if no match


def perform_check(original_hash, check_id, id):
    # Get the check by ID to update the status
    web_info = get_check_by_id(check_id)
    original = True
    Available = True
    # Check if the check exists
    if web_info:
        # Perform the check for each URL    
        for url, hash in original_hash.items():
            if hash:
                current_hash = asyncio.run(get_hash_code(url))
                if current_hash:
                    status = 'Online'
                    print(f'Working on: {url}')
                    print(current_hash)
                    print(hash)
                    if current_hash != hash:
                        original = False
                        result = 'Changes Detected'
                        print('Not Same')
                        # if any changes are detected in any web page exit the loop
                        break
                    else:
                        print('Same')
                        original = True
                else:
                    Available = False
                    break

        if original:
            # If the original is True, it means no changes were detected in any of the web pages, update the status with 'No changes'
            print('Same...')
            # status_update(web_info, 'Online', 'No Changes', '')
        elif Available:
            # If the original is False and Available is True, it means changes were detected in any of the web pages, update the status with 'Changes Detected'
            print('Not Same...')
            # status_update(web_info, 'Online', 'Changes Detected', '')  
        else:
            # If the original is False and Available is False, it means the website is not online, update the status with 'Not Online', and result with 'Not Tested'
            print('Not Online...')
            # status_update(web_info, 'Not Online', 'Not Tested', '')  
    else:
        pass # Print message if no Check is found


def new_check(web_id, urls):
    # Create a dictionary to store the all the URLs and their hash values
    json_urls = {}
    for url in urls:
        link = url["href"]
        # Get the hash value of the URL
        current_hash = asyncio.run(get_hash_code(link)) 
        if current_hash:
            json_urls[f"{link}"] = current_hash
        else:
            pass

    status = 'Online'
    result = 'New Entry'
    # Insert the new check into the database or txt file or any other storage
    # new_entry(Check, web_id, json_urls, status, result)


def status_update(web_info, status, result, content):
    try:
        now = datetime.now()
# Format the date and time with AM/PM
        formatted_time = now.strftime("%Y-%m-%d %I:%M:%S %p") 
        web_info.status = status
        web_info.result = result
        web_info.content = content if content else 'N/A'    
        web_info.last_check = formatted_time
        web_info.save()
        print('Updated')
    except Exception as e:
        print(f'Error: {e}')
        # pass


def new_entry(obj, id, json_urls, status, result):
    try: 
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %I:%M:%S %p")
        content = 'None'
        new_web = obj(
            original_hash=json_urls,
            status=status,
            result=result,
            content=content,
            web_name_id=id,         
            last_check=formatted_time,
        )
        new_web.save()
        print('Inserted...')
    except Exception as e:
        print(f'Error: {e}...')


async def get_all_links(base_url):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=base_url, fit_markdown=True)
        internal_links = result.links.get("internal", [])
        return internal_links


def check_start():
    print('Started...')
    # Fetch data
    web_list = fetch_web_list()
    web_checks = fetch_old_checks()
    # Or you can use the following code
    # web_list = [{'id': 1, 'web_name': 'Google', 'web_url': 'https://www.google.com'}, {'id': 2, 'web_name': 'Facebook', 'web_url': 'https://www.facebook.com'}, {'id': 3, 'web_name': 'Twitter', 'web_url': 'https://www.twitter.com'}]
    # web_checks = [{'id':1, 'original_hash': {'https://www.google.com': 'hash1'}, 'status': 'Online', 'result': 'No Changes', 'content': 'None', 'web_name_id': 1, 'last_check': '2021-09-01 12:00:00 PM'}, {'id':2, 'original_hash': {'https://www.facebook.com': 'hash1'}, 'status': 'Online', 'result': 'No Changes', 'content': 'None', 'web_name_id': 2, 'last_check': '2021-09-01 12:00:00 PM'}, {'id':3, 'original_hash': {'https://www.twitter.com': 'hash1'}, 'status': 'Online', 'result': 'No Changes', 'content': 'None', 'web_name_id': 3, 'last_check': '2021-09-01 12:00:00 PM'}]

    # Loop through the websites and perform the check after you get the data and according to the structure of the data manage th code
    for web in web_list:
        id = web.id
        name = web.web_name
        url = web.web_url
        try:
            # Let's check if the check exists meaning we have already checked this website or it's a new website
            found = False
            for checks in web_checks:
                if id == checks.web_name_id:                   
                    print('Check Found...')
                    original_hash = checks.original_hash
                    # Perform the check
                    perform_check(original_hash, checks.id, checks.web_name_id)
                    found = True
                    break

            # If no check found
            if not found:
                print('Check not found...')
                # Get all internal links of the website
                links =  asyncio.run(get_all_links(url))
                # add base url to the links so that we can check the home page as well
                base = {'href': url, 'text': 'home', 'title': ''}
                links.append(base)
                print(f'Length: {len(links)}')
                new_check(id, links)
            # Sleep for 5 seconds before checking the next website
            print('Sleeping for 5...')
            time.sleep(5)
            print('Waked up...')

        except Exception as e:
            print(f'Error: {e}')
            time.sleep(5)
