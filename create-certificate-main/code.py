from PIL import Image, ImageFont, ImageDraw
import openpyxl

mssv = 19521317
hovaten = "Nguyễn Khải Đăng"

my_background = Image.open("chungnhanv2.png")
text_font = ImageFont.truetype('Montserrat_seminobold.TTF', 45)
text_hoten = hovaten
text_mssv = str(mssv)
image_editable = ImageDraw.Draw(my_background)
image_editable.text((600,510), text_hoten,(0,0,0), font = text_font)
image_editable.text((600,610), text_mssv,(0,0,0), font = text_font)
my_background.save(str(mssv) + ".png")
print("Đã tạo: " + str(mssv))







