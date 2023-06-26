with

    {# import ctes #}
    tags as (select * from {{ ref('int_sleep_tags') }}),

    sleeps as (select * from {{ ref('int_sleeps_date_dim') }}),

    {# logical cte #}
    fnl_tag__count as (
        select sleeps.year, sleeps.month, tags.tags as tag, count(*) as count
        from sleeps
        left join tags on sleeps.id = tags.id
        where tag <> " "
        group by year, month, tag
    )

select *
from fnl_tag__count
