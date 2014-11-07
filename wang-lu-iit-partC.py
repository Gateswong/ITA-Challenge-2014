import re
from math import (sin,
                  cos,
                  radians)

import Image, ImageDraw


class partC():
    
    @classmethod
    def map_coord(self, rx, ry):
        """
        Convert real coordianates into image coordiantes.
        
        **returns**:
        ix, iy
        
        **examples**:
        rx = -1 >> ix = 0; ry = 1 >> iy = 0
        rx = 1 >> ix = 1024; ry = -1 >> iy = -2*(-512) = 1024
        """
        return 512 * (float(rx) + 1), -(512 * (float(ry) - 1))
    
    @classmethod
    def perspective(self, rx, ry, rz):
        """
        Convert 3d real points into 2d real points.
        
        **returns**:
        rx, ry
        """
        return (5*float(rx))/(1/(float(rz)-2)), (5*float(ry))/(1/(float(rz)-2))
    
    def __init__(self):
        self.minx = 0
        self.maxx = 1024
        self.miny = 0
        self.maxy = 1024
        self.img = Image.new('RGB', (self.maxx, self.maxy), 'black')
        self.draw = ImageDraw.Draw(self.img) 
    
    def draw_point(self, point, color):
        """
        Draw a point.
        
        **parameters**:
        
        point: The image coordianates.
        
        color: The color.
        """
        self.draw.point((point[0], point[1]), fill=color)
    
    def draw_line(self, p1, p2, color):
        """
        Draw a line between two points, with given color.
        
        **parameters**:
        
        p1, p2: Two points.
        
        color: The color.
        """
        self.draw.line((p1[0], p1[1], p2[0], p2[1]), color)
        
    def rotate_x(self, points, degree):
        """
        Rotate the given set of points about X axis.
        The points are **real points** (not image points)
        
        This rotate is transformed with matrix, as A = degree:
        
        1 0 0
        
        0 cosA -sinA
        
        0 sinA cosA
        
        **parameters**:
        
        points: the list of given points.
        """
        rotated_points = []
        for point in points:
            x = float(point[0])
            y = float(point[1])
            z = float(point[2])
            np = (x, 
                  y * cos(radians(degree)) - z * sin(radians(degree)),
                  y * sin(radians(degree)) + z * cos(radians(degree)))
            rotated_points.append(np)
        return rotated_points
    
    def rotate_y(self, points, degree):
        """
        Rotate the given set of points about Y axis.
        The points are **real points** (not image points)
        
        This rotate is transformed with matrix, as A = degree:
        
        cosA 0 -sinA
        
        0 1 0
        
        sinA 0 cosA
        
        **parameters**:
        
        points: the list of given points.
        """
        rotated_points = []
        for point in points:
            x = float(point[0])
            y = float(point[1])
            z = float(point[2])
            np = (x * cos(radians(degree)) - z * sin(radians(degree)),
                  y,
                  x * sin(radians(degree)) + z * cos(radians(degree)))
            rotated_points.append(np)
        return rotated_points

def main():
    # LOAD THE DATA
    txtfile = 'wang-lu-iit-partB-result.txt'
    
    float_pattern = '(-?\d+(?:\.\d+(?:E-\d+)?)?)'
    re_point = re.compile('point %s %s %s' % (float_pattern, float_pattern, float_pattern))
    re_face = re.compile('face (\d+) (\d+) (\d+)')
    
    points = []
    faces = []
    
    fi = open(txtfile, 'r')
    
    for line in fi.readlines():
        if re_point.match(line):
            p = re_point.findall(line)[0]
            points.append((float(p[0]), float(p[1]), (float(p[2]))))
        elif re_face.match(line):
            faces.append(re_face.findall(line)[0])
        else:
            print(line)
            
    print('Read %d points and %d faces' % (len(points), len(faces)))
            
    # QUESTION A
    A = partC()
    for p in points:
        rx, ry = partC.perspective(p[0], p[1], p[2])
        ix, iy = partC.map_coord(rx, ry)
        #print(ix, iy)
        A.draw_point((ix, iy), (255, 255, 255))
    A.img.save('wang-lu-iit-partC-A.png', 'PNG')
    
    # QUESTION B
    B = partC()
    pointsRotatedX = B.rotate_x(points, 15)
    pointsRotatedY = B.rotate_y(pointsRotatedX, -30)
    for p in pointsRotatedY:
        rx, ry = partC.perspective(p[0], p[1], p[2])
        ix, iy = partC.map_coord(rx, ry)
        #print(ix, iy)
        B.draw_point((ix, iy), (0, 255, 255))
    B.img.save('wang-lu-iit-partC-B.png', 'PNG')
    
    # QUESTION C
    C = partC()
    for p in points:
        rx, ry = partC.perspective(p[0], p[1], p[2])
        ix, iy = partC.map_coord(rx, ry)
        #print(ix, iy)
        C.draw_point((ix, iy), (255, 255, 255))
    for f in faces:
        try:
            p0 = partC.map_coord(*partC.perspective(*points[int(f[0])]))
            p1 = partC.map_coord(*partC.perspective(*points[int(f[1])]))
            p2 = partC.map_coord(*partC.perspective(*points[int(f[2])]))
            C.draw_line(p0, p1, 'gray')
            C.draw_line(p1, p2, 'gray')
            C.draw_line(p2, p0, 'gray')
        except IndexError as err:
            print(err, f)
            
    C.img.save('wang-lu-iit-partC-C.png', 'PNG')
    

if __name__ == '__main__':
    main()
