import json, base64

def decode_jwt(token):
        try:
            payload_encoded = token.split(".")[1]
            padding = '=' * (-len(payload_encoded) % 4)  # corrige padding
            decoded_bytes = base64.urlsafe_b64decode(payload_encoded + padding)
            return json.loads(decoded_bytes)
        except Exception as e:
            print("Erro ao decodificar JWT:", e)
            return {}