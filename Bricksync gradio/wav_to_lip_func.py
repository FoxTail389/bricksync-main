from allosaurus.app import read_recognizer
from moviepy.editor import *
import random
from PIL import Image
import numpy as np
import math
from itertools import zip_longest
from copy import deepcopy
from tkinter.filedialog import askopenfilename, asksaveasfilename


def mask_eyes(output_folder, initial_clip, pixel_length, box_dimensions,height):
    eyes_clip = ImageClip(np.array(cylindrical_projection(Image.open(f"{output_folder}/Eyes.png").crop(box_dimensions), pixel_length)))
    eyes_closed_clip = ImageClip(np.array(cylindrical_projection(Image.open(f"{output_folder}/Eyes Closed.png").crop(box_dimensions), pixel_length)))
    eyebrows_clip = ImageClip(np.array(cylindrical_projection(Image.open(f"{output_folder}/Eyebrows.png").crop(box_dimensions), pixel_length)))
    
    blinking = []
    blinking_duration = 0.0
    while True:
        open_duration = random.uniform(2, 5)
        blinking.append(eyes_clip.set_duration(open_duration))
        blinking_duration += open_duration
        if blinking_duration >= initial_clip.duration:
            break
        else:
            close_duration = random.uniform(0.05, 0.075)
            blinking.append(eyes_closed_clip.set_duration(close_duration))
            blinking_duration += close_duration
    
    blinking_clip = concatenate_videoclips(blinking, method="compose").set_duration(initial_clip.duration)

    final_clip = CompositeVideoClip([
        initial_clip,
        eyebrows_clip,
        blinking_clip
    ]).set_duration(initial_clip.duration) 
    return final_clip

def wav_to_legomp4(wav_file, gender, eyes, pixel_length, left_pixel,height):
    box_dimensions = [left_pixel, 0, left_pixel + 2000, 1000]
    model = read_recognizer()
    model_output = model.recognize(wav_file, 'eng', timestamp=True)
    formatted_output = [p.split() for p in model_output.splitlines()]
    
    phone_sets = [
        {'a', 'aː', 'æ', 'ɛ', 'ɛː', 'ʔ'},
        {'e', 'eː', 'i', 'iː', 'ʃ'},
        {'e̞', 'ɘ', 'ʌ', 'b', 'v', 'θ'},
        {'o', 'oː', 'øː', 'ɐː', 'ɜː', 'ɵː', 'p', 'pʰ'},
        {'u', 'uː', 'ɑ', 'ɑː', 'ɒ', 'ɒː', 'ɔ', 'ɔː', 'ʉ', 'ʉː'},
        {'ɐ', 'h', 't', 'tʰ', 't̠', 'z', 'ŋ'},
        {'ə', 'əː', 'f', 'k', 'kʰ', 'w', 'ɹ', 'ʍ'},
        {'ɪ', 'ɪ̯', 'd', 'd̠', 'n', 'r', 'x', 'ɡ', 'ʒ'},
        {'ɯ', 'ʊ'},
        {'j', 'l'},
        {'s', 'ð', 'ɻ'},
        {'m'}
    ]
    
    image_list = []
    for i, phone_set in enumerate(phone_sets):
        out_folder = "man out" if gender == "Male" else "woman out"
        image = cylindrical_projection(
            Image.open(f"{out_folder}/{i}.png").crop(box_dimensions),
            pixel_length
        )
        print(i)
        image_list.append(image)
    
    picture_list = []
    for phone in formatted_output:
        for i, phone_set in enumerate(phone_sets):
            if phone[2] in phone_set:
                picture_list.append([phone[0], phone[1], image_list[i]])
    
    audio_clip = AudioFileClip(wav_file)
    clips = []
    for i, m in enumerate(picture_list):
        if i == len(picture_list) - 1:
            clips.append(ImageClip(np.array(m[2])).set_duration(audio_clip.duration - float(m[0])))
        else:
            next_item = picture_list[i + 1]
            clips.append(ImageClip(np.array(m[2])).set_duration(float(next_item[0]) - float(m[0])))
    
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.audio = audio_clip
    
    if eyes:
        return mask_eyes(out_folder, concat_clip, pixel_length, box_dimensions,height)
    else:
        return concat_clip

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def formula(x, a, b):
    return (b / a) * math.sqrt(a ** 2 - (x - a) ** 2)

