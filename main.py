import os
from xml.etree import ElementTree
from PIL import Image
import cv2


def create_img_xml(path_to_img, duration=15):
    images_list = []

    for obj in os.listdir(path_to_img):
        if obj[-3:] == 'jpg' or obj[-3:] == 'png' or obj[-4:] == 'jpeg':
            images_list.append(path_to_img + obj)

    images_list.sort()

    xml_parent = ElementTree.Element('background')

    for image in images_list:
        xml_static = ElementTree.SubElement(xml_parent, 'static')
        xml_static_duration = ElementTree.SubElement(xml_static, 'duration')
        xml_static_file = ElementTree.SubElement(xml_static, 'file')
        xml_static_duration.text = str(duration) + '.0' if duration == int(duration) else str(duration)
        xml_static_file.text = str(os.path.abspath(image))

    xml_tree = ElementTree.ElementTree(xml_parent)
    xml_tree.write(path_to_img + 'wallpapers_list.xml')


def create_gif_xml(path_to_gif):
    path_to_frames_folder = path_to_gif[:-(len(os.path.basename(path_to_gif)))] + os.path.basename(path_to_gif)[:-4]
    os.mkdir(path_to_frames_folder)
    with Image.open(path_to_gif) as gif:
        for frame in range(1000):
            try:
                gif.seek(frame)
                gif.save(path_to_frames_folder + f'/{frame}.png')
            except EOFError:
                break

    create_img_xml(path_to_frames_folder + r'/', 0.5)


def create_mp4_xml(path_to_mp4):
    path_to_frames_folder = path_to_mp4[:-(len(os.path.basename(path_to_mp4)))] + os.path.basename(path_to_mp4)[:-4]

    os.mkdir(path_to_frames_folder)

    mp4_cap = cv2.VideoCapture(path_to_mp4)
    frame_count = int(mp4_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame in range(frame_count):
        ret, frame_image = mp4_cap.read()
        if frame % 16 == 0:
            cv2.imwrite(path_to_frames_folder + f'/{frame}.png', frame_image)

    mp4_cap.release()

    create_img_xml(path_to_frames_folder + r'/', 0.5)


DEFAULT_PATH_TO_IMG = r'../../Pictures/Walls/'
DEFAULT_PATH_TO_GIF = r'../../Pictures/Walls/skelets.gif'
DEFAULT_PATH_TO_MP4 = r'../../Pictures/Walls/Pexels Videos 1654216.mp4'
# create_img_xml(DEFAULT_PATH_TO_IMG)
# create_gif_xml(DEFAULT_PATH_TO_GIF)
create_mp4_xml(DEFAULT_PATH_TO_MP4)
