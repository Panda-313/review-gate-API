from langchain_core.tools import tool


def build_send_message():
    @tool("send_message", description="""
    Wysyła wiadomość do klienta. 
    
    Wejście: tekst wiadomości, którą chcemy wysłać.
    Wyjście: potwierdzenie sukcesu wysłania.""")
    def send_message(message: str):
        print(f"WYSYŁAM WIADOMOŚĆ: {message}")
        return {"success": True, "message_sent": message}

    return send_message
