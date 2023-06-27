with

    {# import cte #}
    sleeps as (select id, tags from {{ ref("stg_sleeps") }}),

    {# recursive cte to split tags in rows #}
    split(id, tags, str) as (
        select id, '', tags || ','
        from sleeps

        union all

        select id, substr(str, 0, instr(str, ',')), substr(str, instr(str, ',') + 1)
        from split
        where str != ''
    ),

    {# final cte #}
    int_sleep_tags as (select id, tags from split where tags not in ("", " "))

select *
from int_sleep_tags
