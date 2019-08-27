#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : mvsi.py 
# @Software: PyCharm
# @Time : 2019/8/26 10:46

from marshmallow import fields

from extensions import db
from models import BasicModel, BaseSchema
from utils import validates as MyValidates, Unicode, date
from utils.file import FileUtil


class Mvsi(BasicModel):
    """
    机动车销售发票
    """
    __tablename__ = 'MVSI_OCR'

    ocr_file_id = db.Column(db.String(length=64), db.ForeignKey('OCR_FILE.ID'),
                            name='OCR_FILE_ID', nullable=False, index=True, comment='OCR流程ID')
    code = db.Column(db.String(length=20), name='CODE', comment='发票代码')
    number = db.Column(db.String(length=20), name='NUMBER', comment='发票号码')
    issue_date = db.Column(db.DateTime, name='ISSUE_DATE', comment='开票日期')
    machine_printed_code = db.Column(db.String(length=20), name='MACHINE_PRINTED_CODE', comment='机打代码')
    machine_printed_number = db.Column(db.String(length=20), name='MACHINE_PRINTED_NUMBER', comment='机打号码')
    machine_number = db.Column(db.String(length=20), name='MACHINE_NUMBER', comment='机器编号')
    fiscal_code = db.Column(db.String(length=190), name='FISCAL_CODE', comment='税控码')
    buyer_name = db.Column(db.String(length=20), name='BUYER_NAME', comment='购买方名称')
    buyer_organization_number = db.Column(db.String(length=18), name='BUYER_ORGANIZATION_NAMBER',
                                          comment='购买方身份证号码/组织机构代码')
    buyer_id = db.Column(db.String(length=20), name='BUYER_ID', comment='购买方纳税人识别号')
    seller_name = db.Column(db.Text, name='SELLER_NAME', comment='销售方名称')
    seller_phone = db.Column(db.String(length=20), name='SELLER_PHONE', comment='销售方电话')
    seller_id = db.Column(db.String(length=20), name='SELLER_ID', comment='销售方纳税人识别号')
    seller_account = db.Column(db.String(length=20), name='SELLER_ACCOUNT', comment='销售方账号')
    seller_address = db.Column(db.Text, name='SELLER_ADDRESS', comment='销售方地址')
    seller_bank = db.Column(db.Text, name='SELLER_BANK', comment='销售方开户行')
    vehicle_type = db.Column(db.Text, name='VEHICLE_TYPE', comment='多用途乘用车')
    brand_model = db.Column(db.Text, name='BRAND_MODEL', comment='厂牌型号')
    manufacturing_location = db.Column(db.String(length=225), name='MANUFACTURING_LOCATION', comment='产地')
    quality_certificate = db.Column(db.String(length=20), name='QUALITY_CERTIFICATE', comment='合格证号')
    import_certificate = db.Column(db.String(length=18), name='IMPORT_CERTIFICATE', comment='进口证明书号')
    inspection_number = db.Column(db.String(length=10), name='INSPECTION_NUMBER', comment='商检单号')
    engine_number = db.Column(db.String(length=8), name='ENGINE_NUMBER', comment='发动机号码')
    vehicle_identification_number = db.Column(db.String(length=17), name='VEHICLE_IDENTIFICATION_NUMBER',
                                              comment='车架号码')
    tonnage = db.Column(db.String(length=10), name='TONNAGE', comment='吨位')
    seating_capacity = db.Column(db.String(length=10), name='SEATING_CAPACITY', comment='限乘人数')
    tax_authority = db.Column(db.Text, name='TAX_AUTHORITY', comment='主管税务机关')
    tax_authority_code = db.Column(db.String(length=9), name='TAX_AUTHORITY_CODE', comment='主管税务机关代码')
    tax_payment_receipt = db.Column(db.String(length=18), name='TAX_PAYMENT_RECEIPT', comment='完税凭证号码')
    tax_rate = db.Column(db.String(length=6), name='TAX_RATE', comment='增值税税率或征收率')
    tax = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TAX', nullable=False,
                    default=0.00, comment='增值税税额')
    tax_exclusive_price = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TAX_EXCLUSIVE_PRICE',
                                    nullable=False, default=0.00, comment='增值税税额')
    total = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TOTAL', nullable=False,
                      default=0.00, comment='价税合计')
    total_chinese = db.Column(db.Text, name='TOTAL_CHINESE', comment='价税合计大写')

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def dao_add(self, ocrFile, file_model, file_path):
        """
        数据入库
        :param ocrFile:
        :param file_model
        :param file_path: 文件路径
        :return:
        """
        super().dao_create()
        with db.auto_commit_db(False, False, error_call=FileUtil.del_file, file_path=file_path) as s:
            # 文件入库
            file_model.dao_init_file(file_path, id=file_model.id, file_name=ocrFile.file_data.file_name, nested=True)

            ocrFile.file_id = file_model.id
            ocrFile.dao_add(nested=True)

            self.ocr_file_id = ocrFile.id
            s.add(self)


