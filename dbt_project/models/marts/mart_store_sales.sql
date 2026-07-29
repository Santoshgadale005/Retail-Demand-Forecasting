{{ config(materialized='table') }}

with fct as (
    select * from {{ ref('fct_sales') }}
),

dim_store as (
    select * from {{ ref('dim_store') }}
),

store_agg as (
    select
        s.store,
        s.state,
        sum(f.sales_qty) as total_units_sold,
        sum(f.sales_qty * f.sell_price) as total_revenue,
        avg(f.sell_price) as avg_selling_price
    from fct f
    join dim_store s on f.store_key = s.store_key
    group by 1, 2
)

select * from store_agg
