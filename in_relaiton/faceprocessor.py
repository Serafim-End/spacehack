import cv2
import itertools
import os
import numpy as np
import openface

class FaceProcessor(object):
    def __init__(
        self,
        dlibFacePredictor = '/root/workspace/model/dlib/shape_predictor_68_face_landmarks.dat',
        networkModel = '/root/workspace/model/nn4.small2.v1.t7',
        imgDim = 96,
    ):
        self.align = openface.AlignDlib(dlibFacePredictor)
        self.net = openface.TorchNeuralNet(networkModel, imgDim)
        self.imgDim = imgDim

    def get(self, imgPath, verbose=False):
        if verbose:
            print("Processing {}.".format(imgPath))
        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        if verbose:
            print("  + Original size: {}".format(rgbImg.shape))

        bb = self.align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            raise Exception("Unable to find a face: {}".format(imgPath))

        alignedFace = self.align.align(self.imgDim, rgbImg, bb,
                                  landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))
        if verbose:
            print("  + Face alignment took {} seconds.".format(time.time() - start))

        rep = self.net.forward(alignedFace)
        if verbose:
            print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
            print("Representation:")
            print(rep)
            print("-----\n")
        return rep
