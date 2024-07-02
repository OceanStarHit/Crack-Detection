

# Function to convert polygon to bounding box
def polygon_to_bbox(polygon):
    x_coords = [point['x'] for point in polygon]
    y_coords = [point['y'] for point in polygon]
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    width = max_x - min_x
    height = max_y - min_y
    return {
        "left": min_x,
        "top": min_y,
        "width": width,
        "height": height
    }


def points_to_bbox(points):
    x_coords = [point['x'] for point in points]
    y_coords = [point['y'] for point in points]
    x_min = min(x_coords)
    y_min = min(y_coords)
    width = max(x_coords) - x_min
    height = max(y_coords) - y_min
    return [x_min, y_min, width, height]


def xywh_to_xyxy(xywh):
    x, y, w, h = xywh
    x2 = x + w
    y2 = y + h
    xyxy = [x, y, x2, y2]
    return xyxy


def xyxy_xywh(xyxy):
    x, y, x2, y2 = xyxy
    w = x2 - x
    h = y2 - y
    xywh = [x, y, w, h]
    return xywh


