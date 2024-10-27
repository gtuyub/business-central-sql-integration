from .base import Base
import sqlalchemy.types as types
from sqlalchemy import Column
from enum import Enum

class CustomString(types.TypeDecorator):
    """ Custom String class which converts the placeholders '' to None,
    which translates to SQL NULL when inserting on the database."""

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


class currencies(Base):
    __tablename__ = 'Currency'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class exchangeRates(Base):
    __tablename__ = 'ExchangeRate'

    startingDate = Column('starting_date',types.Date,primary_key=True)
    currencyCode = Column('currency_code',CustomString,primary_key=True)
    relationalCurrencyCode = Column('relational_currency_code',CustomString,primary_key=True)
    exchangeRateAmount = Column('amount',types.Float)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class paymentTerms(Base):
    __tablename__ = 'PaymentTerms'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class countries(Base):
    __tablename__ = 'Country'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class shipmentMethods(Base):
    __tablename__ = 'ShipmentMethod'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class priceGroups(Base):
    __tablename__ = 'CustomerPriceGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class locations(Base):
    __tablename__ = 'Location'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class paymentMethods(Base):
    __tablename__ = 'PaymentMethod'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class itemCategories(Base):
    __tablename__ = 'ItemCategory'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    hasChildren = Column('has_children',types.Boolean)
    parentCategory = Column('parent_category',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class customerPostingGroups(Base):
    __tablename__ = 'CustomerPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class vendorPostingGroups(Base):
    __tablename__ = 'VendorPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class inventoryPostingGroups(Base):
    __tablename__ = 'InventoryPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class customers(Base):
    __tablename__ = 'Customer'

    no = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    contact = Column('contact_code',CustomString)
    customerPostingGroup = Column('customer_posting_group',CustomString)
    customerPriceGroup = Column('customer_price_group',CustomString)
    paymentTermsCode = Column('payment_terms_code',CustomString)
    countryRegionCode = Column('country_code',CustomString)
    locationCode = Column('location_code',CustomString)
    salespersonCode = Column('salesperson_code',CustomString)
    rfcNo = Column('rfc_code',CustomString)
    blocked = Column('blocked',CustomString)
    systemCreatedAt = Column('created_at', types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class vendors(Base):
    __tablename__ = 'Vendor'

    no = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    primaryContactNo = Column('contact_code',CustomString)
    vendorPostingGroup = Column('vendor_posting_group',CustomString)
    paymentTermsCode = Column('payment_terms_code',CustomString)
    countryRegionCode = Column('country_code',CustomString)
    locationCode = Column('location_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    rfcNo = Column('rfc_code',CustomString)
    blocked = Column('blocked',CustomString)
    systemCreatedAt = Column('created_at', types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class salesmen(Base):
    __tablename__ = 'Salesperson'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    blocked = Column('blocked',types.Boolean)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class items(Base):
    __tablename__ = 'Item'

    no = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    baseUnitOfMeasure = Column('measure_unit',CustomString)
    type = Column('item_type',CustomString)
    inventoryPostingGroup = Column('inventory_posting_group',CustomString)
    itemCategoryCode = Column('item_category_code',CustomString)
    unitPrice = Column('unit_price',types.Float)
    unitCost = Column('unit_cost',types.Float)
    grossWeight = Column('gross_weight',types.Float)
    netWeight = Column('net_weight',types.Float)
    blocked = Column('blocked',types.Boolean)
    salesBlocked = Column('sales_blocked',types.Boolean)
    purchasingBlocked = Column('purchase_blocked',types.Boolean)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class customerLedgerEntries(Base):
    __tablename__ = 'CustomerLedger'

    entryNo = Column('entry_no',types.Integer,primary_key=True,autoincrement=False)
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
    appliesToExtDocNo = Column('apply_to_external_document',CustomString)
    closedByEntryNo = Column('closed_by_entry',types.Integer)
    open = Column('is_open',types.Boolean)
    reversed = Column('is_reversed',types.Boolean)
    reversedByEntryNo = Column('reversed_by_entry',types.Integer)
    reversedEntryNo = Column('reversed_entry',types.Integer)    
    systemCreatedAt = Column('created_at',types.DateTime) 
    systemModifiedAt = Column('modified_at',types.DateTime)



class vendorLedgerEntries(Base):
    __tablename__ = 'VendorLedger'

    entryNo = Column('entry_no',types.Integer,primary_key=True,autoincrement=False)
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
    externalDocumentNo = Column('external_document',CustomString)
    appliesToExtDocNo = Column('apply_to_external_document',CustomString)
    closedByEntryNo = Column('closed_by_entry',types.Integer)
    open = Column('is_open',types.Boolean)
    reversed = Column('is_reversed',types.Boolean)
    reversedByEntryNo = Column('reversed_by_entry')
    reversedEntryNo = Column('reversed_entry')    
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)



class salesInvoices(Base):
    __tablename__ = 'SalesInvoice'

    no = Column('document_no',types.String, primary_key=True)
    custLedgerEntryNo = Column('entry_no',types.Integer)
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
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class salesInvoiceLines(Base):
    __tablename__ = 'SalesInvoiceLine'

    documentNo = Column('document_no',types.String,primary_key=True)
    lineNo = Column('line_no',types.Integer,primary_key=True)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitPrice = Column('unit_price',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class salesCreditMemos(Base):
    __tablename__ = 'SalesCrMemo'

    no = Column('document_no',types.String, primary_key=True)
    custLedgerEntryNo = Column('entry_no',types.Integer)
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
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)

    
class salesCreditMemoLines(Base):
    __tablename__ = 'SalesCrMemoLine'

    documentNo = Column('document_no',types.String,primary_key=True)
    lineNo = Column('line_no',types.Integer,primary_key=True)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitPrice = Column('unit_price',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class purchaseInvoices(Base):
    __tablename__ = 'purchaseInvoice'

    no = Column('document_no',types.String, primary_key=True)
    vendorLedgerEntryNo = Column('entry_no',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    buyFromVendorNo = Column('vendor_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    orderNo = Column('order_no',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class purchaseCreditMemos(Base):
    __tablename__ = 'PurchaseCrMemo'

    no = Column('document_no',types.String, primary_key=True)
    vendorLedgerEntryNo = Column('entry_no',types.Integer)
    postingDate = Column('posting_date', types.Date)
    documentDate = Column('document_date',types.Date)
    buyFromVendorNo = Column('vendor_code',CustomString)
    paymentMethodCode = Column('payment_method_code',CustomString)
    currencyCode = Column('currency_code',CustomString)
    purchaserCode = Column('purchaser_code',CustomString)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    returnOrderNo = Column('return_order_no',CustomString)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)



class purchaseInvoiceLines(Base):
    __tablename__ = 'PurchaseInvoiceLine'

    documentNo = Column('document_no',types.String,primary_key=True)
    lineNo  = Column('line_no',types.Integer,primary_key=True)
    type = Column('item_type', CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitCost = Column('unit_cost',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)



class purchaseCreditMemoLines(Base):
    __tablename__ = 'PurchaseCrMemoLine'

    documentNo = Column('document_no',types.String,primary_key=True)
    lineNo  = Column('line_no',types.Integer,primary_key=True)
    type = Column('item_type',CustomString)
    no = Column('item_code',CustomString)
    quantity = Column('quantity',types.Integer)
    unitCost = Column('unit_cost',types.Float)
    lineDiscount = Column('discount_percentage',types.Float)
    lineDiscountAmount = Column('discount_amount',types.Float)
    amount = Column('amount',types.Float)
    amountIncludingVAT = Column('amount_with_vat',types.Float)
    systemCreatedAt = Column('created_at',types.DateTime)
    systemModifiedAt = Column('modified_at',types.DateTime)


class TablasSQL(Enum):

    currencies = 'Divisas'
    paymentTerms = 'Terminos de Pago'
    countries = 'Paises'
    shipmentMethods = 'Metodos de Entrega'
    priceGroups = 'Grupos de Precios Cliente'
    locations = 'Almacenes'
    paymentMethods = 'Metodos de Pago'
    itemCategories = 'Categorias de Producto'
    customerPostingGroups = 'Grupos de Cliente'
    inventoryPostingGroups = 'Grupos de Inventario'
    vendorPostingGroups = 'Grupos de Proveedor'
    exchangeRates = 'Tipos de Cambio'
    salesmen = 'Vendedores'
    items = 'Productos'
    customers = 'Clientes'
    vendors = 'Proveedores'
    customerLedgerEntries = 'Movimientos Clientes'
    vendorLedgerEntries = 'Movimientos Proveedores'
    salesInvoices = 'Facturas Venta'
    salesInvoiceLines = 'Lineas Facturas Venta'
    salesCreditMemos = 'Notas de Credito Venta'
    salesCreditMemoLines = 'Lineas Notas de Credito Venta'
    purchaseInvoices = 'Facturas Compra'
    purchaseInvoiceLines = 'Lineas Facturas Compra'
    purchaseCreditMemos = 'Notas de Credito Compra'
    purchaseCreditMemoLines = 'Lineas Notas de Credito Compra'
