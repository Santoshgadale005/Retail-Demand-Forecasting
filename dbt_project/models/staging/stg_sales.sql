with source as (
    select * from {{ source('retail_forecasting', 'stg_sales') }}
),

renamed as (
    select
        id as sales_id,
        item_id,
        dept_id,
        cat_id,
        store_id,
        state_id,
        -- Retaining the wide columns for unpivoting later, or if BigQuery's UNPIVOT is used in intermediate
        * except(id, item_id, dept_id, cat_id, store_id, state_id)
    from source
)

select * from renamed
