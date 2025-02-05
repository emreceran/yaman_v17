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


class hirdavat_mentese(models.Model):
    _name = "yaman.hirdavat_mentese"
    _description = 'hirdavat_mentese'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class hirdavat_kapi_kilit(models.Model):
    _name = "yaman.hirdavat_kapi_kilit"
    _description = 'hirdavat_kapi_kilit'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class hirdavat_kapi_kol(models.Model):
    _name = "yaman.hirdavat_kapi_kol"
    _description = 'hirdavat_kapi_kol'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class hirdavat_stoper(models.Model):
    _name = "yaman.hirdavat_stoper"
    _description = 'hirdavat_stoper'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class hirdavat_fitil(models.Model):
    _name = "yaman.hirdavat_fitil"
    _description = 'hirdavat_fitil'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class hirdavat_surgu(models.Model):
    _name = "yaman.hirdavat_surgu"
    _description = 'hirdavat_surgu'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Model ', required=True, translate=True)

class Oda(models.Model):
    _name = "yaman.oda"
    _description = 'Oda'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Oda', required=True, translate=True)
    oda_tip = fields.Selection([
        ('1', 'oda'),
        ('2', 'wc'),
        ('3', 'silindirli')
    ], default='1', index=True, string="Tip", tracking=True)

class EmirWizard(models.TransientModel):
    _name = 'emir.wizard'
    _description = '...'
    
    message = fields.Text(string="mesaj")


    def confirm_action(self):
        # Onaylandıktan sonra yapılacak işlem (isteğe bağlı)
        return {'type': 'ir.actions.act_window_close'}


