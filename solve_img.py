import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

def resize_and_pad(image, target_image_size=(640, 480), target_canvas_size=(640, 640)):
    h, w, _ = image.shape
    target_h, target_w = target_image_size

    scale = min(target_h / h, target_w / w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized_image = cv2.resize(image, (new_w, new_h))

    canvas = np.zeros((target_canvas_size[1], target_canvas_size[0], 3), dtype=np.uint8)
    x_offset = (target_canvas_size[0] - new_w) // 2
    y_offset = (target_canvas_size[1] - new_h) // 2
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_image

    return canvas, (new_w, new_h), (x_offset, y_offset)

def update_bounding_box(bboxs, original_size, new_size, offsets, canvas_size):
    original_w, original_h = original_size
    new_w, new_h = new_size
    x_offset, y_offset = offsets
    canvas_w, canvas_h = canvas_size
    
    scale_x = new_w / original_w
    scale_y = new_h / original_h
    
    updated_bboxes = []
    for bbox in bboxs:
        classId, x_center, y_center, width, height = bbox
        
        new_x_center = (x_center * scale_x * original_w + x_offset) / canvas_w
        new_y_center = (y_center * scale_y * original_h + y_offset) / canvas_h
        new_width = (width * scale_x * original_w) / canvas_w
        new_height = (height * scale_y * original_h) / canvas_h
        
        updated_bboxes.append((classId, new_x_center, new_y_center, new_width, new_height))
    
    return updated_bboxes

def update_bboxes(original_size, resized_size, canvas_size, bboxes):
    orig_w, orig_h = original_size
    new_w, new_h = resized_size
    canvas_w, canvas_h = canvas_size

    updated_bboxes = []
    for bbox in bboxes:
        class_id, x_center, y_center, width, height = bbox

        scale_w = new_w / orig_w
        scale_h = new_h / orig_h
        x_center_new = x_center * scale_w
        y_center_new = y_center * scale_h
        width_new = width * scale_w
        height_new = height * scale_h

        pad_x = (canvas_w - new_w) / 2
        pad_y = (canvas_h - new_h) / 2

        x_center_final = (x_center_new + pad_x) / canvas_w
        y_center_final = (y_center_new + pad_y) / canvas_h
        width_final = width_new / canvas_w
        height_final = height_new / canvas_h

        updated_bboxes.append((class_id, x_center_final, y_center_final, width_final, height_final))

    return updated_bboxes