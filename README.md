# README (short info about projects)
Repository with my personal projects

1) В первом проекте, связанном с E-commerce (https://github.com/RomanFeofanov/my_projects/blob/main/Project_1.ipynb), я загрузил три датафрейма с яндекс диска с помощью api в jupyter notebook, проанализировал данные с помощью библиотек pandas, numpy, matplotlib и seaborn, и определил, сколько у каждого из пользователей в среднем покупок в неделю (по месяцам). Также я провел когортный анализ пользователей и выявил когорту с максимальным retention rate на третий месяц. В заключении я провёл кластерный RFM анализ пользователей. В результате получил распределение пользователей по RFM-кластерам, необходимое для маркетологов.

2) Во втором проектре, связанном с введением новой механики оплаты услуг на сайте для тестовой группы (https://github.com/RomanFeofanov/my_projects/blob/main/Project_2.ipynb), я проанализировал результаты A/B–тестирования. Целью анализа было принятие решения о том, стоит ли запускать новую механику оплаты. Для анализа использовал Bootstrap, так как данные были распределены неравномерно и дисперсии двух групп были не равны, и критерий Хи-квадрат. Также составил несколько SQL-запросов, используя БД Clickhouse, для подсчета продуктовых метрик. 1 — запрос, который даст информацию о количестве усердных студентов за определенный период времени, 2 — запрос, который выгружает следующую информацию о группах пользователей: ARPU, ARPAU, CR в покупку. Реализовал функцию на Python, которая автоматически подгружает информацию из дополнительного файла в главный и пересчитывает метрики. Реализовал функцию, которая строит графики по получаемым метрикам.
