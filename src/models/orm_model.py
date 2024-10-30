from .base import Base
import sqlalchemy.types as types
from sqlalchemy import Column
from enum import Enum

class CustomString(types.TypeDecorator):
    """clase string personalizada para mapear 'empty strings' a None, que a su vez SQLAlchemy mapea a NUL."""

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


#subclases de la clase <Base>, representan las tablas de la base de datos.
#Con el proposito de simplificar, el nombre de las clases coincide con el nombre del endpoint de la API de BC.
#Asi mismo, los nombres de las columnas en cada clase, coinciden con los campos en la API de BC.
#Por lo tanto, aqui se estan mapeando los campos de la API con los nombres de las columnas en SQL.

class currencies(Base):
    __tablename__ = 'Currency'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)

class exchangeRates(Base):
    __tablename__ = 'ExchangeRate'

    startingDate = Column('starting_date',types.Date,primary_key=True)
    currencyCode = Column('currency_code',types.String,primary_key=True)
    relationalCurrencyCode = Column('relational_currency_code',types.String,primary_key=True)
    exchangeRateAmount = Column('amount',types.Float)

class paymentTerms(Base):
    __tablename__ = 'PaymentTerms'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)

class countries(Base):
    __tablename__ = 'Country'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)

class shipmentMethods(Base):
    __tablename__ = 'ShipmentMethod'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)


class priceGroups(Base):
    __tablename__ = 'CustomerPriceGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)

class locations(Base):
    __tablename__ = 'Location'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)


class paymentMethods(Base):
    __tablename__ = 'PaymentMethod'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)


class itemCategories(Base):
    __tablename__ = 'ItemCategory'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)
    hasChildren = Column('has_children',types.Boolean)
    parentCategory = Column('parent_category',CustomString)


class customerPostingGroups(Base):
    __tablename__ = 'CustomerPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)


class vendorPostingGroups(Base):
    __tablename__ = 'VendorPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)


class inventoryPostingGroups(Base):
    __tablename__ = 'InventoryPostingGroup'

    code = Column('code',types.String,primary_key=True)
    description = Column('name',CustomString)


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


class salesmen(Base):
    __tablename__ = 'Salesperson'

    code = Column('code',types.String,primary_key=True)
    name = Column('name',CustomString)
    blocked = Column('blocked',types.Boolean)


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


class TablesEnum(str,Enum) :
    """subclase de Enum que define una descripcion para cada modelo SQLALchemy.
    Cuando se ejecuta un 'flow' o 'deployment' en modo personalizado en el servidor de Prefect, 
    te permite escoger con un 'dropdown' que tablas actualizar, en base a los valores en este Enum."""

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
