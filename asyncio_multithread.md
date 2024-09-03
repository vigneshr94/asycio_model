Using multiple event loops in `asyncio` within the same thread is generally not recommended and can lead to unexpected behavior. Here's a detailed explanation of why this is and when you might consider using multiple event loops:

### 1. **Single Thread, Single Event Loop**

In Python's `asyncio`, the convention and design expectation is to use a single event loop per thread. The event loop is responsible for managing asynchronous tasks, callbacks, and IO-bound operations. Trying to run multiple event loops in the same thread can cause several issues:

- **State Confusion**: The `asyncio` module manages event loops in a thread-local storage manner. This means if you try to manage multiple loops in the same thread, you can easily end up with tasks being scheduled on the wrong loop or losing reference to the correct loop, leading to unexpected behavior or errors.
  
- **Performance Overhead**: Running multiple loops in the same thread doesn’t offer performance benefits since only one event loop can run at a time in a single-threaded context. Instead, this might introduce unnecessary complexity and overhead in managing loops.

- **APIs and Functions**: Many `asyncio` APIs implicitly use the current event loop. If you try to use multiple loops, the default loop might not be what you expect, causing your coroutines and tasks to behave incorrectly.

### 2. **Multiple Event Loops in Different Threads**

It is possible and sometimes useful to have multiple event loops, each running in its own thread. This can be beneficial if you have distinct sets of asynchronous tasks that should be handled independently. For example, if you're developing a server that needs to handle both networking (IO-bound) and intensive computation (CPU-bound), you might use one loop for network tasks and another for computational tasks, each in their own thread.

To use multiple event loops in different threads:

- **Create a new event loop per thread**: You can use `asyncio.new_event_loop()` to create a loop in a thread.
- **Set the event loop for the thread**: Use `asyncio.set_event_loop()` to set the newly created loop as the current loop for that thread.
- **Run tasks on that loop**: You can now schedule tasks and run them on the loop specific to that thread.

Here’s a basic example:

```python
import asyncio
import threading

def run_loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Creating a new event loop
new_loop = asyncio.new_event_loop()

# Starting a new thread and passing the new loop to it
thread = threading.Thread(target=run_loop_in_thread, args=(new_loop,))
thread.start()

# Now you can schedule tasks on `new_loop` from this thread or another
```

### 3. **When to Use Multiple Event Loops**

While most use cases don’t require multiple event loops, here are some scenarios where it might be useful:

- **Separation of Concerns**: When you want to isolate different sets of tasks or subsystems, each handling different workloads or having different priority levels.
  
- **Resource Management**: Different event loops in different threads might be needed if you need to manage different resources that shouldn't interfere with each other.
  
- **Complex Multi-threaded Applications**: In some complex applications where you might already have a multi-threaded architecture, separate event loops can be managed in each thread to isolate async tasks to those specific threads.

### 4. **Caveats**

If you decide to use multiple event loops:

- **Careful Synchronization**: Make sure that data shared between loops/threads is properly synchronized, using locks or queues, to avoid race conditions.
  
- **Proper Shutdown Handling**: You need to ensure each loop and thread is properly closed down. Failure to do so can result in resource leaks or deadlocks.

- **Compatibility with Libraries**: Not all libraries are designed to handle multiple event loops well. Make sure to test libraries in use to ensure compatibility with your architecture.

### Conclusion

In most scenarios, sticking with a single event loop per thread is the way to go. If your use case absolutely demands multiple event loops (and you are running them in separate threads), then it’s technically feasible but requires careful management and understanding of `asyncio` internals.