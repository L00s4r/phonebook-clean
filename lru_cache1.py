from functools import lru_cache
import time

@lru_cache(maxsize=128)
def fumc(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
start_time = time.time()
result1 = fumc(100)
end_time = time.time()
time_without_cache = end_time - start_time

start_time = time.time()
result2 = fumc(100)
end_time = time.time()
time_with_cache = end_time - start_time

print(f"Результат без кэша: {result1}, время: {time_without_cache:.6f} секунд")
print(f"Результат с кэшем: {result2}, время: {time_with_cache:.6f} секунд")