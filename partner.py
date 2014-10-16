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

from openerp.osv import orm, fields
from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.partner import PartnerImportMapper, AddressImportMapper
from .backend import magento_beok


MAGENTO_GENDER = {'1': 'm',
                  '2': 'f'}


@magento_beok
class BeOKPartnerImportMapper(PartnerImportMapper):
    _model_name = 'magento.res.partner'

    beok_direct = [
        ('numero_end' , 'number'),
        ('razaosocial', 'legal_name'),
        ('bairro', 'district'),
        ('rg', 'inscr_est'),
        ('ie', 'inscr_est'),
        ('complemento_end', 'street2'),
        ('dob', 'aniversario'),
        ]

    direct = PartnerImportMapper.direct + beok_direct

    @mapping
    def fiscal_position(self, record):
        if record['tipopessoa'] == 'pf':
            return {'partner_fiscal_type_id': 4}

    @mapping
    def gender(self, record):
        gender = MAGENTO_GENDER.get(record.get('gender'))
        return {'sexo': gender}

    @mapping
    def is_company(self, record):
        if record['tipopessoa'] == 'pj':
            return {'is_company': True}
        else:
            return {'is_company': False}



    @mapping
    def names(self, record):
        parts = [part for part in (record['firstname'],
                                   record['lastname']) if part]
        return {'name': ' '.join(parts)}

    @mapping
    def legal_names(self, record):
        if record['tipopessoa'] == 'pf':
            parts = [part for part in (record['firstname'],
                                       record['middlename'],
                                       record['lastname']) if part]
            return {'legal_name': ' '.join(parts)}

    @mapping
    def cpf_cnpj(self, record):
        cpf = record.get('cpf', None)
        cnpj = record.get('cnpj', None)
        if cpf:
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")
            cpf = "%s.%s.%s-%s" % ( cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11] )
            return {"cnpj_cpf": cpf}
        if cnpj:
            cnpj = cnpj.replace(".", "")
            cnpj = cnpj.replace("-", "")
            cnpj = cnpj.replace("/", "")
            cnpj = "%s.%s.%s/%s-%s" % ( cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14] )
            return {"cnpj_cpf": cnpj}


@magento_beok
class BeOKAddressImportMapper(AddressImportMapper):
    _model_name = 'magento.address'

    beok_direct = [
        ('numero_end' , 'number'),
        ('bairro', 'district'),
        ('complemento_end', 'street2'),
        ]

    direct = AddressImportMapper.direct + beok_direct

    @mapping
    def cidade(self, record):
        if not record.get('city'):
            return
        city_ids = self.session.search('l10n_br_base.city',
            [('name', '=ilike', record['city'])])
        if city_ids:
            return {'l10n_br_city_id': city_ids[0]}

    @mapping
    def cep(self, record):
        cep = record.get('postcode', None)
        if cep:
            cep = cep.replace(".", "")
            cep = cep.replace("-", "")
            cep = "%s-%s" % (cep[0:5], cep[5:8])
            return {"zip": cep}

    @mapping
    def company(self, record):
        try:
            if record['company']:
                record['company'] = None
        except KeyError:
            record['company'] = None
