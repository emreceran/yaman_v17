# -*- coding: utf-8 -*-

import base64
import io
from PIL import Image
from odoo import models, fields, api
from odoo.exceptions import ValidationError # type: ignore
from odoo.exceptions import UserError # type: ignore
from collections import defaultdict
import math, collections



class Project(models.Model):
    _inherit = 'project.project'
    _description = 'yaman.yaman'

    olcu_alan = fields.Many2one('res.users', string ='Ölçüyü Alan', index=True)
    kaydi_giren = fields.Many2one('res.users', string ="Kaydı Giren", index=True)
    kapi_model = fields.Char(string="Kapı Modeli")
    yuzey_tipi = fields.Selection([
        ('1', 'PVC'),
        ('2', 'LAKE'),
        ('3', 'MELAMİN'),
        ('4', 'LAMİNANT'),
    ], default='1', index=True, string="Yüzey Tipi", tracking=True)

    seren_tipi = fields.Selection([
        ('1', 'AĞAÇ'),
        ('2', 'MDF'),
    ], default='1', index=True, string="Seren Tipi", tracking=True)
    kasa_rengi = fields.Many2one('yaman.renk', string="Kasa Rengi ")
    yuzey_rengi = fields.Many2one('yaman.renk', string="Yüzey Rengi ")
    pervaz_rengi = fields.Many2one('yaman.renk', string="Pervaz Rengi ")
    yuzey_kalinlik = fields.Integer(string="Yüzey Kalınlığı ")
    kasa_tipi = fields.Selection([
        ('1', 'DÜZ'),
        ('2', 'BOMBE'),
    ], default='1', index=True, string="Kasa tipi", tracking=True)
    pit_kalinlik = fields.Integer(string="Pervaz İç Taraf Kalınlık")
    pdt_kalinlik = fields.Integer(string="Pervaz Dış Taraf Kalınlık")
    pb_kalinlik = fields.Integer(string="Pervaz Başlık Kalınlık")
    pi_genislik = fields.Integer(string="Pervaz İç Genişlik")
    pd_genislik = fields.Integer(string="Pervaz Dış Genişlik")
    pb_genislik = fields.Integer(string="Pervaz Başlık Genişlik")
    hirdavat = fields.Char(string="Hırdavat")
    cnc_description = fields.Text(string="CNC Emri Açıklaması", default="-")
    image1 = fields.Image("Resim")
    image2 = fields.Image("Resim")
    mentese=fields.Many2one('yaman.hirdavat_mentese', string="Menteşe", index=True)
    kapi_kilit=fields.Many2one('yaman.hirdavat_kapi_kilit', string="Kapı kilit", index=True)
    kapi_kol=fields.Many2one('yaman.hirdavat_kapi_kol', string="Kapı Kol", index=True)
    stoper=fields.Many2one('yaman.hirdavat_stoper', string="Stoper", index=True)
    vida=fields.Selection([
        ('1', 'Yok'),
        ('2', 'Var')
    ], default='1', index=True, string="Vida", tracking=True)
    fitil=fields.Many2one('yaman.hirdavat_fitil', string="Fitil", index=True)
    surgu=fields.Many2one('yaman.hirdavat_surgu', string="Gömme Sürgü", index=True)
    kopuk=fields.Selection([
        ('1', 'Yok'),
        ('2', 'Var')
    ], default='1', index=True, string="Köpük", tracking=True)
    silikon=fields.Selection([
        ('1', 'Yok'),
        ('2', 'Var')
    ], default='1', index=True, string="Silikon", tracking=True)
 
    
    Tum_toplam_kapi = fields.Char(string="Tüm Toplam Kapı Sayısı", compute="_compute_Tum_toplam_kapi")
    toplam_kapi = fields.Char(string="Toplam Kapı Sayısı", compute="_compute_toplam_kapi")
    plastik_kapi = fields.Char(string="Plastik Kapı Sayısı", compute="_compute_toplam_plastik_kapi")
    kapali_toplam_kapi = fields.Char(string="Kapalı Kapı Sayısı", compute="_compute_kapali_toplam_kapi")
    citacamli_toplam_kapi = fields.Char(string="Ç. Camlı Kapı Sayısı", compute="_compute_citacamli_toplam_kapi")
    scamli_toplam_kapi = fields.Char(string="S. Camlı Kapı Sayısı", compute="_compute_scamli_toplam_kapi")
    surgulu_kapali_toplam_kapi = fields.Char(string="Sürgülü Kapalı Kapı Sayısı",
                                             compute="_compute_surgulu_kapali_toplam_kapi")
    surgulu_citacamli_toplam_kapi = fields.Char(string="Sürgülü Ç. Camlı Kapı Sayısı",
                                                compute="_compute_surgulu_citacamli_toplam_kapi")
    surgulu_scamli_toplam_kapi = fields.Char(string="Sürgülü S. Camlı Kapı Sayısı",
                                             compute="_compute_surgulu_scamli_toplam_kapi")
    sadece_kapali_toplam_kapi = fields.Char(string="Sadece Kapalı Kapı Sayısı",
                                            compute="_compute_sadece_kapali_toplam_kapi")
    sadece_citacamli_toplam_kapi = fields.Char(string="Sadece Ç. Camlı Kapı Sayısı",
                                               compute="_compute_sadece_citacamli_toplam_kapi")
    sadece_scamli_toplam_kapi = fields.Char(string="Sadece S. Camlı Kapı Sayısı",
                                            compute="_compute_sadece_scamli_toplam_kapi")

    cam_citasi = fields.Integer(string="Cam Çıtası")
    klapa_citasi = fields.Integer(string="Klapa Çıtası")
    supurgelik = fields.Char(string="Süpürgelik")
    
    sarim_emri_disabled = fields.Boolean(compute="check_stage_tasks", string="Sarım Emri", store=True)
    catim_emri_disabled = fields.Boolean(compute="check_stage_tasks", string="Çatım Emri", store=True)
    cnc_emri_disabled = fields.Boolean(compute="check_stage_tasks", string="CNC Emri", store=True)
    plastik_emri_disabled = fields.Boolean(compute="check_stage_tasks", string="Satın Alma Emri", store=True)

    # @api.depends("task_ids")
    # def _compute_Tum_toplam_kapi(self):
    #     for project in self:
    #         proe = self.env['project.project'].search([('project_id', '=', project.id)])

    #         tasks= proe.task_ids
    #         gorevler = [gorev for gorev in tasks if gorev.stage_id.name == "satırlar"]
    #         toplam_adet = 0
    #         for i in gorevler:
    #             toplam_adet += i.adet

    #         for record in self:
    #             record.Tum_toplam_kapi = str(toplam_adet)
            
            
    @api.depends("task_ids")
    def _compute_toplam_kapi(self):
        for record in self:
            toplam_adet = sum(record.task_ids.filtered(lambda t: t.stage_id.name == "satırlar").mapped('adet'))
            record.toplam_kapi = toplam_adet
        # tasks = self.task_ids
        # gorevler = [gorev for gorev in tasks if gorev.stage_id.name == "satırlar"]
        # toplam_adet = 0
        # for i in gorevler:
        #     toplam_adet += i.adet
        #
        # for record in self:
        #     record.toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_toplam_plastik_kapi(self):
        tasks = self.task_ids
        gorevler = [gorev for gorev in tasks if gorev.stage_id.name == "satırlar" and gorev.plastik == '1']
        toplam_adet = 0
        for i in gorevler:
            toplam_adet += i.adet

        for record in self:
            record.plastik_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_kapali_toplam_kapi(self):
        tasks = self.task_ids
        kapalilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "1":
                    kapalilar.append(gorev)

        toplam_adet = 0
        for i in kapalilar:
            toplam_adet += i.adet

        for record in self:
            record.kapali_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_citacamli_toplam_kapi(self):
        tasks = self.task_ids
        citalicamlilar = []

        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":

                if gorev.tip == "2":
                    citalicamlilar.append(gorev)

        toplam_adet = 0
        for i in citalicamlilar:
            toplam_adet += i.adet

        for record in self:
            record.citacamli_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_scamli_toplam_kapi(self):
        tasks = self.task_ids
        scamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":

                if gorev.tip == "3":
                    scamlilar.append(gorev)

        toplam_adet = 0
        for i in scamlilar:
            toplam_adet += i.adet

        for record in self:
            record.scamli_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_surgulu_kapali_toplam_kapi(self):
        tasks = self.task_ids
        surguluKapalilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "5":
                    surguluKapalilar.append(gorev)

        toplam_adet = 0
        for i in surguluKapalilar:
            toplam_adet += i.adet

        for record in self:
            record.surgulu_kapali_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_surgulu_citacamli_toplam_kapi(self):
        tasks = self.task_ids
        surguluCitaliCamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "6":
                    surguluCitaliCamlilar.append(gorev)

        toplam_adet = 0
        for i in surguluCitaliCamlilar:
            toplam_adet += i.adet

        for record in self:
            record.surgulu_citacamli_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_surgulu_scamli_toplam_kapi(self):
        tasks = self.task_ids
        surguluSCamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "7":
                    surguluSCamlilar.append(gorev)

        toplam_adet = 0
        for i in surguluSCamlilar:
            toplam_adet += i.adet

        for record in self:
            record.surgulu_scamli_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_sadece_kapali_toplam_kapi(self):
        tasks = self.task_ids
        sadeceKapalilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "8":
                    sadeceKapalilar.append(gorev)

        toplam_adet = 0
        for i in sadeceKapalilar:
            toplam_adet += i.adet

        for record in self:
            record.sadece_kapali_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_sadece_citacamli_toplam_kapi(self):
        tasks = self.task_ids
        sadeceCitaliCamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "9":
                    sadeceCitaliCamlilar.append(gorev)

        toplam_adet = 0
        for i in sadeceCitaliCamlilar:
            toplam_adet += i.adet

        for record in self:
            record.sadece_citacamli_toplam_kapi = str(toplam_adet)

    @api.depends("task_ids")
    def _compute_sadece_scamli_toplam_kapi(self):
        tasks = self.task_ids
        sadeceSCamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "10":
                    sadeceSCamlilar.append(gorev)

        toplam_adet = 0
        for i in sadeceSCamlilar:
            toplam_adet += i.adet

        for record in self:
            record.sadece_scamli_toplam_kapi = str(toplam_adet)


    @api.depends('task_ids', 'task_ids.stage_id')
    def check_stage_tasks(self):
        for record in self:
            sarim_emri_stage_id = self.env['project.task.type'].search([('name', '=', 'SARMA EMRİ')], limit=1).id
            catim_emri_stage_id = self.env['project.task.type'].search([('name', '=', 'ÇATIM EMRİ')], limit=1).id
            cnc_emri_stage_id = self.env['project.task.type'].search([('name', '=', 'CNC EMRİ')], limit=1).id
            plastik_emri_stage_id = self.env['project.task.type'].search([('name', '=', 'SATIN ALMA EMRİ')], limit=1).id

            record.sarim_emri_disabled = self.env['project.task'].search_count([('project_id', '=', record.id), ('stage_id', '=', sarim_emri_stage_id)]) > 0
            print(record.sarim_emri_disabled)
            
            record.catim_emri_disabled = self.env['project.task'].search_count([('project_id', '=', record.id), ('stage_id', '=', catim_emri_stage_id)]) > 0
            print(record.catim_emri_disabled)

            record.cnc_emri_disabled = self.env['project.task'].search_count([('project_id', '=', record.id), ('stage_id', '=', cnc_emri_stage_id)]) > 0
            print(record.cnc_emri_disabled)

            record.plastik_emri_disabled = self.env['project.task'].search_count([('project_id', '=', record.id), ('stage_id', '=', plastik_emri_stage_id)]) > 0
            print(record.plastik_emri_disabled)

            print("***********************")
            print("***********************")
            print("***********************")
            
            

    def tip_plastik_toplam_kapi(self, tip):
        tasks = self.task_ids
        plastik_toplam_kapi = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == tip and gorev.plastik=='1':
                    plastik_toplam_kapi.append(gorev)

        toplam_adet = 0
        for i in plastik_toplam_kapi:
            toplam_adet += i.adet

        
        return toplam_adet
    
    def tip_mdf_toplam_kapi(self, tip):
        tasks = self.task_ids
        mdf_toplam_kapi = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == tip and gorev.plastik=='2':
                    mdf_toplam_kapi.append(gorev)

        toplam_adet = 0
        for i in mdf_toplam_kapi:
            toplam_adet += i.adet

        
        return toplam_adet

    def get_field_groups(self):
        fields = [
            {"label": "Müşteri", "value": self.partner_id.name if self.partner_id.name else None},
            {"label": "Ölçüyü Alan", "value": self.olcu_alan.name if self.olcu_alan else None},
            {"label": "Kaydı Giren", "value": self.kaydi_giren.name if self.kaydi_giren else None},
            {"label": "Kapı Modeli", "value": self.kapi_model or None},
            {"label": "Yüzey Tipi", "value": dict(self._fields['yuzey_tipi'].selection).get(self.yuzey_tipi, None)},
            {"label": "Seren Tipi", "value": dict(self._fields['seren_tipi'].selection).get(self.seren_tipi, None)},
            {"label": "Kasa Rengi", "value": self.kasa_rengi.name if self.kasa_rengi else None},
            {"label": "Yüzey Rengi", "value": self.yuzey_rengi.name if self.yuzey_rengi else None},
            {"label": "Pervaz Rengi", "value": self.pervaz_rengi.name if self.pervaz_rengi else None},
            {"label": "Yüzey Kalınlığı", "value": self.yuzey_kalinlik if self.yuzey_kalinlik else None},
            {"label": "Kasa Tipi", "value": dict(self._fields['kasa_tipi'].selection).get(self.kasa_tipi, None)},
            {"label": "Pervaz İç Kalınlık", "value": self.pit_kalinlik if self.pit_kalinlik else None},
            {"label": "Pervaz Dış Kalınlık", "value": self.pdt_kalinlik if self.pdt_kalinlik else None},
            {"label": "Pervaz Başlık Kalınlık", "value": self.pb_kalinlik if self.pb_kalinlik else None},
            {"label": "Pervaz İç Genişlik", "value": self.pi_genislik if self.pi_genislik else None},
            {"label": "Pervaz Dış Genişlik", "value": self.pd_genislik if self.pd_genislik else None},
            {"label": "Pervaz Başlık Genişlik", "value": self.pb_genislik if self.pb_genislik else None},
            {"label": "Toplam Kapı Sayısı", "value": self.toplam_kapi or None},
            {"label": "MDF Kapı Sayısı", "value": (int(self.toplam_kapi) - int(self.plastik_kapi)) or None},
            {"label": "Plastik Kapı Sayısı", "value": self.plastik_kapi or None},
            # {"label": "Kapalı Kapı Sayısı", "value": self.kapali_toplam_kapi or None},
            {"label": "Plastik Kapalı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('1') or None},
            {"label": "MDF Kapalı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('1') or None},
            # {"label": "Ç. Camlı Kapı Sayısı", "value": self.citacamli_toplam_kapi or None},
            {"label": "Plastik Ç. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('2') or None},
            {"label": "MDF Ç. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('2') or None},
            # {"label": "S. Camlı Kapı Sayısı", "value": self.scamli_toplam_kapi or None},
            {"label": "Plastik S. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('3') or None},
            {"label": "MDF S. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('3') or None},
            # {"label": "Sürgülü Kapalı Kapı Sayısı", "value": self.surgulu_kapali_toplam_kapi or None},
            {"label": "Plastik Sürgülü Kapalı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('5') or None},
            {"label": "MDF Sürgülü Kapalı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('5') or None},
            # {"label": "Sürgülü Ç. Camlı Kapı Sayısı", "value": self.surgulu_citacamli_toplam_kapi or None},
            {"label": "Plastik Sürgülü Ç. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('6') or None},
            {"label": "MDF Sürgülü Ç. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('6') or None},
            # {"label": "Sürgülü S. Camlı Kapı Sayısı", "value": self.surgulu_scamli_toplam_kapi or None},
            {"label": "Plastik Sürgülü S. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('7') or None},
            {"label": "MDF Sürgülü S. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('7') or None},
            # {"label": "Sadece Kapalı Kapı Sayısı", "value": self.sadece_kapali_toplam_kapi or None},
            {"label": "Plastik Sadece Kapalı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('8') or None},
            {"label": "MDF Sadece Kapalı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('8') or None},
            # {"label": "Sadece Ç. Camlı Kapı Sayısı", "value": self.sadece_citacamli_toplam_kapi or None},
            {"label": "Plastik Sadece Ç. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('9') or None},
            {"label": "MDF Sadece Ç. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('9') or None},
            # {"label": "Sadece S. Camlı Kapı Sayısı", "value": self.sadece_scamli_toplam_kapi or None},
            {"label": "Plastik Sadece S. Camlı Kapı Sayısı", "value": self.tip_plastik_toplam_kapi('10') or None},
            {"label": "MDF Sadece S. Camlı Kapı Sayısı", "value": self.tip_mdf_toplam_kapi('10') or None},
            {"label": "Cam Çıtası", "value": self.cam_citasi or None},
            {"label": "Klapa Çıtası", "value": self.klapa_citasi or None},
            {"label": "Süpürgelik", "value": self.supurgelik or None},
            {"label": "Hırdavat", "value": self.hirdavat or None},
        ]

        # Boş (None) ve 0 değerlerini filtrele
        filtered_fields = [field for field in fields if field['value'] not in [0, '0', None]]
        
        # Eğer liste tek sayıda eleman içeriyorsa, bir yer tutucu ekle
        if len(filtered_fields) % 2 != 0:
            filtered_fields.append({"label": "", "value": ""})
        
        # İkişerli gruplara böl
        grouped_fields = [filtered_fields[i:i+2] for i in range(0, len(filtered_fields), 2)]
            
        return grouped_fields

    def uretim_emirleri(self):
        tasks = self.task_ids

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                gorevler.append(gorev)

        return gorevler

    def _sarim_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id:
                gorevler.append(gorev)

        return gorevler

    def _tum_yuzey_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'YÜZEY' in gorev.name:
                gorevler.append(gorev)

        return gorevler

    def _plastik_yuzey_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'YÜZEY' in gorev.name and gorev.plastik == '1':
                gorevler.append(gorev)

        return gorevler

    def _mdf_yuzey_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'YÜZEY' in gorev.name and gorev.plastik == '2':
                gorevler.append(gorev)

        return gorevler

    def cnc_emirleri_getir(self):

        tasks = self.task_ids
        CNC_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "CNC EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == CNC_emri_stage_id:
                gorevler.append(gorev)

        return gorevler

    def _pervaz_emirleri_getir(self):
        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'PERVAZ' in gorev.name:
                gorevler.append(gorev)

        return gorevler
    
    def _siparis_emirleri_getir(self):
        tasks = self.task_ids
        plastik_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SATIN ALMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == plastik_emri_stage_id:
                gorevler.append(gorev)

        return gorevler
    def hirdavat_emirleri_getir(self):
        tasks = self.task_ids
        hırdavat_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "HIRDAVAT EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == hırdavat_emri_stage_id:
                gorevler.append(gorev)

        return gorevler

    def _kas_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'KASA' in gorev.name:
                gorevler.append(gorev)

        return gorevler

    def _catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id:
                gorevler.append(gorev)
        return gorevler

    def _plastik_catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '1' and gorev.plastik == '1':
                gorevler.append(gorev)
        return gorevler

    def _mdf_catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '1' and gorev.plastik == '2':
                gorevler.append(gorev)
        return gorevler

    def _plastik_kesim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '2' and gorev.plastik == '1':
                gorevler.append(gorev)
        return gorevler

    def _mdf_kesim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '2' and gorev.plastik == '2':
                gorevler.append(gorev)
        return gorevler

    def cam_citalari_getir(self):

        """
        1- cam_citasini çıtalı camlıların adedi ile çarp
        2- klapa_citasi çıtalı camlıalrın adeti ile çarp
        3- en>100 olan çıtalı camlıların adetini 2 ile çarp bini_citasi yap
        4- toplam süpürge adetini direk yaz

        """

        gorevler = self.uretim_emirleri()
        citali_gorevler = [gorev for gorev in gorevler if gorev.tip in ['2', '6', '9']]  # kontrol edilecek
        citali_kapi_adeti = 0
        for kapi in citali_gorevler:
            citali_kapi_adeti += kapi.adet

        cam_cita_adet = self.cam_citasi * citali_kapi_adeti
        klapa_adet = self.klapa_citasi * citali_kapi_adeti

        buyuk_yuz_gorevler = [gorev for gorev in citali_gorevler if gorev.en > 100]
        bini_cita_adet = 0
        for kapi in buyuk_yuz_gorevler:
            bini_cita_adet += kapi.adet
        bini_cita_adet = bini_cita_adet * 2
        
        salmaCamlilar = [gorev for gorev in gorevler if gorev.tip == "3"] 
        buyuk_yuz_salmaCamlilar = [gorev for gorev in salmaCamlilar if gorev.en > 100]
        salmaCamlilar_bini_cita_adet = 0
        for kapi in buyuk_yuz_salmaCamlilar:
           salmaCamlilar_bini_cita_adet += kapi.adet
        salmaCamlilar_bini_cita_adet = salmaCamlilar_bini_cita_adet * 2
        
        
        liste = [cam_cita_adet, klapa_adet, bini_cita_adet + salmaCamlilar_bini_cita_adet]
        return liste


    def kasa_emirleri(self, gorevler, sarma_emri_stage_id, plastik):

        kucukenli_gorevler = []
        buyukenli_gorevler = []
        surgulu_kucukenli_gorevler = []
        surgulu_buyukenli_gorevler = []

        """"tüm üretim emirleri küçükenli ve büyükenli olacak şeilde ikiye ayrılır
        görevn eni 100cmden büyükse büyükenli denir"""

        for gorev in gorevler:
            if gorev.tip in ['1', '2', '3','4']:  # normal tip
                if gorev.en > 100:
                    buyukenli_gorevler.append(gorev)
                else:
                    kucukenli_gorevler.append(gorev)
            elif gorev.tip in ['5', '6', '7']:  # sürgülü tip
                if gorev.en > 100:
                    surgulu_buyukenli_gorevler.append(gorev)
                else:
                    surgulu_kucukenli_gorevler.append(gorev)

        """kasa boylaarı ikiye ayrılır küçük ve büyük enlilerin set yapmaamız tekrarlyan
        değerleri teke indirmek için çünkü aynı kasa emirlerini birleyecez"""
        kucukenli_kasa_boylari = set([a.kasa_eni for a in kucukenli_gorevler])
        buyukenli_kasa_boylari = set([a.kasa_eni for a in buyukenli_gorevler])
        surgulu_kucukenli_kasa_boylari = set([a.kasa_eni for a in surgulu_kucukenli_gorevler])
        surgulu_buyukenli_kasa_boylari = set([a.kasa_eni for a in surgulu_buyukenli_gorevler])

        """küçükenli listesi oluşturulur boş liste aşağıdaki for döngüü içinde aynı
        kasaenine sahip görevlerin adetleri toplanıor boy, adet] olarak listeye yazılır """
        kucuk_adetler = []

        for boy in kucukenli_kasa_boylari:
            adet = 0
            for gorev in kucukenli_gorevler:

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            kucuk_adetler.append([boy, adet])

        """büyükenli adetler küçükenlide olduğu gibi toplanır"""

        buyuk_adetler = []

        for boy in buyukenli_kasa_boylari:
            adet = 0
            for gorev in buyukenli_gorevler:

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            buyuk_adetler.append([boy, adet])

        surgulu_kucuk_adetler = []

        for boy in surgulu_kucukenli_kasa_boylari:
            adet = 0
            for gorev in surgulu_kucukenli_gorevler:

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            surgulu_kucuk_adetler.append([boy, adet])
            buyuk_adetler = []

        surgulu_buyuk_adetler = []

        for boy in surgulu_buyukenli_kasa_boylari:
            adet = 0
            for gorev in surgulu_buyukenli_gorevler:

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            surgulu_buyuk_adetler.append([boy, adet])

        """kasa emirleri oluşturuyoruz...
        küçük_adetler listesindeki her bir eleman sta[1] ile adeti çağrılır bu adet 2.5 ile çarpılıp üste yuarlanır.
        aynı proje_id seçilir proje içinde olsun diye,
        plaanned_hours üretimi takip etmek için kullanılacak planaanlanan saatler
        yerine üretilenmiktarlar girilecek,
        görrevin plastik olup olmadığı belirtilir,
        isim olarak "KASA" + str(sta[0]) + " cm " + str(math.ceil(sta[1] * 2.5)) + " Adet"  değeri verilir"""

        for sta in kucuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': math.ceil(sta[1] * 2.5),
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'adet': math.ceil(sta[1] * 2.5),
                                             'name': "KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * 2.5)) + " Adet"})

        """küçükenlinin üretildiği gibi büyükenliler de üretilir tek fark 
        2.5 değil 3 ile çarpılır"""
        for sta in buyuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': math.ceil(sta[1] * 3),
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name': "KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * (2.5 if sta[0] < 138 else 3))) + " Adet"})

        for sta in surgulu_kucuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': math.ceil(sta[1] * 2.5),
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name': "Lambasız KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * 2.5)) + " Adet"})

        """küçükenlinin üretildiği gibi büyükenliler de üretilir tek fark 
        2.5 değil 3 ile çarpılır"""
        for sta in surgulu_buyuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': math.ceil(sta[1] * 3),
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name': "Lambasız KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * (2.5 if sta[0] < 138 else 3))) + " Adet"})

    def pervaz_emirleri(self, gorevler, sarma_emri_stage_id):


        """tüm görevlerdeki adetler toplanır"""
        toplam_adet = 0
        for gorev in gorevler:
            if gorev.tip not in ['8', '9', '10']:
                toplam_adet += gorev.adet

        "pervaz iç, dış ve başlık kalınlık değerli çağılır"
        pit_kalinlik = self.pit_kalinlik
        pdt_kalinlik = self.pdt_kalinlik
        pb_kalinlik = self.pb_kalinlik
        pi_genislik = self.pi_genislik
        pd_genislik = self.pd_genislik
        pb_genislik = self.pb_genislik

        """""pervaz iç dış ve başlık kalınlık ve genişlik değerleri karşılaştırılır
        hepsi eşitse toplan_adet * 5 ile pervaz aadeti hesaplanır,
        diğer satılarda kontroller yapılır eşitolmasınaa göre etler belirleenir"""
        if pit_kalinlik == pdt_kalinlik == pb_kalinlik and pi_genislik == pd_genislik == pb_genislik:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 5,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " mm " + str(
                                                 pi_genislik) + " cm  " + str(toplam_adet * 5) + " Adet"})



        elif pit_kalinlik == pdt_kalinlik and pi_genislik == pd_genislik:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 4,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " mm " + str(
                                                 pi_genislik) + " cm  " + str(toplam_adet * 4) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " mm " + str(
                                                 pb_genislik) + " cm  " + str(
                                                 toplam_adet * 1) + " Adet"})

        elif pit_kalinlik == pb_kalinlik and pi_genislik == pb_genislik:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " mm " + str(
                                                 pi_genislik) + " cm  " + str(toplam_adet * 3) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " mm " + str(
                                                 pd_genislik) + " cm  " + str(
                                                 toplam_adet * 2) + " Adet"})



        elif pdt_kalinlik == pb_kalinlik and pd_genislik == pb_genislik:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " mm " + str(
                                                 pi_genislik) + " cm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " mm " + str(
                                                 pd_genislik) + " cm  " + str(
                                                 toplam_adet * 3) + " Adet"})



        else:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " mm " + str(
                                                 pi_genislik) + " cm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " mm " + str(
                                                 pd_genislik) + " cm  " + str(
                                                 toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " mm " + str(
                                                 pb_genislik) + " cm  " + str(
                                                 toplam_adet * 1) + " Adet"})

    def yuzey_emirleri(self, gorevler, sarma_emri_stage_id, plastik):

        kapali_gorevler = []
        citali_gorevler = []
        scamli_gorevler = []
        surgulu_kapali_gorevler = []
        surgulu_citali_gorevler = []
        surgulu_scamli_gorevler = []
        sadece_kapali_gorevler = []
        sadece_citali_gorevler = []
        sadece_scamli_gorevler = []

        for gorev in gorevler:
            if gorev.tip == "1":  # ('1', 'Kapalı')
                kapali_gorevler.append(gorev)
            elif gorev.tip == "2":  # ('2', 'Çıtalı Camlı')
                citali_gorevler.append(gorev)
            elif gorev.tip == "3":  # ('3', 'Salma Camlı')
                scamli_gorevler.append(gorev)
            elif gorev.tip == "5":  # ('5', 'Sürgülü Kapalı')
                surgulu_kapali_gorevler.append(gorev)
            elif gorev.tip == "6":  # ('6', 'Sürgülü Çıtalı Camlı')
                surgulu_citali_gorevler.append(gorev)
            elif gorev.tip == "7":  # ('7', 'Sürgülü Salma Camlı')
                surgulu_scamli_gorevler.append(gorev)
            elif gorev.tip == "8":  # ('8', 'Sadece Kapalı')
                sadece_kapali_gorevler.append(gorev)
            elif gorev.tip == "9":  # ('9', 'Sadece Çıtalı Camlı')
               sadece_citali_gorevler.append(gorev)
            elif gorev.tip == "10":  # ('10', 'Sadece Salma Camlı')
                sadece_scamli_gorevler.append(gorev)

# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        scamli_enler = set([a.en for a in scamli_gorevler if a.en <= 100])

        scamlienadetler = []
        """salma camlılarda aynı ende olan emirlerin toplaam adetlerri bulunur"""

        for boy in scamli_enler :
            adet = 0
            for gorev in scamli_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            scamlienadetler.append([boy, adet])

        """salma camlı emirler için yüzey emirleri oluşturulru:
        YÜZEY 18mm 210 cm (boy-5) adet*2 olarak simlenddirilir"""

        for i in scamlienadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SALMA CAMLI" + " YÜZEY 18mm " + str(210) + " cm " + str(
                                                 i[0] - 5) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        
        """Salma camlılarda aynı en ve en2 olanların toplam adetlerini belirler"""
        scamli_en2_uniq = {}
        for gorev in scamli_gorevler:
            if gorev.en > 100:
                key = (gorev.en, gorev.en2)
                if key not in scamli_en2_uniq:
                    scamli_en2_uniq[key] = 0
                scamli_en2_uniq[key] += gorev.adet

        scamli_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in scamli_en2_uniq.items()]

        for i in scamli_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"SALMA CAMLI YÜZEY 18mm 210 cm {i['en2']} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"SALMA CAMLI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """ÇITALI görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        citali_enler = set([a.en for a in citali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        citaliadetler = []

        for boy in citali_enler:
            adet = 0
            for gorev in citali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            citaliadetler.append([boy, adet])

        """kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy -4 cm """
        for i in citaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"ÇITALI" + " YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] - 4) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})
           
# *******************************************************************************************************************************************
        """Çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        citali_en2_uniq = {}
        for gorev in citali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in citali_en2_uniq:
                    citali_en2_uniq[key] = 0
                citali_en2_uniq[key] += gorev.adet

        citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in citali_en2_uniq.items()]

        for i in citali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY {self.yuzey_kalinlik}mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY {self.yuzey_kalinlik}mm 210 cm {i['en'] - i['en2'] - 4} cm {i['adet'] * 2} Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        kapali_enler = set([a.en for a in kapali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        kapaliadetler = []

        for boy in kapali_enler:
            adet = 0
            for gorev in kapali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            kapaliadetler.append([boy, adet])

        """kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy -4 cm """
        for i in kapaliadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"KAPALI " + "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] - 4) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        """kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        kapali_en2_uniq = {}
        for gorev in kapali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in kapali_en2_uniq:
                    kapali_en2_uniq[key] = 0
                kapali_en2_uniq[key] += gorev.adet

        kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in kapali_en2_uniq.items()]

        for i in kapali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"KAPALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"KAPALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 4} cm {i['adet'] * 2} Adet"
            })




# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """surgulu_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        surgulu_scamli_enler = set([a.en for a in surgulu_scamli_gorevler if a.en <= 100])

        surgulu_scamlienadetler = []
        """surgulu_salma camlılardaaynı ende olan emirlerin toplaam adetlerri bulunur"""

        for boy in surgulu_scamli_enler:
            adet = 0
            for gorev in surgulu_scamli_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            surgulu_scamlienadetler.append([boy, adet])

        """surgulu_salma camlı emirler için yüzey emirleri oluşturulru:
        YÜZEY 18mm 210 cm boy adet*2 olarak simlenddirilir"""

        for i in surgulu_scamlienadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"sÜRGÜLÜ SALMA CAMLI " +  "YÜZEY 18mm " + str(210) + " cm " + str(
                                                 i[0]) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        """sürgülü salma camlılarda aynı en ve en2 olanların toplam adetlerini belirler"""
        surgulu_scamli_en2_uniq = {}
        for gorev in surgulu_scamli_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in surgulu_scamli_en2_uniq:
                    surgulu_scamli_en2_uniq[key] = 0
                surgulu_scamli_en2_uniq[key] += gorev.adet

        surgulu_scamli_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_scamli_en2_uniq.items()]

        for i in surgulu_scamli_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': "SÜRGÜLÜ SALMA CAMLI YÜZEY 18mm " + str(210) + " cm " + str(i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': "SÜRGÜLÜ SALMA CAMLI YÜZEY 18mm " + str(210) + " cm " + str(i["en"] - i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """surgulu_citali görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_citali_enler = set([a.en for a in surgulu_citali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        surgulu_citaliadetler = []

        for boy in surgulu_citali_enler:
            adet = 0
            for gorev in surgulu_citaliadetler:

                if gorev.en == boy:
                    adet += gorev.adet
            surgulu_citaliadetler.append([boy, adet])

        """surgulu_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
        for i in surgulu_citaliadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SÜRGÜLÜ ÇITALI " +  "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] + 1) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})
            
