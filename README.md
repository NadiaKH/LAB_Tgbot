# LAB_Tgbot
Описание
========
С помощью бота можно группировать сообщения.

Commands
======
new
---
/new [group_name] - создает группу с именем group_name.

Пример, создали группу с именем recepies:
```telegram
/new recepies 
```

show
----
/show - присылает сообщением список всех групп

tail
----
/tail [group_name] [n] - выводит n последних сообщений из группы с именем group_name

Пример, выведет 5 последних сообщений из группы recepies:
```telegram
/tail recepies 5
```
