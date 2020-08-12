import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import tqdm


#coco_names_path = '../data/coco.names'
#with open(coco_names_path, 'r') as f:
#    classes = f.read().strip().split('\n')
classes =['person','bicycle', 'car','motorcycle','airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog','horse', 'sheep','cow','elephant','bear', 'zebra', 'giraffe','backpack','umbrella', 'handbag','tie', 'suitcase', 'frisbee', 'skis', 'snowboard','sports ball', 'kite', 'baseball bat', 'baseball glove','skateboard', 'surfboard', 'tennis racket','bottle', 'wine glass', 'cup', 'fork','knife', 'spoon', 'bowl', 'banana','apple', 'sandwich', 'orange','broccoli', 'carrot', 'hot dog', 'pizza','donut', 'cake', 'chair', 'couch', 'potted plant', 'bed','dining table', 'toilet','tv','laptop', 'mouse','remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
print('classes', len(classes), classes)



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
    in_file = open('%s/VOCdevkitCOCO/VOCCOCO/Annotations/%s.xml'%(data_dir, image_id))
    out_file = open('%s/VOCdevkitCOCO/VOCCOCO/labels/%s.txt'%(data_dir, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        #print('obj', obj.find('name'))
        if obj.find('name') is None:
            continue

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
image_sets = ['trainval', 'test']

if not os.path.exists('%s/VOCdevkitCOCO/VOCCOCO/labels/' % data_dir):
    os.makedirs('%s/VOCdevkitCOCO/VOCCOCO/labels/' % data_dir)

for image_set in image_sets:
    image_ids = open('%s/VOCdevkitCOCO/VOCCOCO/ImageSets/Main/%s.txt'% (data_dir, image_set)).read().strip().split()
    #image_ids = [f.replace('.jpg', '') for f in os.listdir('%s/VOCdevkitCOCO/VOCCOCO/JPEGImages' % data_dir) if f.endswith('.jpg')]
    print('image_ids', len(image_ids))
    list_file = open('%s/%s.txt' % (data_dir, image_set), 'w')
    for image_id in tqdm.tqdm(image_ids):
        list_file.write('%s/VOCdevkitCOCO/VOCCOCO/JPEGImages/%s.jpg\n'%(data_dir, image_id))
        convert_annotation(data_dir, image_id)
    list_file.close()

#os.system("cat %s.txt > train.txt" % image_set)
#os.system("cat %s.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

