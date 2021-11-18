# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError

class Faturer(models.Model):
    _inherit        = 'account.move.line'

    @api.depends('price_unit')
    def _get_pourcentage_quarante(self):
        # self.ensure_one()
        for rec in self:
            if rec.applique_pourcentage_benefice:
                rec.pourcentage_40 = int(rec.price_unit * 0.4)
            else:
                rec.pourcentage_40 = 0
        # if rec:
        #     self.pourcentage_40 = rec.pourcentage_40

    @api.depends('pourcentage_40','le_pourcentage')
    def _get_benefice(self):
        # self.ensure_one()
        for rec in self:
            if rec.montant_benefice > 0 :
                rec.pourcentage_40_benefice =  rec.montant_benefice
                rec.price_subtotal = rec.montant_benefice
            else:
                rec.pourcentage_40_benefice = int(rec.pourcentage_40 * float(rec.le_pourcentage))
                rec.price_subtotal = rec.pourcentage_40_benefice

    @api.depends('price_subtotal', 'le_pourcentage')
    def _get_montant_benefice_pourcentage(self):
        self.ensure_one()
        for rec in self:
            rec.benefice_pourcentage_montant_total = rec.price_subtotal * float(rec.le_pourcentage)

    applique_pourcentage_benefice  = fields.Boolean(string='Appliquez le per', default=False)
    le_pourcentage = fields.Selection([('0.01', '1per'), ('0.02','2per'), ('0.03', '3per'),('0.04','4per'), ('0.05', '5per')], string='Le per')
    pourcentage_40       = fields.Integer(string='per 40', compute='_get_pourcentage_quarante')
    pourcentage_40_benefice      = fields.Integer(string='Sous Total', default=0, compute='_get_benefice', domain="[{'applique_pourcentage_benefice', '=', True}]")

    # benefice_pourcentage_montant_total = fields.Float('Montant Benefice', comput='_get_montant_benefice_pourcentage')
    applique_montant_benefice    = fields.Boolean(string='Mt Benefice', default=False)
    montant_benefice            = fields.Integer(string='M Benefice', default=0)

    price_unit               = fields.Integer(string='Montant')
    price_total             = fields.Integer(string='Total')
    price_subtotal         = fields.Integer(string='Sous-Total')
    code                = fields.Integer(string='Num', default=lambda x: x.env['ir.sequence'].get('account.move.line'))




class Facturation_bella(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids.pourcentage_40_benefice')
    def _calcule_total(self):
        lines =  self.env['account.move.line'].search([('move_id', '=', self.id)])
        to = 0
        if lines:
            to = sum(lines.mapped('pourcentage_40_benefice'))
            # self.invoice_line_ids.price_subtotal = lines.mapped('pourcentage_40_benefice')
        self.amount_total = to
        self.amount_total_signed = to
        self.amount_residual_signed = to
        # self.invoice_line_ids.price_subtotal = to


    amount_total   = fields.Integer(string='Total', compute='_calcule_total')
    amount_untaxed = fields.Integer()
    amount_total_signed = fields.Integer()
    amount_residual_signed = fields.Integer()
