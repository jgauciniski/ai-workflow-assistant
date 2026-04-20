import time

def retry(func, label: str, retries: int = 3, delay: float = 0.5):
    """
    Retry a function if it raises an exception.
    """
    for attempt in range(retries):
        try:
            print(f"[{label}] Attempt {attempt + 1}")
            return func()

        except Exception as e:
            print(f"Failed: {e}") 

            if attempt == retries - 1:
                raise

            time.sleep(delay)