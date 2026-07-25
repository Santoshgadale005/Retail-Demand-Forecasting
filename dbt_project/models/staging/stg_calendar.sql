with source as (
    select * from {{ source('retail_forecasting', 'stg_calendar') }}
),

renamed as (
    select
        date as date_day,
        cast(wm_yr_wk as int64) as week_id,
        weekday,
        cast(wday as int64) as day_of_week_num,
        cast(month as int64) as month_num,
        cast(year as int64) as year_num,
        d as date_id,
        {{ clean_string('event_name_1') }} as event_name_1,
        {{ clean_string('event_type_1') }} as event_type_1,
        {{ clean_string('event_name_2') }} as event_name_2,
        {{ clean_string('event_type_2') }} as event_type_2,
        cast(snap_ca as int64) as snap_ca,
        cast(snap_tx as int64) as snap_tx,
        cast(snap_wi as int64) as snap_wi
    from source
)

select * from renamed
