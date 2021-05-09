#!/usr/bin/env python3
# coding=UTF-8
# 學號: M093040067
# 系級: 資工系碩一
# 姓名: 歐陽安媛

from geometry import *
from divider import Divider


class ConvexHull:
	def __init__(self, points, upper=None, lower=None):
		self.points = points
		self.upper, self.lower = upper, lower

	@staticmethod
	def convexhull_of(points):
		if len(points) <= 3:
			Point.sort_counterclockwisely(points)
			return ConvexHull(points)
		points.sort(key=lambda p: p.x)
		half = int(len(points) / 2)
		cl = ConvexHull.convexhull_of(points[:half])
		cr = ConvexHull.convexhull_of(points[half:])
		return ConvexHull.convexhull_merge(cl, cr)

	@staticmethod
	def convexhull_merge(cl, cr):
		pu, qu, pl, ql, points = ConvexHull.merge(cl, cr)
		du = Divider.divider_of(pu, qu)
		dl = Divider.divider_of(pl, ql)
		return ConvexHull(points, upper=du, lower=dl)

	@staticmethod
	def can_clockwise(p1, p2, p3):
		v1 = Vector.vector_of(p1, p2)
		v2 = Vector.vector_of(p1, p3)
		return Vector.crossproduct_of(v1, v2) > 0

	@staticmethod
	def can_counterclockwise(p1, p2, p3):
		v1 = Vector.vector_of(p1, p2)
		v2 = Vector.vector_of(p1, p3)
		return Vector.crossproduct_of(v1, v2) < 0

	@staticmethod
	def merge(cl, cr):
		Point.sort_counterclockwisely(cl.points)
		Point.sort_counterclockwisely(cr.points)
		pi = cl.points.index(max(cl.points, key=lambda p: p.x))
		qi = cr.points.index(min(cr.points, key=lambda p: p.x))
		pn, qn = len(cl.points), len(cr.points)
		

		# upper
		prev_p = None
		prev_q = None
		pu, qu = pi, qi
		while (True):
			prev_p, prev_q = pu, qu
			while (ConvexHull.can_counterclockwise(cl.points[pu], cr.points[qu], cr.points[(qu-1+qn)%qn])):
				qu = (qu-1+qn)%qn
			
			while (ConvexHull.can_clockwise(cr.points[qu], cl.points[pu], cl.points[(pu+1+pn)%pn])):
				pu = (pu+1+pn)%pn
			
			if pu == prev_p and qu == prev_q:
				break

		
		#lower
		prev_p = None
		prev_q = None
		pl, ql = pi, qi
		while (True):
			prev_p, prev_q = pl, ql
			while (ConvexHull.can_counterclockwise(cr.points[ql], cl.points[pl], cl.points[(pl-1+pn)%pn])):
				pl = (pl-1+pn)%pn

			while (ConvexHull.can_clockwise(cl.points[pl], cr.points[ql], cr.points[(ql+1+qn)%qn])):
				ql = (ql+1+qn)%qn

			if pl == prev_p and ql == prev_q:
				break

		res = []
		#upper index is bigger to lower for left and right
		if (pl < pu):
			res += cl.points[:pl+1] + cl.points[pu:]
		else:
			res += cl.points[pu:pl+1]
		
		if (qu < ql):
			res += cr.points[:qu+1] + cr.points[ql:]
		else:
			res += cr.points[ql:qu+1]

		Point.sort_counterclockwisely(res)

		return (cl.points[pu], cr.points[qu], cl.points[pl], cr.points[ql], res)