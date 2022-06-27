#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import sys
class yamlInterpreter:
    def importYaml(self, content):
        elems = {}
        try :
            sys.modules['os'] = None
            sys.modules['subprocess'] = None
            elems = yaml.load(content, Loader=yaml.UnsafeLoader)
        except Exception as e:
            return {'fail': str(e)}
        return elems

    def exportYaml(self, elems):
        s = yaml.dump(elems, default_flow_style=False)
        return s
