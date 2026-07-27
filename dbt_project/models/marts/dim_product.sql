{{ config(materialized='table') }}

with sales as (
    select * from {{ ref('stg_sales') }}
),

final as (
    select distinct
        -- Surrogate Key
        farm_fingerprint(item_id) as product_key,
        
        -- Attributes
        item_id,
        dept_id as department,
        cat_id as category
    from sales
)

select * from final
