from datetime import datetime


def timestamp() -> str:
    """Retorna la fecha y hora actual en formato YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def fecha_actual() -> str:
    """Retorna la fecha actual en formato YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")