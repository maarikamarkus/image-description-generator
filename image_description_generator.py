import io
import json
import os

import openai
import requests
from dotenv import load_dotenv
from google.cloud import vision
from PIL import ExifTags, Image

load_dotenv()

GOOGLE_API_KEY = os.environ.get('google_api_key')
OPENAI_API_KEY = os.environ.get('openai_api_key')

def get_img_keywords(file_name):
  client = vision.ImageAnnotatorClient()
  file_name = os.path.abspath(file_name)

  with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
  
  image = vision.Image(content=content)

  response = client.label_detection(image=image)
  labels = response.label_annotations
  labels = list(map(lambda x : x.description.lower(), labels))
  
  return labels

def get_img_location(path):
  img = Image.open(path)
  exif_data = img._getexif()

  if exif_data is None:
    return (None, None)

  exif = {
    ExifTags.TAGS[k]: v 
    for k, v in exif_data.items()
    if k in ExifTags.TAGS
  }
  
  if 'GPSInfo' not in exif:
    return (None, None)

  gps_info = exif['GPSInfo']
  if gps_info == None:
    return (None, None)

  lat, lng = to_decimal(gps_info[2]), to_decimal(gps_info[4])
  if gps_info[1] == 'S':
    lat *= -1
  elif gps_info[3] == 'W':
    lng *= -1  

  return (lat, lng) 

def to_decimal(x):
  deg, mins, secs = x
  return float(deg + mins/60 + secs/60/60)

def get_address(path):
  lat, lng = get_img_location(path)
  if lat is None:
    return None

  r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}').json()
  #with open('data_2.json', 'w') as f:
  #  f.write(json.dumps(r))
  #with open('data_2.json') as f:
  #  r = json.loads(f.read())

  if r['status'] != "OK":
    return None

  return [comp['long_name'] for comp in r['results'][0]['address_components'] \
    if 'country' in comp['types'] or 'locality' in comp['types']]
  #print(json.dumps(r, indent=2))

def get_img_desc(img_path):
  img_keywords = get_img_keywords(img_path)
  loc_keywords = get_address(img_path)

  print("Img keywords:", img_keywords)
  print("Loc keywords:", loc_keywords)

  #loc_keywords = ['Kõpu', 'Estonia']
  #img_keywords = ['sunny', 'lighthouse', 'tree']
  
  openai.api_key = OPENAI_API_KEY

  if loc_keywords is None:
    prompt = f"Describe picture using keywords: {', '.join(img_keywords)}"
  else:
    prompt = f"Describe picture taken at {', '.join(loc_keywords)} using keywords: {', '.join(img_keywords)}"

  response = openai.Completion.create(
    engine="davinci-instruct-beta-v3", 
    prompt=prompt,
    max_tokens=100
  )

  desc = response['choices'][0]['text'].strip()
  print(desc)
  return desc

#get_address()
#print(get_img_location())
#get_img_desc()

#print(get_img_keywords('C:\\Users\\maarikam\\kool\\tehisintellekt\\kodu7\\maarika-kopu-tuletorn.jpeg'))
