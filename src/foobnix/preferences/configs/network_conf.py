#-*- coding: utf-8 -*-
'''
Created on 1 сент. 2010

@author: ivan
'''
from foobnix.preferences.config_plugin import ConfigPlugin
import gtk
from foobnix.util.proxy_connect import set_proxy_settings
import time
import urllib2
import logging
from foobnix.util.fc import FC
class NetworkConfig(ConfigPlugin):
    
    name = _("Network Settings")
    
    def __init__(self, controls):
                
        box = gtk.VBox(False, 0)        
        box.hide()
        
        self.enable_proxy = gtk.CheckButton(label=_("Enable HTTP proxy"), use_underline=True)
        self.enable_proxy.connect("clicked", self.on_enable_http_proxy)
        self.enable_proxy.show()
        
        self.frame = gtk.Frame(label=_("Settings"))
        self.frame.set_border_width(0)
        self.frame.show()
        
        all = gtk.VBox(False, 0)
        all.show()
        
        
        """URL"""
        proxy_box = gtk.HBox(False, 0)
        proxy_box.show()
        
        proxy_lable = gtk.Label(_("Server"))
        proxy_lable.set_size_request(150, -1)
        proxy_lable.show()
        
        self.proxy_server = gtk.Entry()
        self.proxy_server.show()
        
        require = gtk.Label(_("example: 66.42.182.178:3128"))
        require.show()
        
        proxy_box.pack_start(proxy_lable, False, False, 0)
        proxy_box.pack_start(self.proxy_server, False, True, 0)
        proxy_box.pack_start(require, False, True, 0)
        
        
        """LOGIN"""
        lbox = gtk.HBox(False, 0)
        lbox.show()
        
        login = gtk.Label(_("Login"))
        login.set_size_request(150, -1)
        login.show()
        
        self.login_text = gtk.Entry()
        self.login_text.show()
        
        lbox.pack_start(login, False, False, 0)
        lbox.pack_start(self.login_text, False, True, 0)
        
        """PASSWORD"""
        pbox = gtk.HBox(False, 0)
        pbox.show()
        
        password = gtk.Label(_("Password"))
        password.set_size_request(150, -1)
        password.show()
        
        self.password_text = gtk.Entry()
        self.password_text.set_visibility(False)
        self.password_text.set_invisible_char("*")
        self.password_text.show()
        
        pbox.pack_start(password, False, False, 0)
        pbox.pack_start(self.password_text, False, True, 0)
        
        """check"""
        
        check = gtk.HBox(False, 0)
        check.show()

        self.vk_test = gtk.Entry()
        self.vk_test.set_text("http://vkontakte.ru")        
        self.vk_test.show()
        
        self.test_button = gtk.Button(_("Check Connection"))
        self.test_button.set_size_request(150, -1)
        self.test_button.connect("clicked", self.text_connection)        
        self.test_button.show()
        
        self.result = gtk.Label(_("Result:"))
        self.result.show()
        
        check.pack_start(self.test_button, False, True, 0)
        check.pack_start(self.vk_test, False, False, 0)        
        check.pack_start(self.result, False, True, 0)
        
        """global"""
        all.pack_start(proxy_box, False, False, 0)
        all.pack_start(lbox, False, False, 0)
        all.pack_start(pbox, False, False, 0)        
        all.pack_start(check, False, False, 0)
        
        self.frame.add(all)

        frame_box = gtk.HBox(False, 0)
        frame_box.set_border_width(5)
        frame_box.show()
        
        box.pack_start(self.enable_proxy, False, True, 0)
        box.pack_start(self.frame, False, True, 0)
        
        self.widget = box
    
    
    def text_connection(self, *a):
        self.on_save()
        set_proxy_settings()
        init = time.time()
        try:
            f = urllib2.urlopen(self.vk_test.get_text())
            f.read()
            f.close()
        except Exception, e:
            logging.error(e)
            self.result.set_text(str(e))
            return None
        
        seconds = time.time() - init
        self.result.set_text(_("Result:") + _(" OK in seconds: ") + str(seconds))
    
    def on_enable_http_proxy(self, *a):
        if  self.enable_proxy.get_active():
            self.frame.set_sensitive(True)
            FC().proxy_enable = True
        else:
            self.frame.set_sensitive(False)
            FC().proxy_enable = False

    def on_load(self):
        self.enable_proxy.set_active(FC().proxy_enable)
        self.frame.set_sensitive(FC().proxy_enable)
        
        if  self.enable_proxy.get_active():
            FC().cookie = None
        
        if FC().proxy_url:
            self.proxy_server.set_text(FC().proxy_url)
        if FC().proxy_user:
            self.login_text.set_text(FC().proxy_user)
        if FC().proxy_password:
            self.password_text.set_text(FC().proxy_password)
            
            
    def on_save(self):
        if self.proxy_server.get_text():
            FC().proxy_url = self.proxy_server.get_text()
        else:
            FC().proxy_url = None
        
        if self.login_text.get_text():
            FC().proxy_user = self.login_text.get_text()
        else:
            FC().proxy_user = None
        
        if self.password_text.get_text():     
            FC().proxy_password = self.password_text.get_text()
        else:     
            FC().proxy_password = None
