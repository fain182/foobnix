'''
Created on Sep 28, 2010

@author: ivan
'''
from foobnix.regui.state import LoadSave
import gtk
from foobnix.regui.treeview.common_tree import CommonTreeControl
from foobnix.util.mouse_utils import is_rigth_click, is_double_left_click, \
    is_left_click
from foobnix.helpers.menu import Popup
from foobnix.util.const import FTYPE_NOT_UPDATE_INFO_PANEL, \
     DOWNLOAD_STATUS_ALL
from foobnix.regui.model import FTreeModel

class SimpleTreeControl(CommonTreeControl, LoadSave):
    def __init__(self, title_name, controls, head_visible=True):        
        CommonTreeControl.__init__(self, controls)
        self.title_name = title_name 
        
        self.set_reorderable(False)
        
        """column config"""
        column = gtk.TreeViewColumn(title_name, gtk.CellRendererText(), text=self.text[0], font=self.font[0])
        column.set_resizable(True)
        self.append_column(column)
        self.set_headers_visible(head_visible)
        
        self.configure_send_drug()
        
        self.set_type_plain()
        #self.populate_all([FModel("Madonna").add_is_file(True)])
        
        self.line_title = None
    
    def get_title(self):
        return self.title_name
    
    def on_button_press(self, w, e):
        active = self.get_selected_bean()
        if active:
            active.type = FTYPE_NOT_UPDATE_INFO_PANEL
        else:
            return None
        
        if is_left_click(e):
            if active.get_status():
                if active.get_status() == DOWNLOAD_STATUS_ALL:
                    self.controls.dm.filter(None, FTreeModel().status[0])
                else:
                    self.controls.dm.filter(active.get_status(), FTreeModel().status[0])
                
        if is_double_left_click(e):
            self.controls.play(active)
        
        if is_rigth_click(e):
            menu = Popup()
            menu.add_item('Play', gtk.STOCK_MEDIA_PLAY, self.controls.play, active)
            menu.add_item('Copy to Search Line', gtk.STOCK_COPY, self.controls.searchPanel.set_search_text, active.text)            
            menu.show(e)
        
    def on_load(self):
        pass
    
    def on_save(self):
        pass

class SimpleListTreeControl(SimpleTreeControl):
    def __init__(self, title_name, controls, head_visible=True):
        SimpleTreeControl.__init__(self, title_name, controls, head_visible)
        
        self.left_click_func = None
        self.left_click_arg = None
        
        self.connect("cursor-changed", lambda * a:self.on_func())
    
    def set_left_click_func(self, func=None, arg=None):
        self.left_click_func = func
        self.left_click_arg = arg
    
    def on_func(self):
        if self.left_click_func and self.left_click_arg:
            self.left_click_func(self.left_click_arg)
        elif self.left_click_func:
            self.left_click_func()  
    
    def on_button_press(self, w, e):
        if is_left_click(e):            
            self.on_func()                         
        if is_double_left_click(e):
            pass
        
        if is_rigth_click(e):
            pass


