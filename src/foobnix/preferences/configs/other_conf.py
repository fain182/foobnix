#-*- coding: utf-8 -*-
'''
Created on 23 дек. 2010

@author: ivan
'''

import gtk
import logging

from foobnix.preferences.config_plugin import ConfigPlugin
from foobnix.util.fc import FC
from foobnix.helpers.dialog_entry import info_dialog_with_link_and_donate
from foobnix.helpers.pref_widgets import IconBlock
from foobnix.preferences.configs import CONFIG_OTHER

class OtherConfig(ConfigPlugin):
    
    name = CONFIG_OTHER
    
    def __init__(self, controls):
        self.controls = controls
        box = gtk.VBox(False, 0)
        box.hide()        

        """save to"""
        hbox = gtk.HBox(False, 0)
        
        self.online_dir = gtk.FileChooserButton("set place")
        self.online_dir.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.online_dir.connect("current-folder-changed", self.on_change_folder)        
        self.online_dir.show()
        
        hbox.pack_start(gtk.Label(_("Save music to folder")), False, True, 0)
        hbox.pack_start(self.online_dir, True, True, 0)
        
        """disc cover size"""
        cbox = gtk.HBox(False, 0)
        cbox.show()
        
        tab_label = gtk.Label(_("Disc cover size"))
        tab_label.show()
        
        adjustment = gtk.Adjustment(value=1, lower=100, upper=350, step_incr=20, page_incr=50, page_size=0)
        self.image_size_spin = gtk.SpinButton(adjustment)
        self.image_size_spin.show()
        
        cbox.pack_start(tab_label, False, False, 0)
        cbox.pack_start(self.image_size_spin, False, True, 0)
                
        """notification"""
        self.check_new_version = gtk.CheckButton(label=_("Check for new foobnix release on start"), use_underline=True)
        self.check_new_version.show()
        
        demo = gtk.Button(_("Show new foobnix release avaliable demo dialog"))
        demo.connect("clicked", lambda * a:info_dialog_with_link_and_donate("foobnix [version]"))
        demo.show()
        
        """background image"""
        
        catbox = gtk.HBox(False, 0)
        
        self.bg_image = IconBlock("", controls, FC().background_image, FC().background_image_themes)
        
        self.is_show = gtk.CheckButton(label=_("Enable theme image"), use_underline=True)
        
        def on_change(*a):            
            active = self.is_show.get_active()
            if not active:       
                FC().background_image = None
        
        self.is_show.connect("clicked", on_change)
        
        catbox.pack_start(self.is_show, False, True, 0)
        catbox.pack_start(self.bg_image, True, True, 0)
        
        """menu position"""
        pbox = gtk.HBox(False, 0)
        pbox.show()
        
        label = gtk.Label(_("Menu type: "))
        
        self.old_style = gtk.RadioButton(None, _("Old Style (Menu Bar)"))
        self.old_style.connect("toggled", self.on_change_menu_type)
        
        self.new_style = gtk.RadioButton(self.old_style, _("New Style (Button)"))
        self.new_style.connect("toggled", self.on_change_menu_type)
        
        pbox.pack_start(label, False, False, 0)
        pbox.pack_start(self.new_style, False, True, 0)
        pbox.pack_start(self.old_style, False, False, 0)
        
        o_r_box = gtk.HBox()
        o_r_box.show()
        
        o_r_label = gtk.Label(_("Order-Repeat Switcher Style: "))
        
        self.buttons = gtk.RadioButton(None, _("Toggle Buttons"))
        #self.buttons.connect("toggled", self.on_change_o_r_style)
        
        self.labels = gtk.RadioButton(self.buttons, _("Text Labels"))
        #self.labels.connect("toggled", self.on_change_o_r_style)
        
        o_r_box.pack_start(o_r_label, False, False, 0)
        o_r_box.pack_start(self.buttons, False, True, 0)
        o_r_box.pack_start(self.labels, False, False, 0)
        
        """opacity"""
        obox = gtk.HBox(False, 0)
        obox.show()
        
        tab_label = gtk.Label(_("Opacity"))
        tab_label.show()
        
     
        
        adjustment = gtk.Adjustment(value=1, lower=20, upper=100, step_incr=1, page_incr=1, page_size=0)
        self.opacity_size = gtk.SpinButton(adjustment)
        self.opacity_size.connect("value-changed", self.on_chage_opacity)
        self.opacity_size.show()
        
        obox.pack_start(tab_label, False, False, 0)
        obox.pack_start(self.opacity_size, False, True, 0)
        
        
        """packaging"""        
        box.pack_start(hbox, False, True, 0)
        box.pack_start(cbox, False, True, 0)
        box.pack_start(self.check_new_version, False, True, 0)
        box.pack_start(demo, False, False, 0)
        box.pack_start(catbox, False, False, 0)
        box.pack_start(pbox, False, False, 0)
        box.pack_start(o_r_box, False, False, 0)
        box.pack_start(obox, False, False, 0)
        
        
        self.widget = box
    
    def on_chage_opacity(self, *a):
        opacity = self.opacity_size.get_value() / 100
        self.controls.main_window.set_opacity(opacity)
        self.controls.preferences.set_opacity(opacity)
    
    def on_change_menu_type(self, *a):
        if self.old_style.get_active():
            FC().menu_style = "old"
            
        elif self.new_style.get_active():
            FC().menu_style = "new"
        
        self.controls.top_panel.update_menu_style()
    
    '''def on_change_o_r_style(self, *a):
        if self.buttons.get_active():
            FC().order_repeat_style = "ToggleButtons"
        else:
            FC().order_repeat_style = "TextLabels"'''
        
    def on_change_folder(self, *a):
        path = self.online_dir.get_filename()       
        FC().online_save_to_folder = path        
        logging.info("Change music online folder: "+ path)  
                
    
    def on_load(self):
        self.online_dir.set_current_folder(FC().online_save_to_folder)
        self.online_dir.set_sensitive(FC().is_save_online)
        
        """disc"""
        self.image_size_spin.set_value(FC().info_panel_image_size)
        self.opacity_size.set_value(int(FC().window_opacity * 100))
        
        self.check_new_version.set_active(FC().check_new_version)
        if FC().background_image:
            self.is_show.set_active(True)   
        
        """menu style"""
        if  FC().menu_style == "new":
            self.new_style.set_active(True)        
        else: 
            self.old_style.set_active(True)
        
        if FC().order_repeat_style == "TextLabels":
            self.labels.set_active(True)
            
    def on_save(self):
        if self.is_show.get_active():    
            FC().background_image = self.bg_image.get_active_path()
            
        if self.buttons.get_active():
            FC().order_repeat_style = "ToggleButtons"
        else:
            FC().order_repeat_style = "TextLabels"
        self.controls.os.on_load()
        
        FC().info_panel_image_size = self.image_size_spin.get_value_as_int()
        FC().window_opacity = self.opacity_size.get_value() / 100
        FC().check_new_version = self.check_new_version.get_active()
        self.controls.change_backgound()
                    