# *******************************************************************************************************************************************

        """sürgülü çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        surgulu_citali_en2_uniq = {}
        for gorev in surgulu_citali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in surgulu_citali_en2_uniq:
                    surgulu_citali_en2_uniq[key] = 0
                surgulu_citali_en2_uniq[key] += gorev.adet

        surgulu_citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_citali_en2_uniq.items()]

        for i in surgulu_citali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """surgulu_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_kapali_enler = set([a.en for a in surgulu_kapali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        surgulu_kapaliadetler = []

        for boy in surgulu_kapali_enler:
            adet = 0
            for gorev in surgulu_kapali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            surgulu_kapaliadetler.append([boy, adet])

        """surgulu_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
        for i in surgulu_kapaliadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SÜRGÜLÜ KAPALI " +  "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] + 1) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})
            
# *******************************************************************************************************************************************

        """Sürgülü kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        surgulu_kapali_en2_uniq = {}
        for gorev in surgulu_kapali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in surgulu_kapali_en2_uniq:
                    surgulu_kapali_en2_uniq[key] = 0
                surgulu_kapali_en2_uniq[key] += gorev.adet

        surgulu_kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_kapali_en2_uniq.items()]

        for i in surgulu_kapali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        sadece_scamli_en2_uniq = {}
        for gorev in sadece_scamli_gorevler:
            if gorev.en <= 100:  # en <= 100 koşulu
                key = (gorev.en, gorev.boy)
                if key not in sadece_scamli_en2_uniq:
                    sadece_scamli_en2_uniq[key] = 0
                sadece_scamli_en2_uniq[key] += gorev.adet

        sadece_scamli_en_listesi = [{"en": k[0], "boy": k[1], "adet": v} for k, v in sadece_scamli_en2_uniq.items()]

        for i in sadece_scamli_en_listesi:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i["adet"] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en"]) + " cm  " + str(i["adet"] * 2) + " Adet"
            })
            
