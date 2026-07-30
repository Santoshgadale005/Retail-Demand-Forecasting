-- Ensures no sales records have a negative selling price
select *
from {{ ref('fct_sales') }}
where sell_price < 0
