from typing import Optional, Tuple, Dict, Any
from .session_adapter import InstagramSessionAdapter
from ..utils import session_manager

async def login_with_password(username: str, password: str, proxy: Optional[str]) -> Tuple[InstagramSessionAdapter, Dict[str, Any]]:
    client = InstagramSessionAdapter(username=username, proxy=proxy)
    await client.login(username=username, password=password)
    session = await client.serialize()
    try:
        session_manager.save_session(username, session)
    except Exception as e:
        print(f"Erro ao salvar sessão: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
    return client, session

async def resume_session(username: str) -> InstagramSessionAdapter:
    saved = session_manager.load_session(username)
    if not saved:
        raise ValueError("Sessão não encontrada")
    client = InstagramSessionAdapter(username=username, proxy=saved.get("proxy"))
    await client.deserialize(saved)  # usa set_settings(dict)
    return client
