# -*- encoding: utf-8 -*-
#                                                                            #
#   OpenERP Module                                                           #
#   Copyright (C) 2014 Gustavo Lepri <gustavolepri@gmail.com>                #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU Affero General Public License as           #
#   published by the Free Software Foundation, either version 3 of the       #
#   License, or (at your option) any later version.                          #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU Affero General Public License for more details.                      #
#                                                                            #
#   You should have received a copy of the GNU Affero General Public License #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                            #
##############################################################################

from openerp.osv import orm


class SaleOrderLine(orm.Model):
    _inherit='sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='',
                          partner_id=False, lang=False, update_tax=True,
                          date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):

        if not context:
            context = {}
        parent_fiscal_category_id = context.get('parent_fiscal_category_id')
        if not parent_fiscal_category_id:
            parent_fiscal_category_id = 1
        shop_id = context.get('shop_id')
        if not shop_id:
            shop_id = 3
        partner_invoice_id = context.get('partner_invoice_id')
        if not partner_invoice_id:
            partner_invoice_id = partner_id
        result = {'value': {}}
        if parent_fiscal_category_id and product and partner_invoice_id \
        and shop_id:
            obj_fp_rule = self.pool.get('account.fiscal.position.rule')
            product_fc_id = obj_fp_rule.product_fiscal_category_map(
                cr, uid, product, parent_fiscal_category_id)

            if product_fc_id:
                parent_fiscal_category_id = product_fc_id

            result['value']['fiscal_category_id'] = parent_fiscal_category_id

            kwargs = {
                'shop_id': shop_id,
                'partner_id': partner_id,
                'partner_invoice_id': partner_invoice_id,
                'fiscal_category_id': parent_fiscal_category_id,
                'context': context
            }
            result.update(self._fiscal_position_map(cr, uid, result, **kwargs))
            if result['value'].get('fiscal_position'):
                fiscal_position = result['value'].get('fiscal_position')
         
            obj_product = self.pool.get('product.product').browse(
                cr, uid, product)
            context.update({'fiscal_type': obj_product.fiscal_type,
                'type_tax_use': 'sale'})

        result_super = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name,
            partner_id, lang, update_tax, date_order, packaging,
            fiscal_position, flag, context)
        result_super['value'].update(result['value'])
        if product:
            obj_product = self.pool.get('product.product').browse(cr, uid, product, context=context)
            self.pool.get('product.product').name_get(cr, uid,obj_product.id, context=context)[0][1]
            if obj_product.name:
                result_super['value']['name'] = obj_product.name
        return result_super

        res=super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)

        #Above lines are going to call the native function and 'res' is going to store the result, so you can change the value right there

        if not flag:
            res['value']['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                res['value']['name'] += product_obj.name

        return res

