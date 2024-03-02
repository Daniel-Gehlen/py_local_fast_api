import uvicorn
from fastapi import FastAPI, Query, Header, HTTPException
import json
import os

app = FastAPI()

# Carregar chaves de acesso
api_keys_file = os.path.join("data", "api_keys.json")
with open(api_keys_file) as f:
    api_keys_data = json.load(f)
    api_keys = api_keys_data.get("api_keys", {})

# Carregar dados dos tweets
tweets_file = os.path.join("data", "tweets.json")
with open(tweets_file) as f:
    tweets_data = json.load(f)


# Rota para obter os últimos tweets de um usuário
@app.get("/tweets/{username}")
def read_tweets(
        username: str,
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        api_key: str = Header(None)
):
    if api_key not in api_keys:
        raise HTTPException(status_code=403, detail="Chave de acesso inválida")

    tweets = tweets_data.get(username, {}).get("tweets", [])
    tweets_slice = tweets[offset:offset + limit]

    return {"username": username, "tweets": tweets_slice}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
