with

    sleeps as (select * from {{ ref('int_sleeps_date_dim') }}),

    wake_up_data as (
        select
            wake_day_of_week as day_of_week,
            avg(sleep_to) as sleep_to,
            avg(sleep_to - sched) as snooze,
            avg(sched) as alarm
        from sleeps
        group by day_of_week
    ),

    sleep_data as (
        select
            sleep_day_of_week as day_of_week,
            avg(sleep_from) as sleep_from,
            avg(snore) as snore,
            avg(deepsleep) as deepsleep,
            avg(cycles) as cycles,
            avg(hours) as hours,
            avg(corrected_hours) as corrected_hours
        from sleeps
        group by day_of_week
    ),

    fnl_sleep__weekly as (
        select
            wake_up_data.day_of_week,
            weekdays.short_name,
            weekdays.long_name,
            wake_up_data.sleep_to,
            wake_up_data.snooze,
            wake_up_data.alarm,
            sleep_data.sleep_from,
            sleep_data.snore,
            sleep_data.deepsleep,
            sleep_data.cycles,
            sleep_data.hours,
            sleep_data.corrected_hours
        from wake_up_data
        left join sleep_data on wake_up_data.day_of_week = sleep_data.day_of_week
        left join
            {{ ref('weekdays') }} as weekdays on weekdays.id = wake_up_data.day_of_week
    )

select *
from fnl_sleep__weekly
