#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from sources import launch_app

app = launch_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
