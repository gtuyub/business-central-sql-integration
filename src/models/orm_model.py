from typing import Dict, List
from sqlalchemy.orm import Session
from .base import Base
import sqlalchemy.types as types
from sqlalchemy import Column
from enum import Enum

class CustomString(types.TypeDecorator):
    """Custom string type decorator which maps empty strings to NULL"""

    impl = types.String
    cache_ok = True

    def process_bind_param(self,value,dialect):
        if value == '' or value == ' ':
            return None
        return value
    
    def process_result_value(self, value, dialect):
        return value
    
    def copy(self, **kw):
        return CustomString(self.impl.length)


#Subclasses of Base class, each represents a table on sql database.
#Class names coincide with the corresponding api endpoint.
#Therefore, we map api endpoint field names as class attributes, to sql table column names.

class currencies(Base):
    __tablename__ = 'currency'

    code = Column('currency_code',types.String,unique=True)
    description = Column('currency_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']
    
class exchangeRates(Base):
    __tablename__ = 'exchange_rate'

    startingDate = Column('starting_date',types.Date)
    currencyCode = Column('currency_code',types.String)
    relationalCurrencyCode = Column('related_currency_code',types.String)
    exchangeRateAmount = Column('amount',types.Float)

    @classmethod
    def get_update_keys(cls):
        return [
            'startingDate',
            'currencyCode',
            'relationalCurrencyCode'
            ]

class paymentTerms(Base):
    __tablename__ = 'payment_terms'

    code = Column('payment_terms_code',types.String,unique=True)
    description = Column('payment_terms_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']

class countries(Base):
    __tablename__ = 'country'

    code = Column('country_code',types.String,unique=True)
    name = Column('country_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']

