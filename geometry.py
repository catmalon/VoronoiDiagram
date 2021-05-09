#!/usr/bin/env python3
# coding=UTF-8
# 學號: M093040067
# 系級: 資工系碩一
# 姓名: 歐陽安媛

from functools import cmp_to_key


class Point:
	def __init__(self, x, y):
		self.x, self.y = float(x), float(y)

	def __eq__(self, p):
		return False if (p == None) else ((self.x == p.x) and (self.y == p.y))

	def __str__(self):
		return "(%d, %d)" % (self.x, self.y)

	@staticmethod
	def midpoint_of(pa, pb):
		return Point((pa.x + pb.x) / 2.0, (pa.y + pb.y) / 2.0)

	@staticmethod
	def centroid_of(points):
		count = float(len(points))
		sum_x = sum([p.x for p in points])
		sum_y = sum([p.y for p in points])
		return Point(sum_x/count, sum_y/count)

	@staticmethod
	def sort_counterclockwisely(points):
		centroid = Point.centroid_of(points)
		def counterclockwise_cmp(pa, pb):
			va = (pa.x - centroid.x, pa.y - centroid.y)
			vb = (pb.x - centroid.x, pb.y - centroid.y)
			return -1 if va[0] * vb[1] - va[1] * vb[0] <= 0 else 1
		points.sort(key=cmp_to_key(counterclockwise_cmp))


class Vector:
	def __init__(self, dx, dy):
		self.dx, self.dy = dx, dy
	
	def is_zero(self):
		return (self.dx == 0 and self.dy == 0)

	def crossproduct_with(self, v):
		return Vector.crossproduct_of(self, v)

	@staticmethod
	def vector_of(start, end):
		return Vector(end.x - start.x, end.y - start.y)

	@staticmethod
	def normalvector_of(v):
		return Vector(-v.dy, v.dx)

	@staticmethod
	def crossproduct_of(v1, v2):
		return v1.dx * v2.dy - v1.dy * v2.dx

	@staticmethod
	def cross(p1, p2, p3):
		v1 = Vector.vector_of(p1, p2)
		v2 = Vector.vector_of(p1, p3)
		return Vector.crossproduct_of(v1, v2)


class Triangle:
	@staticmethod
	def calc_area(pa, pb, pc):
		#       | pa.x pa.y 1 |
		# 1/2 * | pb.x pb.y 1 |
		#       | pc.x pc.y 1 |
		return ((pa.x * pb.y + pa.y * pc.x + pb.x * pc.y) - (pa.x * pc.y + pb.x * pa.y + pc.x * pb.y)) * 0.5

	@staticmethod
	def circumcenter_of(pa, pb, pc):
		#      | pa.x^2+pa.y^2 pa.y 1 |                   | pa.x pa.x^2+pa.y^2 1 |
		#  x = | pb.x^2+pb.y^2 pb.y 1 | / (4 * area), y = | pb.x pb.x^2+pb.y^2 1 | / (4 * area)
		#      | pc.x^2+pc.y^2 pc.y 1 |                   | pc.x pc.x^2+pc.y^2 1 |
		area = Triangle.calc_area(pa, pb, pc)
		pa2 = pa.x * pa.x + pa.y * pa.y
		pb2 = pb.x * pb.x + pb.y * pb.y
		pc2 = pc.x * pc.x + pc.y * pc.y
		x = (pa2 * pb.y + pa.y * pc2 + pb2 * pc.y - pa2 * pc.y - pb2 * pa.y - pc2 * pb.y) / 4 / area
		y = (pa.x * pb2 + pa2 * pc.x + pb.x * pc2 - pa.x * pc2 - pb.x * pa2 - pc.x * pb2) / 4 / area
		return Point(x, y)