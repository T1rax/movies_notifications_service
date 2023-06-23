# Movies Notifications Service
Online cinema service for notifications. Contains admin panel, api and senders

## Contributors

- Vladimir Nikishov - T1rax - @nikishov.va
- Victoria Axentii - wiky-avis - @wikyavis
- Oleg Podryadov - opodryadov - @oleg_podryadov

# Основные компоненты
## notifications_api
Входной компонент системы. Принимает сообщения для отправки и регистрирует их в очереди.
Производит минимальную валидацию и возвращает сгенерированный delivery_id.
Основные пользователи:
- Админка - разовые отправки инициированные из интерфейса
- Внутренние сервисы - регулярные или триггерные отправки. Логика сбора данных настраивается внутри сервисов и в нужный момент они сами дергают апишку
Также может возвращать статус зарегистрированной отправки и обрабатывать отписки пользователей от коммуникаций.
## admin_panel
Админка, в которую ходят маркетологи.
Умеет делать разовые отправки - маркетолог в интерфейсе выбирает id шаблона и загружает CSV с получателями и подставляемыми параметрами.
Также в админке создаются шаблоны коммуникаций.
Не хранит собственные данные и работает как интерфейс для API внутренних сервисов.
## templates_service
CRUD сервис для работы с шаблонами. 
Также может его "срендерить" - на вход получает id шаблона и параметры и отдает готовый заполненный текст
## notifications_controllers
Внутренние консьюмеры и крон-воркеры. Не имеют внешнего API, работают на данных из очередей и БД.
### notifications_enricher_consumer
Читает сообщения, которые пишет notifications_api и обогощает недостающими данными.
Основные этапы работы:
- Догружает из auth таймзону пользователя и имейл при необходимости. Для этого был доработан сервис auth - https://github.com/wiky-avis/Auth_sprint_1/pull/90. Добавлены поля в модель и новая "сервисная" ручка
- Проверяет не отписан ли пользователь
- Роутит быстрые отправки сразу консьюмерам и обычные кладет в общую очередь
### delivery_trigger_starter
Читает из общей очереди. В нее попадают отправки с типом "не ночью". Читает пачки пользователей и проверяет по таймзоне можно ли им отправить сейчас коммуникацию. Если можно, то ставит в очередь для отправки.
### email_consumer
Читает из очереди для отправки. Сюда попадают уже обработанные и отфильтрованные коммуникации. 
Рендерит шаблон в сервисе templates и передает Email провайдеру на отправку.

# Как запустить проект
- В корневой папке проекта нужно создать .env файл. Наполняется содержимым файлов .env.example из всех основных компонентов (перечислены выше)
- Запускаем команду `make up-local` или `make up-local-d` для detach режима

# Дополнительная Информация
Пришлось удалить github actions. Они стояли большую часть проекта, но ближе к концу закончился лимит и он обновится только первого июля.
Через мейкфайл можно повторить логику их работы при необходимости.

# Схемы в C4 нотации
Их можно найти в папке docs.
