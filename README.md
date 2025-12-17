# Прошивка коробки связи команды SPbUnited

## Подготовка Raspberry Pi

### Имя пользователя и пароль

- login: `ssl`
- password: `1`

### Включение SSH

1. Открыть терминал
2. Ввести команду `sudo raspi-config`
3. Выбрать пункт `Interfacing Options`
4. Выбрать пункт `SSH`
5. Подтвердить включение SSH
6. Закрыть утилиту

Теперь можно подключиться к Raspberry Pi через SSH

### Настройка статического IP

1. Открыть терминал
2. Открыть `sudo nmtui` -> `Edit a connection` -> `Wired connection 1` -> `Edit...`
3. Изменить `IPv4 CONFIGURATION`: с `<Automatic>` на `<Manual>`
4. Открыв подробные настроки добавить необходимый IP адрес в поле `Addresses`, например: `10.0.120.220/24`
5. Изменить `IPv6 CONFIGURATION`: с `<Automatic>` на `<Disabled>`
6. Сохранить изменения и выйти из утилиты
7. Выполнить `sudo systemctl restart NetworkManager`
8. (Опционально) Выполнить `sudo reboot`

### Клонирование репозитория



## Запуск

```
./start.py
```
