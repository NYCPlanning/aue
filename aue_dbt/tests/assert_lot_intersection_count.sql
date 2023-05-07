-- Lot intersections are pairs of tax lots, so the number of intersection records
-- should always be a function of the number of tax lots
-- intersections_count = tax_lots_count * (tax_lots_count - 1).
-- Therefore return records where this isn't true to make the test fail

with tax_lots_count as (
    select
        (count(*) * count(*))
        - count(*) as expected_intersections_count
    from {{ ref('stg_dcp__restricted_lots' ) }}
),


intersections_count as (
    select count(*) as intersections_count
    from {{ ref('buffered_lot_intersections' ) }}
)

select
    tax_lots_count.*,
    intersections_count.*
from tax_lots_count
full outer join intersections_count
    on
        tax_lots_count.expected_intersections_count
        = intersections_count.intersections_count
where
    tax_lots_count.expected_intersections_count is null
    or intersections_count.intersections_count is null
