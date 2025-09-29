# The Visual Occluders Dataset

This repository contains the code necessary to apply the Visual Occluders 
Dataset to images, either to make new datasets or during model 
training/evaluation to apply occluders to inputs during the dataloading process. 
The figure below summarizes the dataset as used in an upcoming publication:

![Alt text](VOD.png)

The Visual Occluders Dataset and application to images. (A) Examples of each
occluder type (upper two rows) and visibility level (lower row), with visibility
indicating the approximate area of an underlying image (±5%) that remains
visible after the occluder is applied. The dataset contains 32 different
occluder types (2 natural, 30 artificial), each of which contains up to 1000
individual occluder masks for each visibility level. Eight examples are shown
for each of the two natural types in the green and brown boxes. For the purposes
of the present study, the 30 artificial occluder types (one example shown per
type) were combined into three arbitrary groups shown by the blue, red and
purple boxes. (B) Procedure for applying occluders within the SimCLR dataset
augmentation (Chen et al. 2020). See Materials and Methods for more
information. (C) Example input images from each type of occlusion training.

The Visual Occluders Dataset can be downloaded [here](
https://drive.google.com/file/d/1BSQk5L94GNNqIOB7a-iKwjE_nDd8esHK/view?usp=share_link).