r = env['sale.report'].read_group(
    [('state', 'not in', ['draft', 'sent', 'cancel'])],
    ['price_subtotal:sum', 'product_uom_qty:sum'],
    ['product_id'], limit=3, orderby='price_subtotal DESC')
print('TOP_ITEMS:', r)
c = env['sale.report'].read_group(
    [('state', 'not in', ['draft', 'sent', 'cancel'])],
    ['price_subtotal:sum'], ['categ_id'], limit=2)
print('BY_CATEG:', c)
p = env['sale.report'].read_group(
    [('state', 'not in', ['draft', 'sent', 'cancel'])],
    ['price_subtotal:sum'], ['partner_id'], limit=2)
print('BY_PARTNER:', p)
