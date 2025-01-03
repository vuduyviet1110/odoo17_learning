from odoo import http
from odoo.http import request


class Main(http.Controller):
   @http.route('/course', type='http', auth="user", website=True)
   def course(self):
      return request.render(
         'education.course', {
            'courses': request.env['course'].search([]),
         })