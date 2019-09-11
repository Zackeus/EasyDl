#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Title : 
# @Author : Zackeus
# @File : ocr.py 
# @Software: PyCharm
# @Time : 2019/8/26 9:47

import json
import requests
from marshmallow import fields, Schema, pre_load, post_load

from extensions import db
from utils.huawei_cloud.huawei import HuaweiCloud
from utils import BaseObject, encodes, MyError, is_empty, is_not_empty, auto_wired, codes, ContentType, Assert, \
    validates as MyValidates, Unicode, date, str_util


class OCR(BaseObject):

    @auto_wired('utils.hauwei_cloud.ocr.OCR')
    def __init__(self, user_name=None, password=None, domain_name=None, token=None, huawei_cloud=None):
        """
        华为云OCR识别
        :param user_name: 用户名称
        :param password: 用户的登录密码
        :param domain_name: 用户所属的账号名称
        :param huawei_cloud:
        """
        if is_not_empty(token):
            self.token = token
        elif is_not_empty(user_name) and is_not_empty(password) and is_not_empty(domain_name):
            huawei_cloud = HuaweiCloud(user_name, password, domain_name)
            huawei_cloud.init_token()
            self.token = huawei_cloud.token
        elif is_not_empty(huawei_cloud) and is_not_empty(huawei_cloud.token):
            self.token = huawei_cloud.token
        else:
            raise MyError('缺失鉴权 Token 参数.')

    @auto_wired('utils.hauwei_cloud.ocr.OCR.mvsi')
    def mvsi(self, url, image_bs64):
        """
        机动车销售发票OCR识别
        :param url: OCR接口地址
        :param image_bs64: 图片base64数据, base64编码后大小不超过10M。图片最小边不小于15像素，最长边不超过4096像素,
        支持JPG/PNG/BMP/TIFF格式
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'X-Auth-Token': self.token
        }
        res = requests.post(url=url, data=json.dumps(obj={'image': image_bs64}), headers=headers)
        res.encoding = encodes.Unicode.UTF_8.value

        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

        if res is None or res.status_code != codes.ok:
            mvsi_error, errors = MvsiResultSchema(only=MvsiResultSchema().only_error()).load(res.json())
            Assert.is_true(is_empty(errors), errors)
            return mvsi_error
        mvsi_result, errors = MvsiResultSchema(only=MvsiResultSchema().only_success()).load(res.json().get('result'))
        Assert.is_true(is_empty(errors), errors)
        return mvsi_result


class MvsiResult(BaseObject, db.Model):
    """
    机动车销售发票OCR识别 响应实体
    """
    __abstract__ = True

    code = db.Column(db.String(length=20), name='CODE', comment='发票代码')
    number = db.Column(db.String(length=20), name='NUMBER', comment='发票号码')
    issue_date = db.Column(db.DateTime, name='ISSUE_DATE', comment='开票日期')
    machine_printed_code = db.Column(db.String(length=20), name='MACHINE_PRINTED_CODE', comment='机打代码')
    machine_printed_number = db.Column(db.String(length=20), name='MACHINE_PRINTED_NUMBER', comment='机打号码')
    machine_number = db.Column(db.String(length=20), name='MACHINE_NUMBER', comment='机器编号')
    fiscal_code = db.Column(db.String(length=190), name='FISCAL_CODE', comment='税控码')
    buyer_name = db.Column(db.String(length=20), name='BUYER_NAME', comment='购买方名称')
    buyer_organization_number = db.Column(db.String(length=30), name='BUYER_ORGANIZATION_NAMBER',
                                          comment='购买方身份证号码/组织机构代码')
    buyer_id = db.Column(db.String(length=20), name='BUYER_ID', comment='购买方纳税人识别号')
    seller_name = db.Column(db.Text, name='SELLER_NAME', comment='销售方名称')
    seller_phone = db.Column(db.String(length=20), name='SELLER_PHONE', comment='销售方电话')
    seller_id = db.Column(db.String(length=20), name='SELLER_ID', comment='销售方纳税人识别号')
    seller_account = db.Column(db.String(length=64), name='SELLER_ACCOUNT', comment='销售方账号')
    seller_address = db.Column(db.Text, name='SELLER_ADDRESS', comment='销售方地址')
    seller_bank = db.Column(db.Text, name='SELLER_BANK', comment='销售方开户行')
    vehicle_type = db.Column(db.Text, name='VEHICLE_TYPE', comment='多用途乘用车')
    brand_model = db.Column(db.Text, name='BRAND_MODEL', comment='厂牌型号')
    manufacturing_location = db.Column(db.String(length=225), name='MANUFACTURING_LOCATION', comment='产地')
    quality_certificate = db.Column(db.String(length=20), name='QUALITY_CERTIFICATE', comment='合格证号')
    import_certificate = db.Column(db.String(length=18), name='IMPORT_CERTIFICATE', comment='进口证明书号')
    inspection_number = db.Column(db.String(length=20), name='INSPECTION_NUMBER', comment='商检单号')
    engine_number = db.Column(db.String(length=20), name='ENGINE_NUMBER', comment='发动机号码')
    vehicle_identification_number = db.Column(db.String(length=20), name='VEHICLE_IDENTIFICATION_NUMBER',
                                              comment='车架号码')
    tonnage = db.Column(db.String(length=10), name='TONNAGE', comment='吨位')
    seating_capacity = db.Column(db.String(length=10), name='SEATING_CAPACITY', comment='限乘人数')
    tax_authority = db.Column(db.Text, name='TAX_AUTHORITY', comment='主管税务机关')
    tax_authority_code = db.Column(db.String(length=20), name='TAX_AUTHORITY_CODE', comment='主管税务机关代码')
    tax_payment_receipt = db.Column(db.String(length=18), name='TAX_PAYMENT_RECEIPT', comment='完税凭证号码')
    tax_rate = db.Column(db.String(length=6), name='TAX_RATE', comment='增值税税率或征收率')
    tax = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TAX', nullable=False,
                    default=0.00, comment='增值税税额')
    tax_exclusive_price = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TAX_EXCLUSIVE_PRICE',
                                    nullable=False, default=0.00, comment='增值税税额')
    total = db.Column(db.Numeric(precision=20, scale=2, asdecimal=False), name='TOTAL', nullable=False,
                      default=0.00, comment='价税合计')
    total_chinese = db.Column(db.Text, name='TOTAL_CHINESE', comment='价税合计大写')

    def __init__(self, error_code=None, error_msg=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.error_code = error_code
        self.error_msg = error_msg


class MvsiResultSchema(Schema):
    __AMOUNT = ['￥', '$']

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
        validate=MyValidates.MyLength(max=30, encode_str=Unicode.UTF_8.value),
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
        validate=MyValidates.MyLength(max=64, encode_str=Unicode.UTF_8.value),
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
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='inspectionNumber'
    )
    engine_number = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
        load_from='engineNumber'
    )
    vehicle_identification_number = fields.Str(
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
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
        validate=MyValidates.MyLength(max=20, encode_str=Unicode.UTF_8.value),
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

    error_code = fields.Str(load_from='errorCode')
    error_msg = fields.Str(load_from='errorMsg')

    @pre_load
    def pre_load_data(self, data):
        """
        预处理数据
        :param data:
        :return:
        """
        issue_date = data.get('issue_date')
        if is_not_empty(issue_date):
            # noinspection PyBroadException
            try:
                date.str_to_time(issue_date)
            except:
                data['issue_date'] = None

        data['tax_exclusive_price'] = str_util.amount_formatting(data.get('tax_exclusive_price'), self.__AMOUNT)
        data['tax'] = str_util.amount_formatting(data.get('tax'), self.__AMOUNT)
        data['total'] = str_util.amount_formatting(data.get('total'), self.__AMOUNT)
        return data

    @post_load
    def make_object(self, data):
        return MvsiResult(**data)

    def only_success(self):
        return 'code', 'number', 'issue_date', 'machine_printed_code', 'machine_printed_number', \
               'machine_number', 'fiscal_code', 'buyer_name', 'buyer_organization_number',\
               'buyer_id', 'seller_name', 'seller_phone', 'seller_id', 'seller_account',\
               'seller_address', 'seller_bank', 'vehicle_type', 'brand_model', 'manufacturing_location',\
               'quality_certificate', 'import_certificate', 'inspection_number', 'engine_number',\
               'vehicle_identification_number', 'tonnage', 'seating_capacity', 'tax_authority',\
               'tax_authority_code', 'tax_payment_receipt', 'tax_rate', 'tax', 'tax_exclusive_price',\
               'total', 'total_chinese'

    def only_error(self):
        return 'error_code', 'error_msg'


if __name__ == '__main__':
    pass
    # from utils.file import img
    # img_path = 'D:/AIData/12.jpg'
    #
    # ocr = OCR('Zackeus', 'syr391592723*', 'Zackeus')
    # mvsi = ocr.mvsi('https://ocr.cn-north-1.myhuaweicloud.com/v1.0/ocr/mvs-invoice',
    #                 img.ImgUtil.img_compress(path=img_path, threshold=5))
    # print(mvsi)


