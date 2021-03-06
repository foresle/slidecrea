import datetime
import os
import time
from xml.etree import ElementTree
from PIL import Image
# import cv2
from slidecrea import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
# import sys


def create_img_xml(path_to_img, progress_bar, duration=15):
    path_to_img = path_to_img + '/'
    images_list = []

    duration = duration*60

    for obj in os.listdir(path_to_img):
        if obj[-3:] == 'jpg' or obj[-3:] == 'png' or obj[-4:] == 'jpeg':
            images_list.append(path_to_img + obj)

    images_list.sort()

    xml_parent = ElementTree.Element('background')

    progres_value = 1
    progress_bar.setValue(progres_value)
    progres_deltax = int(100/len(images_list))

    xml_start_time = ElementTree.SubElement(xml_parent, 'starttime')
    xml_start_time_year = ElementTree.SubElement(xml_start_time, 'year')
    xml_start_time_month = ElementTree.SubElement(xml_start_time, 'month')
    xml_start_time_day = ElementTree.SubElement(xml_start_time, 'day')
    xml_start_time_hour = ElementTree.SubElement(xml_start_time, 'hour')
    xml_start_time_minute = ElementTree.SubElement(xml_start_time, 'minute')
    xml_start_time_second = ElementTree.SubElement(xml_start_time, 'second')
    datetime_now = datetime.datetime.now()
    xml_start_time_year.text = str(datetime_now.strftime('%Y'))
    xml_start_time_month.text = str(datetime_now.strftime('%m'))
    xml_start_time_day.text = str(datetime_now.strftime('%d'))
    xml_start_time_hour.text = str(datetime_now.strftime('%H'))
    xml_start_time_minute.text = '00'
    xml_start_time_second.text = '00'

    image_id = 0
    for image in images_list:
        xml_static = ElementTree.SubElement(xml_parent, 'static')
        xml_static_duration = ElementTree.SubElement(xml_static, 'duration')
        xml_static_file = ElementTree.SubElement(xml_static, 'file')
        xml_static_duration.text = str(duration) # + '.0' if duration == int(duration) else str(duration)
        xml_static_file.text = str(os.path.abspath(image))

        if image_id != len(images_list)-1:
            xml_transition = ElementTree.SubElement(xml_parent,'transition')
            xml_transition_duration = ElementTree.SubElement(xml_transition, 'duration')
            xml_transition_from = ElementTree.SubElement(xml_transition, 'from')
            xml_transition_to = ElementTree.SubElement(xml_transition, 'to')
            xml_transition_duration.text = '5.0'
            xml_transition_from.text = str(os.path.abspath(image))
            xml_transition_to.text = str(os.path.abspath(images_list[image_id+1]))
        else:
            xml_transition = ElementTree.SubElement(xml_parent,'transition')
            xml_transition_duration = ElementTree.SubElement(xml_transition, 'duration')
            xml_transition_from = ElementTree.SubElement(xml_transition, 'from')
            xml_transition_to = ElementTree.SubElement(xml_transition, 'to')
            xml_transition_duration.text = '2.0'
            xml_transition_from.text = str(os.path.abspath(image))
            xml_transition_to.text = str(os.path.abspath(images_list[0]))


        image_id+=1
        progres_value += progres_deltax
        progress_bar.setValue(progres_value)

    xml_tree = ElementTree.ElementTree(xml_parent)
    xml_tree.write(path_to_img + 'wallpapers_list.xml')
    '00'
    progres_value = 100
    progress_bar.setValue(progres_value)


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


#
# def create_mp4_xml(path_to_mp4):
#     path_to_frames_folder = path_to_mp4[:-(len(os.path.basename(path_to_mp4)))] + os.path.basename(path_to_mp4)[:-4]
#
#     os.mkdir(path_to_frames_folder)
#
#     mp4_cap = cv2.VideoCapture(path_to_mp4)
#     frame_count = int(mp4_cap.get(cv2.CAP_PROP_FRAME_COUNT))
#
#     for frame in range(frame_count):
#         ret, frame_image = mp4_cap.read()
#         if frame % 16 == 0:
#             cv2.imwrite(path_to_frames_folder + f'/{frame}.png', frame_image)
#
#     mp4_cap.release()
#
#     create_img_xml(path_to_frames_folder + r'/', 0.5)
#

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('slidecrea.ico'))

        # ???????????????????????? ????????????
        self.selectImagesPathButton.clicked.connect(self.select_images_path_button)
        self.createXMLImagesFileButton.clicked.connect(self.create_xml_images_file_button)
        self.btnOpenGnomeTweaks.clicked.connect(self.open_gnome_tweks)

    def open_gnome_tweks(self):
        os.system('gnome-tweaks')

    def select_images_path_button(self):
        self.lineEditImagesPath.setText(str(QtWidgets.QFileDialog.getExistingDirectory()))

    def create_xml_images_file_button(self):
        self.createXMLImagesFileButton.setEnabled(False)
        self.selectImagesPathButton.setEnabled(False)
        create_img_xml(self.lineEditImagesPath.text(), self.progressBarIImagesXML, duration=self.spinSlideDuration.value())
        time.sleep(1)
        self.createXMLImagesFileButton.setEnabled(True)
        self.selectImagesPathButton.setEnabled(True)
        self.progressBarIImagesXML.setValue(0)


# DEFAULT_PATH_TO_IMG = r'../../Pictures/Walls/'????
# DEFAULT_PATH_TO_GIF = r'../../Pictures/Walls/skelets.gif'
# DEFAULT_PATH_TO_MP4 = r'../../Pictures/Walls/Pexels Videos 1654216.mp4'
# create_img_xml(DEFAULT_PATH_TO_IMG)
# create_gif_xml(DEFAULT_PATH_TO_GIF)
# create_mp4_xml(DEFAULT_PATH_TO_MP4)


if __name__ == "__main__":
    import sys

    # ???????????????????????? ???? ?????????????????? ?????????????? ??????????
    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = MainWindow()
    appMainWindow.show()
    sys.exit(app.exec_())
