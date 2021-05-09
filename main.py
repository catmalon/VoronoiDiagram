#!/usr/bin/env python3
# coding=UTF-8
# 學號: M093040067
# 系級: 資工系碩一
# 姓名: 歐陽安媛

import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
from functools import cmp_to_key
from geometry import *
from voronoi import *

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600


class VoronoiRecord:
    @staticmethod
    def parse_file(filename):
        input_lines = open(filename, encoding='utf-8').readlines()
        # filter out empty lines and one-line comments
        input_lines = [l for l in input_lines if l.strip() != "" and l.strip().split()[0][0] != "#"]
        if (len(input_lines) <= 0 or not input_lines[0][0].isalpha()):
            return None
        i, n, points, dividers = 0, len(input_lines), [], []
        while (i < n):
            data = input_lines[i].split()
            if (data[0] == 'P'):
                points.append(Point(float(data[1]), float(data[2])))
            elif (data[0] == 'E'):
                start = Point(float(data[1]), float(data[2]))
                end = Point(float(data[3]), float(data[4]))
                dividers.append(Divider(start, end, start, start))
            i += 1

        return VoronoiRecord(points, dividers)

    def __init__(self, points, dividers):
        self.points, self.dividers = points, dividers

class TestData(list):
    @staticmethod
    def parse_file(filename):
        input_lines = open(filename, encoding='utf-8').readlines()
        # filter out empty lines and one-line comments
        input_lines = [l.strip() for l in input_lines if l.strip() != "" and l.strip().split()[0][0] != "#"]
        if (len(input_lines) <= 0 or not input_lines[0][0].isdigit()):
            return None
        i, n, res = 0, len(input_lines), []
        while (i < n):
            num, points = int(input_lines[i]), TestData()
            if (num == 0 or i + num > n):
                break
            for j in range(num):
                data = input_lines[i+j+1].split()
                points.append(Point(int(data[0]), int(data[1])))
            res.append(points)
            i = i + num + 1
        return res


