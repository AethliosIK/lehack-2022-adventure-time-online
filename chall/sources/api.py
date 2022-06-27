#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import hashlib
from flask import request, jsonify, Blueprint
from flask_security import login_required
from flask_login import current_user

from .yamlInterpreter import yamlInterpreter
from .models.profile_model import get_profile_manager

logger = logging.getLogger(__name__)

endpoints = Blueprint('endpoints', __name__, template_folder='templates')

#utils

def api_return(succes, msg, elems=""):
    if not succes:
        return jsonify(status='danger', message=msg, elems=elems)
    return jsonify(status='success', message=msg, elems=elems)

def filter_input(value):
    if value.find("os.") != -1 or value.find("subprocess.") != -1 or value.find("socket.") != -1 or value.find("pty.") != -1:
        return True
    return False

def validateFileType(f):
        return '.' in f.filename and f.filename.split('.')[-1] == 'yml'\
                and f.content_type == "application/x-yaml"\
                and f.mimetype == "application/x-yaml"

#Endpoints

@endpoints.route('/api/<string:action>', methods=['POST'])
@login_required
def api(action):
    r, msg, elems = (False, 'Bad action', {})
    interpreter = yamlInterpreter()
    user_id = current_user.get_id()
    profileManager = get_profile_manager()
    if action == 'save':
        user_id = current_user.get_id()
        profileManager.setProfile(request.values, user_id)
        r, msg = (True, 'Successfully saved')
        logger.info("%s;save;%s" % (user_id, str(request.values)))
    if action == 'import':
        if len(request.files) == 1:
            f = request.files['file']
            value = f.stream.read()
            if validateFileType(f):
                value = value.decode("utf8")
                if filter_input(value):
                    r, msg = (False, "You can't use shell !")
                else:
                    elems = interpreter.importYaml(value)
                    if 'fail' in elems:
                        r, msg, elems = (False, 'Failure during importation : %s' % (elems['fail']), {})
                    else:
                        for k in elems:
                            e = elems[k]
                            if not isinstance(e, str):
                                elems[k] = str(e)
                        r, msg = (True, 'Successfully imported')
                    value = value.replace('\n', '\\n')
            else:
                r, msg = (False, "Only *.yml file accepted !")
            logger.info("%s;import;%s;%s" % (user_id, value, str(elems)))
        else:
            r,msg = (False, "Did you import a file ?")
            logger.info("%s;import;fail" % (user_id))
    if action == 'export':
        inputs = request.values.to_dict()
        elems = interpreter.exportYaml(inputs)
        r, msg = (True, 'Successfully exported')
        logger.info("%s;export;%s;%s" % (user_id, str(request.values), elems.replace('\n', '\\n')))
    return api_return(r, msg, elems)
