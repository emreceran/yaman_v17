# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math, collections


class Renk(models.Model):
    _name = "yaman.renk"
    _description = 'Kapı Rengi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Renk', required=True, translate=True)


class plastikpervaz(models.Model):
    _name = "yaman.plastik"
    _description = 'PLastik Pervaz'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='PLastik Pervaz tipi ', required=True, translate=True)


class Oda(models.Model):
    _name = "yaman.oda"
    _description = 'Oda'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Oda', required=True, translate=True)
