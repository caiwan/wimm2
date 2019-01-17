# coding=utf-8

import components

class AppSettingsController(components.Controller):
    path = "/settings/"
    def get(self):
        return ({
            'root': '',
            'csrftoken': 'i_swear_i_ill_set_up_my_csrf_tokens_at_sone_point',
            'smartimport': {},
            'estateplan': {},
        },200)

def init(app, api, models):
    components.register_controllers(api, [AppSettingsController])
    pass
