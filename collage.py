import urllib
import requests
import json
import random
from resources import requestspool
from PIL import Image, ImageDraw, ImageFont

def get_page_data(username, timeframe, page_num, fetch_num, API_KEY):
    print("get_page_data")
    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&period="+timeframe+"&page="+str(page_num)+"&api_key="+API_KEY+"&limit="+str(fetch_num)+"&format=json"
    with urllib.request.urlopen(url) as url:
        data = json.load(url)   # loaded as dict
    data = data.get("topalbums").get("album")
    return data

def condense_data(data):
    print("condense_data")
    album_data_list = []
    album_url_list = []
    i = 0
    for album in data:
        i += 1
        playcount = album["playcount"]
        image_url = album["image"][3]["#text"]
        name = album["name"]
        album_data_list.append([playcount, name])
        album_url_list.append(image_url)
    return album_data_list, album_url_list

def request_images(url_list):
    print("request_images")
    pool = requestspool.ImageRequestPool(url_list)
    return pool.output

def join_data(compiled_data, images, hue=False):
    print("join_data")
    new_data = []

    if hue:
        for index in range(len(compiled_data)):
            hue_value = average_colour(images[index][0], 10, boundaries=(0, 299), hue=True)
            compiled_data[index] += [images[index][0], hue_value]
            # compiled_data[index][2] = Image.new("HSV", (300, 300), (int(hue_value), 100, 100))
        compiled_data = sorted(compiled_data, key=lambda x: x[3])

    else:
        for index in range(len(compiled_data)):
            compiled_data[index] += [images[index][0], None]
    return compiled_data

def average_colour(image, reference_point_count, boundaries=(0, 30), hue=False):
    print("average_colour")
    r = []
    g = []
    b = []
    h = []
    colours = []

    if hue:
        image = image.convert("HSV")
        for _ in range(reference_point_count):
            x = random.randint(boundaries[0], boundaries[1])
            y = random.randint(boundaries[0], boundaries[1])

            pixel = image.getpixel((x, y))
            h.append(pixel[0])

        avg_h = (sum(h) / reference_point_count)
        return avg_h

    else:
        for _ in range(reference_point_count):
            x = random.randint(boundaries[0], boundaries[1])
            y = random.randint(boundaries[0], boundaries[1])

            pixel = image.getpixel((x, y))
            r.append(pixel[0] ^ 2)
            g.append(pixel[1] ^ 2)
            b.append(pixel[2] ^ 2)

        avg_r = (sum(r) / reference_point_count)
        avg_g = (sum(g) / reference_point_count)
        avg_b = (sum(b) / reference_point_count)

        return avg_r, avg_g, avg_b

def draw_text_on_cover(album_cover, name, playcount):
    print("draw_text_on_cover")
    try:
        average = sum(average_colour(album_cover, 2)) / 3
    except TypeError:
        average = 1

    if average >= 127.5:
        font_colour = 0, 0, 0, 255
    else:
        font_colour = 255, 255, 255, 255

    font = ImageFont.truetype("resources/arial.ttf", 20)
    draw = ImageDraw.Draw(album_cover)
    draw.text((5,5), name, font=font, fill=(font_colour))
    draw.text((2,25), playcount, font=font, fill=(font_colour))

    return album_cover

def move_coordinates(coordinates, canvas_length):
    print("move_coordinates")
    if coordinates[2] >= canvas_length:
        coordinates = list(coordinates)
        coordinates[0] = 0
        coordinates[1] += 300
        coordinates[2] = 300
        coordinates[3] += 300
        coordinates = tuple(coordinates)
    else:
        coordinates = list(coordinates)
        coordinates[0] += 300
        coordinates[2] += 300
        coordinates = tuple(coordinates)
    return coordinates

def draw_collage(data, size, total, canvas_length):
    print("draw_collage")
    canvas = Image.new('RGB', (canvas_length, canvas_length))
    coordinates = (0, 0, 300, 300)

    for i in range(total):
        album = data[i]
        album_cover = draw_text_on_cover(album[2], album[1], album[0])
        canvas.paste(album_cover, coordinates)
        coordinates = move_coordinates(coordinates, canvas_length)
    return canvas

def collage(username, timeframe, API_KEY, size=7, hue=False):
    compiled_data = []
    compiled_urls = []
    cached_compile_len = -1
    count, fetch_num = 1, 500
    total, canvas_length = size ** 2, size*300

    while len(compiled_data) < total:
        if cached_compile_len == len(compiled_data):    # no progress
            raise IndexError

        cached_compile_len = len(compiled_data)
        print(len(compiled_data), "| page:", count)

        # if we're fetching more than we need; get how much we actually need.
        if fetch_num >= total-len(compiled_data):
            fetch_num = total-len(compiled_data)

        data = get_page_data(username, timeframe, count, fetch_num, API_KEY)
        data, data2 = condense_data(data)
        compiled_data += data
        compiled_urls += data2
        count += 1

    images = request_images(compiled_urls)
    final_data = join_data(compiled_data, images, hue=hue)

    collage = draw_collage(final_data, size, total, canvas_length)
    return collage

if __name__ == "__main__":
    with open("resources/keys.txt", "r") as f:
        LASTFM_KEY = f.readline().split("=")[1].strip("\n")
    collage = collage("shktv", "overall", LASTFM_KEY, size=30)
    collage.show()
