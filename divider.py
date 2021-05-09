#!/usr/bin/env python3
# coding=UTF-8
# 學號: M093040067
# 系級: 資工系碩一
# 姓名: 歐陽安媛

from geometry import *


class Divider:
	def __init__(self, start, end, A, B):
		# set start point higher than end point in this homework domain
		self.A, self.B = A, B
		if (start.y < end.y or (start.y == end.y and start.x < end.x)):
			self.start, self.end = start, end
		else:
			self.start, self.end = end, start

	def __ne__(self, d2):
		if (d2 == None):
			return True
		if (self.A == d2.A and self.B == d2.B):
			return False
		if (self.A == d2.B and self.B == d2.A):
			return False
		return True

	def get_inpoint_with(self, d2):
		if (self.start == d2.start or self.start == d2.end):
			return self.start
		if (self.end == d2.start or self.end == d2.end):
			return self.end
		v1 = Vector.vector_of(self.start, self.end)
		v2 = Vector.vector_of(d2.start, d2.end)
		v3 = Vector.vector_of(self.start, d2.start)
		c1 = Vector.crossproduct_of(v1, v2)
		c2 = Vector.crossproduct_of(v3, v2)
		c4 = Vector.crossproduct_of(v3, v1)
		if (c1 < 0):
			c1, c2, c4 = -c1, -c2, -c4
		if (c1 != 0 and c2 >= 0 and c2 <= c1 and c4 >=0 and c4 <= c1):
			x = self.start.x + v1.dx * c2 / c1
			y = self.start.y + v1.dy * c2 / c1
			return Point(x, y)
		return None

	def trim_border(self):
		leftLimit = Divider(Point(0,0), Point(0,600), 0, 0)
		topLimit = Divider(Point(0,0), Point(600,0), 0, 0)
		rightLimit = Divider(Point(600,0), Point(600,600), 0, 0)
		bottomLimit = Divider(Point(0,600), Point(600,600), 0, 0)

		pl = self.get_inpoint_with(leftLimit)
		pt = self.get_inpoint_with(topLimit)
		pr = self.get_inpoint_with(rightLimit)
		pb = self.get_inpoint_with(bottomLimit)

		if (self.start.x > self.end.x):
			self.start, self.end = self.end, self.start

		if (pl):
			self.start = pl
		if (pr):
			self.end = pr
		if (pt):
			if (self.start.y < self.end.y):
				self.start = pt
			else:
				self.end = pt
		if (pb):
			if (self.start.y > self.end.y):
				self.start = pb
			else:
				self.end = pb

	@staticmethod
	def divider_of(p1, p2):
		pmid = Point.midpoint_of(p1 ,p2)
		v1 = Vector.vector_of(p1, p2)
		vn = Vector.normalvector_of(v1)
		ps = Point(pmid.x + vn.dx*600, pmid.y + vn.dy*600)
		pe = Point(pmid.x - vn.dx*600, pmid.y - vn.dy*600)
		return Divider(ps, pe, p1, p2)

	@staticmethod
	def copy(d):
		return Divider(d.start, d.end, d.A, d.B)

	@staticmethod
	def copy_list(l):
		return [Divider(d.start, d.end, d.A, d.B) for d in l]

	def _trim(self, divider, base):
		if (divider == None or divider.start.y < self.start.y or divider.end.y > self.end.y or self.start == self.end):
			return divider
		inpoint = self.get_inpoint_with(divider)
		vb = Vector.vector_of(inpoint, base)
		if (inpoint != None):
			p1 = self.start if (inpoint != self.start) else self.end
			v1 = Vector.vector_of(inpoint, p1)
			v2 = Vector.vector_of(inpoint, divider.start)
			v3 = Vector.vector_of(inpoint, divider.end)
			if (not v2.is_zero() and v1.crossproduct_with(v2) * v1.crossproduct_with(vb) >= 0):
				print("v1.crossproduct_with(v2) = %f" % v1.crossproduct_with(v2))
				print("Trim start to", str(inpoint))
				divider.start = inpoint
			if (not v3.is_zero() and v1.crossproduct_with(v3) * v1.crossproduct_with(vb) >= 0):
				print("v1.crossproduct_with(v3) = %f" % v1.crossproduct_with(v3))
				print("Trim end to", str(inpoint))
				divider.end = inpoint
			return None if (divider.start == divider.end) else divider
		else:
			v1 = Vector.vector_of(self.start, self.end)
			v2 = Vector.vector_of(self.start, divider.start)
			return None if (v1.crossproduct_with(v2) * v1.crossproduct_with(vb) > 0) else divider

	def trim_leftpart(self, divider):
		mid = Point.midpoint_of(divider.start, divider.end)
		mid.x -= 100
		return self._trim(divider, mid)

	def trim_rightpart(self, divider):
		mid = Point.midpoint_of(divider.start, divider.end)
		mid.x += 100
		return self._trim(divider, mid)