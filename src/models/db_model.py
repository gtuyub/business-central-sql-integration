from .base import Base
from sqlalchemy.types import TypeDecorator, String, Integer, Float, Boolean, Date
from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

class CustomString(TypeDecorator):
    """Custom string type to map empty strings to NULL"""

    impl = String
    cache_ok = True

    def process_bind_param(self,value,dialect):
        if value == '' or value == ' ':
            return None
        return value
    
    def process_result_value(self, value, dialect):
        return value
    
    def copy(self, **kw):
        return CustomString(self.impl.length)


#For each subclass of the base class the following is true:
#The attribute name of a column matches with the corresponding api field name.
#The class name matches with the corresponding api endpoint.

class currencies(Base):
    __tablename__ = 'currency'
 
    code : Mapped[str] = mapped_column('currency_code',String[10],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('currency_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']
    
class exchangeRates(Base):
    __tablename__ = 'exchange_rate'

    startingDate : Mapped[date] = mapped_column('starting_date',Date,nullable=False)
    currencyCode : Mapped[str] = mapped_column('currency_code',String[10])
    relationalCurrencyCode : Mapped[str] = mapped_column('related_currency_code',String[10])
    exchangeRateAmount : Mapped[float] =  mapped_column('amount',Float)

    @classmethod    
    def get_update_keys(cls):
        return ['startingDate','currencyCode','relationalCurrencyCode']

class paymentTerms(Base):
    __tablename__ = 'payment_terms'

    code : Mapped[str] = mapped_column('payment_terms_code',String[10],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('payment_terms_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']

class countries(Base):
    __tablename__ = 'country'

    code : Mapped[str]= mapped_column('country_code',String[10],unique=True,nullable=False)
    name : Mapped[Optional[str]] = mapped_column('country_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']

class shipmentMethods(Base):
    __tablename__ = 'shipment_method'

    code : Mapped[str] = mapped_column('shipment_method_code',String[10],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('shipment_method_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class priceGroups(Base):
    __tablename__ = 'customer_price_group'

    code : Mapped[str] = mapped_column('customer_price_group_code',String[10],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('customer_price_group_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']

class locations(Base):
    __tablename__ = 'location'

    code : Mapped[str] = mapped_column('location_code',String[20],unique=True,nullable=False)
    name : Mapped[Optional[str]] = mapped_column('location_name',CustomString[100])
    countryRegionCode : Mapped[Optional[str]] = mapped_column('country_code',CustomString[10])



    @classmethod
    def get_update_keys(cls):
        return ['code']


class paymentMethods(Base):
    __tablename__ = 'payment_method'

    code : Mapped[str] = mapped_column('payment_method_code',String[20],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('payment_method_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class itemCategories(Base):
    __tablename__ = 'item_category'

    code : Mapped[str] = mapped_column('item_category_code',String[20],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('item_category_name',CustomString[100])
    hasChildren : Mapped[Optional[bool]] = mapped_column('has_children',Boolean)
    parentCategory : Mapped[Optional[str]] = mapped_column('parent_category',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class customerPostingGroups(Base):
    __tablename__ = 'customer_posting_group'

    code : Mapped[str] = mapped_column('customer_posting_group_code',String[20],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('customer_posting_group_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class vendorPostingGroups(Base):
    __tablename__ = 'vendor_posting_group'

    code : Mapped[str] = mapped_column('vendor_posting_group_code',String[20],unique=True, nullable=False)
    description : Mapped[str] = mapped_column('vendor_posting_group_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class inventoryPostingGroups(Base):
    __tablename__ = 'inventory_posting_group'

    code : Mapped[str] = mapped_column('inventory_posting_group_code',String[20],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('inventory_posting_group_name',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['code']


class customers(Base):
    __tablename__ = 'customer'

    no : Mapped[str] = mapped_column('customer_code',String[20],unique=True,nullable=False)
    name : Mapped[Optional[str]] = mapped_column('customer_name',CustomString[100])
    contact : Mapped[Optional[str]] = mapped_column('contact_code',String[20])
    customerPostingGroup : Mapped[Optional[str]] = mapped_column('customer_posting_group_code',String[20])
    customerPriceGroup : Mapped[Optional[str]] = mapped_column('customer_price_group_code',String[20])
    paymentTermsCode : Mapped[Optional[str]] = mapped_column('payment_terms_code',String[20])
    countryRegionCode : Mapped[Optional[str]] = mapped_column('country_code',String[10])
    locationCode : Mapped[Optional[str]] = mapped_column('location_code',String[20])
    salespersonCode : Mapped[Optional[str]] = mapped_column('salesperson_code',String[20])
    rfcNo : Mapped[Optional[str]] = mapped_column('rfc_code',CustomString[13])
    blocked : Mapped[Optional[str]] = mapped_column('is_blocked',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['no']


class vendors(Base):
    __tablename__ = 'vendor'

    no : Mapped[str] = mapped_column('vendor_code',String[20],unique=True,nullable=False)
    name : Mapped[Optional[str]] = mapped_column('vendor_name',CustomString[100])
    primaryContactNo : Mapped[Optional[str]] = mapped_column('contact_code',String[20])
    vendorPostingGroup : Mapped[Optional[str]] = mapped_column('vendor_posting_group',String[20])
    paymentTermsCode : Mapped[Optional[str]] = mapped_column('payment_terms_code',String[20])
    countryRegionCode : Mapped[Optional[str]] = mapped_column('country_code',String[20])
    locationCode : Mapped[Optional[str]] = mapped_column('location_code',String[20])
    purchaserCode : Mapped[Optional[str]] = mapped_column('purchaser_code',String[20])
    rfcNo : Mapped[Optional[str]] = mapped_column('rfc_code',CustomString[13])
    blocked : Mapped[Optional[str]] = mapped_column('is_blocked',CustomString[100])

    @classmethod
    def get_update_keys(cls):
        return ['no']


class salesmen(Base):
    __tablename__ = 'salesperson'

    code : Mapped[str] = mapped_column('salesperson_code',String[20],unique=True,nullable=False)
    name : Mapped[Optional[str]] = mapped_column('salesperson_name',CustomString[100])
    blocked : Mapped[Optional[bool]] = mapped_column('is_blocked',Boolean)

    @classmethod
    def get_update_keys(cls):
        return ['code']


class items(Base):
    __tablename__ = 'item'

    no : Mapped[str] = mapped_column('item_code',String[20],unique=True,nullable=False)
    description : Mapped[Optional[str]] = mapped_column('item_name',CustomString[100])
    baseUnitOfMeasure : Mapped[Optional[str]] = mapped_column('measure_unit',CustomString[50])
    type : Mapped[Optional[str]] = mapped_column('item_type',CustomString[100])
    inventoryPostingGroup : Mapped[Optional[str]] =  mapped_column('inventory_posting_group_code',String[20])
    itemCategoryCode : Mapped[Optional[str]] = mapped_column('item_category_code',String[20])
    unitPrice : Mapped[Optional[float]] = mapped_column('unit_price',Float)
    unitCost : Mapped[Optional[float]] = mapped_column('unit_cost',Float)
    grossWeight : Mapped[Optional[float]] = mapped_column('gross_weight',Float)
    netWeight : Mapped[Optional[float]] = mapped_column('net_weight',Float)
    blocked : Mapped[Optional[bool]] = mapped_column('is_blocked',Boolean)
    salesBlocked : Mapped[Optional[bool]] = mapped_column('sales_blocked',Boolean)
    purchasingBlocked : Mapped[Optional[bool]] = mapped_column('purchase_blocked',Boolean)

    @classmethod
    def get_update_keys(cls):
        return ['no']

class customerLedgerEntries(Base):
    __tablename__ = 'customer_ledger'

    entryNo : Mapped[int] = mapped_column('entry_id',Integer,unique=True,nullable=False,autoincrement=False)
    postingDate : Mapped[date] = mapped_column('posting_date',Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    documentType : Mapped[Optional[str]] = mapped_column('document_type',CustomString[100])
    documentNo : Mapped[str] = mapped_column('document_no',String[25])
    customerNo : Mapped[str] = mapped_column('customer_code',String[20])
    currencyCode : Mapped[Optional[str]] = mapped_column('currency_code',String[10])
    amount : Mapped[float] = mapped_column('amount',Float)
    remainingAmount : Mapped[float] = mapped_column('remaining_amount',Float)
    positive : Mapped[bool] = mapped_column('is_positive',Boolean)
    transactionNo : Mapped[int] = mapped_column('transaction_no',Integer)
    externalDocumentNo : Mapped[Optional[str]] = mapped_column('external_document_no',CustomString[35])
    appliesToExtDocNo : Mapped[Optional[str]] = mapped_column('apply_to_external_document_no',CustomString[35])
    closedByEntryNo : Mapped[int]= mapped_column('closed_by_entry',Integer)
    open : Mapped[bool] = mapped_column('is_open',Boolean)
    reversed : Mapped[bool] = mapped_column('is_reversed',Boolean)
    reversedByEntryNo : Mapped[int] = mapped_column('reversed_by_entry',Integer)
    reversedEntryNo : Mapped[int] = mapped_column('reversed_entry',Integer)   

    @classmethod
    def get_update_keys(cls):
        return ['entryNo'] 


class vendorLedgerEntries(Base):
    __tablename__ = 'vendor_ledger'

    entryNo : Mapped[int] = mapped_column('entry_id',Integer,unique=True,nullable=False,autoincrement=False)
    postingDate : Mapped[date] = mapped_column('posting_date',Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    documentType : Mapped[date] = mapped_column('document_type',CustomString[100])
    documentNo : Mapped[str] = mapped_column('document_no', String[25])
    vendorNo : Mapped[str] = mapped_column('vendor_code',String[20])
    currencyCode : Mapped[str] = mapped_column('currency_code',String[10])
    amount : Mapped[float] = mapped_column('amount',Float)
    remainingAmount : Mapped[float] = mapped_column('remaining_amount',Float)
    positive : Mapped[Optional[bool]] = mapped_column('is_positive',Boolean)
    transactionNo : Mapped[int] = mapped_column('transaction_no',Integer)
    externalDocumentNo : Mapped[str] = mapped_column('external_document_no',CustomString[35])
    appliesToExtDocNo : Mapped[str] = mapped_column('apply_to_external_document_no',CustomString[35])
    closedByEntryNo : Mapped[Integer] = mapped_column('closed_by_entry',Integer)
    open : Mapped[bool] = mapped_column('is_open',Boolean)
    reversed : Mapped[bool] = mapped_column('is_reversed',Boolean)
    reversedByEntryNo : Mapped[int] = mapped_column('reversed_by_entry',Integer)
    reversedEntryNo : Mapped[int] = mapped_column('reversed_entry',Integer)    

    @classmethod
    def get_update_keys(cls):
        return ['entryNo']


class salesInvoices(Base):
    __tablename__ = 'sales_invoice'

    no : Mapped[str] = mapped_column('document_no',String[25],unique=True,nullable=False)
    custLedgerEntryNo : Mapped[int] = mapped_column('entry_id',Integer,nullable=False)
    postingDate : Mapped[date] = mapped_column('posting_date', Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    sellToCustomerNo : Mapped[str] = mapped_column('customer_code',String[20])
    shipToCode : Mapped[Optional[str]] = mapped_column('ship_to_code',String[10])
    paymentMethodCode : Mapped[Optional[str]] = mapped_column('payment_method_code',String[20])
    shipmentMethodCode : Mapped[Optional[str]] = mapped_column('shipment_method_code',String[20])
    locationCode : Mapped[Optional[str]] = mapped_column('location_code',String[20])
    currencyCode : Mapped[Optional[str]] = mapped_column('currency_code',String[10])
    salespersonCode : Mapped[Optional[str]]= mapped_column('salesperson_code',String[20])
    amount : Mapped[float]= mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)
    orderNo : Mapped[Optional[str]] = mapped_column('order_no',CustomString[25])

    @classmethod
    def get_update_keys(cls):
        return ['no']

class salesInvoiceLines(Base):
    __tablename__ = 'sales_invoice_line'

    documentNo : Mapped[str] = mapped_column('document_no', String[25], nullable=False)
    lineNo : Mapped[int] = mapped_column('line_no',Integer)
    type : Mapped[Optional[str]] = mapped_column('item_type',CustomString[100])
    no : Mapped[str] = mapped_column('item_code',CustomString[25])
    quantity : Mapped[int] = mapped_column('quantity',Integer)
    unitPrice : Mapped[Optional[float]]= mapped_column('unit_price',Float)
    lineDiscount : Mapped[Optional[float]] = mapped_column('discount_percentage',Float)
    lineDiscountAmount : Mapped[Optional[float]] = mapped_column('discount_amount',Float)
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float]= mapped_column('amount_with_vat',Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo','lineNo']


class salesCreditMemos(Base):
    __tablename__ = 'sales_cr_memo'

    no : Mapped[str] = mapped_column('document_no',String[25],unique=True,nullable=False)
    custLedgerEntryNo : Mapped[int] = mapped_column('entry_id',Integer,nullable=False)
    postingDate : Mapped[date] = mapped_column('posting_date',Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    sellToCustomerNo : Mapped[str] = mapped_column('customer_code',String[20])
    shipToCode : Mapped[Optional[str]] = mapped_column('ship_to_code',String[10])
    paymentMethodCode : Mapped[Optional[str]] = mapped_column('payment_method_code',String[20])
    shipmentMethodCode : Mapped[Optional[str]] = mapped_column('shipment_method_code',String[20])
    locationCode : Mapped[Optional[str]] = mapped_column('location_code',String[20])
    currencyCode : Mapped[Optional[str]] = mapped_column('currency_code',String[10])
    salespersonCode : Mapped[Optional[str]] = mapped_column('salesperson_code',String[20])
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)
    returnOrderNo : Mapped[Optional[str]] = mapped_column('return_order_no',CustomString[25])

    @classmethod
    def get_update_keys(cls):
        return ['no']

    
class salesCreditMemoLines(Base):
    __tablename__ = 'sales_cr_memo_line'

    documentNo : Mapped[str] = mapped_column('document_no',String[25],nullable=False)
    lineNo : Mapped[int]  = mapped_column('line_no',Integer)
    type : Mapped[Optional[str]] = mapped_column('item_type',CustomString[100])
    no : Mapped[Optional[str]] = mapped_column('item_code',CustomString[20])
    quantity : Mapped[int] = mapped_column('quantity',Integer)
    unitPrice : Mapped[float] = mapped_column('unit_price', Float)
    lineDiscount : Mapped[float] = mapped_column('discount_percentage',Float)
    lineDiscountAmount : Mapped[float] = mapped_column('discount_amount',Float)
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo','lineNo']


class purchaseInvoices(Base):
    __tablename__ = 'purchase_invoice'

    no : Mapped[str] = mapped_column('document_no',String[25],unique=True,nullable=False)
    vendorLedgerEntryNo : Mapped[int] = mapped_column('entry_id',Integer,nullable=False)
    postingDate : Mapped[date] = mapped_column('posting_date', Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    buyFromVendorNo : Mapped[str] = mapped_column('vendor_code',String[20])
    paymentMethodCode : Mapped[Optional[str]] = mapped_column('payment_method_code',String[20])
    currencyCode : Mapped[Optional[str]] = mapped_column('currency_code',String[10])
    purchaserCode : Mapped[Optional[str]] = mapped_column('purchaser_code',String[20])
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)
    orderNo : Mapped[str] = mapped_column('order_no',CustomString[25])

    @classmethod
    def get_update_keys(cls):
        return ['no']

class purchaseCreditMemos(Base):
    __tablename__ = 'purchase_cr_memo'

    no : Mapped[str] = mapped_column('document_no',String[25], unique=True, nullable=False)
    vendorLedgerEntryNo : Mapped[int] = mapped_column('entry_id',Integer,nullable=False)
    postingDate : Mapped[date] = mapped_column('posting_date', Date)
    documentDate : Mapped[date] = mapped_column('document_date',Date)
    buyFromVendorNo : Mapped[str] = mapped_column('vendor_code',String[20])
    paymentMethodCode : Mapped[Optional[str]] = mapped_column('payment_method_code',String[20])
    currencyCode : Mapped[Optional[str]] = mapped_column('currency_code',String[10])
    purchaserCode : Mapped[Optional[str]] = mapped_column('purchaser_code',String[20])
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)
    returnOrderNo : Mapped[Optional[str]] = mapped_column('return_order_no',CustomString[25])

    @classmethod
    def get_update_keys(cls):
        return ['no']

class purchaseInvoiceLines(Base):
    __tablename__ = 'purchase_invoice_line'

    documentNo : Mapped[str] = mapped_column('document_no',String[25],nullable=False)
    lineNo : Mapped[int] = mapped_column('line_no',Integer)
    type : Mapped[Optional[str]] = mapped_column('item_type', CustomString[100])
    no : Mapped[Optional[str]] = mapped_column('item_code',CustomString[20])
    quantity : Mapped[int] = mapped_column('quantity',Integer)
    unitCost : Mapped[float] = mapped_column('unit_cost',Float)
    lineDiscount : Mapped[float] = mapped_column('discount_percentage',Float)
    lineDiscountAmount : Mapped[float] = mapped_column('discount_amount',Float)
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo', 'lineNo']

class purchaseCreditMemoLines(Base):
    __tablename__ = 'purchase_cr_memo_line'

    documentNo : Mapped[str] = mapped_column('document_no',String[25],nullable=False)
    lineNo : Mapped[int] = mapped_column('line_no',Integer)
    type : Mapped[str] = mapped_column('item_type',CustomString[100])
    no : Mapped[Optional[str]] = mapped_column('item_code',CustomString[20])
    quantity : Mapped[int] = mapped_column('quantity',Integer)
    unitCost : Mapped[float] = mapped_column('unit_cost',Float)
    lineDiscount : Mapped[float] = mapped_column('discount_percentage',Float)
    lineDiscountAmount : Mapped[float] = mapped_column('discount_amount',Float)
    amount : Mapped[float] = mapped_column('amount',Float)
    amountIncludingVAT : Mapped[float] = mapped_column('amount_with_vat',Float)

    @classmethod
    def get_update_keys(cls):
        return ['documentNo', 'lineNo']


class Tables(str,Enum):

    currencies = 'divisas'
    paymentTerms = 'terminos_de_pago'
    countries = 'paises'
    shipmentMethods = 'metodos_de_entrega'
    priceGroups = 'grupos_de_precio'
    locations = 'almacenes'
    paymentMethods = 'metodos_de_pago'
    itemCategories = 'categorias_de_producto'
    customerPostingGroups = 'grupos_de_cliente'
    inventoryPostingGroups = 'grupos_de_inventario'
    vendorPostingGroups = 'grupos_contables_proveedor'
    exchangeRates = 'tipos_de_cambio'
    salesmen = 'vendedores'
    items = 'productos'
    customers = 'clientes'
    vendors = 'proveedores'
    customerLedgerEntries = 'movimientos_cliente'
    vendorLedgerEntries = 'movimientos_proveedores'
    salesInvoices = 'facturas_de_venta'
    salesInvoiceLines = 'detalle_facturas_de_venta'
    salesCreditMemos = 'notas_de_credito_de_venta'
    salesCreditMemoLines = 'detalle_notas_de_credito_de_venta'
    purchaseInvoices = 'facturas_de_compra'
    purchaseInvoiceLines = 'detalle_facturas_de_compra'
    purchaseCreditMemos = 'notas_de_credito_de_compra'
    purchaseCreditMemoLines = 'detalle_notas_de_credito_de_compra'
