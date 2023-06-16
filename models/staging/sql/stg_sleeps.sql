with
    sleeps as (select * from {{ source('raw', 'sleeps') }}),

    stg_sleeps as (

        {# Remove framerate columns, which is not used #}
        select
            id,
            tz,
            sleep_from,
            sleep_to,
            sched,
            hours,
            rating,
            comment,
            snore,
            noise,
            cycles,
            deepsleep,
            lenadjust,
            geo

        from sleeps

    )

select *
from stg_sleeps
