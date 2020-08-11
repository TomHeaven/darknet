import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["红细胞", "白细胞"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(data_dir, image_id):
    in_file = open('%s/red_cells_voc/Annotations/%s.xml'%(data_dir, image_id))
    out_file = open('%s/red_cells_voc/labels/%s.txt'%(data_dir, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        #if cls not in classes or int(difficult)==1:
        #    print('Unknown cls', cls)
        #    continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

data_dir = '../data'
image_set = 'red_cells_voc'

if not os.path.exists('%s/red_cells_voc/labels/' % data_dir):
    os.makedirs('%s/red_cells_voc/labels/' % data_dir)
#image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
image_ids = [f.replace('.jpg', '') for f in os.listdir('%s/red_cells_voc/JPEGImages' % data_dir) if f.endswith('.jpg')]
print('image_ids', len(image_ids))
list_file = open('%s.txt' % image_set, 'w')
for image_id in image_ids:
    list_file.write('%s/red_cells_voc/JPEGImages/%s.jpg\n'%(data_dir, image_id))
    convert_annotation(data_dir, image_id)
list_file.close()

os.system("cat %s.txt > train.txt" % image_set)
#os.system("cat %s.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

