import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator, AsyncIterator, cast


async def sync_to_async[T](iterator: Iterator[T]) -> AsyncIterator[T]:
    loop = asyncio.get_event_loop()
    
    def get_safe_iterator():
        yield from iterator
        yield StopIteration
        
    safe_iterator = get_safe_iterator()
        
    with ThreadPoolExecutor() as executor:
        while True:
            value = await loop.run_in_executor(executor, next, safe_iterator)
            if value is StopIteration:
                break
            else:
                yield cast(T, value)
            
            
def async_to_sync[T](async_gen: AsyncIterator[T]) -> Iterator[T]:
    loop = asyncio.new_event_loop()
    while True:
        try:
            yield loop.run_until_complete(anext(async_gen))
        except StopAsyncIteration:
            break
        