class shipmentMethods(Base):
    __tablename__ = 'shipment_method'

    code = Column('shipment_method_code',types.String,unique=True)
    description = Column('shipment_method_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class priceGroups(Base):
    __tablename__ = 'customer_price_group'

    code = Column('customer_price_group_code',types.String,unique=True)
    description = Column('customer_price_group_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']

class locations(Base):
    __tablename__ = 'location'

    code = Column('location_code',types.String,unique=True)
    name = Column('location_name',CustomString)
    countryRegionCode = Column('country_code',CustomString)



    @classmethod
    def get_update_keys(cls):
        return ['code']


class paymentMethods(Base):
    __tablename__ = 'payment_method'

    code = Column('payment_method_code',types.String,unique=True)
    description = Column('payment_method_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class itemCategories(Base):
    __tablename__ = 'item_category'

    code = Column('item_category_code',types.String,unique=True)
    description = Column('item_category_name',CustomString)
    hasChildren = Column('has_children',types.Boolean)
    parentCategory = Column('parent_category',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class customerPostingGroups(Base):
    __tablename__ = 'customer_posting_group'

    code = Column('customer_posting_group_code',types.String,unique=True)
    description = Column('customer_posting_group_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class vendorPostingGroups(Base):
    __tablename__ = 'vendor_posting_group'

    code = Column('vendor_posting_group_code',types.String,unique=True)
    description = Column('vendor_posting_group_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class inventoryPostingGroups(Base):
    __tablename__ = 'inventory_posting_group'

    code = Column('inventory_posting_group_code',types.String,unique=True)
    description = Column('inventory_posting_group_name',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class customers(Base):
    __tablename__ = 'customer'

    no = Column('customer_code',types.String,unique=True)
    name = Column('customer_name',CustomString)
    contact = Column('contact_code',CustomString)
    customerPostingGroup = Column('customer_posting_group_code',CustomString)
    customerPriceGroup = Column('customer_price_group_code',CustomString)
    paymentTermsCode = Column('payment_terms_code',CustomString)
    countryRegionCode = Column('country_code',CustomString)
    locationCode = Column('location_code',CustomString)
    salespersonCode = Column('salesperson_code',CustomString)
    rfcNo = Column('rfc_code',CustomString)
    blocked = Column('is_blocked',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']


class vendors(Base):
    __tablename__ = 'vendor'

    no = Column('vendor_code',types.String,unique=True)
    name = Column('vendor_name',CustomString)
    primaryContactNo = Column('contact_code',CustomString)
    vendorPostingGroup = Column('vendor_posting_group',CustomString)
    paymentTermsCode = Column('payment_terms_code',CustomString)
    countryRegionCode = Column('country_code',CustomString)
    locationCode = Column('location_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    rfcNo = Column('rfc_code',CustomString)
    blocked = Column('is_blocked',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']


class salesmen(Base):
    __tablename__ = 'salesperson'

    code = Column('salesperson_code',types.String,unique=True)
    name = Column('salesperson_name',CustomString)
    blocked = Column('is_blocked',types.Boolean)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class items(Base):
    __tablename__ = 'item'

    no = Column('item_code',types.String,unique=True)
    description = Column('item_name',CustomString)
    baseUnitOfMeasure = Column('measure_unit',CustomString)
    type = Column('item_type',CustomString)
    inventoryPostingGroup = Column('inventory_posting_group_code',CustomString)
    itemCategoryCode = Column('item_category_code',CustomString)
    unitPrice = Column('unit_price',types.Float)
    unitCost = Column('unit_cost',types.Float)
    grossWeight = Column('gross_weight',types.Float)
    netWeight = Column('net_weight',types.Float)
    blocked = Column('is_blocked',types.Boolean)
    salesBlocked = Column('sales_blocked',types.Boolean)
    purchasingBlocked = Column('purchase_blocked',types.Boolean)

    @classmethod
    def get_update_keys(cls):
        return ['no']

class customerLedgerEntries(Base):
    __tablename__ = 'customer_ledger'

    entryNo = Column('entry_id',types.Integer,unique=True,autoincrement=False)
    postingDate = Column('posting_date',types.Date)
    documentDate = Column('document_date',types.Date)
    documentType = Column('document_type',CustomString)
    documentNo = Column('document_no',types.String)
    customerNo = Column('customer_code',types.String)
    currencyCode = Column('currency_code',CustomString)
    amount = Column('amount',types.Float)
    remainingAmount = Column('remaining_amount',types.Float)
    positive = Column('is_positive',types.Boolean)
    transactionNo = Column('transaction_no',types.Integer)
    externalDocumentNo = Column('external_document_no',CustomString)
    appliesToExtDocNo = Column('apply_to_external_document_no',CustomString)
    closedByEntryNo = Column('closed_by_entry',types.Integer)
    open = Column('is_open',types.Boolean)
    reversed = Column('is_reversed',types.Boolean)
    reversedByEntryNo = Column('reversed_by_entry',types.Integer)
    reversedEntryNo = Column('reversed_entry',types.Integer)   

    @classmethod
    def get_update_keys(cls):
        return ['entryNo'] 


class vendorLedgerEntries(Base):
    __tablename__ = 'vendor_ledger'

    entryNo = Column('entry_id',types.Integer,unique=True,autoincrement=False)
    postingDate = Column('posting_date',types.Date)
    documentDate = Column('document_date',types.Date)
    documentType = Column('document_type',CustomString)
    documentNo = Column('document_no',types.String)
    vendorNo = Column('vendor_code',types.String)
    currencyCode = Column('currency_code',CustomString)
    amount = Column('amount',types.Float)
    remainingAmount = Column('remaining_amount',types.Float)
    positive = Column('is_positive',types.Boolean)
    transactionNo = Column('transaction_no',types.Integer)
    externalDocumentNo = Column('external_document_no',CustomString)
    appliesToExtDocNo = Column('apply_to_external_document_no',CustomString)
    closedByEntryNo = Column('closed_by_entry',types.Integer)
    open = Column('is_open',types.Boolean)
    reversed = Column('is_reversed',types.Boolean)
    reversedByEntryNo = Column('reversed_by_entry')
    reversedEntryNo = Column('reversed_entry')    

    @classmethod
    def get_update_keys(cls):
        return ['entryNo']


class salesInvoices(Base):
    __tablename__ = 'sales_invoice'

    no = Column('document_no',types.String, unique=True)
    custLedgerEntryNo = Column('entry_id',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    sellToCustomerNo = Column('customer_code',types.String)
    shipToCode = Column('ship_to_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    shipmentMethodCode = Column('shipment_method_code',CustomString)
    locationCode = Column('location_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    salespersonCode = Column('salesperson_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    orderNo = Column('order_no',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']

class salesInvoiceLines(Base):
    __tablename__ = 'sales_invoice_line'

    documentNo = Column('document_no',types.String)
    lineNo = Column('line_no',types.Integer)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitPrice = Column('unit_price',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo','lineNo']


class salesCreditMemos(Base):
    __tablename__ = 'sales_cr_memo'

    no = Column('document_no',types.String, unique=True)
    custLedgerEntryNo = Column('entry_id',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    sellToCustomerNo = Column('customer_code',CustomString)
    shipToCode = Column('ship_to_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    shipmentMethodCode = Column('shipment_method_code',CustomString)
    locationCode = Column('location_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    salespersonCode = Column('salesperson_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    returnOrderNo = Column('return_order_no',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']

    
class salesCreditMemoLines(Base):
    __tablename__ = 'sales_cr_memo_line'

    documentNo = Column('document_no',types.String)
    lineNo = Column('line_no',types.Integer)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitPrice = Column('unit_price',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo','lineNo']


class purchaseInvoices(Base):
    __tablename__ = 'purchase_invoice'

    no = Column('document_no',types.String,unique=True)
    vendorLedgerEntryNo = Column('entry_id',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    buyFromVendorNo = Column('vendor_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    orderNo = Column('order_no',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']

class purchaseCreditMemos(Base):
    __tablename__ = 'purchase_cr_memo'

    no = Column('document_no',types.String, unique=True)
    vendorLedgerEntryNo = Column('entry_id',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    buyFromVendorNo = Column('vendor_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    returnOrderNo = Column('return_order_no',CustomString)

    @classmethod
    def get_update_keys(cls):
        return ['no']

class purchaseInvoiceLines(Base):
    __tablename__ = 'purchase_invoice_line'

    documentNo = Column('document_no',types.String)
    lineNo  = Column('line_no',types.Integer)
    type = Column('item_type', CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitCost = Column('unit_cost',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo', 'lineNo']

class purchaseCreditMemoLines(Base):
    __tablename__ = 'purchase_cr_memo_line'

    documentNo = Column('document_no',types.String)
    lineNo  = Column('line_no',types.Integer)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitCost = Column('unit_cost',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo', 'lineNo']


class Tables(str,Enum) :

    currencies = 'Divisas'
    paymentTerms = 'TerminosPago'
    countries = 'Paises'
    shipmentMethods = 'MetodosEntrega'
    priceGroups = 'GruposPreciosCliente'
    locations = 'Almacenes'
    paymentMethods = 'MetodosPago'
    itemCategories = 'CategoriasProducto'
    customerPostingGroups = 'GruposCliente'
    inventoryPostingGroups = 'GruposInventario'
    vendorPostingGroups = 'GruposProveedor'
    exchangeRates = 'TiposCambio'
    salesmen = 'Vendedores'
    items = 'Productos'
    customers = 'Clientes'
    vendors = 'Proveedores'
    customerLedgerEntries = 'MovimientosClientes'
    vendorLedgerEntries = 'MovimientosProveedores'
    salesInvoices = 'FacturasVenta'
    salesInvoiceLines = 'LineasFacturasVenta'
    salesCreditMemos = 'NotasCreditoVenta'
    salesCreditMemoLines = 'LineasNotasCreditoVenta'
    purchaseInvoices = 'FacturasCompra'
    purchaseInvoiceLines = 'LineasFacturasCompra'
    purchaseCreditMemos = 'NotasCreditoCompra'
    purchaseCreditMemoLines = 'LineasNotasCreditoCompra'
