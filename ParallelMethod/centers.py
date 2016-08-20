"""
Ahmet BAGLAN
"""

import sys
sys.path.append("../../sketchfe/sketchfe")
sys.path.append('../predict/')
from FileIO import *
import numpy as np


def saveCenters():
    """This file computes centers of classses and saves it to  the ./data/csv/allCenters.csv"""

    files = ['airplane', 'alarm-clock', 'angel', 'ant', 'apple', 'arm', 'armchair', 'ashtray', 'axe', 'backpack', 'banana',
         'barn', 'baseball-bat', 'basket', 'bathtub', 'bear-(animal)', 'bed', 'bee', 'beer-mug', 'bell', 'bench',
         'bicycle', 'binoculars', 'blimp', 'book', 'bookshelf', 'boomerang', 'bottle-opener', 'bowl', 'brain', 'bread',
         'bridge', 'bulldozer', 'bus', 'bush', 'butterfly', 'cabinet', 'cactus', 'cake', 'calculator', 'camel',
         'camera', 'candle', 'cannon', 'canoe', 'car-(sedan)', 'carrot', 'castle', 'cat', 'cell-phone', 'chair', 'chandelier',
         'church', 'cigarette', 'cloud', 'comb', 'computer-monitor', 'computer-mouse', 'couch', 'cow', 'crab',
         'crane-(machine)', 'crocodile', 'crown', 'cup', 'diamond', 'dog', 'dolphin', 'donut', 'door', 'door-handle',
         'dragon', 'duck', 'ear', 'elephant', 'envelope', 'eye', 'eyeglasses', 'face', 'fan', 'feather', 'fire-hydrant',
         'fish', 'flashlight', 'floor-lamp', 'flower-with-stem', 'flying-bird', 'flying-saucer', 'foot', 'fork', 'frog',
         'frying-pan', 'giraffe', 'grapes', 'grenade', 'guitar', 'hamburger', 'hammer', 'hand', 'harp', 'hat', 'head',
         'head-phones', 'hedgehog', 'helicopter', 'helmet', 'horse', 'hot-air-balloon', 'hot-dog', 'hourglass', 'house',
         'human-skeleton', 'ice-cream-cone', 'ipod', 'kangaroo', 'key', 'keyboard', 'knife', 'ladder', 'laptop', 'leaf',
         'lightbulb', 'lighter', 'lion', 'lobster', 'loudspeaker', 'mailbox', 'megaphone', 'mermaid', 'microphone',
         'microscope', 'monkey', 'moon', 'mosquito', 'motorbike', 'mouse-(animal)', 'mouth', 'mug', 'mushroom', 'nose',
         'octopus', 'owl', 'palm-tree', 'panda', 'paper-clip', 'parachute', 'parking-meter', 'parrot', 'pear', 'pen',
         'penguin', 'person-sitting', 'person-walking', 'piano', 'pickup-truck', 'pig', 'pigeon', 'pineapple',
         'pipe-(for-smoking)', 'pizza', 'potted-plant', 'power-outlet', 'present', 'pretzel', 'pumpkin', 'purse',
         'rabbit', 'race-car', 'radio', 'rainbow', 'revolver', 'rifle', 'rollerblades', 'rooster', 'sailboat',
         'santa-claus', 'satellite', 'satellite-dish', 'saxophone', 'scissors', 'scorpion', 'screwdriver', 'sea-turtle',
         'seagull', 'shark', 'sheep', 'ship', 'shoe', 'shovel', 'skateboard']

    k  = []
    my_names = []
    my_isFull = []
    f = FileIO()
    for mfile in files[:]:
        print mfile
        names, isFull, features = f.load('../data/csv/' + mfile + '/' + mfile + '.csv')
        nowCenter = np.zeros(len(features[0]))
        totalNumOfInstances = len(features)
        for instance in features:
            nowCenter += instance
        nowCenter = nowCenter/totalNumOfInstances
        k.append(nowCenter)
        my_names.append(mfile)
        my_isFull.append(0)
    f.save(my_isFull,my_names,k,'../data/csv/allCenters.csv')


if __name__ == '__main__':saveCenters()