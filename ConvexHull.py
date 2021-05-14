import queue
import math
import numpy as np

# Point class
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __lt__(self, other):
        return (self.z < other.z) or (self.y < other.y) or (self.x < other.x)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __truediv__(self, number):
        if number == 0:
            return None

        return Point(self.x / number, self.y / number, self.z / number)

    def __mul__(self, number):
        return Point(self.x * number, self.y * number, self.z * number)

    def __hash__(self):
        return int((self.x + self.y ** 2 + self.z ** 3) % 100)


# Edge class
class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def length(self):
        return self.vector().length()

    def vector(self):
        return self.end - self.start

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)

    def reverse(self):
        return Edge(self.end, self.start)


def dot_product(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z


def project(a, b):
    length = dot_product(a, b)
    return Point(length * b.x, length * b.y, length * b.z)


def cross_product(a, b):
    aa = [a.x, a.y, a.z]
    bb = [b.x, b.y, b.z]

    c = np.cross(aa, bb)
    return Point(c[0], c[1], c[2])


# a triangular face
class Face:
    def __init__(self, p1, p2, p3):
        self.points = [p1, p2, p3]

    def edges(self):
        edges = []
        for i in range(3):
            edges.append(Edge(self.points[i], self.points[(i + 1) % 3]))
        return edges

    # requires that edge is in the face
    def other_point(self, edge):
        ls = [edge.start, edge.end]
        for i in range(3):
            if self.points[i] not in ls:
                return self.points[i]

        return self.points[0]

    def __eq__(self, other):
        return set(self.points) == set(other.points)

    def __hash__(self):
        return (hash(self.points[0]) + hash(self.points[1]) ** 2 + hash(self.points[2]) ** 3) % 100


def merge(e1, e2):
    result = e1
    for e in e2:
        if e in e1:
            result.remove(e)
        elif e.reverse() in e1:
            result.remove(e.reverse())
        else:
            result.append(e)
    return result


def find_lowest_point(points):
    # First checks z, then y, and then x.
    best_point = points[0]
    for p in points[1:]:
        if p < best_point:
            best_point = p

    return best_point


def find_next_point(points, p1, p2):
    if p2 is None:
        p2 = p1 - Point(1, 1, 0)

    edge = p2 - p1

    best_point = None
    for p in points:
        if p not in [p1, p2]:
            if best_point is None:
                best_point = p
            else:
                # The volume is positive if p is to the left of the plane defined by the triangle (p1,p2,best_point)
                # This means p is a better choice than before.

                # These vector calculations give the singed volume of the tetrahedron (p1, p2, best_point, p).
                v = p - p1
                v = v - project(v, edge)

                u = best_point - p1
                u = u - project(u, edge)

                cross = cross_product(u, v)
                if dot_product(cross, edge) > 0:
                    best_point = p
    return best_point


def gift_wrapping(points):
    hull = []

    # Queue of edges and list of edges processed
    edges_available = queue.Queue()
    edges_created = []

    # A function to create an edge indicating that it has been processed. 
    # If the reverse of this edge has not been processed before, then add that to the queue.
    def add_edge(e):
        edges_created.append(e)
        if e.reverse() not in edges_created:
            edges_available.put(e.reverse())

    # Find the first edge
    fp1 = find_lowest_point(points)
    fp2 = find_next_point(points, fp1, None)

    add_edge(Edge(fp2, fp1))

    while not edges_available.empty():
        edge = edges_available.get()
        p1 = edge.start
        p2 = edge.end

        if edge not in edges_created:
            # Get next point
            p3 = find_next_point(points, p1, p2)

            # Add the face to the convex hull, and its edges to the queue.
            hull.append(Face(p1, p2, p3))
            add_edge(Edge(p1, p2))
            add_edge(Edge(p2, p3))
            add_edge(Edge(p3, p1))

    return hull