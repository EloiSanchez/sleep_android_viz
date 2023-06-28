{% set time_cols = get_time_cols() %}

with

    {# import ctes #}
    sleeps as (select * from {{ ref("stg_sleeps") }}),

    {# final cte #}
    int_sleeps_date_dim_sql as (
        select
            sleeps.id,
            strftime('%Y', sleep_to, '-1 days') as sleep_year,
            strftime('%m', sleep_to, '-1 days') as sleep_month,
            strftime('%d', sleep_to, '-1 days') as sleep_day_of_month,
            strftime('%W', sleep_to, '-1 days') as sleep_week,
            strftime('%w', sleep_to, '-1 days') as sleep_day_of_week,
            strftime('%Y', sleep_to) as wake_year,
            strftime('%m', sleep_to) as wake_month,
            strftime('%d', sleep_to) as wake_day_of_month,
            strftime('%W', sleep_to) as wake_week,
            strftime('%w', sleep_to) as wake_day_of_week,
            {%- for time_col in time_cols %}
                case
                    {# when cast(strftime('%H', {{ time_col }}) as real) < 12 #}
                    when cast(strftime('%H', {{ time_col }}) as real) > 18
                    then
                        {# cast(strftime('%H', {{ time_col }}) + 24 as real) #}
                        cast(strftime('%H', {{ time_col }}) - 24 as real)
                        + cast(strftime('%M', {{ time_col }}) as real) / 60
                    else
                        cast(strftime('%H', {{ time_col }}) as real)
                        + cast(strftime('%M', {{ time_col }}) as real) / 60
                end as {{ time_col }},
            {%- endfor %}
            hours,
            lenadjust,
            hours + (lenadjust / 60) as corrected_hours,
            rating,
            snore,
            noise,
            cycles,
            deepsleep,
            geo
        from sleeps
    )

select *
from int_sleeps_date_dim_sql
