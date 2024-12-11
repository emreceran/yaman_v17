# -*- coding: utf-8 -*-
# from odoo import http


# class YamanV17(http.Controller):
#     @http.route('/yaman_v17/yaman_v17', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/yaman_v17/yaman_v17/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('yaman_v17.listing', {
#             'root': '/yaman_v17/yaman_v17',
#             'objects': http.request.env['yaman_v17.yaman_v17'].search([]),
#         })

#     @http.route('/yaman_v17/yaman_v17/objects/<model("yaman_v17.yaman_v17"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('yaman_v17.object', {
#             'object': obj
#         })

