from fastapi import FastAPI

app = FastAPI(
    title="battleship",
    debug=True
    )

@app.get("/")
def read_root():
    return {"hello" : "world"}

