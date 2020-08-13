import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import numpy as np
import skimage.io as io
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)


def eval_coco(res_path, ann_path, tpye='bbox'):
    #annType = ['segm','bbox','keypoints']
    annType = tpye
    prefix = 'person_keypoints' if annType=='keypoints' else 'instances'
    print('Running demo for *%s* results.'%(annType))

    #dataDir='../'
    #dataType='val2017'
    #annFile = '%s/annotations/%s_%s.json'%(dataDir,prefix,dataType)
    cocoGt=COCO(ann_path)

    #initialize COCO detections api
    #resFile='%s/results/%s_%s_fake%s100_results.json'
    #resFile = resFile%(dataDir, prefix, dataType, annType)
    cocoDt=cocoGt.loadRes(res_path)

    imgIds=sorted(cocoGt.getImgIds())
    #imgIds=imgIds[0:100]
    #imgId = imgIds[np.random.randint(100)]

    # running evaluation
    cocoEval = COCOeval(cocoGt,cocoDt,annType)
    cocoEval.params.imgIds  = imgIds
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()


if __name__ == '__main__':
    res_path = 'results/coco_results.json'
    ann_path = '../data/instances_val2017.json'
    eval_coco(res_path, ann_path, 'bbox')