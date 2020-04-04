# original fields of detection from JSON
ID = 'id'
DEVICE_ID = 'device_id'
TIMESTAMP = 'timestamp'

WIDTH = 'width'
HEIGHT = 'height'

X = 'x'
Y = 'y'

FRAME_CONTENT = 'frame_content'


# added fields by processing functions
FRAME_DECODED = 'frame_decoded'
IMAGE = 'image'

# image basic stats
DARKNESS = 'image_darkness'
BRIGHTEST = 'image_brightest'
BRIGHTER_COUNT = 'image_brighter_count_%d'

# reconstruction dark filled area
EDGE = 'edge'
CROP_X = 'crop_x'
CROP_Y = 'crop_y'
CROP_SIZE = 'crop_size'

# classification
CLASSIFIED = 'classified'
CLASS_ARTIFACT = 'artifact'

# artifact filter values
ARTIFACT_TOO_OFTEN = 'artifact_too_often'
ARTIFACT_HOT_PIXEL = 'artifact_hot_pixel'
ARTIFACT_NEAR_HOT_PIXEL = 'artifact_near_hot_pixel'
ARTIFACT_NEAR_HOT_PIXEL_REFXY = 'artifact_near_hot_pixel_refxy'
ARTIFACT_TOO_DARK = 'artifact_too_dark'
ARTIFACT_TOO_LARGE_BRIGHT_AREA = 'artifact_too_large_bright_area'
