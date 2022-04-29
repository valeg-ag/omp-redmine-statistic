## Grafana

### Grafana Preferences

Timezone: `Coordinated Universal Time, UTC`

### Dashboard Variables

name: `groupByPeriod`
values: `month, quarter, year`

### Queries For Grafana Panels

#### Fact Duration By Dev

```sql
SELECT
  spent_on_month as time,
  sum(hours) as value,
  d.name as metric
FROM 
    ( select date_trunc('$groupByPeriod', spent_on) as spent_on_month,
           sum(hours) as hours,
           user_id as user_id
      from time_entries 
      where auto_cherry_pick = 0
	  group by date_trunc('$groupByPeriod', spent_on), user_id
	) as time_entries_by_month
inner join developers d on(d.id = time_entries_by_month.user_id)
WHERE
  $__timeFilter(spent_on_month)
group by spent_on_month, user_id, d.name
  order by spent_on_month
```

#### Plan Duration By Dev

```sql
SELECT
  closed_on as time,
  sum(estimated_hours) as value,
  d.name as metric
FROM 
    ( select date_trunc('$groupByPeriod', closed_on) as closed_on,
           sum(estimated_hours) as estimated_hours,
           assigned_to_id as assigned_to_id
      from issues 
	  group by date_trunc('$groupByPeriod', closed_on), assigned_to_id
	) as issues_view
inner join developers d on(d.id = issues_view.assigned_to_id)
WHERE
  $__timeFilter(closed_on)
group by closed_on, assigned_to_id, d.name
  order by closed_on
```

#### Quantity of Improvements/Errors

##### Improvements

```sql
SELECT
  created_on as time,
  estimated_hours as hours_of_improvements
from
   (select date_trunc('$groupByPeriod', created_on) as created_on, sum(estimated_hours) as estimated_hours from issues
     where tracker_id = 2
       and project_id <> 1
     group by date_trunc('$groupByPeriod', created_on) ) issues_view
WHERE
  $__timeFilter(created_on)
  order by created_on
```

##### Errors

```sql
SELECT
  created_on as time,
  estimated_hours as hors_of_errors
from
   (select date_trunc('$groupByPeriod', created_on) as created_on, sum(estimated_hours) as estimated_hours from issues
     where tracker_id = 1
     group by date_trunc('$groupByPeriod', created_on) ) issues_view
WHERE
  $__timeFilter(created_on)
  order by created_on
```


#### Fact Dur In Selected Period

```sql
select NOW() as time_sec,
       hours as value,
       user_name as metric
  from (SELECT sum(t.hours) as hours,
               d.name as user_name
          from time_entries t
               inner join developers d on(d.id = t.user_id)
         WHERE t.auto_cherry_pick = 0
               and $__timeFilter(t.spent_on)
         group by d.name) fact_hourse_by_dev
order by hours desc
```

#### Plan Dur In Selected Period

```sql
select NOW() as time_sec,
       hours as value,
       user_name as metric
  from (SELECT sum(i.estimated_hours) as hours,
               d.name as user_name
          from issues i
               inner join developers d on(d.id = i.assigned_to_id)
         WHERE $__timeFilter(i.closed_on)
         group by d.name) plan_hours_by_dev
order by hours desc
```
