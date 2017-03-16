# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import time
import imgui
from settings import Settings


class ImporterOBJ():

    def __init__(self):
        self.position_x = 10
        self.position_y = 10
        self.width = 700
        self.height = 500
        self.parser_model = -1

    def draw_window(self, title, is_opened, func_process_file):
        imgui.set_next_window_size(self.width, self.height, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(self.position_x, self.position_y, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin(title, is_opened, imgui.WINDOW_SHOW_BORDERS)

        imgui.text('Select OBJ File : ' + Settings.Settings_CurrentFolder)
        imgui.separator()

        imgui.text('Parser Model:')
        imgui.same_line()
        parser_items = ['Kuplung Obj Parser 1.0', 'Kuplung Obj Parser 2.0', 'Assimp']
        _, self.parser_model = imgui.combo('##00392', self.parser_model, parser_items)
        Settings.ModelFileParser = self.parser_model

        imgui.separator()

        imgui.begin_child('scrolling')
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2(0, 1))

        imgui.columns(4, 'fileList')

        imgui.separator()
        imgui.text("ID")
        imgui.next_column()
        imgui.text("File")
        imgui.next_column()
        imgui.text("Size")
        imgui.next_column()
        imgui.text("Last Modified")
        imgui.next_column()
        imgui.separator()
        imgui.set_column_offset(1, 40)
        is_opened = self.draw_files(func_process_file)
        imgui.columns(1)
        imgui.pop_style_var(1)
        imgui.end_child()
        imgui.end()

        return is_opened

    def draw_files(self, func_process_file):
        folderContents = self.getFolderContents(Settings.Settings_CurrentFolder)
        i = 0
        selected = -1
        for entity in folderContents:
            label = '%i' % i
            _, sel = imgui.selectable(label, selected == i, imgui.SELECTABLE_SPAN_ALL_COLUMNS)
            if sel:
                selected = i
                file_name, ext = os.path.splitext(entity['path'])
                if entity['is_file'] and ext == '.obj':
                    func_process_file(os.path.dirname(entity['path']) + '/', entity['title'])
                    return False
                elif os.path.isdir(entity['path']):
                    Settings.Settings_CurrentFolder = entity['path']
                    self.draw_files(func_process_file)
            imgui.next_column()
            imgui.text(entity['title'])
            imgui.next_column()
            imgui.text(entity['size'])
            imgui.next_column()
            imgui.text(entity['modified_date'])
            imgui.next_column()
            i += 1
        return True

    def getFolderContents(self, folder):
        folderContents = []
        if os.path.isdir(folder):
            Settings.Settings_CurrentFolder = folder
            if not self.root_path(Settings.Settings_CurrentFolder):
                file = {
                    'is_file': False,
                    'title': '..',
                    'path': os.path.join(folder + '/..'),
                    'size': '',
                    'modified_date': ''
                }
                folderContents.append(file)

            ffs = os.listdir(folder)
            for file in ffs:
                full_path = folder + '/' + file
                if os.path.exists(full_path) and self.is_not_hidden(file):
                    entity = {
                        'is_file': True,
                        'title': file,
                        'path': full_path,
                        'size': self.get_file_size(os.path.getsize(folder + '/' + file)),
                        'modified_date': self.get_file_mod_date(os.path.getmtime(folder + '/' + file))
                    }
                    if os.path.isdir(full_path):
                        entity['is_file'] = False
                        entity['title'] = '<' + entity['title'] + '>'
                        entity['size'] = ''
                    folderContents.append(entity)
        return folderContents

    def root_path(self, path):
        return path == os.path.abspath(os.sep)

    def get_file_size(self, size):
        sizes = ['B', 'KB', 'MB', 'GB']
        div = rem = 0
        while size >= 1025 and div < 4:
            rem = size % 1024
            div += 1
            size /= 1024
        size_d = float(size + (rem / 1024.0))
        result = ('%.2f' % self.roundOff(size_d)) + ' ' + sizes[div]
        return result

    def roundOff(self, n):
        d = n * 100.0
        i = d + 0.5
        d = float(i) / 100.0
        return d

    def get_file_mod_date(self, timestamp):
        return time.strftime(" %Y/%m/%d,%H:%M:%S ", time.localtime(timestamp))

    def is_not_hidden(self, file_name):
        result = True
        if file_name == '.' or file_name == '..' or file_name[0] == '.':
            result = False
        return result
