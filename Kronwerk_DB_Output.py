#!/usr/bin/env python3

# ---------------------------- 72 символа ------------------------------
# ---------------------------- 79 символов ------------------------------------

"""Kronwwerk_DB_Output:

Выборка данных: Ф.И.О, подразделение, организация, фотография, номер карты,
дата окончания действия карты, группа доступа, зоны доступа; из базы данных
Firebird v.1.5.6, используемой для работы старой СКУД 2010 года 'Кронверк'.
Начало работы над скриптом: 19 мая 2017 г. 14:05.
Обновление скрипта: в процессе"""

# Версия скрипта.
Version = '0.2'

# Планирование разработки:
# ------------------------
# план работ на ver. Y.X:
# 1. Добавить выборку из таблиц WORKSITE, SUBDIVISIOS.
# 2. Добавить выборку из таблицы OWNERPHOTO.
# 3. добавить выборку из таблиц AGRIGHTS, AGROUPS.
#
# План работ на ver. 0.2:
# 1. Из таблицы CARD вывести нужные столбцы на экран.
#
# Введены изменения в ver. 0.1:
# 1. Сделать вывод приветствия.
# 2. Установить стабильное соединение с базой данных.
# 3. Из таблицы OWNER вывести нужные столбцы на экран.

# Подключаем модуль работы с базой данных Firebird.
import firebirdsql 

# Перечень переменых.
# -------------------
# Старая база данных:
# -------------------
# Сервер со старой базой данных.
OFBServer = 'localhost'
# Путь к старой безе данных.
OFBPath = '/var/lib/firebird/2.5/data/IBNET.GDB'
# Администратор старой базы данных.
OFBUser = 'sysdba'
# Пароль к учетной записи администратора старой базы данных.
OFBPassword = 'c38c9f81'

# Не учитывать записи таблицы OWNER, в которой вместо поля фамилия/имя/отчество
# присутствуют записи "none" (1 - true, 0 - false).
EmptyOwner = 1

# Убираем записи таблицы CARDS, в которой отсутствует время окончания действия
# карты, либо срок действия истёк (1 - true, 0 - false).
DeadCard = 1

# Счётчик (временная переменная).
Counter = 1

# Вывод приветствия.
print ('Скрипт Kronwerk_DB_Output ver.' + Version)
print ('Реализован на языке программирования Python v.3.4.2')
print ('\n')

# Подключаемся к базе данных.
OldDB = firebirdsql.connect(dsn = OFBServer + ':' + OFBPath,
                            user = OFBUser,
                            password = OFBPassword)

# Делаем запрос в старую базу данных для таблицы OWNER. 
OwnerTable = OldDB.cursor()

SELECT = ("SELECT OW_ID, OW_FIRSTNAME, OW_MIDDLENAME, OW_LASTNAME, " +
         "OW_SDV_ID, OW_WS_ID FROM OWNER")

# Отключение строки с хотя бы одним пустым полем Ф.И.О.
if (EmptyOwner):
    SELECT = (SELECT + " WHERE OW_FIRSTNAME IS NOT NULL AND " +
              "OW_MIDDLENAME IS NOT NULL AND OW_LASTNAME IS NOT NULL")

# Сортируем все по столбцу OW_ID.
SELECT = (SELECT + " ORDER BY OW_ID")
OwnerTable.execute(SELECT)

# Выводим на экран нужные колонки таблицы OWNER.
for (ow_id, ow_firstname, ow_middlename, ow_lastname, ow_sdv_id,
     ow_ws_id) in OwnerTable:

    # До следующей версии отключем вывод OW_SDV_ID и OW_WS_ID.
    OUTPUT = (str(Counter) + " " + str(ow_id) + " " + ow_lastname +
               " " + ow_firstname + " " + ow_middlename)
 
    # Подготавливаем запрос в старую базу данных для таблицы CADRS.
    CardsTable = OldDB.cursor()
    SELECT = ("SELECT CA_OW_ID, CA_AG_ID, CA_DEADLINE " +
              "FROM CARDS")
    
    # Смотрим информацию по CA_OW_ID, он же OW_ID таблицы OWNER.
    SELECT = (SELECT + " WHERE CA_OW_ID = " + str(ow_id)) 
    CardsTable.execute(SELECT)
   
    # Добавляем в запись CA_AG_ID и CA_DEADLINE.
    for (ca_ow_id, ca_ag_id, ca_deadline) in  CardsTable:
        pass

    # Убираем записи карты которых не имеют срока давности.
    CardValid = 1
    if (DeadCard):
        CardValid = 0
        if ((ca_deadline) and (int(str(ca_deadline)[0:4]) >= 2016)):
            CardValid = 1
    
    # Выводим запись на экран.
    if (CardValid):
        # До следующей версии отключаем вывод OW_SDV_ID и OW_WS_ID.
        OUTPUT = (str(Counter) + " " + str(ow_id) + " " +
                  ow_lastname + " " + ow_firstname + " " +
                  ow_middlename + " " + str(ca_ag_id) + " " +
                  str(ca_deadline))
        print (OUTPUT)

        # Производим итерацию счётчика выведенных записей.
        Counter = Counter + 1

# Закрываем старую базу данных.
OldDB.close()
