import asyncio
from abc import ABC, abstractmethod
from typing import Union, List, IO, Dict

from khl import Context, User, MessageTypes, PublicTextChannel, Role, Guild, GuildMuteTypes, ChannelTypes, PublicChannel
from khl.channel import ChannelPermission, Channel, PrivateChannel
from khl.guild import ChannelCategory


class SyncContext:

    def __init__(self, context: Context) -> None:
        self._channel = context.channel
        self._guild = context.guild

    @property
    def channel(self):
        if isinstance(self._channel, PublicTextChannel):
            return SyncPublicTextChannel(self._channel)
        elif isinstance(self._channel, PrivateChannel):
            return SyncPrivateChannel(self._channel)

    @property
    def guild(self):
        return SyncGuild(self._guild)


class SyncGuild(Guild):

    def __init__(self, guild: Guild):
        kwargs = guild.__dict__
        kwargs['channels'] = kwargs['_channels']
        kwargs['roles'] = kwargs['_roles']
        kwargs['_lazy_loaded_'] = kwargs['_loaded']
        super().__init__(**kwargs)
        self._loop = asyncio.get_event_loop()
        self._guild = guild

    def fetch_channel_category_list(self, force_update: bool = True) -> List[ChannelCategory]:
        return self._loop.run_until_complete(self._guild.fetch_channel_category_list(force_update))

    def fetch_channel_list(self, force_update: bool = True) -> List[PublicChannel]:
        return self._loop.run_until_complete(self._guild.fetch_channel_list(force_update))

    def list_user(self, channel: Channel) -> List[User]:
        return self._loop.run_until_complete(self._guild.list_user(channel))

    def fetch_user(self, user_id: str) -> User:
        return self._loop.run_until_complete(self._guild.fetch_user(user_id))

    def set_user_nickname(self, user: User, new_nickname: str):
        return self._loop.run_until_complete(self._guild.set_user_nickname(user, new_nickname))

    def fetch_roles(self, force_update: bool = True) -> List[Role]:
        return self._loop.run_until_complete(self._guild.fetch_roles(force_update))

    def create_role(self, role_name: str) -> Role:
        return self._loop.run_until_complete(self._guild.create_role(role_name))

    def update_role(self, new_role: Role) -> Role:
        return self._loop.run_until_complete(self._guild.update_role(new_role))

    def delete_role(self, role_id: int):
        self._loop.run_until_complete(self._guild.delete_role(role_id))

    def grant_role(self, user: User, role: Union[Role, str]):
        self._loop.run_until_complete(self._guild.grant_role(user, role))

    def revoke_role(self, user: User, role: Union[Role, str]):
        self._loop.run_until_complete(self._guild.revoke_role(user, role))

    def create_channel(self, name: str, type: ChannelTypes = None, category: Union[str, ChannelCategory] = None,
                       limit_amount: int = None, voice_quality: int = None):
        self._loop.run_until_complete(self._guild.create_channel(name, type, category, limit_amount, voice_quality))

    def delete_channel(self, channel: Channel):
        self._loop.run_until_complete(self._guild.delete_channel(channel))

    def kickout(self, user: Union[User, str]):
        self._loop.run_until_complete(self._guild.kickout(user))

    def leave(self):
        self._loop.run_until_complete(self._guild.leave())

    def get_mute_list(self, return_type: str = 'detail'):
        self._loop.run_until_complete(self._guild.get_mute_list(return_type))

    def create_mute(self, user: Union[User, str], type: GuildMuteTypes):
        self._loop.run_until_complete(self._guild.create_mute(user, type))

    def delete_mute(self, user: Union[User, str], type: GuildMuteTypes):
        self._loop.run_until_complete(self._guild.delete_mute(user, type))

    def fetch_emoji_list(self) -> List[Dict]:
        return self._loop.run_until_complete(self._guild.fetch_emoji_list())

    def create_emoji(self, emoji: Union[IO, str], *, name: str = None):
        self._loop.run_until_complete(self._guild.create_emoji(emoji, name=name))

    def update_emoji(self, id: str, *, name: str = None):
        self._loop.run_until_complete(self._guild.update_emoji(id, name=name))

    def delete_emoji(self, id: str):
        self._loop.run_until_complete(self._guild.delete_emoji(id))


class SyncChannel(Channel, ABC):

    @abstractmethod
    def send(self, content: Union[str, List], *, type: MessageTypes = None, **kwargs):
        ...


class SyncPublicTextChannel(PublicTextChannel, SyncChannel):

    def __init__(self, channel: PublicTextChannel):
        kwargs = channel.__dict__
        kwargs['_gate_'] = kwargs['gate']
        super().__init__(**kwargs)
        self._channel = channel
        self._loop = asyncio.get_event_loop()

    def send(self, content: Union[str, List], *, type: MessageTypes = None, temp_target_id: str = '', **kwargs):
        self._loop.run_until_complete(self._channel.send(content, type=type, temp_target_id=temp_target_id, **kwargs))

    def fetch_permission(self, force_update: bool = True) -> ChannelPermission:
        return self._loop.run_until_complete(self._channel.fetch_permission(force_update))

    def create_permission(self, target: Union[User, Role]):
        self._loop.run_until_complete(self._channel.create_permission(target))

    def update_permission(self, target: Union[User, Role], allow: int = 0, deny: int = 0) -> Role:
        return self._loop.run_until_complete(self._channel.update_permission(target, allow, deny))

    def delete_permission(self, target: Union[User, Role]):
        self._loop.run_until_complete(self._channel.delete_permission(target))


class SyncPrivateChannel(PrivateChannel, SyncChannel):

    def __init__(self, channel: PrivateChannel):
        super().__init__(**channel.__dict__)
        self._loop = asyncio.get_event_loop()
        self._channel = channel

    def send(self, content: Union[str, List], *, type: MessageTypes = None, **kwargs):
        self._loop.run_until_complete(self._channel.send(content, type=type, **kwargs))


class SyncUser(User):

    def __init__(self, user: User):
        super().__init__(**user.__dict__)
        self._user = user
        self._loop = asyncio.get_event_loop()

    def send(self, content: Union[str, List], *, type: MessageTypes = None, **kwargs):
        self._loop.run_until_complete(self._user.send(content, type=type, **kwargs))
