from typing import Any, Dict, List, Optional
import tempfile
import os
from instagrapi import Client
from instagrapi.types import DirectMessage, DirectThread


class InstagramSessionAdapter:
    def __init__(self, username: str, proxy: Optional[str] = None) -> None:
        self.username = username
        self.proxy = proxy
        self.client: Optional[Client] = None

    async def login(self, username: str, password: str) -> None:
        # Inicializa client com login
        self.client = Client()
        if self.proxy:
            self.client.set_proxy(self.proxy)
        self.client.login(username, password)

    async def serialize(self) -> Dict[str, Any]:
        # instagrapi settings são serializáveis
        settings = self.client.get_settings()
        return {
            "username": self.username, 
            "proxy": self.proxy or None, 
            "settings": settings
        }

    async def deserialize(self, state: Dict[str, Any]) -> None:
        self.proxy = state.get("proxy")
        settings = state.get("settings")
        
        if settings:
            self.client = Client()
            if self.proxy:
                self.client.set_proxy(self.proxy)
            self.client.load_settings(settings)
        else:
            raise ValueError("Settings ausentes na sessão")

    async def current_user(self) -> Dict[str, Any]:
        user = self.client.account_info()
        return {
            "username": user.username,
            "full_name": user.full_name,
            "profile_pic_url": user.profile_pic_url,
        }

    async def publish_photo(self, file_bytes: bytes, caption: Optional[str] = None) -> Dict[str, Any]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        try:
            media = self.client.photo_upload(tmp_path, caption=caption or "")
            return {"id": media.id, "caption": caption or ""}
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    async def publish_story_photo(self, file_bytes: bytes) -> Dict[str, Any]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        try:
            story = self.client.photo_upload_to_story(tmp_path)
            return {"id": story.id}
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    async def send_text_dm(self, to_username: str, message: str) -> None:
        # Obter user_id do username
        user_id = self.client.user_id_from_username(to_username)
        
        # Criar thread e enviar mensagem
        thread = self.client.direct_thread([user_id])
        thread.direct_message(message)

    async def send_photo_dm_from_bytes(self, to_username: str, image_bytes: bytes) -> None:
        # Obter user_id do username
        user_id = self.client.user_id_from_username(to_username)
        
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        
        try:
            # Criar thread e enviar foto
            thread = self.client.direct_thread([user_id])
            thread.direct_media(tmp_path)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    async def inbox(self) -> list:
        # Obter inbox de DMs
        threads = self.client.direct_threads()
        
        simplified = []
        for thread in threads:
            users = []
            for user in thread.users:
                users.append({
                    "username": user.username,
                    "full_name": user.full_name,
                    "profile_pic_url": user.profile_pic_url,
                })
            
            last_message = None
            last_message_timestamp = None
            if thread.messages:
                last_msg = thread.messages[-1]
                last_message = last_msg.text
                last_message_timestamp = last_msg.timestamp
            
            simplified.append({
                "thread_id": thread.id,
                "thread_title": thread.title,
                "users": users,
                "last_message": last_message,
                "last_message_timestamp": last_message_timestamp,
            })
        
        return simplified

    async def thread_messages(self, thread_id: str) -> Dict[str, Any]:
        # Obter mensagens de uma thread específica
        thread = self.client.direct_thread(thread_id)
        messages = []
        
        for msg in thread.messages:
            messages.append({
                "id": msg.id,
                "text": msg.text,
                "timestamp": msg.timestamp,
                "user_id": msg.user_id,
                "media": msg.media if hasattr(msg, 'media') else None,
            })
        
        return {"thread_id": thread_id, "messages": messages}

    async def user_info(self, target_username: str) -> Dict[str, Any]:
        user = self.client.user_info_by_username(target_username)
        return {
            "pk": user.pk,
            "username": user.username,
            "full_name": user.full_name,
            "biography": user.biography,
            "follower_count": user.follower_count,
            "following_count": user.following_count,
            "media_count": user.media_count,
            "is_private": user.is_private,
            "profile_pic_url": user.profile_pic_url,
        }

    async def user_stories(self, target_username: str) -> List[Dict[str, Any]]:
        user_id = self.client.user_id_from_username(target_username)
        stories = self.client.user_stories(user_id)
        
        result = []
        for story in stories:
            media_type = "photo" if story.media_type == 1 else "video"
            result.append({
                "username": target_username,
                "media_type": media_type,
                "taken_at": story.taken_at,
                "media_url": story.thumbnail_url,
            })
        
        return result

    async def change_profile_picture(self, file_bytes: bytes) -> None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        try:
            self.client.account_change_picture(tmp_path)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    async def edit_bio(self, bio: str) -> None:
        self.client.account_edit(biography=bio)
