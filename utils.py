# -*- coding: utf-8 -*-
"""
@author yumu
@version 1.0.0
"""
class ColorPrinter:
    foregroundColor = {
        "black":"30",
        "red":"31",
        "green":"32",
        "yellow":"33",
        "blue":"34",
        "purple":"35",
        "cyan":"36",
        "white":"37"
    }

    backgroundColor = {
        "black": "40",
        "red": "41",
        "green": "42",
        "yellow": "43",
        "blue": "44",
        "purple": "45",
        "cyan": "46",
        "white": "47"
    }

    def info_text(self,text:str)->str:
        return "\033[0;32m"+str(text)+"\033[0m"

    def wrong_text(self,text:str)->str:
        return "\033[0;31m"+str(text)+"\033[0m"

    def warn_text(self,text:str)->str:
        return "\033[0;33m" + str(text) + "\033[0m"

    def other_text(self,text:str)->str:
        return "\033[0;34m" + str(text) + "\033[0m"

    def special_text(self,text:str)->str:
        return "\033[0;35m" + str(text) + "\033[0m"

    def custom_text(self,text:str,foreground_color:str,background_color:str,show_method)->str:
        return "\033["+str(show_method)+";"+str(self.foregroundColor[foreground_color])+";"+str(self.backgroundColor[background_color])+"m" + text + "\033[0m"
