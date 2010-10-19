#-*- coding: utf-8 -*-
import gtk
#import gobject
from foobnix.regui.treeview.scanner import DirectoryScanner
from foobnix.regui.model import FTreeModel, FModel
from foobnix.util import LOG
import uuid
from foobnix.regui.model.signal import FControl
import copy
from foobnix.regui.treeview.drug_tree import DrugDropTree


class TreeViewControl(DrugDropTree, FTreeModel, FControl):

    def __init__(self, controls):        
        DrugDropTree.__init__(self)
        
        FTreeModel.__init__(self)
        FControl.__init__(self, controls)

        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.set_enable_tree_lines(True)

        """model config"""
        print "types", FTreeModel().types()
        self.model = gtk.TreeStore(*FTreeModel().types())

        """filter config"""
        self.filter_model = self.model.filter_new()
        print "visible", self.visible[0]
        self.filter_model.set_visible_column(self.visible[0])
        self.set_model(self.filter_model)

        """connectors"""
        self.connect("button-press-event", self.on_button_press)
        self.connect("key-release-event", self.on_key_release)

        self.count_index = 0

        self.set_reorderable(False)
        self.set_headers_visible(False)

        self.prev_iter_play_icon = None
        
        self.set_type_plain()


    def set_scrolled(self, policy_horizontal, policy_vertical):
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(policy_horizontal, policy_vertical)
        self.scroll.add_with_viewport(self)
        self.scroll.show_all()
        return self

    def get_bean_from_iter(self, model, iter):
        bean = FModel()
        id_dict = FTreeModel().cut().__dict__
        for key in id_dict.keys():
            num = id_dict[key]
            val = model.get_value(iter, num)
            setattr(bean, key, val)
        return bean
    
    def get_bean_from_row(self, row):
        bean = FModel()
        id_dict = FTreeModel().cut().__dict__
        for key in id_dict.keys():
            num = id_dict[key]
            setattr(bean, key, row[num])
        return bean


    def get_row_from_bean(self, bean):
        attributes = []
        m_dict = FTreeModel().cut().__dict__
        new_dict = dict (zip(m_dict.values(), m_dict.keys()))

        for key in new_dict.values():
            value = getattr(bean, key)
            attributes.append(value)
        return attributes

    def get_row_from_model_iter(self, model, iter):
        attributes = []
        size = len(FTreeModel().__dict__)
        for i in xrange(size):
            value = model.get_value(iter, i)
            attributes.append(value)
        return attributes

    def clear(self):
        self.count_index = 0
        self.model.clear()

    def on_button_press(self, w, e):
        pass

    def on_key_release(self, w, e):
        pass

    def delete_selected(self):
        selection = self.get_selection()
        fm, paths = selection.get_selected_rows()
        path = paths[0]
        path = self.filter_model.convert_path_to_child_path(path)
        iter = self.model.get_iter(path)
        self.model.remove(iter)

    def get_selected_bean(self):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if not paths:
            return None
        selected_bean = self._get_bean_by_path(paths[0])
        print "Selected bean", selected_bean
        return selected_bean

    def set_play_icon_to_selected_bean(self):
        selection = self.get_selection()
        filter_model, paths = selection.get_selected_rows()
        if not paths:
            return None
        path = filter_model.convert_path_to_child_path(paths[0])
        model = filter_model.get_model()
        iter = model.get_iter(path)
        model.set_value(iter, self.play_icon[0], gtk.STOCK_MEDIA_PLAY)
        if self.prev_iter_play_icon:
            model.set_value(self.prev_iter_play_icon, self.play_icon[0], None)
        self.prev_iter_play_icon = iter

    def get_child_level1_beans_by_selected(self):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        selected = model.get_iter(paths[0])
        n = model.iter_n_children(selected)
        iterch = model.iter_children(selected)

        results = []

        for i in xrange(n):
            path = model.get_path(iterch)
            bean = self._get_bean_by_path(path)
            results.append(bean)
            iterch = model.iter_next(iterch)

        return results

    def _get_bean_by_path(self, path):
        model = self.model
        LOG.info("Selecte bean path", path)

        path = self.filter_model.convert_path_to_child_path(path)
        LOG.info("Selecte bean path", path)
        iter = model.get_iter(path)

        if iter:
            bean = FModel()
            dt = FTreeModel().__dict__
            for key in dt.keys():
                setattr(bean, key, model.get_value(iter, dt[key][0]))
            return bean
        return None

    def get_bean_by_position(self, position):
        bean = FModel()
        dt = FTreeModel().__dict__
        for key in dt.keys():
            setattr(bean, key, self.model[position][dt[key][0]])

        return bean
    
    def get_all_child_beans_by_selected(self):
            filter_model, paths = self.get_selection().get_selected_rows()
            model = filter_model.get_model()
            iter = model.get_iter(paths[0])
            
            result = self.get_child_iters_by_parent(iter)
            beans = []
            for iter_cur in result:
                print iter_cur
                beans.append(self.get_bean_from_iter(model,iter_cur))
            return beans
    
    def get_child_iters_by_parent(self, iter):
        list = []
        if self.model.iter_has_child(iter):
            for i in range(0, self.model.iter_n_children(iter)):
                next_iter = self.model.iter_nth_child(iter, i)
                list.append(next_iter) 
                res = self.get_child_iters_by_parent(next_iter)
                if res:                    
                    list.extend(res) 
        return list
                
    
    def get_all_beans(self):
        beans = []
        for i in xrange(len(self.model)):
            beans.append(self.get_bean_by_position(i))
        return beans

    def get_all_selected_beans(self):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if not paths:
            return None
        beans = []
        for path in paths:
            selection.select_path(path)
            bean = self._get_bean_by_path(path)
            beans.append(bean)
        return beans

    def filter(self, query):
        if len(query.strip()) > 0:
            query = query.strip().decode("utf-8").lower()

            for line in self.model:
                name = line[self.text[0]].lower()

                if name.find(query) >= 0:
                    #LOG.info("FIND PARENT:", name, query)
                    line[self.visible[0]] = True
                else:
                    find = False
                    child_count = 0;
                    for child in line.iterchildren():
                        name = str(child[self.text[0]]).decode("utf-8").lower()
                        #name = child[self.text[0]]
                        if name.find(query) >= 0:
                            child_count += 1
                            #LOG.info("FIND CHILD :", name, query)
                            child[self.visible[0]] = True
                            line[self.visible[0]] = True
                            #line[self.POS_FILTER_CHILD_COUNT] = child_count
                            find = True
                        else:
                            child[self.visible[0]] = False
                    if not find:
                        line[self.visible[0]] = False
                    else:
                        self.expand_all()
        else:
            self.collapse_all()
            for line in self.model:
                line[self.visible[0]] = True
                for child in line.iterchildren():
                    child[self.visible[0]] = True
