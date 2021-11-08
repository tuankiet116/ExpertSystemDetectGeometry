import wx
import os
import shape_items
import cv2
import numpy as np
import sys
from rule_editor import EditorFrame
sys.path.append('..')
from engine.inference_engine import *

def draw_lines(image, facts, contour_num):
    for i in range(contour_num):
        for fact in facts['Contour' + str(i)]:
            for line in fact.about:
                cv2.line(image, line.point1, line.point2, (0, 255, 0), 2)


def get_result(results):
    return '\n'.join(results)


def get_matched_facts(facts, contour_num):
    s = ''
    for i in range(contour_num):
        if facts['Contour' + str(i)]:
            s += '---- Shape %d ----\n' % i
        for fact in facts['Contour' + str(i)]:
            s += (fact.fact + '\n')
    return s


def get_hit_rules(rules, contour_num):
    s = ''
    for i in range(contour_num):
        if rules['Contour' + str(i)]:
            s += '---- Shape %d ----\n' % i
        for rule in rules['Contour' + str(i)]:
            s += str(rule)
    return s


class RuleFrame(wx.Frame):
    def __init__(self, parent, id, title, text):
        wx.Frame.__init__(self, parent, id, title, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX |
                                                          wx.MAXIMIZE_BOX))
        self.SetSize((400, 780))
        self.SetPosition((200, 0))
        self.ruleText = wx.TextCtrl(self, pos=(0, 0), size=(400, 780), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.ruleText.WriteText(text)


class FactFrame(wx.Frame):
    def __init__(self, parent, id, title, text):
        wx.Frame.__init__(self, parent, id, title, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX |
                                                          wx.MAXIMIZE_BOX))
        self.SetSize((400, 780))
        self.SetPosition((600, 0))
        self.factText = wx.TextCtrl(self, pos=(0, 0), size=(400, 780), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.factText.WriteText(text)


class MainFrame(wx.Frame):
    #Khởi tạo GUI với wxPython
    def __init__(self, parent, id, title, size): 
        wx.Frame.__init__(self, parent, id, title,
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX |
                                                          wx.MAXIMIZE_BOX))
        self.SetSize(size)
        self.Center()
        self.sourceLabel = wx.StaticText(self, label='Ảnh nguồn', pos=(150, 10), size=(100, 30))
        self.detectionLabel = wx.StaticText(self, label='Nhận diện hình ảnh', pos=(550, 10), size=(120, 30))
        self.openPicButton = wx.Button(self, label='Mở ảnh', pos=(830, 40), size=(150, 30))
        self.openPicButton.Bind(wx.EVT_BUTTON, self.open_picture)
        self.openEditorButton = wx.Button(self, label='Mở Trang Chỉnh Sửa Luật', pos=(830, 80), size=(150, 30))
        self.openEditorButton.Bind(wx.EVT_BUTTON, self.open_rule_editor)
        self.showRuleButton = wx.Button(self, label='Xem Luật', pos=(830, 120), size=(150, 30))
        self.showRuleButton.Bind(wx.EVT_BUTTON, self.show_rules)
        self.showFactButton = wx.Button(self, label='Show Facts', pos=(830, 160), size=(150, 30))
        self.showFactButton.Bind(wx.EVT_BUTTON, self.show_facts)
        self.treeLabel = wx.StaticText(self, label='Chọn hình dạng nhận diện', pos=(830, 210), size=(150, 30))
        self.shapeTree = wx.TreeCtrl(self, pos=(830, 240), size=(260, 200))
        root = self.shapeTree.AddRoot('Tất cả') #Khởi tạo cây chọn hình ảnh
        self.add_tree_nodes(root, shape_items.tree) #Thêm các nhánh con
        self.shapeTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.shape_chosen)
        self.shapeTree.Expand(root)
        self.show_picture('init_source.png', (10, 40))
        self.show_picture('init_detection.png', (420, 40))
        self.resultLabel = wx.StaticText(self, label='Kết quả nhận diện', pos=(100, 460), size=(150, 30))
        self.resultText = wx.TextCtrl(self, pos=(10, 490), size=(310, 280), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.matchedFactLabel = wx.StaticText(self, label='Facts đã khớp', pos=(430, 460), size=(100, 30))
        self.matchedFactText = wx.TextCtrl(self, pos=(340, 490), size=(310, 280), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.hitRuleLabel = wx.StaticText(self, label='Theo luật', pos=(780, 460), size=(100, 30))
        self.hitRuleText = wx.TextCtrl(self, pos=(670, 490), size=(310, 280), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.title = title
        self.pic_path = None
        self.engine = None
        self.contour_num = None
        self.Show()

    # Mở dialog chọn ảnh
    def open_picture(self, event):
        file_wildcard = 'picture file(*.png)|*.png|All files(*.*)|*.*' # Định dạng file có thể mở
        dlg = wx.FileDialog(self, 'Mở File Ảnh', (os.getcwd() + '/../test'), style=wx.FD_OPEN , wildcard=file_wildcard) #Khởi tạo dialog
        if dlg.ShowModal() == wx.ID_OK:
            self.pic_path = dlg.GetPath()
            self.SetTitle(self.title + ' -- Nguồn ảnh: ' + dlg.GetPath())
        else:
            dlg.Destroy()
            return
        dlg.Destroy()
        self.show_picture(self.pic_path, (10, 30))
        self.show_picture('init_detection.png', (420, 30))
        self.engine = setup_engine(self.pic_path) # cài đặt công cụ suy diễn
        self.contour_num = len(self.engine.fact_library) #lấy số lượng 

    #Mở trang thêm luật
    def open_rule_editor(self, event):
        editor = EditorFrame(self, 0, 'Chỉnh sửa luật', (600, 400))
        editor.Show()

    #Hiển thị luật 
    def show_rules(self, event):
        with open('../rules/rules.txt') as f:
            text = ''.join(f.readlines())
        ruleFrame = RuleFrame(self, 1, 'Tất cả luật', text)
        ruleFrame.Show()

    #Hiển thị thông tin đã tính toán ra 1 file fact
    def show_facts(self, event):
        with open('../facts/facts.txt') as f:
            text = ''.join(f.readlines())
        factFrame = FactFrame(self, 2, 'All Facts', text)
        factFrame.Show()

    #Hiển thị ảnh bitmap
    def show_picture(self, path, pos):
        pic = wx.Image(path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmp = wx.StaticBitmap(self, 0, pic, pos=pos)
        bmp.Show()

    #Thêm vào cây hình học
    def add_tree_nodes(self, parent_item, items):
        for item in items:
            if type(item) == str:
                self.shapeTree.AppendItem(parent_item, item)
            else:
                newItem = self.shapeTree.AppendItem(parent_item, item[0])
                self.add_tree_nodes(newItem, item[1])

    #Lấy Item được chọn trên cây hình học
    def get_item_text(self, item):
        if self.shapeTree.GetItemText(item) == 'All Shapes':
            return
        elif item:
            return self.shapeTree.GetItemText(item)
        else:
            return ''

    # Xử lý khi chọn vào các hình học trong cây hình học => dự đoán xem là hình nào?
    def shape_chosen(self, event):
        tmp = self.get_item_text(event.GetItem())
        if not tmp:
            return
        else:
            chosen_shape = ('the shape is ' + tmp)
            set_goal(self.engine, chosen_shape) # Đặt mục tiêu cho công cụ suy luận
            results, matched_facts, hit_rules = main_run(self.engine) #Khởi chạy công cụ suy luận
            source_image = cv2.imread(self.pic_path)
            detection_image = np.zeros(source_image.shape, np.uint8)
            draw_lines(detection_image, matched_facts, self.contour_num)
            cv2.imwrite('detection.png', detection_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            self.show_picture('detection.png', (420, 30))
            self.resultText.Clear()
            self.resultText.WriteText(get_result(results))
            self.matchedFactText.Clear()
            self.matchedFactText.WriteText(get_matched_facts(matched_facts, self.contour_num))
            self.hitRuleText.Clear()
            self.hitRuleText.WriteText(get_hit_rules(hit_rules, self.contour_num))


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1, title='Nhận diện hình học', size=(1050, 850))
    app.MainLoop()