def cylindrical_correction(image: Image.Image, slanted_number: int, left_direction: bool, up_direction: bool):
    if slanted_number == 0:
        return image
    
    rotation_angle = -90 if left_direction else 90
    image_rotated = image.rotate(rotation_angle, expand=True)
    new_image = image_rotated.crop([slanted_number if left_direction else 0, 0, 1000 if left_direction else 1000 - slanted_number, 500])
    blank_image = image_rotated.crop([0 if left_direction else 1000 - slanted_number, 0, slanted_number if left_direction else 1000, 500])
    
    blank_image_data = list(grouper(blank_image.getdata(), int(slanted_number)))
    image_width = image_rotated.height
    new_array = list(grouper(new_image.getdata(), 1000 - slanted_number))
    
    array = []
    for x, row in enumerate(new_array):
        y = slanted_number - round(formula(x, image_width, slanted_number)) if not left_direction else round(formula(x, image_width, slanted_number))
        y = slanted_number - y if not up_direction else y
        blank_row = blank_image_data[x]
        start = blank_row[0:y]
        end = blank_row[y:slanted_number]
        array.extend(start)
        array.extend(row)
        array.extend(end)
    
    image_rotated.putdata(array)
    image_out = image_rotated.rotate(-rotation_angle, expand=True)
    return image_out

def cylindrical_warp(image: Image.Image, left_direction: bool):
    rotation_angle = -90 if left_direction else 90
    im_rotated = image.rotate(rotation_angle, expand=True)
    image_width = im_rotated.width
    pixel_angle = float(90 / image_width)
    numpy_data = np.asarray(im_rotated)
    list1 = numpy_data.tolist()
    list123 = []
    
    for i, data in enumerate(list1):
        ppw = i + 1
        angle = pixel_angle * ppw
        new_image_width = image_width / 2
        hype = 2 * new_image_width * (math.sin(math.radians(angle / 2.0)) ** 2)
        list123.append(round(hype))
    
    pi = []
    for i in range(int(image_width / 2)):
        x = deepcopy(list123)
        x.reverse()
        pixel_index = len(x) - x.index(i)
        pi.append(pixel_index)
    
    new_image = Image.fromarray(np.array([numpy_data[i] for i in pi]))
    return new_image.rotate(-rotation_angle, expand=True)

def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def pixels_to_angle(pixel_num, image_height):
    distance_from_bottom = image_height - pixel_num
    angle = math.degrees(math.acos(distance_from_bottom / image_height))
    return angle

def slanted_warp(image: Image.Image, slanted_number: int):
    image_height = image.height
    pixel_angle = pixels_to_angle(slanted_number, image_height)
    numpy_data = np.asarray(image)
    list1 = numpy_data.tolist()
    list123 = []
    
    for i, data in enumerate(list1):
        pph = i + 1
        hype = pph * math.cos(math.radians(pixel_angle))
        list123.append(round(hype))
    
    pi = []
    for i in range(int(image_height)):
        x = deepcopy(list123)
        x.reverse()
        if i + 1 in list123:
            pixel_index = len(x) - x.index(i + 1)
            pi.append(pixel_index)
        else:
            pi.append(-1)
    
    black_image = Image.fromarray(np.ones((pi.count(-1), image_height, 3), np.uint8))
    rgba_black = black_image.convert("RGBA")
    new_data = [(255, 255, 255, 0) for _ in black_image.getdata()]
    rgba_black.putdata(new_data)
    new_image = Image.fromarray(np.array([numpy_data[i - 1] for i in pi if i != -1]))
    new_image_converted = new_image.convert("RGBA")
    return get_concat_v(new_image_converted, rgba_black)

def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def cylindrical_projection(image, pixel_length):
    image_left = image.crop([0, 0, 1000, 1000])
    image_right = image.crop([1000, 0, 2000, 1000])
    slanted_angle = abs(pixel_length)
    up_direction = True if pixel_length > 0 else False
    
    new_image_left = cylindrical_correction(slanted_warp(cylindrical_warp(image_left, True), slanted_angle), slanted_angle, True, up_direction)
    new_image_right = cylindrical_correction(slanted_warp(cylindrical_warp(image_right, False), slanted_angle), slanted_angle, False, up_direction)
    
    final_image = get_concat_h(new_image_left, new_image_right)
    return final_image
def wave_complete_mp4(wav:str,image_mask:ImageClip,gender:str, left_pixel:int,points:tuple[tuple[int]]):
    x1,y1 = points[0]
    x2,y2 = points[1]
    width = int(math.sqrt((x1-x2)**2+(y1-y2)**2))
    x3,y3 = points[2]
    x4,y4 = ((x1+x2)/2,(y1+y2)/2)
    pixel_distance = int(math.sqrt((x3-x4)**2+(y3-y4)**2))
    s = int((1000/width)*pixel_distance)
    lego_face_mask:VideoClip = wav_to_legomp4(wav,gender,True,s,left_pixel,width)
    print(1234)
    n= lego_face_mask.set_opacity(0.85).resize(height=width)
    final_clip:VideoClip = CompositeVideoClip([
        image_mask,
        n.set_position((x1,y1-width+(width/8)))
    ]).set_duration(lego_face_mask.duration)
    return final_clip
