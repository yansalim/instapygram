from typing import Any, Dict, List, Optional
import tempfile
import os
from instagram_private_api import Client, ClientLoginError


class InstagramSessionAdapter:
    def __init__(self, username: str, proxy: Optional[str] = None) -> None:
        self.username = username
        self.proxy = proxy
        # instagram_private_api Client requer username/password no login
        self.client: Optional[Client] = None

    # Métodos síncronos, mas mantendo a interface dos serviços
    async def login(self, username: str, password: str) -> None:
        # Inicializa client com login
        self.client = Client(username, password, proxy=self.proxy, auto_patch=True)

    async def serialize(self) -> Dict[str, Any]:
        # instagram_private_api settings podem conter bytes, convertemos para dict serializável
        settings = self.client.settings
        # Converter settings para dict serializável
        serializable_settings = {}
        for key, value in settings.items():
            if isinstance(value, bytes):
                serializable_settings[key] = value.hex()
            else:
                serializable_settings[key] = value
        return {"username": self.username, "proxy": self.proxy or None, "settings": serializable_settings}

    async def deserialize(self, state: Dict[str, Any]) -> None:
        self.proxy = state.get("proxy")
        settings = state.get("settings")
        # Recria client usando settings (evitar relogin)
        if settings:
            # Converter de volta bytes se necessário
            deserialized_settings = {}
            for key, value in settings.items():
                if isinstance(value, str) and len(value) % 2 == 0:
                    try:
                        deserialized_settings[key] = bytes.fromhex(value)
                    except ValueError:
                        deserialized_settings[key] = value
                else:
                    deserialized_settings[key] = value
            self.client = Client(self.username, "", settings=deserialized_settings, proxy=self.proxy, auto_patch=True)
        else:
            raise ValueError("Settings ausentes na sessão")

    async def current_user(self) -> Dict[str, Any]:
        user = self.client.username_info(self.username)["user"]
        return {
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "profile_pic_url": user.get("profile_pic_url"),
        }

    async def publish_photo(self, file_bytes: bytes, caption: Optional[str] = None) -> Dict[str, Any]:
        media = self.client.post_photo(photo_data=file_bytes, caption=caption or "")
        return {"id": media.get("media", {}).get("id"), "caption": caption or ""}

    async def publish_story_photo(self, file_bytes: bytes) -> Dict[str, Any]:
        res = self.client.post_photo_story(photo_data=file_bytes)
        return {"id": res.get("reel", {}).get("id")}

    async def send_text_dm(self, to_username: str, message: str) -> None:
        uid = self.client.username_info(to_username)["user"]["pk"]
        # Usar o método correto da API para enviar DM
        # Baseado na documentação, vou usar uma abordagem diferente
        # Primeiro vou verificar se há métodos disponíveis
        try:
            # Tentar usar o método correto da API
            self.client.direct_message(text=message, user_ids=[uid])
        except AttributeError:
            # Se não existir, tentar uma abordagem alternativa
            raise NotImplementedError("Método de envio de DM não implementado na versão atual da API")

    async def send_photo_dm_from_bytes(self, to_username: str, image_bytes: bytes) -> None:
        uid = self.client.username_info(to_username)["user"]["pk"]
        # Salvar arquivo temporário e enviar via método correto
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as fp:
                data = fp.read()
            # Tentar usar o método correto da API
            try:
                self.client.direct_message(photo_data=data, user_ids=[uid])
            except AttributeError:
                raise NotImplementedError("Método de envio de foto por DM não implementado na versão atual da API")
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    async def inbox(self) -> list:
        try:
            threads = self.client.direct_inbox()["inbox"]["threads"]
        except AttributeError:
            # Se não existir, tentar uma abordagem alternativa
            raise NotImplementedError("Método de inbox não implementado na versão atual da API")
        
        simplified = []
        for t in threads:
            simplified.append({
                "thread_id": t.get("thread_id"),
                "thread_title": t.get("thread_title"),
                "users": [{
                    "username": u.get("username"),
                    "full_name": u.get("full_name"),
                    "profile_pic_url": u.get("profile_pic_url"),
                } for u in t.get("users", [])],
                "last_message": (t.get("last_permanent_item") or {}).get("text"),
                "last_message_timestamp": (t.get("last_permanent_item") or {}).get("timestamp"),
            })
        return simplified

    async def thread_messages(self, thread_id: str) -> Dict[str, Any]:
        try:
            res = self.client.direct_thread(thread_id)
        except AttributeError:
            # Se não existir, tentar uma abordagem alternativa
            raise NotImplementedError("Método de thread_messages não implementado na versão atual da API")
        
        items = res.get("items", [])
        return {"thread_id": thread_id, "messages": items}

    async def user_info(self, target_username: str) -> Dict[str, Any]:
        info = self.client.username_info(target_username)["user"]
        return {
            "pk": info.get("pk"),
            "username": info.get("username"),
            "full_name": info.get("full_name"),
            "biography": info.get("biography"),
            "follower_count": info.get("follower_count"),
            "following_count": info.get("following_count"),
            "media_count": info.get("media_count"),
            "is_private": info.get("is_private"),
            "profile_pic_url": info.get("profile_pic_url"),
        }

    async def user_stories(self, target_username: str) -> List[Dict[str, Any]]:
        uid = self.client.username_info(target_username)["user"]["pk"]
        stories = self.client.reels_feed(reel_ids=[uid])["reels"].get(str(uid), {}).get("items", [])
        result: List[Dict[str, Any]] = []
        for s in stories:
            media_type = "photo" if s.get("media_type") == 1 else "video"
            media_url = None
            if media_type == "photo":
                candidates = (((s.get("image_versions2") or {}).get("candidates")) or [])
                media_url = candidates[0]["url"] if candidates else None
            else:
                versions = s.get("video_versions") or []
                media_url = versions[0]["url"] if versions else None
            result.append({
                "username": target_username,
                "media_type": media_type,
                "taken_at": s.get("taken_at")
                ,
                "media_url": media_url,
            })
        return result

    async def change_profile_picture(self, file_bytes: bytes) -> None:
        self.client.profile_change_picture(photo_data=file_bytes)

    async def edit_bio(self, bio: str) -> None:
        self.client.set_account_private() if False else None
        # Editar bio requer form completo — aqui enviamos somente biography
        self.client.current_user()  # ensure session
        self.client.set_biography(biography=bio)
