"""
install in venv pip3 PILLOW and pytesseract then
to use tesseract in linux install the binary:
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
sudo apt-get install tesseract-ocr-spa
"""

from pytesseract import image_to_string
from PIL import Image
import pytesseract
import argparse
import json
import os


def scrap_instagram(account_name, maximum=None, type=None, ):
    maximum_arg,type_arg,latest_arg = "","",""
    if maximum != None:
        maximum_arg = "-m "+str(maximum)
    if type != None:
        type_arg = "-t "+str(type)
    options = " "+maximum_arg+" "+type_arg+" "+latest_arg+" "+"--media-metadata --latest"
    terminal_command = "instagram-scraper " + account_name + options
    os.system(terminal_command)


def image_to_string(img_path):
    pytesseract.pytesseract.tesseract_cmd = 'D:/Tesseract/tesseract'
    TESSDATA_PREFIX = 'D:/Tesseract'
    return pytesseract.image_to_string(Image.open(img_path).convert("RGB"), lang="spa")


def read_json_file(file_path):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def get_url_from_json(img_id, json_file):
    data = read_json_file(json_file)["GraphImages"]
    shortcode = ""
    url = ""
    for img in data:
        if img_id in img["display_url"]:
            shortcode = img["shortcode"]
            break
    if shortcode != "":
        url = "https://www.instagram.com/p/"+shortcode+"/"
    return url


def get_post_content_from_json(img_id, json_file):
    data = read_json_file(json_file)["GraphImages"]
    post_caption = ""
    for img in data:
        if img_id in img["display_url"]:
            for edge in img["edge_media_to_caption"]["edges"]:
                post_caption += edge["node"]["text"]+" "
    return post_caption


def images_to_json(account_name):
    data = {
        "account" : account_name,
        "media":[]
        }
    for root, dirs, files in os.walk(account_name):
        json_file = account_name + "/" + account_name+".json"
        for file in files:
            file_path_splited = os.path.splitext(file)
            file_name,file_extension  = file_path_splited[0],file_path_splited[1]
            if file_extension not in [".json", ".mp4"]:
                media = {
                    "id" : file_name,
                    "url" : get_url_from_json(file_name, json_file),
                    "post_caption" : get_post_content_from_json(file_name, json_file),
                    "img_text_content" : image_to_string(account_name+"/"+file)
                    }
                data["media"].append(media)
    return data


def write_json_output_file(data, detination_path):
    with open(detination_path+'.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__== "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--account', help='Is the instagram account name to scrape')
    parser.add_argument('--maximum', '-m', help='Is the maximum number of items to scrape')
    parser.add_argument('--type', '-t', help='Specify media types to scrape. Enter as space separated values. Valid values are image, video, story (story-image & story-video), or none. Stories require a --login-user and --login-pass to be defined.')
    args=parser.parse_args()
    if args.account != None:
        instagram_acount = args.account
        scrap_instagram(instagram_acount, args.maximum, args.type)
        data = images_to_json(instagram_acount)
        write_json_output_file(data,instagram_acount+"_data")
    else:
        print("Error: account arg must be entered (python3 main.py --account <instagram_account_name>)")
