# coding=utf-8

import components

class AppSettingsController(components.Controller):
    path = "/settings/"
    def get(self):
        return ({
            'root': '',
            'csrftoken': 'have_some_csrftoken_for_now' # I will somve this, I swear
        },200)

def init(app, api, models):
    components.register_controllers(api, [AppSettingsController])
    pass
