-- Ensures no sales records have a negative quantity
select *
from {{ ref('fct_sales') }}
where sales_qty < 0