class VoronoiTK(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # data
        self.keyin_data = TestData()
        self.input_data, self.display_index = [], 0
        self.divide_st, self.merge_st = [], [] # for step by step
        self.voronoi_res = None # for output

        # title
        self.title("Voronoi Diagram")

        # top botton
        self.top_frame = tk.Frame(self)
        self.top_frame.pack()

        # buttons
        def create_btn(name, gif, func, enable=True):
            btn = tk.Button(self.top_frame, text=name, command=func, image=gif)
            btn.pack(side=tk.LEFT)
            if (not enable):
                btn['state'] = tk.DISABLED
            return btn
        self.res = [tk.PhotoImage(file='pic/open.gif'),
                    tk.PhotoImage(file='pic/step.gif'),
                    tk.PhotoImage(file='pic/play.gif'),
                    tk.PhotoImage(file='pic/save.gif'),
                    tk.PhotoImage(file='pic/clean.gif')]
        self.open_button = create_btn("Open", self.res[0], self.on_open)
        self.step_button = create_btn("Step", self.res[1], self.on_step)
        self.play_button = create_btn("Play", self.res[2], self.on_play)
        self.save_button = create_btn("Save", self.res[3], self.on_save, enable=False)
        self.clen_button = create_btn("Clean", self.res[4], self.on_clean)

        # canvas frame and point frame
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self, height=CANVAS_HEIGHT+10, width=10, borderwidth=1)
        self.left_frame.pack(side='left')
        self.right_frame.pack(side='right')
        self.canvas = tk.Canvas(self.left_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        # TO-DO: have test data, don't paint and return
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black')
        p = Point(event.x, event.y)
        self.keyin_data.append(p)
        
        # show in right panel for debug
        xy = '(%d, %d)' % (event.x, event.y)
        pointxy = tk.Label(self.right_frame, text=xy)
        pointxy.pack(anchor=tk.SE)

        # disable open file button for reading input file
        self.open_button['state'] = tk.DISABLED

    def on_clean(self):
        print('Clean all point and edge')
        self.canvas.delete("all")
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        del self.keyin_data[:]
        self.divide_st, self.merge_st = [], []
        self.save_button['state'] = tk.DISABLED
        self.open_button['state'] = self.step_button['state'] = self.play_button['state'] = tk.NORMAL

    # open file function
    def on_open(self):
        print('Open file')
        filename = askopenfilename(title = "Select file", filetypes = (("input files", "*.txt"), ("all files", "*.*")))
        self.input_data = TestData.parse_file(filename)
        if (self.input_data):
            self.display_index = 0
            self.on_clean()
            self.open_button['state'] = tk.DISABLED
        else:
            print("output.txt")
            record = VoronoiRecord.parse_file(filename)
            self.canvas.delete("all")
            self.draw_points(record.points)
            self.draw_dividers(record.dividers)

    # play the voronoi function
    def on_play(self):
        print('Display the Voronoi')
        self.canvas.delete("all")

        if (len(self.keyin_data) == 0 and self.display_index > len(self.input_data)):
            return

        if (self.display_index < len(self.input_data)):
            points = self.input_data[self.display_index]
            self.display_index += 1
        else:
            points = self.keyin_data
        self.voronoi_res = VoronoiDiagram.voronoi_of(points, debug=self)
        self.draw_points(points)
        self.draw_voronoi()
        self.save_button['state'] = tk.NORMAL

        # change play button state
        if (self.display_index >= len(self.input_data)):
            self.play_button['state'] = tk.DISABLED

    # save function
    def on_save(self):
        print('Save point and edge')
        f = open("output.txt", "w")
        self.voronoi_res.points.sort(key=cmp_to_key(lambda p1, p2 : -1 if (p1.x < p2.x or (p1.x == p2.x and p1.y <= p2.y)) else 1))

        for p in self.voronoi_res.points:
            f.write("P %d %d\n" % (p.x, p.y))
        for d in self.voronoi_res.dividers:
            d.trim_border()
            f.write("E %d %d %d %d\n" % (d.start.x, d.start.y, d.end.x, d.end.y))
        f.close()
    
    # step by step runing the voronoi function
    def on_step(self):
        # on start
        if (len(self.divide_st) == 0 and len(self.merge_st) == 0):
            self.canvas.delete("all")
            if (self.display_index < len(self.input_data)):
                points = self.input_data[self.display_index]
                self.display_index += 1
            else:
                points = self.keyin_data
            self.divide_st.append((0, points))

        # run until there are 2 elements for merge or 1 element with top level (result)
        while (not ((len(self.merge_st) == 1 and self.merge_st[-1][0] == 0) or 
            (len(self.merge_st) >= 2 and self.merge_st[-1][0] == self.merge_st[-2][0]))):
            level, points = self.divide_st.pop()
            if (len(points) <= 3):
                self.merge_st.append((level, VoronoiDiagram.voronoi_of(points)))
                # self.draw_points(merge_st[-1][1].points, color='Orange')
                # self.draw_dividers(merge_st[-1][1].dividers, color='Orange')
            else:
                points.sort(key=lambda p: p.x)
                half = int(len(points) / 2)
                self.divide_st.append((level+1, points[half:]))
                self.divide_st.append((level+1, points[:half]))

        # on need merge (there are 2 elements with same depth on merge stack)
        self.canvas.delete("all")

        if (len(self.merge_st) >= 2 and self.merge_st[-1][0] == self.merge_st[-2][0]):
            level = self.merge_st[-1][0] - 1
            right, left = self.merge_st.pop()[1], self.merge_st.pop()[1]
            merged = VoronoiDiagram.voronoi_merge(left, right, self)
            self.merge_st.append((level, merged))

            self.draw_points(merged.left.points, color='Orange')
            self.draw_dividers(merged.left.dividers, color='Orange')
            self.draw_points(merged.right.points, color='CornflowerBlue')
            self.draw_dividers(merged.right.dividers, color='CornflowerBlue')
            self.draw_dividers(merged.hyperplanes, color='Black', thick=2)
        else:
            # display final result, and terminate
            self.voronoi_res = self.merge_st.pop()[1]
            self.draw_points(self.voronoi_res.points)
            self.draw_voronoi()
            self.play_button['state'] = tk.DISABLED
            self.save_button['state'] = tk.NORMAL

    def draw_points(self, points, color='black'):
        for p in points:
            self.canvas.create_oval(p.x-1.5, p.y-1.5, p.x+1.5, p.y+1.5, fill=color)

    def draw_dividers(self, dividers, color='black', thick=1):
        for d in dividers:
            self.canvas.create_line(d.start.x, d.start.y, d.end.x, d.end.y, fill=color, smooth=True, width=thick)

    def draw_voronoi(self):
        # draw line and point from divider
        for d in self.voronoi_res.dividers:
            self.canvas.create_oval(d.A.x-1.5, d.A.y-1.5, d.A.x+1.5, d.A.y+1.5, fill='black')
            self.canvas.create_oval(d.B.x-1.5, d.B.y-1.5, d.B.x+1.5, d.B.y+1.5, fill='black')
            self.canvas.create_line(d.start.x, d.start.y, d.end.x, d.end.y)
    
        # draw point from convexhull
        for p in self.voronoi_res.convexhull.points:
            self.canvas.create_oval(p.x-1, p.y-1, p.x+1, p.y+1, fill='red')
    
        #draw edge from convexhull
        n = len(self.voronoi_res.convexhull.points)
        for i in range(n):
            x1, y1 = self.voronoi_res.convexhull.points[i].x, self.voronoi_res.convexhull.points[i].y
            x2, y2 = self.voronoi_res.convexhull.points[(i+1)%n].x, self.voronoi_res.convexhull.points[(i+1)%n].y
            self.canvas.create_line(x1, y1, x2, y2, fill='red', dash=(4,4))

window = VoronoiTK()
window.mainloop()