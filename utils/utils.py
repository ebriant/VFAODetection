import numpy as np


def bbox_iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
    xB, yB = min(boxA[0] + boxA[2], boxB[0] + boxB[2]), min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA[2] + 1) * (boxA[3] + 1)
    boxBArea = (boxB[2] + 1) * (boxB[3] + 1)
    return interArea / float(boxAArea + boxBArea - interArea)


def bbox_landmarks_match(bbox, landmarks):
    x, y = min(landmarks[0]), min(landmarks[1])
    width = max(landmarks[0]) - min(landmarks[0])
    height = max(landmarks[1]) - min(landmarks[1])
    lm_bbox = [x, y, width, height]
    return bbox_iou(bbox, lm_bbox) > 0.35


def get_roi(img, bbox, *, scale=1, padding=0):
    size = max(bbox[2], bbox[3])
    x_c = bbox[0] + bbox[2] / 2
    y_c = bbox[1] + bbox[3] / 2
    new_size = (size * scale) + padding
    xmin = int(x_c - new_size / 2)
    ymin = int(y_c - new_size / 2)
    xmax = int(x_c + new_size / 2)
    ymax = int(y_c + new_size / 2)
    return xmin, ymin, xmax, ymax


def crop_roi(img, bbox, *, scale=1, padding=0):
    xmin, ymin, xmax, ymax = get_roi(img, bbox, scale=scale, padding=padding)
    return img[ymin:ymax, xmin:xmax], [xmin, ymin, xmin - xmax, ymin - ymax]


def gradient(y1, y2, t=1):
    return (y2 - y1) / t


def build_suffix(param_list):
    string_char = ""
    count = 1
    last_value = ""
    for idx, value in enumerate(param_list):
        if value == last_value:
            count += 1
        else:
            if len(str(last_value)) > 0:
                string_char += "." + (str(last_value) if count == 1 else "%sx%d" %(last_value, count))
            count = 1
            last_value = value
    string_char += "." + (str(last_value) if count == 1 else "%sx%d" %(last_value, count))

    return string_char


if __name__ == "__main__":
    print(build_suffix([512, 512, 512, 1024, 1024]))
