# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math, collections



class Project(models.Model):
    _inherit = 'project.project'
    _description = 'yaman.yaman'

    olcu_alan = fields.Many2one('res.users', string='Ölçüyü Alan', index=True)
    kaydi_giren = fields.Many2one('res.users', string="Kaydı Giren", index=True)
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
    cnc_description = fields.Text(string="CNC Emri Açıklaması", default="_")
    image1 = fields.Image("Resim")
    image2 = fields.Image("Resim")

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
    supurge_adet = fields.Integer(string="Süpürge Adeti")

    @api.depends("task_ids")
    def _compute_toplam_kapi(self):
        tasks = self.task_ids
        gorevler = [gorev for gorev in tasks if gorev.stage_id.name == "satırlar"]
        toplam_adet = 0
        for i in gorevler:
            toplam_adet += i.adet

        for record in self:
            record.toplam_kapi = str(toplam_adet)

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

        liste = [cam_cita_adet, klapa_adet, bini_cita_adet]
        dict = {'cam_cita_adet': cam_cita_adet, 'klapa_adet': klapa_adet, 'bini_cita_adet': bini_cita_adet}
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
                                                 math.ceil(sta[1] * 3)) + " Adet"})

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
                                                 math.ceil(sta[1] * 3)) + " Adet"})

    def pervaz_emirleri(self, gorevler, sarma_emri_stage_id):

        """tüm görevlerdeki adeler toplanır"""
        toplam_adet = 0
        for gorev in gorevler:
            if gorev.tip not in ['4', '8', '9', '10']:
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
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 5) + " Adet"})



        elif pit_kalinlik == pdt_kalinlik and pi_genislik == pd_genislik:

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 4,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 4) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " cm " + str(
                                                 pb_genislik) + " mm  " + str(
                                                 toplam_adet * 1) + " Adet"})

        elif pit_kalinlik == pb_kalinlik and pi_genislik == pb_genislik:

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 3) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 2) + " Adet"})



        elif pdt_kalinlik == pb_kalinlik and pd_genislik == pb_genislik:

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 3) + " Adet"})



        else:

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " cm " + str(
                                                 pb_genislik) + " mm  " + str(
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

        """salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        scamli_enler = set([a.en for a in scamli_gorevler])

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
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SALMA CAMLI" + " YÜZEY 18mm " + str(210) + " cm " + str(
                                                 i[0] - 5) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})

# *******************************************************************************************************************************************

        """ÇITALI görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        citali_enler = set([a.en for a in citali_gorevler])

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

        """kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        kapali_enler = set([a.en for a in kapali_gorevler])

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

        """surgulu_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        surgulu_scamli_enler = set([a.en for a in surgulu_scamli_gorevler])

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

        """surgulu_citali görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_citali_enler = set([a.en for a in surgulu_citali_gorevler])

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

        """surgulu_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_kapali_enler = set([a.en for a in surgulu_kapali_gorevler])

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

        """sadece_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        sadece_scamli_enler = set([a.en for a in sadece_scamli_gorevler])

        sadece_scamlienadetler = []
        """salma camlılardaaynı ende olan emirlerin toplaam adetlerri bulunur"""
        boy = 0
        for en in sadece_scamli_enler:
            adet = 0
            for gorev in sadece_scamli_gorevler:

                if gorev.en == en:
                    boy = gorev.boy
                    adet += gorev.adet
            sadece_scamlienadetler.append([en, adet, boy])

        """sadece_salma camlı emirler için yüzey emirleri oluşturulru:
        YÜZEY 18mm boy cm en cm adet*2 olarak simlenddirilir"""

        for i in sadece_scamlienadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik': plastik,
                                             'name':"SADECE SALMA CAMLI " +  "YÜZEY 18mm " + str(i[2]) + " cm " + str(
                                                 i[0]) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})
            
# *******************************************************************************************************************************************

        """sadece_çitalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_citali_enler = set([a.en for a in sadece_citali_gorevler])

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

        """sadece_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_kapali_enler = set([a.en for a in sadece_kapali_gorevler])

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

    def sarma_emri(self):
        gorevler = self.uretim_emirleri()

        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        plastik = '2'
        gorevler = [gorev for gorev in gorevler if gorev.plastik == str(2)]

        self.kasa_emirleri(gorevler, sarma_emri_stage_id, plastik)
        self.pervaz_emirleri(gorevler, sarma_emri_stage_id)
        self.yuzey_emirleri(gorevler, sarma_emri_stage_id, plastik)

        plastik = '1'
        gorevler = self.uretim_emirleri()

        gorevler = [gorev for gorev in gorevler if gorev.plastik == str(1)]

        self.yuzey_emirleri(gorevler, sarma_emri_stage_id, plastik)

    def cnc_emri(self):

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
        scamli_enler = set([a.en for a in scamli_gorevler])

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
            
# *******************************************************************************************************************************************

        citali_enler = set([a.en for a in kapali_gorevler])

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

# *******************************************************************************************************************************************

        """kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        kapali_enler = set([a.en for a in kapali_gorevler])

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
            
# *******************************************************************************************************************************************


        """surgulu_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        surgulu_scamli_enler = set([a.en for a in surgulu_scamli_gorevler])

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
            
# *******************************************************************************************************************************************

        """surgulu_citali görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_citali_enler = set([a.en for a in surgulu_citali_gorevler])

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
 
# *******************************************************************************************************************************************

        """surgulu_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        surgulu_kapali_enler = set([a.en for a in surgulu_kapali_gorevler])

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
            
# *******************************************************************************************************************************************

        """sadece_salma camlı enler belirlenir tekrarlayanlar iptal edenler"""
        sadece_scamli_enler = set([a.en for a in sadece_scamli_gorevler])

        sadece_scamlienadetler = []
        """salma camlılardaaynı ende olan emirlerin toplaam adetlerri bulunur"""
        boy = 0
        for en in sadece_scamli_enler:
            adet = 0
            for gorev in sadece_scamli_gorevler:

                if gorev.en == en:
                    boy = gorev.boy
                    adet += gorev.adet
            sadece_scamlienadetler.append([en, adet, boy])

        """sadece_salma camlı emirler için yüzey emirleri oluşturulru:
        YÜZEY 18mm boy cm en cm adet*2 olarak simlenddirilir"""

        for i in sadece_scamlienadetler:
            self.env['project.task'].create({'project_id': self.id, 'allocated_hours': i[1] * 2,
                                             'stage_id': cnc_emri_stage_id,
                                             'name': "SADECE SALMA CAMLI" + " YÜZEY 18mm " + str(
                                                 i[2]) + " cm " + str(
                                                 i[0]) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})
            
# *******************************************************************************************************************************************

        """sadece_çitalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_citali_enler = set([a.en for a in sadece_citali_gorevler])

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
            
# *******************************************************************************************************************************************

        """sadece_kapalı görevlerin ennleri tekrar etmeyecek şiekilde listelebeir aynı enlileri birlemek için"""
        sadece_kapali_enler = set([a.en for a in sadece_kapali_gorevler])

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

        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if
                           gorev.tip in ['1', '2', '5', '6', '8', '9'] and gorev.plastik == '2']

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

        # gorevler = self.uretim_emirleri()
        # kapali_gorevler = [gorev for gorev in gorevler if
        #                    gorev.tip in ['1', '2', '5', '6', '8', '9'] and gorev.plastik == '2' and gorev.en > 100]

        # kapali_gorevler_adetli = []

        # for gorev in kapali_gorevler:
        #     if gorev.tip in ['5', '6']:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy) + " cm " + \
        #                     str(gorev.en) + " cm : "
        #     elif gorev.tip in ['8', '9']:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en2) + " cm : "
        #         gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en - gorev.en2 - 5) + " cm : "
        #     else:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en2) + " cm : "
        #         gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en - gorev.en2 - 5) + " cm : "
        #     adet = gorev.adet
        #     kapali_gorevler_adetli.append([gorev_adi, [adet]])
        #     kapali_gorevler_adetli.append([gorev_adi2, [adet]])

        # kapali_gorevler_dict = {}

        # for item in kapali_gorevler_adetli:

        #     if item[0] in kapali_gorevler_dict:
        #         kapali_gorevler_dict[item[0]].append(item[1][0])
        #     else:
        #         kapali_gorevler_dict[item[0]] = item[1]

        # for item in kapali_gorevler_dict:
        #     kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        # for key in kapali_gorevler_dict:
        #     gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
        #     gorev_Adet = kapali_gorevler_dict[key]
        #     self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
        #                                      'stage_id': catim_emri_stage_id, 'plastik': '2',
        #                                      'gorev_turu': '1', 'name': gorev_adi})
    #********************************************************************************************************

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if
                           gorev.tip in ['1', '2', '5', '6', '8', '9'] and gorev.plastik == '1']

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

        # gorevler = self.uretim_emirleri()
        # kapali_gorevler = [gorev for gorev in gorevler if
        #                    gorev.tip in ['1', '2', '5', '6', '8', '9'] and gorev.plastik == '1' and gorev.en > 100]

        # kapali_gorevler_adetli = []

        # for gorev in kapali_gorevler:
        #     if gorev.tip in ['5', '6']:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy) + " cm " + \
        #                     str(gorev.en) + " cm : "
        #     elif gorev.tip in ['8', '9']:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en2) + " cm : "
        #         gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en - gorev.en2 - 5) + " cm : "
        #     else:
        #         gorev_adi = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en2) + " cm : "
        #         gorev_adi2 = str(self.yuzey_kalinlik) + " mm " + str(self.tip_degeri_bul(gorev.tip)) + " : " + str(
        #             gorev.boy - 3) + " cm " + \
        #                     str(gorev.en - gorev.en2 - 5) + " cm : "
        #     adet = gorev.adet
        #     kapali_gorevler_adetli.append([gorev_adi, [adet]])
        #     kapali_gorevler_adetli.append([gorev_adi2, [adet]])

        # kapali_gorevler_dict = {}

        # for item in kapali_gorevler_adetli:

        #     if item[0] in kapali_gorevler_dict:
        #         kapali_gorevler_dict[item[0]].append(item[1][0])
        #     else:
        #         kapali_gorevler_dict[item[0]] = item[1]

        # for item in kapali_gorevler_dict:
        #     kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        # for key in kapali_gorevler_dict:
        #     gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
        #     gorev_Adet = kapali_gorevler_dict[key]
        #     self.env['project.task'].create({'project_id': self.id, 'allocated_hours': gorev_Adet,
        #                                      'stage_id': catim_emri_stage_id, 'plastik': '2',
        #                                      'gorev_turu': '1', 'name': gorev_adi})
            
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
                gorev_adi = str(gorev.pk) + " x " + str(gorev.boy) + " x " + str(gorev.en)
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

        gorevler = self.uretim_emirleri()

        plastik_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SATIN ALMA EMRİ")], limit=1).id

        plastik_gorevler = [gorev for gorev in gorevler if gorev.plastik == "1"]

        tasks = []
        for gorev in plastik_gorevler:
            tasks.append([(gorev.pop.name, gorev.pop.description), gorev.adet*2])
            tasks.append([(gorev.pap.name, gorev.pap.description), gorev.adet*2])
            tasks.append([(gorev.pbpo.name, gorev.pbpo.description), gorev.adet*0.5])
            tasks.append([(gorev.pbpa.name, gorev.pbpa.description), gorev.adet*0.5])
            tasks.append([(gorev.pk.name, gorev.pk.description), gorev.adet*2.5])

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
            gorev_adi = key[0] + ":" + key[1] + ":" + str(adet)
            self.env['project.task'].create({
                'project_id': self.id,
                'allocated_hours': adet,
                'stage_id': plastik_emri_stage_id,
                'name': gorev_adi,
            })

 


        


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

   





