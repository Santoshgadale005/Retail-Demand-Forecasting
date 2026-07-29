{{ config(materialized='table') }}

with fct as (
    select * from {{ ref('fct_sales') }}
),

dim_product as (
    select * from {{ ref('dim_product') }}
),

dept_agg as (
    select
        p.department,
        sum(f.sales_qty) as total_units_sold,
        sum(f.sales_qty * f.sell_price) as total_revenue,
        avg(f.sell_price) as avg_selling_price
    from fct f
    join dim_product p on f.product_key = p.product_key
    group by 1
)

select * from dept_agg
