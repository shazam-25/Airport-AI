from airport_ai.config import config
from airport_ai.app.builder import ApplicationBuilder

def main():
    builder = ApplicationBuilder(config)
    application = builder.build()
    try:
        application.run()
    except KeyboardInterrupt:
        application.stop()
    

if __name__ == "__main__":
    main()