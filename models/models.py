# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ScreenItems(models.Model):
    _name = 'screen.items'
    _rec_name = 'item_name'

    item_name = fields.Text(string="Item Name", required=False, )
    item_description = fields.Text(string="Item Description", required=False, )


class ScreenSettings(models.Model):
    _name = 'screen.settings'

    @api.depends('req_quantity', 'price','exec_quantity')
    def _amount_all(self):
        for record in self:
            total_price = pre_quantity= exec_quantity=0
            if record.order_id :
                total_price = record.req_quantity * record.price
            if record.order_id_2 :
                total_price = record.exec_quantity * record.price
            record.update({
                'total_price': total_price,
            })

    item_id = fields.Many2one(comodel_name="screen.items")
    req_quantity = fields.Integer(default=1)
    pre_quantity = fields.Integer(default=1)
    exec_quantity = fields.Integer(default=1)
    price = fields.Float(string="Price", digits=(16, 2))
    total_price = fields.Float(
        string="Total", store=True, readonly=True, digits=(16, 2),
        track_visibility='always', compute='_amount_all'
    )
    order_id = fields.Many2one(
        comodel_name="screen.contract", string="Order"
    )
    order_id_2 = fields.Many2one(
        comodel_name="screen.abstract", string="Order"
    )


class ScreenContract(models.Model):
    _name = 'screen.contract'
    _rec_name = 'contract_name'

    @api.depends('item_ids.total_price')
    def _amount_all(self):
        for rec in self:
            amount_total = 0.0
            for line in rec.item_ids:
                amount_total += line.total_price
            rec.update({
                'amount_total': amount_total,
            })

    contract_name = fields.Text()
    date_from = fields.Date()
    date_to = fields.Date()
    user_id = fields.Many2one(comodel_name="res.users", string="Customer")
    item_ids = fields.One2many(
        comodel_name="screen.settings", inverse_name="order_id",
        track_visibility='onchange', copy=True
    )
    amount_total = fields.Float(
        store=True, digits=(16, 2), track_visibility='always',
        compute='_amount_all'
    )


class ScreenAbstract(models.Model):
    _name = 'screen.abstract'

    @api.depends('contract_ids.total_price')
    def _amount_all(self):
        for rec in self:
            amount_total = 0.0
            for line in rec.contract_ids:
                amount_total += line.total_price
            rec.update({
                'amount_total': amount_total,
            })

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        """
            safnjsfkjf
        :return: fields vals
        """
        if not self.contract_id:
            return
        self.contract_ids = False
        items_values = self.contract_id.item_ids.read([
            'item_id', 'req_quantity', 'price', 'total_price'
        ])
        for item in items_values:
            self.contract_ids += self.contract_ids.new({
                'price': item['price'],
                'total_price': item['total_price'],
                'item_id': item['item_id'][0],
                'req_quantity': item['req_quantity'],
            })

    contract_id = fields.Many2one(
        comodel_name="screen.contract",
        string="Contract Name"
    )
    contract_ids = fields.One2many(
        comodel_name="screen.settings",
        inverse_name="order_id_2",
        track_visibility='onchange', copy=True
    )
    amount_total = fields.Float(
        string="Amount Total", store=True, readonly=True,
        digits=(16, 2), track_visibility='always', compute='_amount_all'
    )