# *******************************************************************************************************************************************

        """sadece salma camlı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        sadece_scamli_en2_uniq = {}
        for gorev in sadece_scamli_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2, gorev.boy)
                if key not in sadece_scamli_en2_uniq:
                    sadece_scamli_en2_uniq[key] = 0
                sadece_scamli_en2_uniq[key] += gorev.adet

        sadece_scamli_en2_listesi = [{"en": k[0], "en2": k[1], "boy": k[2], "adet": v} for k, v in sadece_scamli_en2_uniq.items()]

        for i in sadece_scamli_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en"] - i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
            })


# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """sadece_çitalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_citali_enler = set([a.en for a in sadece_citali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        sadece_citaliadetler = []

        for boy in sadece_citali_enler:
            adet = 0
            for gorev in sadece_citali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            sadece_citaliadetler.append([boy, adet])

        """sadece_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
        for i in sadece_citaliadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SADECE ÇITALI " + "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] + 1) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        """Sadece çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        sadece_citali_en2_uniq = {}
        for gorev in sadece_citali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in sadece_citali_en2_uniq:
                    sadece_citali_en2_uniq[key] = 0
                sadece_citali_en2_uniq[key] += gorev.adet

        sadece_citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in sadece_citali_en2_uniq.items()]

        for i in sadece_citali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
            })



