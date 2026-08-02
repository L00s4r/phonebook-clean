from functools import lru_cache
import time

@lru_cache(maxsize=None)  # Неограниченный размер кэша
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

def test_performance():
    n = 35
    
    # Замеряем время с кэшированием
    start = time.time()
    result = fibonacci_cached(n)
    elapsed = time.time() - start
    print(f"Результат: {result}")
    print(f"Время с кэшированием: {elapsed:.6f} секунд")
    
    # Смотрим статистику кэша
    cache_stats = fibonacci_cached.cache_info()
    print(f"Статистика кэша: hits={cache_stats.hits}, misses={cache_stats.misses}")

if __name__ == "__main__":
    test_performance()
