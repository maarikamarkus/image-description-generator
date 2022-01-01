import os
import openai
import io
from PIL import Image, ExifTags
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get('google_api_key')
OPENAI_API_KEY = os.environ.get('openai_api_key')

def get_img_location():
  img = Image.open("test.jpg")
  exif_data = img._getexif()

  exif = {
    ExifTags.TAGS[k]: v 
    for k, v in exif_data.items()
    if k in ExifTags.TAGS
  }

  gps_info = exif['GPSInfo']
  return (to_decimal(gps_info[2]), to_decimal(gps_info[4]))

def to_decimal(x):
  deg, mins, secs = x
  return float(deg + mins/60 + secs/60/60)

def get_img_desc():
  openai.api_key = OPENAI_API_KEY

  response = openai.Completion.create(
    engine="davinci-instruct-beta-v3", 
    prompt="Describe picture taken at Kõpu, Estonia using keywords: sunny, lighthouse, sky, tree, tower",
    max_tokens=100
  )

  print(response['choices'][0]['text'].strip())


def get_address():
  lat, lng = get_img_location()
  #r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}').json()
  #with open('data_2.json', 'w') as f:
   # f.write(json.dumps(r))
  with open('data_2.json') as f:
    r = json.loads(f.read())

  if r['status'] != "OK":
    return None

  print([comp['long_name'] for comp in r['results'][0]['address_components'] \
    if 'country' in comp['types'] or 'locality' in comp['types']])
  #print(json.dumps(r, indent=2))


#get_address()
#print(get_img_location())
get_img_desc()

