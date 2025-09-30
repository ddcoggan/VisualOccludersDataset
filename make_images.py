from PIL import Image
import numpy as np
import os
import os.path as op
import shutil, glob, sys
import math
import itertools


def tile(images, out_path, num_rows=None, num_cols=None, by_col=False,
         base_gap=0, colgap=None, colgapfreq=None, rowgap=None, rowgapfreq=None,
         bgcol=(0, 0, 0, 0)):
    """
    Tiles images into a single image.  Images can be provided as filepaths or
    PIL Image objects.
    """

    # calculate num_rows and / or num_cols if not specified
    if num_rows is None and num_cols is None:
        num_rows = math.ceil(np.sqrt(len(images)))
        num_cols = math.ceil(len(images) / num_rows)
    elif num_rows is None:
        num_rows = math.ceil(len(images) / num_cols)
    elif num_cols is None:
        num_cols = math.ceil(len(images) / num_rows)

    # load images
    ims = []
    for image in images:
        if type(image) is str:
            im = Image.open(image)
            ims.append(im)
        else:
            ims.append(image)
    ims += [None] * (num_rows * num_cols - len(ims))

    # specify spatial arrangement of images
    order = 'F' if by_col else 'C'
    image_locations = np.arange(len(ims)).reshape((num_rows, num_cols),
        order=order)

    # width of each column is as wide as the widest image
    col_coords = []
    col_widths = []
    cumulative_width = base_gap
    for col in range(num_cols):

        col_images = [ims[x] for x in image_locations[:, col]]
        widths = []
        for col_image in col_images:
            if col_image:
                widths.append(col_image.size[0])
        max_width = np.max(widths)
        col_widths.append(max_width)
        col_coords.append(cumulative_width)

        # add column gap
        cumulative_width += base_gap
        if colgap and (col + 1) % colgapfreq == 0 and col < (num_cols - 1):
            cumulative_width += colgap

        cumulative_width += max_width

    # height of each row is as tall as the tallest image
    row_coords = []
    row_heights = []
    cumulative_height = base_gap
    for row in range(num_rows):

        row_images = [ims[x] for x in image_locations[row, :]]
        heights = []
        for row_image in row_images:
            if row_image is not None:
                heights.append(row_image.size[1])
        max_height = np.max(heights)
        row_heights.append(max_height)
        row_coords.append(cumulative_height)

        # add row gap
        cumulative_height += base_gap
        if rowgap and (row + 1) % rowgapfreq == 0 and row < (num_rows - 1):
            cumulative_height += rowgap

        cumulative_height += max_height

    # build tiled image
    montage = Image.new(mode='RGBA', size=(cumulative_width, cumulative_height),
        color=bgcol)
    for row, col in itertools.product(range(num_rows), range(num_cols)):
        image = ims[image_locations[row, col]]
        if image:
            # centre the image in the window
            width, height = image.size
            col_coord = col_coords[col] + math.floor(
                (col_widths[col] - width) / 2)
            row_coord = row_coords[row] + math.floor(
                (row_heights[row] - height) / 2)
            montage.paste(image, (col_coord, row_coord))
    montage.save(out_path)


def invert_tile_masks(input_paths, output_path):

    inverted_occluders = []
    for input_path in input_paths:
        if '/natural/' in input_path:
            inverted_occluders.append(Image.open(input_path))
        else:
            img = Image.open(input_path).convert('L')  # Convert to grayscale

            # white background
            img_array = 255 - np.array(img) # black image with mask

            # transparent background
            #img_array = np.zeros((256, 256, 3))
            #img_array[:, :, 3] += np.array(img)

            inverted_occluders.append(
                Image.fromarray(img_array.astype(np.uint8))
            )

    tile(inverted_occluders, output_path, num_rows=4, base_gap=16, rowgap=128,
        rowgapfreq=1)


occluders = [
    'natural',
    'natural_silhouette',
    'mud_splash',
    'patch_drop',
    'cardinal_crossed_bars',
    'oblique_crossed_bars',
    'polkadot',
    'polkasquare',

    'curved_lines',
    'straight_lines',
    'filled_ellipses',
    'empty_ellipses',
    'filled_triangles',
    'empty_triangles',
    'filled_rectangles',
    'empty_rectangles',

    'coarse_noise',
    'fine_noise',
    'fine_oriented_noise',
    'pink_noise',
    'oblique_bars_02',
    'oblique_bars_04',
    'oblique_bars_08',
    'oblique_bars_16',

    'horizontal_bars_02',
    'horizontal_bars_04',
    'horizontal_bars_08',
    'horizontal_bars_16',
    'vertical_bars_02',
    'vertical_bars_04',
    'vertical_bars_08',
    'vertical_bars_16',
]

occluder_paths = [sorted(i.lower() for i in glob.glob(
    f'VisualOccludersDataset/{occluder}/50/*.png'))[0] for occluder in occluders
]
os.makedirs('images', exist_ok=True)
invert_tile_masks(occluder_paths, f'images/occluder_examples.png')

