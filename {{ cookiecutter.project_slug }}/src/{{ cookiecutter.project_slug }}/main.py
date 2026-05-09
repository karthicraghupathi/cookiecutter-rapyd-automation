from .settings import PROJECT_NAME, logger


def main() -> None:
    logger.info("Running %s", PROJECT_NAME)


if __name__ == "__main__":
    main()
