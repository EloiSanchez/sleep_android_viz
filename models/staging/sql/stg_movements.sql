with

    {# Remove the low amount of duplicate measures that could appear #}
    movements as (
        select id, time, avg(value) as value
        from {{ source('raw', 'movements') }}
        group by id, time
    )

select *
from movements
