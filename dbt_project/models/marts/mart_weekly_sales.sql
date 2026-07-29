{{ config(materialized='table') }}

with fct as (
    select * from {{ ref('fct_sales') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

weekly_agg as (
    select
        d.year,
        d.week,
        sum(f.sales_qty) as total_units_sold,
        sum(f.sales_qty * f.sell_price) as total_revenue,
        avg(f.sell_price) as avg_selling_price
    from fct f
    join dim_date d on f.date_key = d.date_key
    group by 1, 2
)

select * from weekly_agg