class MvsiSchema(BaseSchema):
    """
    机动车销售发票校验器
    """
    __model__ = Mvsi

    ocr_file_id = fields.Str(
        validate=MyValidates.MyLength(min=1, max=64, encode_str=Unicode.UTF_8.value, not_empty=False),
        load_from='ocrFileId'
    )
    code = fields.Str(validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value))
    number = fields.Str(validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value))
    issue_date = fields.DateTime(format=date._TIME_FORMAT[0], load_from='issueDate')
    machine_printed_code = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='machinePrintedCode'
    )
    machine_printed_number = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='machinePrintedNumber'
    )
    machine_number = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='machineNumber'
    )
    fiscal_code = fields.Str(
        validate=MyValidates.MyLength(max=190, encode_str=Unicode.UTF_8.value),
        load_from='fiscalCode'
    )
    buyer_name = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='buyerName'
    )
    buyer_organization_number = fields.Str(
        validate=MyValidates.MyLength(max=18, encode_str=Unicode.UTF_8.value),
        load_from='buyerOrganizationNumber'
    )
    buyer_id = fields.Str(validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value), load_from='buyerId')
    seller_name = fields.Str(load_from='sellerName')
    seller_phone = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='sellerPhone'
    )
    seller_id = fields.Str(validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value), load_from='sellerId')
    seller_account = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='sellerAccount'
    )
    seller_address = fields.Str(load_from='sellerAddress')
    seller_bank = fields.Str(load_from='sellerBank')
    vehicle_type = fields.Str(load_from='vehicleType')
    brand_model = fields.Str(load_from='brandModel')
    manufacturing_location = fields.Str(
        validate=MyValidates.MyLength(max=225, encode_str=Unicode.UTF_8.value),
        load_from='manufacturingLocation'
    )
    quality_certificate = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='qualityCertificate'
    )
    import_certificate = fields.Str(
        validate=MyValidates.MyLength(max=18, encode_str=Unicode.UTF_8.value),
        load_from='importCertificate'
    )
    inspection_number = fields.Str(
        validate=MyValidates.MyLength(max=10, encode_str=Unicode.UTF_8.value),
        load_from='inspectionNumber'
    )
    engine_number = fields.Str(
        validate=MyValidates.MyLength(max=8, encode_str=Unicode.UTF_8.value),
        load_from='engineNumber'
    )
    vehicle_identification_number = fields.Str(
        validate=MyValidates.MyLength(max=17, encode_str=Unicode.UTF_8.value),
        load_from='vehicleIdentificationNumber'
    )
    tonnage = fields.Str(
        validate=MyValidates.MyLength(max=10, encode_str=Unicode.UTF_8.value),
    )
    seating_capacity = fields.Str(
        validate=MyValidates.MyLength(max=10, encode_str=Unicode.UTF_8.value),
        load_from='seatingCapacity'
    )
    tax_authority = fields.Str(load_from='taxAuthority')
    tax_authority_code = fields.Str(
        validate=MyValidates.MyLength(max=9, encode_str=Unicode.UTF_8.value),
        load_from='taxAuthorityCode'
    )
    tax_payment_receipt = fields.Str(
        validate=MyValidates.MyLength(max=18, encode_str=Unicode.UTF_8.value),
        load_from='taxPaymentReceipt'
    )
    tax_rate = fields.Str(
        validate=MyValidates.MyLength(max=6, encode_str=Unicode.UTF_8.value),
        load_from='taxRate'
    )
    tax = fields.Decimal(places=2)
    tax_exclusive_price = fields.Decimal(places=2, load_from='taxExclusivePrice')
    total = fields.Decimal(places=2)
    total_chinese = fields.Str(load_from='totalChinese')

    def only_create(self):
        return super().only_create() + \
               ('code', 'number', 'issue_date', 'machine_printed_code', 'machine_printed_number',
                'machine_number', 'fiscal_code', 'buyer_name', 'buyer_organization_number',
                'buyer_id', 'seller_name', 'seller_phone', 'seller_id', 'seller_account',
                'seller_address', 'seller_bank', 'vehicle_type', 'brand_model', 'manufacturing_location',
                'quality_certificate', 'import_certificate', 'inspection_number', 'engine_number',
                'vehicle_identification_number', 'tonnage', 'seating_capacity', 'tax_authority',
                'tax_authority_code', 'tax_payment_receipt', 'tax_rate', 'tax', 'tax_exclusive_price',
                'total', 'total_chinese')
