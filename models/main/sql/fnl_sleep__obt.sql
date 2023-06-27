with

    {# import ctes #}
    sleeps as (
        select
            id,
            year,
            month,
            week,
            day_of_week,
            day_of_month,
            day_of_year,
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
