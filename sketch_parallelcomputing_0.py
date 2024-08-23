import time
from concurrent.futures import ThreadPoolExecutor

from rich import print

# fmt: off


class A:
    def __init__(self):
        self.a = 1
aaa = [A() for i in range(10_000)]


t0 = time.time()
for a in aaa:
    a.a += 10
print(f"[green]Time: {time.time() - t0}s")


def update_a(a_obj):
    a_obj.a += 10
with ThreadPoolExecutor(max_workers=20) as executor:
    t0 = time.time()
    executor.map(update_a, aaa)
    print(f"[green]Time: {time.time() - t0}s")
