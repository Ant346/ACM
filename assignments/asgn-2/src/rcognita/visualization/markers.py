from svgpath2mpl import parse_path
import matplotlib


class RobotMarker:
    """
    Robot marker for visualization.

    """

    def __init__(self, angle=None, path_string=None):
        self.angle = angle or 0.0
        self.path_string = (
            path_string
            or """m 66.893258,227.10128 h 5.37899 v 0.91881 h 1.65571 l 1e-5,-3.8513 3.68556,-1e-5 v -1.43933
        l -2.23863,10e-6 v -2.73937 l 5.379,-1e-5 v 2.73938 h -2.23862 v 1.43933 h 3.68556 v 8.60486 l -3.68556,1e-5 v 1.43158
        h 2.23862 v 2.73989 h -5.37899 l -1e-5,-2.73989 h 2.23863 v -1.43159 h -3.68556 v -3.8513 h -1.65573 l 1e-5,0.91881 h -5.379 z"""
        )
        self.path = parse_path(self.path_string)
        self.path.vertices -= self.path.vertices.mean(axis=0)
        self.marker = matplotlib.markers.MarkerStyle(marker=self.path)
        self.marker._transform = self.marker.get_transform().rotate_deg(angle)

    def rotate(self, angle=0):
        self.marker._transform = self.marker.get_transform().rotate_deg(
            angle - self.angle
        )
        self.angle = angle


class LanderMarker:
    """
    Robot marker for visualization.

    """

    def __init__(self, angle=None):
        self.angle = angle or 0.0
        self.path_string = """m 266.3418,632.89453 
            -28.98047,33.63867 h -36.52344 v 49.21094 h 18.17383 
            l -16.86914,69.9693 59.58398,-69.9693 h 113.7793 113.7793 
            l 59.58398,69.9693 L 532,715.74414 h 18.17383 V 666.5332 H 513.65039 
            L 484.66992,632.89453 375.50585,622.02539 Z"""
        self.path = parse_path(self.path_string)
        self.path.vertices -= self.path.vertices.mean(axis=0)
        self.marker = matplotlib.markers.MarkerStyle(marker=self.path)
        self.marker._transform = self.marker.get_transform().rotate_deg(angle)

    def rotate(self, angle=0):
        self.marker._transform = self.marker.get_transform().rotate_deg(
            angle - self.angle
        )
        self.angle = angle
