import base64

def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode()).decode()
