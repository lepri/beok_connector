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

from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.product import ProductImportMapper
from .backend import magento_beok


@magento_beok
class BeOKProductImportMapper(ProductImportMapper):
    _model_name = 'magento.product.product'


#    beok_direct = [
#        ('ncm' , 'ncm_id'),
#        ]
#
#    direct = ProductImportMapper.direct + beok_direct

    @mapping
    def fiscal_type(self, record):
        return {'fiscal_type': 'product'}

    @mapping
    def type(self, record):
        return {'type': 'consu'}

    @mapping
    def ncm(self, record):
        if not record.get('ncm'):
            return
        cr = self.session.cr
        sql = """ SELECT * FROM account_product_fiscal_classification WHERE replace(name, '.', '') = '%s'; """ % record['ncm'].strip()
        cr.execute(sql)
        ncm_id = cr.dictfetchone()['id']
        if ncm_id:
            return {'ncm_id': ncm_id}
