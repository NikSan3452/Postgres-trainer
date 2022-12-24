if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=True, reload_dirs="/backend", host="0.0.0.0", port=8000
    )






