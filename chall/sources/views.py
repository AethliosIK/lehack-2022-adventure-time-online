#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_security import login_required
from flask_login import current_user

from .models.profile_model import Profile, get_profile_manager

index = Blueprint('index', __name__)

@index.route('/')
def index_f():
    return render_template('home.html', name="Welcome")

from wtforms_alchemy import ModelForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user_id']

@index.route('/profile', methods=['GET'])
@login_required
def profile_f():
    form = {}
    user_id = current_user.get_id()
    print(user_id)
    if user_id: 
        profileManager = get_profile_manager()
        elems = profileManager.getProfile(user_id)
        print(elems)
        form = ProfileForm(**elems)
        print(form)
    return render_template('profile.html', form=form)

