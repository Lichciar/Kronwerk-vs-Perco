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
Version = '0.1'

# Планирование разработки:
# ------------------------
# План работ на ver. 0.1:
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

# Не учитывать записи таблицы owner, в которой вместо поля фамилия/имя/отчество
# присутствуют записи none, РАЗОВЫЙ.
EmptyOwner = 1 #1 - true, 0 - false

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

# Делаем запрос в старую базу данных для таблицы owner. 
OwnerTables = OldDB.cursor()

SELECT = ("SELECT ow_id, ow_firstname, ow_middlename, ow_lastname, " +
         "ow_sdv_id, ow_ws_id FROM owner")

# Отключение строки с хотя бы одним пустым полем Ф.И.О.
if (EmptyOwner):
    SELECT = (SELECT + " WHERE ow_firstname IS NOT NULL AND " +
              "ow_middlename IS NOT NULL AND ow_lastname IS NOT NULL")

# Сортируем все по столбцу ow_id.
SELECT = (SELECT + " ORDER BY ow_id")
OwnerTables.execute(SELECT)

# Выводим на экран нужные колонки таблицы owner.
for (ow_id, ow_firstname, ow_middlename, ow_lastname, ow_sdv_id,
     ow_ws_id) in OwnerTables:
    print (Counter, ow_id, ow_lastname, ow_firstname, ow_middlename,
           ow_sdv_id, ow_ws_id)
    Counter = Counter + 1

# Закрываем старую базу данных.
OldDB.close()
