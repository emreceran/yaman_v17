# -*- coding: utf-8 -*-

from odoo import models, fields, api
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
    name = fields.Char(string='PLastik Pervaz kodu ', required=True, translate=True)
    description = fields.Char(string='PLastik Pervaz adı ', required=True, translate=True)

class plastikkasa(models.Model):
    _name = "yaman.plastikkasa"
    _description = 'PLastik Kasa'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='PLastik kasa kodu ', required=True, translate=True)
    description = fields.Char(string='PLastik kasa adı ', required=True, translate=True)
    value = fields.Char(string='PLastik kasa değeri ', required=True, translate=True)


class Oda(models.Model):
    _name = "yaman.oda"
    _description = 'Oda'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Oda', required=True, translate=True)