# *******************************************************************************************************************************************
# *******************************************************************************************************************************************
# *******************************************************************************************************************************************

        """sadece_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_kapali_enler = set([a.en for a in sadece_kapali_gorevler if a.en <= 100])

        """ aynı enli görrelerin toplaam adetleri belirlenir"""
        sadece_kapaliadetler = []

        for boy in sadece_kapali_enler:
            adet = 0
            for gorev in sadece_kapali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            sadece_kapaliadetler.append([boy, adet])

        """sadece_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
        for i in sadece_kapaliadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SADECE KAPALI " + "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(
                                                 210) + " cm " + str(
                                                 i[0] + 1) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        """Sadece kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
        sadece_kapali_en2_uniq = {}
        for gorev in sadece_kapali_gorevler:
            if gorev.en > 100:  # en > 100 koşulu
                key = (gorev.en, gorev.en2)
                if key not in sadece_kapali_en2_uniq:
                    sadece_kapali_en2_uniq[key] = 0
                sadece_kapali_en2_uniq[key] += gorev.adet

        sadece_kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in sadece_kapali_en2_uniq.items()]

        for i in sadece_kapali_en2_listesi:
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
            })

            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': i["adet"] * 2,
                'stage_id': sarma_emri_stage_id,
                'plastik': plastik,
                'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
            })

    def sarma_emri(self):
        if self.sarim_emri_disabled:
           return {
                'type': 'ir.actions.act_window',
                'res_model': 'emir.wizard',
                'view_mode': 'form',
                'target': 'new',
                'name': 'Sarım Emri Uyarısı',
                'context': {
                    'default_message': "Yeni Sarım Emri oluşturulamıyor ! \nMevcut Sarım Emirlerini silerek yeni emirler oluştarabilirsiniz."
                },
            }

        else:
            gorevler = self.uretim_emirleri()

            sarma_emri_stage_id = self.env['project.task.type'].search(
                [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

            
            gorevler = [gorev for gorev in gorevler if gorev.plastik == str(2)]
            if gorevler:
                self.kasa_emirleri(gorevler, sarma_emri_stage_id, "2")
                self.pervaz_emirleri(gorevler, sarma_emri_stage_id)
                self.yuzey_emirleri(gorevler, sarma_emri_stage_id, "2")

            
            gorevler = self.uretim_emirleri()

            gorevler = [gorev for gorev in gorevler if gorev.plastik == str(1)]
            if gorevler:
                self.yuzey_emirleri(gorevler, sarma_emri_stage_id, "1")

    def cnc_emri(self):
        if self.cnc_emri_disabled:
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'emir.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'name': 'CNC Emri Uyarısı',
                    'context': {
                        'default_message': "Yeni CNC Emri oluşturulamıyor ! \nMevcut CNC Emirlerini silerek yeni emirler oluştarabilirsiniz."
                    },
                }

        else:
            gorevler = self.uretim_emirleri()

            cnc_emri_stage_id = self.env['project.task.type'].search(
                [('project_ids', 'in', self.id), ('name', 'like', "CNC EMRİ")], limit=1).id

            kapali_gorevler = []
            citali_gorevler = []
            scamli_gorevler = []
            surgulu_kapali_gorevler = []
            surgulu_citali_gorevler = []
            surgulu_scamli_gorevler = []
            sadece_kapali_gorevler = []
            sadece_citali_gorevler = []
            sadece_scamli_gorevler = []

            for gorev in gorevler:
                print(str(gorev.tip) +"************************")
                if gorev.tip == "1":  # ('1', 'Kapalı')
                    kapali_gorevler.append(gorev)
                elif gorev.tip == "2":  # ('2', 'Çıtalı Camlı')
                    citali_gorevler.append(gorev)
                elif gorev.tip == "3":  # ('3', 'Salma Camlı')
                    scamli_gorevler.append(gorev)
                elif gorev.tip == "5":  # ('5', 'Sürgülü Kapalı')
                    surgulu_kapali_gorevler.append(gorev)
                elif gorev.tip == "6":  # ('6', 'Sürgülü Çıtalı Camlı')
                    surgulu_citali_gorevler.append(gorev)
                elif gorev.tip == "7":  # ('7', 'Sürgülü Salma Camlı')
                    surgulu_scamli_gorevler.append(gorev)
                elif gorev.tip == "8":  # ('8', 'Sadece Kapalı')
                    sadece_kapali_gorevler.append(gorev)
                elif gorev.tip == "9":  # ('9', 'Sadece Çıtalı Camlı')
                    sadece_citali_gorevler.append(gorev)
                elif gorev.tip == "10":  # ('10', 'Sadece Salma Camlı')
                    sadece_scamli_gorevler.append(gorev)

    # *******************************************************************************************************************************************

            """salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
            scamli_enler = set([a.en for a in scamli_gorevler if a.en <= 100])

            scamlienadetler = []
            """salma camlılardaaynı ende olan emirlerin toplaam adetlerri bulunur"""

            for boy in scamli_enler:
                adet = 0
                for gorev in scamli_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                scamlienadetler.append([boy, adet])

            """salma camlı emirler için yüzey emirleri oluşturulru:
            YÜZEY 18mm 210 cm (boy-5) adet*2 olarak simlenddirilir"""

            for i in scamlienadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SALMA CAMLI" + " YÜZEY 18mm " + str(
                                                    210) + " cm " + str(
                                                    i[0] - 5) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                

            """Salma camlılarda aynı en ve en2 olanların toplam adetlerini belirler"""
            scamli_en2_uniq = {}
            for gorev in scamli_gorevler:
                if gorev.en > 100:
                    key = (gorev.en, gorev.en2)
                    if key not in scamli_en2_uniq:
                        scamli_en2_uniq[key] = 0
                    scamli_en2_uniq[key] += gorev.adet

            scamli_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in scamli_en2_uniq.items()]

            for i in scamli_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"SALMA CAMLI YÜZEY 18mm 210 cm {i['en2']} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"SALMA CAMLI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
                })

                
    # *******************************************************************************************************************************************

            citali_enler = set([a.en for a in citali_gorevler if a.en <= 100])

            citaliadetler = []

            for boy in citali_enler:
                adet = 0
                for gorev in citali_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                citaliadetler.append([boy, adet])

            """kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy -4 cm """
            for i in citaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"ÇITALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] - 4) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})


            """Çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            citali_en2_uniq = {}
            for gorev in citali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in citali_en2_uniq:
                        citali_en2_uniq[key] = 0
                    citali_en2_uniq[key] += gorev.adet

            citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in citali_en2_uniq.items()]

            for i in citali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY {self.yuzey_kalinlik} mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY {self.yuzey_kalinlik} mm 210 cm {i['en'] - i['en2'] - 4} cm {i['adet'] * 2} Adet"
                })

    # *******************************************************************************************************************************************

            """kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
            kapali_enler = set([a.en for a in kapali_gorevler if a.en <= 100])

            """ aynı enli görrelerin toplaam adetleri belirlenir"""
            kapaliadetler = []

            for boy in kapali_enler:
                adet = 0
                for gorev in kapali_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                kapaliadetler.append([boy, adet])

            """kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy -4 cm """
            for i in kapaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"KAPALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] - 4) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                
                """kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            kapali_en2_uniq = {}
            for gorev in kapali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in kapali_en2_uniq:
                        kapali_en2_uniq[key] = 0
                    kapali_en2_uniq[key] += gorev.adet

            kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in kapali_en2_uniq.items()]

            for i in kapali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"KAPALI YÜZEY {self.yuzey_kalinlik} mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"KAPALI YÜZEY {self.yuzey_kalinlik} mm 210 cm {i['en'] - i['en2'] - 4} cm {i['adet'] * 2} Adet"
                })
                
    # *******************************************************************************************************************************************


            """surgulu_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
            surgulu_scamli_enler = set([a.en for a in surgulu_scamli_gorevler if a.en <= 100])

            surgulu_scamlienadetler = []
            """surgulu_salma camlılardaaynı ende olan emirlerin toplaam adetlerri bulunur"""

            for boy in surgulu_scamli_enler:
                adet = 0
                for gorev in surgulu_scamli_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                surgulu_scamlienadetler.append([boy, adet])

            """surgulu_salma camlı emirler için yüzey emirleri oluşturulru:
            YÜZEY 18mm 210 cm boy adet*2 olarak simlenddirilir"""

            for i in surgulu_scamlienadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SÜRGÜLÜ SALMA CAMLI" + " YÜZEY 18mm " + str(
                                                    210) + " cm " + str(
                                                    i[0]) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                
            """sürgülü salma camlılarda aynı en ve en2 olanların toplam adetlerini belirler"""
            surgulu_scamli_en2_uniq = {}
            for gorev in surgulu_scamli_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in surgulu_scamli_en2_uniq:
                        surgulu_scamli_en2_uniq[key] = 0
                    surgulu_scamli_en2_uniq[key] += gorev.adet

            surgulu_scamli_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_scamli_en2_uniq.items()]

            for i in surgulu_scamli_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': "SÜRGÜLÜ SALMA CAMLI YÜZEY 18mm " + str(210) + " cm " + str(i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': "SÜRGÜLÜ SALMA CAMLI YÜZEY 18mm " + str(210) + " cm " + str(i["en"] - i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
                })
                
    # *******************************************************************************************************************************************

            """surgulu_citali görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
            surgulu_citali_enler = set([a.en for a in surgulu_citali_gorevler if a.en <= 100])

            """ aynı enli görrelerin toplaam adetleri belirlenir"""
            surgulu_citaliadetler = []

            for boy in surgulu_citali_enler:
                adet = 0
                for gorev in surgulu_citaliadetler:

                    if gorev.en == boy:
                        adet += gorev.adet
                surgulu_citaliadetler.append([boy, adet])

            """surgulu_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
            for i in surgulu_citaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SÜRGÜLÜ ÇITALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] + 1) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
    
            """sürgülü çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            surgulu_citali_en2_uniq = {}
            for gorev in surgulu_citali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in surgulu_citali_en2_uniq:
                        surgulu_citali_en2_uniq[key] = 0
                    surgulu_citali_en2_uniq[key] += gorev.adet

            surgulu_citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_citali_en2_uniq.items()]

            for i in surgulu_citali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

    # *******************************************************************************************************************************************

            """surgulu_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
            surgulu_kapali_enler = set([a.en for a in surgulu_kapali_gorevler if a.en <= 100])

            """ aynı enli görrelerin toplaam adetleri belirlenir"""
            surgulu_kapaliadetler = []

            for boy in surgulu_kapali_enler:
                adet = 0
                for gorev in surgulu_kapali_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                surgulu_kapaliadetler.append([boy, adet])

            """surgulu_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
            for i in surgulu_kapaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SÜRGÜLÜ KAPALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] + 1) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                
            """Sürgülü kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            surgulu_kapali_en2_uniq = {}
            for gorev in surgulu_kapali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in surgulu_kapali_en2_uniq:
                        surgulu_kapali_en2_uniq[key] = 0
                    surgulu_kapali_en2_uniq[key] += gorev.adet

            surgulu_kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in surgulu_kapali_en2_uniq.items()]

            for i in surgulu_kapali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                
    # *******************************************************************************************************************************************

            sadece_scamli_en2_uniq = {}
            for gorev in sadece_scamli_gorevler:
                if gorev.en <= 100:  # en <= 100 koşulu
                    key = (gorev.en, gorev.boy)
                    if key not in sadece_scamli_en2_uniq:
                        sadece_scamli_en2_uniq[key] = 0
                    sadece_scamli_en2_uniq[key] += gorev.adet

            sadece_scamli_en_listesi = [{"en": k[0], "boy": k[1], "adet": v} for k, v in sadece_scamli_en2_uniq.items()]

            for i in sadece_scamli_en_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en"]) + " cm  " + str(i["adet"] * 2) + " Adet"
                })
                
                """sadece salma camlı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            sadece_scamli_en2_uniq = {}
            for gorev in sadece_scamli_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2, gorev.boy)
                    if key not in sadece_scamli_en2_uniq:
                        sadece_scamli_en2_uniq[key] = 0
                    sadece_scamli_en2_uniq[key] += gorev.adet

            sadece_scamli_en2_listesi = [{"en": k[0], "en2": k[1], "boy": k[2], "adet": v} for k, v in sadece_scamli_en2_uniq.items()]

            for i in sadece_scamli_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': "SADECE SALMA CAMLI YÜZEY 18mm " + str(i["boy"]) + " cm " + str(i["en"] - i["en2"]) + " cm  " + str(i["adet"] * 2) + " Adet"
                })

    # *******************************************************************************************************************************************

            """sadece_çitalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
            sadece_citali_enler = set([a.en for a in sadece_citali_gorevler if a.en <= 100])

            """ aynı enli görrelerin toplaam adetleri belirlenir"""
            sadece_citaliadetler = []

            for boy in sadece_citali_enler:
                adet = 0
                for gorev in sadece_citali_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                sadece_citaliadetler.append([boy, adet])

            """sadece_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
            for i in sadece_citaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SADECE ÇITALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] + 1) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                
                """Sadece çıtalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            sadece_citali_en2_uniq = {}
            for gorev in sadece_citali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in sadece_citali_en2_uniq:
                        sadece_citali_en2_uniq[key] = 0
                    sadece_citali_en2_uniq[key] += gorev.adet

            sadece_citali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in sadece_citali_en2_uniq.items()]

            for i in sadece_citali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
                })

                
    # *******************************************************************************************************************************************

            """sadece_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
            sadece_kapali_enler = set([a.en for a in sadece_kapali_gorevler if a.en <= 100])

            """ aynı enli görrelerin toplaam adetleri belirlenir"""
            sadece_kapaliadetler = []

            for boy in sadece_kapali_enler:
                adet = 0
                for gorev in sadece_kapali_gorevler:

                    if gorev.en == boy:
                        adet += gorev.adet
                sadece_kapaliadetler.append([boy, adet])

            """sadece_kapalı görevler YÜZEY yuzey_kalinlik mm 210 cm boy +1 cm """
            for i in sadece_kapaliadetler:
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                                'stage_id': cnc_emri_stage_id,
                                                'name':"SADECE KAPALI" + " YÜZEY  " + str(
                                                    self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                    i[0] + 1) + " cm  " + str(
                                                    i[1] * 2) + " Adet"})
                
                """Sadece kapalı görevlerde aynı en ve en2 olanların toplam adetlerini belirler"""
            sadece_kapali_en2_uniq = {}
            for gorev in sadece_kapali_gorevler:
                if gorev.en > 100:  # en > 100 koşulu
                    key = (gorev.en, gorev.en2)
                    if key not in sadece_kapali_en2_uniq:
                        sadece_kapali_en2_uniq[key] = 0
                    sadece_kapali_en2_uniq[key] += gorev.adet

            sadece_kapali_en2_listesi = [{"en": k[0], "en2": k[1], "adet": v} for k, v in sadece_kapali_en2_uniq.items()]

            for i in sadece_kapali_en2_listesi:
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en2'] + 1} cm {i['adet'] * 2} Adet"
                })

                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': i["adet"] * 2,
                    'stage_id': cnc_emri_stage_id,
                    'name': f"ÇITALI YÜZEY 18mm 210 cm {i['en'] - i['en2'] - 5} cm {i['adet'] * 2} Adet"
                })

    def kasa_ebatlama(self, gorevler, catim_emri_stage_id):

        kasaenler = []
        for gorev in gorevler:
            kasaenler.append((gorev.kasa_eni, [gorev]))

        kasaen_gorevler = {}

        for item in kasaenler:

            if item[0] in kasaen_gorevler:
                kasaen_gorevler[item[0]].append(item[1][0])
            else:
                kasaen_gorevler[item[0]] = item[1]

        ebatlama_gorevler = []

        for item in kasaen_gorevler:
            for i in kasaen_gorevler[item]:
                gr = str(i.kasa_eni) + " mm " + str(i.boy) + " cm x " + str(i.en) + " cm "
                ebatlama_gorevler.append((gr, [i.adet]))

        ebatlama_gorevler_dict = {}

        for item in ebatlama_gorevler:

            if item[0] in ebatlama_gorevler_dict:
                ebatlama_gorevler_dict[item[0]].append(item[1][0])
            else:
                ebatlama_gorevler_dict[item[0]] = item[1]

        for item in ebatlama_gorevler_dict:
            ebatlama_gorevler_dict[item] = sum(ebatlama_gorevler_dict[item])

        for key in ebatlama_gorevler_dict:
            gorev_adi = key + str(ebatlama_gorevler_dict[key]) + " Adet"
            gorev_adet = ebatlama_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_adet,
                                             'stage_id': catim_emri_stage_id,
                                             'name': gorev_adi})

    def tip_degeri_bul(self, tip):
        return dict(self.env["project.task"].fields_get(allfields=["tip"])["tip"]['selection'])[tip]

    def catim_emri(self):
        if self.catim_emri_disabled:
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'emir.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'name': 'Çatım Emri Uyarısı',
                    'context': {
                        'default_message': "Yeni Çatım Emri oluşturulamıyor ! \nMevcut Çatım Emirlerini silerek yeni emirler oluştarabilirsiniz."
                    },
                }

        else:
            catim_emri_stage_id = self.env['project.task.type'].search(
                [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

            gorevler = self.uretim_emirleri()
            kapali_gorevler = [gorev for gorev in gorevler if
                            gorev.tip in ['1', '2', '3', '5', '6', '7', '8', '9', '10'] and gorev.plastik == '2' and gorev.en <=100]

            kapali_gorevler_adetli = []

            for gorev in kapali_gorevler:
                if gorev.tip in ['5', '6']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en) + " cm : "
                elif gorev.tip in ['8', '9']:
                    gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en) + " cm : "
                elif gorev.tip in ['3', '7', '10']:
                    if gorev.tip == '3' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy-3) + " cm " + str(
                                                    gorev.en - 5) + " cm  "
                    elif gorev.tip == '7' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en) + " cm  "
                    elif gorev.tip == '10' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en) + " cm "
                else:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en - 5) + " cm : "
                adet = gorev.adet
                kapali_gorevler_adetli.append([gorev_adi, [adet]])

            kapali_gorevler_dict = {}

            for item in kapali_gorevler_adetli:

                if item[0] in kapali_gorevler_dict:
                    kapali_gorevler_dict[item[0]].append(item[1][0])
                else:
                    kapali_gorevler_dict[item[0]] = item[1]

            for item in kapali_gorevler_dict:
                kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

            for key in kapali_gorevler_dict:
                gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
                gorev_Adet = kapali_gorevler_dict[key]
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                                'stage_id': catim_emri_stage_id, 'plastik': '2',
                                                'gorev_turu': '1', 'name': gorev_adi})
                
            #********************************************************************************************************

            gorevler = self.uretim_emirleri()
            kapali_gorevler = [gorev for gorev in gorevler if
                            gorev.tip in ['1', '2', '3', '5', '6', '7', '8', '9', '10'] and gorev.plastik == '2' and gorev.en > 100]

            kapali_gorevler_adetli = []

            for gorev in kapali_gorevler:
                if gorev.tip in ['5', '6']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en - gorev.en2) + " cm : "
                elif gorev.tip in ['8', '9']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en - gorev.en2) + " cm : "
                elif gorev.tip in ['3', '7', '10']:
                    if gorev.tip == '3' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy - 3) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy - 3) + " cm " + str(
                                                    gorev.en - gorev.en2 - 5) + " cm  "
                    elif gorev.tip == '7' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en - gorev.en2) + " cm  "
                        
                    elif gorev.tip == '10' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en - gorev.en2) + " cm  "
                else:
                    gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en - gorev.en2 - 5) + " cm : "
                adet = gorev.adet
                kapali_gorevler_adetli.append([gorev_adi, [adet]])
                kapali_gorevler_adetli.append([gorev_adi2, [adet]])

            kapali_gorevler_dict = {}

            for item in kapali_gorevler_adetli:

                if item[0] in kapali_gorevler_dict:
                    kapali_gorevler_dict[item[0]].append(item[1][0])
                else:
                    kapali_gorevler_dict[item[0]] = item[1]

            for item in kapali_gorevler_dict:
                kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

            for key in kapali_gorevler_dict:
                gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
                gorev_Adet = kapali_gorevler_dict[key]
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                                'stage_id': catim_emri_stage_id, 'plastik': '2',
                                                'gorev_turu': '1', 'name': gorev_adi})
        #********************************************************************************************************

            gorevler = self.uretim_emirleri()
            kapali_gorevler = [gorev for gorev in gorevler if
                            gorev.tip in ['1', '2', '3', '5', '6', '7', '8', '9', '10'] and gorev.plastik == '1' and gorev.en <= 100]

            kapali_gorevler_adetli = []

            for gorev in kapali_gorevler:
                if gorev.tip in ['5', '6']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en) + " cm : "
                elif gorev.tip in ['8', '9']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en) + " cm : "
                elif gorev.tip in ['3', '7', '10']:
                    if gorev.tip == '3' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy-3) + " cm " + str(
                                                    gorev.en - 5) + " cm  "
                    elif gorev.tip == '7' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en) + " cm  " 
                                                    
                    elif gorev.tip == '10' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en) + " cm  "
                else:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en - 5) + " cm : "
                adet = gorev.adet
                kapali_gorevler_adetli.append([gorev_adi, [adet]])

            kapali_gorevler_dict = {}

            for item in kapali_gorevler_adetli:

                if item[0] in kapali_gorevler_dict:
                    kapali_gorevler_dict[item[0]].append(item[1][0])
                else:
                    kapali_gorevler_dict[item[0]] = item[1]

            for item in kapali_gorevler_dict:
                kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

            for key in kapali_gorevler_dict:
                gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
                gorev_Adet = kapali_gorevler_dict[key]
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                                'stage_id': catim_emri_stage_id, 'plastik': '1',
                                                'gorev_turu': '1', 'name': gorev_adi})
            #********************************************************************************************************

            gorevler = self.uretim_emirleri()
            kapali_gorevler = [gorev for gorev in gorevler if
                            gorev.tip in ['1', '2', '3', '5', '6', '7', '8', '9', '10'] and gorev.plastik == '1' and gorev.en > 100]

            kapali_gorevler_adetli = []

            for gorev in kapali_gorevler:
                if gorev.tip in ['5', '6']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en - gorev.en2) + " cm : "
                elif gorev.tip in ['8', '9']:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy) + " cm " + \
                                str(gorev.en - gorev.en2) + " cm : "
                elif gorev.tip in ['3', '7', '10']:
                    if gorev.tip == '3' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy - 3) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy - 3) + " cm " + str(
                                                    gorev.en - gorev.en2 - 5) + " cm  "
                    elif gorev.tip == '7' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en - gorev.en2) + " cm  "
                        
                    elif gorev.tip == '10' :
                        gorev_adi = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en2) + " cm  "
                        gorev_adi2 = "18 mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                                                    gorev.boy) + " cm " + str(
                                                    gorev.en - gorev.en2) + " cm  "
                else:
                    gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en2) + " cm : "
                    gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
                        gorev.boy - 3) + " cm " + \
                                str(gorev.en - gorev.en2 - 5) + " cm : "
                adet = gorev.adet
                kapali_gorevler_adetli.append([gorev_adi, [adet]])
                kapali_gorevler_adetli.append([gorev_adi2, [adet]])

            kapali_gorevler_dict = {}

            for item in kapali_gorevler_adetli:

                if item[0] in kapali_gorevler_dict:
                    kapali_gorevler_dict[item[0]].append(item[1][0])
                else:
                    kapali_gorevler_dict[item[0]] = item[1]

            for item in kapali_gorevler_dict:
                kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

            for key in kapali_gorevler_dict:
                gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
                gorev_Adet = kapali_gorevler_dict[key]
                self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                                'stage_id': catim_emri_stage_id, 'plastik': '2',
                                                'gorev_turu': '1', 'name': gorev_adi})
                
        #********************************************************************************************************

            self.kesim_emri()

    def kesim_emri(self):

        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if
            gorev.tip in ['1', '2', '3', '4', '5', '6', '7'] and gorev.plastik == '2']

        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            if gorev.tip in ['5', '6', '7']:
                gorev_adi = "lambasız " + str(gorev.kasa_eni) + " x " + str(gorev.boy) + " x " + str(gorev.en)
            else:
                gorev_adi = str(gorev.kasa_eni) + " x " + str(gorev.boy) + " x " + str(gorev.en)
            adet = gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + " : " + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik': '2',
                                             'gorev_turu': '2', 'name': gorev_adi})

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if
                           gorev.tip in ['1', '2', '3', '4', '5', '6', '7'] and gorev.plastik == '1']

        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            if gorev.tip in ['5', '6', '7']:
                gorev_adi = "lambasız " + str(gorev.pk.value) + " x " + str(gorev.boy) + " x " + str(gorev.en)
            else:
                gorev_adi = str(gorev.pk.value) + " x " + str(gorev.boy) + " x " + str(gorev.en)
            adet = gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + " : " + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik': '1',
                                             'gorev_turu': '2', 'name': gorev_adi})

    def plastik_siparis_emri(self):
        if self.plastik_emri_disabled:
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'emir.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'name': 'Plastik Sipariş Uyarısı',
                    'context': {
                        'default_message': "Yeni Satın Alma Emri oluşturulamıyor ! \nMevcut Satın Alma Emirlerini silerek yeni emirler oluştarabilirsiniz."
                    },
                }
        else:
            gorevler = self.uretim_emirleri()

            plastik_emri_stage_id = self.env['project.task.type'].search(
                [('project_ids', 'in', self.id), ('name', 'like', "SATIN ALMA EMRİ")], limit=1).id

            plastik_gorevler = [gorev for gorev in gorevler if gorev.plastik == "1"]
            if not plastik_gorevler:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'emir.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'name': 'Plastik Sipariş Uyarısı',
                    'context': {
                        'default_message': "plastik ürün yok!"
                    },
                }
            tasks = []
            for gorev in plastik_gorevler:
                if gorev.pop:
                    tasks.append([(gorev.pop.name, gorev.pop.description), int(math.ceil(gorev.adet * 2))])
                if gorev.pap:
                    tasks.append([(gorev.pap.name, gorev.pap.description), int(math.ceil(gorev.adet * 2))])
                if gorev.pbpo:
                    tasks.append([(gorev.pbpo.name, gorev.pbpo.description), int(math.ceil(gorev.adet * 0.5))])
                if gorev.pbpa:
                    tasks.append([(gorev.pbpa.name, gorev.pbpa.description), int(math.ceil(gorev.adet * 0.5))])
                if gorev.pk:
                    tasks.append([(gorev.pk.name, gorev.pk.description), int(math.ceil(gorev.adet * 2.5))])

            result = {}
            for item in tasks:
                key = item[0]  # kodu kontrol etmek için
                adet = item[1]  # adetleri toplamak için

                if key in result:
                    result[key] += adet  # Aynı anahtar varsa adetleri topla
                else:
                    result[key] = adet  # Yeni anahtar oluştur

                
            for key in result:
                adet = result[key]
                gorev_adi = f"{key[0]}:{key[1]}:{adet} adet"
                self.env['project.task'].create({
                    'project_id': self.id,
                    'allocated_hours': adet,
                    'stage_id': plastik_emri_stage_id,
                    'name': gorev_adi,
                })

    def project_emri(self):
        print("emir oluşturuldu")
        
    def hirdavat_emri(self):
        
        gorevler = self.uretim_emirleri()

        hirdavat_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "HIRDAVAT EMRİ")], limit=1).id

        
        hirdavatlar = {
        'mentese': self.mentese,
        'kapi_kilit': self.kapi_kilit,
        'kapi_kol': self.kapi_kol,
        'stoper': self.stoper,
        'fitil': self.fitil,
        'surgu': self.surgu,
        'vida': self.vida,
        'kopuk': self.kopuk,
        'silikon': self.silikon,
        }
        hirdavat_adetleri={}
        for key, value in hirdavatlar.items():
            if value and value != "1":  # Eğer model var ise
                match key:
                    case "mentese":
                        menteseToplam = sum(gorev.adet * (3 if gorev.en < 100 else 6)for gorev in gorevler if gorev.tip in ["1", "2", "3"])
                        if menteseToplam > 0:
                            hirdavat_adetleri["mentese"] = f'MENTEŞE: {value.name} {menteseToplam} Adet'

                    case "kapi_kilit":
                        odaKilitToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "1")
                        wcKilitToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "2")
                        silindirKilitToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "3")
                        
                        if odaKilitToplam > 0:
                            hirdavat_adetleri["oda_kilit"] = f'KAPI KİLİT: ODA {value.name} {odaKilitToplam} Adet'
                        if wcKilitToplam > 0:
                            hirdavat_adetleri["wc_kilit"] = f'KAPI KİLİT: WC {value.name} {wcKilitToplam} Adet'
                        if silindirKilitToplam > 0:
                            hirdavat_adetleri["silindir_kilit"] = f'KAPI KİLİT: SİLİNDİR {value.name} {silindirKilitToplam} Adet'

                    case "kapi_kol":
                        odaKolToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "1")
                        wcKolToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "2")
                        silindirKolToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.oda.oda_tip == "3")
                        
                        if odaKolToplam > 0:
                            hirdavat_adetleri["oda_kol"] = f'KAPI KOL: ODA {value.name} {odaKolToplam} Adet'
                        if wcKolToplam > 0:
                            hirdavat_adetleri["wc_kol"] = f'KAPI KOL: WC {value.name} {wcKolToplam} Adet'
                        if silindirKolToplam > 0:
                            hirdavat_adetleri["silindir_kol"] = f'KAPI KOL: SİLİNDİR {value.name} {silindirKolToplam} Adet'

                    case "stoper":
                        stoperToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"])
                        if stoperToplam > 0:
                            hirdavat_adetleri["stoper"] = f'STOPER: {value.name} {stoperToplam} Adet'

                    case "fitil":
                        fitilToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.plastik == "2")
                        if fitilToplam > 0:
                            hirdavat_adetleri["fitil"] = f'FİTİL: {value.name} {fitilToplam} Adet'

                    case "surgu":
                        surguToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"] and gorev.en > 100)
                        if surguToplam > 0:
                            hirdavat_adetleri["surgu"] = f'GÖMME SÜRGÜ: {value.name} {surguToplam} Adet'

                    case "vida":
                        vidaToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"])
                        if vidaToplam > 0:
                            hirdavat_adetleri["vida_4x50"] = f'VİDA: 4X50 {vidaToplam * 6} Adet'
                            hirdavat_adetleri["vida_3.5x25"] = f'VİDA: 3,5X25 {vidaToplam * 16} Adet'
                            hirdavat_adetleri["vida_3x20"] = f'VİDA: 3X20 {vidaToplam * 16} Adet'
                            hirdavat_adetleri["vida_3.5x18"] = f'VİDA: 3,5X18 {vidaToplam * 6} Adet'

                    case "kopuk":
                        kopukToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"])
                        if kopukToplam > 0:
                            hirdavat_adetleri["kopuk"] = f'KÖPÜK: {kopukToplam / 2} Adet'

                    case "silikon":
                        silikonToplam = sum(gorev.adet for gorev in gorevler if gorev.tip in ["1", "2", "3"])
                        if silikonToplam > 0:
                            hirdavat_adetleri["silikon"] = f'SİLİKON: {silikonToplam / 2} Adet'

                    case _:
                        hirdavat_adetleri[key] = "Bilinmeyen hırdavat türü"
                        
        for key, value in reversed(hirdavat_adetleri.items()):
                self.env['project.task'].create({'project_id': self.id,
                                                'stage_id': hirdavat_emri_stage_id,
                                                'name':value})    
                    
                 

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _description = 'Task inherit'

    kasa_eni = fields.Integer(string="Kasa", default=1.0)
    en = fields.Integer(string="En", default=1.0)
    boy = fields.Integer(string="Boy", default=1.0)
    adet = fields.Integer(string="Adet", default=1.0)

    tip = fields.Selection([
        ('1', 'Kapalı'),
        ('2', 'Çıtalı Camlı'),
        ('3', 'Salma Camlı'),
        ('4', 'kanat Yok'),
        ('5', 'Sürgülü Kapalı'),
        ('6', 'Sürgülü Çıtalı Camlı'),
        ('7', 'Sürgülü Salma Camlı'),
        ('8', 'Sadece Kapalı'),
        ('9', 'Sadece Çıtalı Camlı'),
        ('10', 'Sadece Salma Camlı'),
    ], string="Tip")

    plastik = fields.Selection([
        ('1', 'Evet'),
        ('2', 'Hayır'),
    ], default='2', string="Plastik mi?")

    gorev_turu = fields.Selection([
        ('1', 'catim'),
        ('2', 'kesim'),
        ('3', 'kasa'),
        ('4', 'pervaz'),
        ('5', 'yuzey'),
    ], default='1', string="gorev turu?")

    oda = fields.Many2one('yaman.oda', string="Oda")
    pop = fields.Many2one('yaman.plastik', string="Pervaz Ön Plastik")
    pap = fields.Many2one('yaman.plastik', string="Pervaz Arka Plastik")
    pbpo = fields.Many2one('yaman.plastik', string="Pervaz Başlık Ön Plastik")
    pbpa = fields.Many2one('yaman.plastik', string="Pervaz Başlık Arka Plastik")
    pk = fields.Many2one('yaman.plastikkasa', string="Kasa Plastik")
    en2 = fields.Integer(string="En 2", default=0.0)

    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Status',
        copy=False, default='normal', required=True, readonly=False, store=True)