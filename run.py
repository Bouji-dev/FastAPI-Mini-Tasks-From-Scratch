# run.py
import uvicorn

if __name__ == "__main__":
    # اجرای اپلیکیشن 'app' که در ماژول 'db' تعریف شده است.
    uvicorn.run(
        "db:app", # نام ماژول: نام متغیر FastAPI
        host="0.0.0.0",
        port=11111,
        reload=True,
        forwarded_allow_ips="*",
    )