from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]

req_image = []
final_text = ''

image_pdf = Image(filename="./tst.pdf", resolution=300)
image_jpeg = image_pdf.convert('jpeg')
print ('appending imgs')
for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))
print ('img ----> string')
for img in req_image: 
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    final_text=final_text+txt

file = open('testfile.txt','w') 
 
file.write(final_text)

#file.close() 
print (final_text)