from PIL import Image, ImageOps, ImageFont, ImageDraw
import random

IMAGE = Image.open('app/image_processing/BaseDefaultProfile.png').convert("L")
COLORS = [(255, 0, 0), (255, 196, 0), (0, 110, 255),
          (138, 64, 207), (207, 64, 138), (75, 115, 2)]
FONT = ImageFont.truetype('app/image_processing/ARIALBD.TTF', 32)

def createDefaultProfile(user_name):
    colorpicker = COLORS[random.randint(0,len(COLORS)-1)]
    profile_pic = ImageOps.colorize(IMAGE, colorpicker, colorpicker)
    write_name = ImageDraw.Draw(profile_pic)
    write_name.text((30,18), user_name[0], (255,255,255), FONT)
    result_url = f'media/images/profiles/{user_name}.png'
    profile_pic.save(result_url)
    return result_url.split('media/')[1]

