# E:\DUT Courses\Thông\fossile-supporter\R.png  
# Read the image, then convert it to base64
import asyncio
import json
import base64

image_link = r"E:\DUT Courses\Thông\fossile-supporter\R.png"

with open(image_link, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode()
print(image_data)