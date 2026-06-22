# Oracle NoSQL дел

## Инсталација

Oracle NoSQL Database е инсталирана локално со Docker container, користејќи Oracle NoSQL Community Edition KVLite. Базата е достапна преку endpoint:

`http://localhost:8080`

За пристап до базата е користен Python SDK пакетот `borneo`.

## Модел на податоци

Податоците од Yelp dataset се зачувани во key-value формат во табела `kv_store`.

Табелата има две главни полиња:

- `k` – клуч
- `v` – JSON вредност

## Примери за клучеви

- `business:{business_id}`
- `user:{user_id}`
- `review:{review_id}`
- `business_reviews:{business_id}`
- `user_reviews:{user_id}`
- `stats:business:{business_id}`
- `city_category:Philadelphia:Restaurants`

## Нивоа на агрегација

Прво ниво:
- Секој business, user и review се чува како посебен key-value запис.

Второ ниво:
- Се креираат денормализирани и агрегирани клучеви за побрз пристап, како:
  - сите reviews за business
  - сите reviews од user
  - статистика за business
  - restaurants по град и категорија

## Query сценарија

1. Пребарување business по ID
2. Пребарување user по ID
3. Пребарување review по ID
4. Сите reviews за даден business
5. Статистика за business
6. Restaurants во Philadelphia
7. Performance мерење на key-value пристапи

## Ограничувања

Oracle NoSQL како key-value модел не е наменета за ad-hoc пребарување како SQL JOIN. Затоа однапред се креираат дополнителни клучеви и агрегирани записи.