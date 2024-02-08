# from aikitchen.music import Music
# from aikitchen.login import Login
# from aikitchen.image import Image
from AIKitchen_API.AIKitchen import Music, Login, Image
# Create a new instance of Music
login = Login()
token = login.token
music = Music()

input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2, token)

if isinstance(tracks, list):
    music.b64toMP3(tracks, input,)


image = Image()

input = 'Silver coin with an smiling cat, words " 5 catnips" "handmade"'
images = image.get_image(input, 3, token)

if isinstance(images, list):
    image.b64toImg(images, input)