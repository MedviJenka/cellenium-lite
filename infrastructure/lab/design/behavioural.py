from dataclasses import dataclass
from abc import ABC, abstractmethod


class SubscriptionInterface(ABC):

    @abstractmethod
    def send_notification(self, channel_name: str, event: str) -> None:
        ...


@dataclass
class User(SubscriptionInterface):

    user_name: str

    def send_notification(self, channel_name: str, event: str) -> None:
        print(f'hello {self.user_name}, message from {channel_name}:{event}')


class Channel:

    def __init__(self, channel_name: str) -> None:
        self.channel_name = channel_name
        self.users_list = []

    def subscribe_user(self, new_user: User) -> None:
        self.users_list.append(new_user)

    def notify_all(self, event: str) -> None:
        for each_user in self.users_list:
            each_user.send_notification(self.channel_name, event)


if __name__ == '__main__':
    channel = Channel(channel_name='Jenia')
    channel.subscribe_user(new_user=User(user_name='1'))
    channel.subscribe_user(new_user=User(user_name='2'))
    channel.subscribe_user(new_user=User(user_name='3'))
    channel.notify_all(event='new video!')


# from dataclasses import dataclass
# from abc import ABC, abstractmethod
#
#
# class NotificationEngine(ABC):
#     @abstractmethod
#     def send_notification(self, channel_name: str, event: str) -> None:
#         ...
#
#
# @dataclass
# class YoutubeUser(NotificationEngine):
#
#     name: str
#
#     def send_notification(self, channel_name: str, event: str) -> str:
#         message = f'\nhello {self.name}, message from {channel_name}: {event}'
#         print(message)
#         return message
#
#
# class YoutubeChannel:
#
#     def __init__(self, channel_name: str) -> None:
#         self.channel_name = channel_name
#         self.subscribers_list = []
#
#     def add_subscriber(self, subscriber_name: object) -> None:
#         self.subscribers_list.append(subscriber_name)
#
#     def notify(self, event: str) -> list:
#         _list = []
#         for each_subscriber in self.subscribers_list:
#             _list.append(each_subscriber.send_notification(self.channel_name, event))
#         return _list
#
#
# def test() -> None:
#     channel = YoutubeChannel(channel_name='digital space')
#     channel.add_subscriber(YoutubeUser(name='1'))
#     channel.add_subscriber(YoutubeUser(name='2'))
#     channel.add_subscriber(YoutubeUser(name='3'))
#     outcome = channel.notify(event='new video has been released!')
#     for each in range(1, 4):
#         assert f'\nhello {each}, message from digital space: new video has been released!' in outcome
