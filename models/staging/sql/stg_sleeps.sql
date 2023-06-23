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
            cast(rating as real) rating,
            comment,
            snore,
            noise,
            cycles,
            deepsleep,
            cast(lenadjust as real) lenadjust,
            geo

        from sleeps

    )

select *
from stg_sleeps
