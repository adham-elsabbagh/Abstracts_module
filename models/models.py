# -*- coding: utf-8 -*-

from odoo import models, fields, api

class screen_items(models.Model):
    _name = 'screen.items'
    _rec_name = 'item_name'

    item_name = fields.Text(string="Item Name", required=False, )
    item_description = fields.Text(string="Item Description", required=False, )

class screen_settings(models.Model):
    _name = 'screen.settings'

    @api.depends('req_quantity','price')
    def _amount_all(self):
        for record in self:
            total_price=0
            if record.req_quantity and record.price:
                total_price = record.req_quantity*record.price
            record.update({
                'total_price':total_price,
            })
    item_id=fields.Many2one(comodel_name="screen.items")
    req_quantity = fields.Integer(default=1,string="")
    pre_quantity = fields.Integer(default=1,string="")
    exec_quantity = fields.Integer(default=1,string="")
    price = fields.Float(string="Price",digits=(16, 2))
    total_price = fields.Float(string="Total", store=True, readonly=True,digits=(16, 2) ,track_visibility='always',compute='_amount_all')
    order_id = fields.Many2one(comodel_name="screen.contract", string="Order", required=False,)
    order_id_2 = fields.Many2one(comodel_name="screen.abstract", string="Order", required=False,)

class screen_contract(models.Model):
    _name = 'screen.contract'
    _rec_name = 'contract_name'

    @api.depends('item_ids.total_price')
    def _amount_all(self):
        for rec in self:
            amount_total=0.0
            for line in rec.item_ids:
                amount_total+= line.total_price
            rec.update({
                'amount_total':amount_total,
            })

    contract_name = fields.Text(string="Contract Name", required=False, )
    date_from = fields.Date(string="Date From", required=False, )
    date_to = fields.Date(string="Date To", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="Customer")
    item_ids = fields.One2many(comodel_name="screen.settings", inverse_name="order_id",
                                  track_visibility='onchange', copy=True,)
    amount_total = fields.Float(string="Amount Total", store=True, readonly=True,digits=(16, 2) ,track_visibility='always',compute='_amount_all')

class screen_abstract(models.Model):
    _name = 'screen.abstract'

    @api.depends('contract_ids.total_price')
    def _amount_all(self):
        for rec in self:
            amount_total=0.0
            for line in rec.contract_ids:
                amount_total+= line.total_price
            rec.update({
                'amount_total':amount_total,
            })



    contract_id = fields.Many2one(comodel_name="screen.contract", string="Contract Name",)
    contract_ids=fields.One2many(comodel_name="screen.settings", inverse_name="order_id_2",
                                  track_visibility='onchange', copy=True,)
    amount_total = fields.Float(string="Amount Total", store=True, readonly=True,digits=(16, 2) ,
                                track_visibility='always',compute='_amount_all')



