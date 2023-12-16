from browsermobproxy import Server
from selenium import webdriver
import json
import csv 

# create a browsermob server instance
server = Server("/Users/evant/Documents/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy(params=dict(trustAllServers=True))
print(f"Proxy is listening on port: {proxy.port}")

# create a new chromedriver instance
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(10)

for i in range(1000):
    with open('top-1m.csv') as file:
        reader = csv.reader(file)
        # Replace x to start parsing the csv at that line number
        # for _ in range(x - 1):
        #     next(reader, None)
        
        for row in reader:
            retry_count = 3
            while retry_count > 0:
                try:
                    proxy.new_har(str(row[0]), options = {'captureHeaders': True, 'captureCookies': True})
                    driver.get("http://www."+str(row[1]))

                    with open(str(row[0])+".har", 'w') as f:
                        f.write(json.dumps(proxy.har))
                    
                    print(f"Processed: {row[0]}")
                    break
                except:
                    retry_count -= 1
                    if retry_count != 0:
                        print(f"Error processing {row[0]}. Retrying...")
                    elif retry_count == 0:
                        with open("missing_indices.txt", "a") as m:
                            m.write(f"{row[0]}, ")
                        print(f"Error: Unable to process {row[0]}")

# stop server and exit
server.stop()
driver.quit()