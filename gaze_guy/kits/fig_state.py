from PIL import Image

path = '/Users/lucas/Downloads/01/face_img/1680843936562.jpg'
img = Image.open(path)
exif_data = img._getexif()
ImageDate = exif_data[306]

print(ImageDate)