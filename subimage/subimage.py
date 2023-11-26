import argparse
import logging

import numpy as np
import matplotlib.pyplot as plt

from skimage import data, io
from skimage.feature import match_template
from skimage.color import rgb2gray

# Example based on docs here:
# https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_template.html#sphx-glr-auto-examples-features-detection-plot-template-py
logger = logging.getLogger("find_subimage")


class SubImgSearch:
    def __init__(self) -> None:
        self.image_to_search = None
        self.search_rect_top_left_coord = None
        self.search_rect_bottom_right_coord = None
        self.matching_image = None
        self.x = None
        self.y = None
        self.result = None

    def find_subimage(
        self,
        image_to_search: str,
        search_rect_top_left_coord: tuple = None,
        search_rect_bottom_right_coord: tuple = None,
        matching_image=None,
    ) -> tuple:
        """Finds sub-image in an image

        Parameters
        ----------
        image_to_search : str
            source image to search in
        search_rect_top_left_coord : tuple
            optional.
            top left corner of rectangle defining the
            image to match.
        search_rect_bottom_right_coord : tuple
            bottom right corner of rectangle defining the
            image to match.
        matching_image : _type_, optional
            image to match
            , by default None

        Returns
        -------
        tuple
            (x,y) center of found image within image to search for in pixels
        """
        with open(image_to_search, mode="rb") as image_to_search:
            self.image_to_search = io.imread(image_to_search)

        # convert to grayscale - fast and simpler to search pattern, seems to work for test.
        self.image_to_search = rgb2gray(self.image_to_search)

        if all([search_rect_top_left_coord, search_rect_bottom_right_coord]):
            # [tly:bry, tlx:brx]
            self.matching_image = self.image_to_search[
                search_rect_top_left_coord[1] : search_rect_bottom_right_coord[1],
                search_rect_top_left_coord[0] : search_rect_bottom_right_coord[0],
            ]
        elif matching_image:
            try:
                with open(matching_image, mode="rb") as matching_image:
                    self.matching_image = io.imread(matching_image)
                    self.matching_image = rgb2gray(self.matching_image)
            except FileNotFoundError as e:
                logger.error("%s filepath not found", matching_image)
                logger.error(e)
        elif all([search_rect_top_left_coord, search_rect_bottom_right_coord, matching_image]):
            logger.warning("Either provide coords or source image, not both")
            logger.warning("Defaulting to image")

        # this is where the image is detected
        self.result = match_template(self.image_to_search, self.matching_image)

        # convert coordinated to x, y
        ij = np.unravel_index(np.argmax(self.result), self.result.shape)
        self.x, self.y = ij[::-1]

        return (self.x, self.y)

    def plot_match_info(self):
        """Utility function to display image with information
        about the image we found.
        """
        fig = plt.figure(figsize=(8, 3))
        ax1 = plt.subplot(1, 3, 1)
        ax2 = plt.subplot(1, 3, 2)
        ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

        ax1.imshow(self.matching_image, cmap=plt.cm.gray)
        ax1.set_axis_off()
        ax1.set_title("template")

        ax2.imshow(self.image_to_search, cmap=plt.cm.gray)
        ax2.set_axis_off()
        ax2.set_title("image")

        # highlight matched region
        hmatching_image, wmatching_image = self.matching_image.shape
        rect = plt.Rectangle((self.x, self.y), wmatching_image, hmatching_image, edgecolor="r", facecolor="none")
        ax2.add_patch(rect)

        ax3.imshow(self.result)
        ax3.set_axis_off()

        # highlight matched region
        # print x and y
        ax3.autoscale(False)
        ax3.plot(self.x, self.y, "o", markeredgecolor="r", markerfacecolor="none", markersize=10)

        ax3.set_title(f"`match_template`\nfound position: x: {self.x}, y: {self.y}")

        plt.show()
