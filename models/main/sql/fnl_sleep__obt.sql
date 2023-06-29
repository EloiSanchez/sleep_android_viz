with

    {# import ctes #}
    sleeps as (
        select
            id,
            sleep_year,
            sleep_month,
            sleep_week,
            sleep_day_of_week,
            sleep_day_of_month,
            sleep_from,
            sleep_to,
            sched,
            hours,
            lenadjust,
            corrected_hours,
            rating,
            snore,
            noise,
            cycles,
            deepsleep,
            geo
        from {{ ref('int_sleeps_date_dim') }}
    )

select *
from sleeps
