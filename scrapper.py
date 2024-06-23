import sys
import os
import re
import csv

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def get_tor_session():
    import requests
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

def torSearcher(url):
    import requests
    import random

    session = get_tor_session()

    print("Getting ...", url)
    result = session.get(url).text

    emails = extract_emails(result)

    import string
    filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    with open(f"{filename}.txt", "w+", encoding="utf-8") as newthing:
        newthing.write(result)
    
    return emails

def main():
    programname = os.path.basename(sys.argv[0])
    try:
        filename = 'urls.txt'
        print("Opening ...", filename)
        with open(filename, "r", encoding="utf-8") as newfile:
            data = newfile.readlines()
            all_emails = []
            try:
                for k in data:
                    k = k.replace("\n", "")
                    emails = torSearcher(k)
                    for email in emails:
                        all_emails.append((k, email))
            except Exception as E:
                print(E)
            
            if all_emails:
                with open('emails.csv', 'w', newline='') as csvfile:
                    email_writer = csv.writer(csvfile)
                    email_writer.writerow(['URL', 'Email'])
                    for url, email in all_emails:
                        email_writer.writerow([url, email])

    except:
        print("Usage : {} <newlineSeperatedList.txt>".format(programname))

if __name__ == "__main__":
    main()
