# coding: utf-8
import time
import json
import logging
from selenium import webdriver

logger = logging.getLogger()
# ログレベル設定
# info以下のログレベルのログを削るようにする
logger.setLevel(logging.INFO)

def lambda_handler(event, contxt):
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1200,2000')
    options.add_argument('--blink-settings=imagesEnabled=false')


    driver = webdriver.Chrome(
        executable_path="./bin/chromedriver",
        chrome_options=options
    )

    # logger.info(event['body'])

    driver.get(event["body"])

    time.sleep(0.3)

    if(driver.find_elements_by_class_name('project-title')) == []:
        title = ""
    else:
        title = driver.find_element_by_class_name('project-title').text

    if(driver.find_element_by_xpath('//*[@id="project-show-body"]/div/div[2]/div/section[2]/div/div[1]')) == []:
        support_count = "0"
    else:
        support_count = driver.find_element_by_xpath('//*[@id="project-show-body"]/div/div[2]/div/section[2]/div/div[1]').text
        support_count = support_count.replace('人が応援しています','')

    if(driver.find_element_by_xpath('//*[@id="project-show-header"]/div[1]/div/div[2]/span[2]')) == "":
        total_view = "0"
    else:
        total_view = driver.find_element_by_xpath('//*[@id="project-show-header"]/div[1]/div/div[2]/span[2]').text
        total_view = total_view.replace(' views','')

    if(driver.find_elements_by_class_name('entry-info')) == []:
        entry_count = "0"
    else:
        entry_count = driver.find_element_by_class_name('entry-info').text
        entry_count = entry_count.replace('人がエントリー中','')

    # title = "タイトル"
    # support_count = "10"
    # total_view = "100"
    # entry_count = "10"
    json_data = {
                    'title': title,
                    'supportCount': support_count,
                    'totalView': total_view,
                    'entryCount': entry_count
                }
 
    encode_json_data = json.dumps(json_data, indent=4)

    return {
        "isBase64Encoded" : False,
        'statusCode' : 200,
        'headers' : {
                'access-control-allow-origin' : '*',
                'content-type' : 'application/json'
        },
        'body' :  encode_json_data
    }