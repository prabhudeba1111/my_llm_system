## MY LLM SYSTEM

A failure-aware, configurable LLM client system built in Python.

This project focuses on **correctness, reliability, and system design**, making it an ideal tool for developers working on applications that integrate with LLMs.

## Why this project exists
Most LLM examples focus on chat interfaces or prompt tricks.
Real-world systems fail in less visible ways:

- network timeouts
- empty or malformed model outputs
- retry storms
- unbounded concurrency
- unclear failure semantics

This project was built to explore how to design an LLM client that
fails safely, behaves predictably, and can be extended without
breaking guarantees.

## Features
- Simulates network timeouts with configurable probabilities.
- Handles empty prompts and generates appropriate failure responses.
- Implements retry logic for transient errors.
- Provides detailed logging for debugging and analysis.
- Easy to extend and customize for different testing scenarios.

- **LLM backends**:
    - MockLLM: A mock implementation for testing purposes.
        - Used for testing and development.
        - Simulates timeouts and failures.
        - Zero external dependencies.
    - LocalLLM: An LLM that runs locally on the user's machine.
        - Uses a locally running Ollama server.
        - No external API calls.
        - Suitable for offline development.

    Both LLM backends implement the same interface, allowing for easy switching between them in your application.

- **Failure handling**:
    - An LLM call can result in either a successful response (`LLMResponse`) or a failure (`LLMFailure`).
    - Failures can be retryable or non-retryable, allowing for robust error handling in your application.

- **Sync vs Async**:
    - The system provides both synchronous and asynchronous interfaces for LLM clients.
    - Async clients include:
        - concurrency limits.
        - rate limiting.
        - total timeout handling.
        - cancellation handling.

## Installation
This project requires Python 3.11 or higher. To install the necessary dependencies, run:
```bash
pip install -r requirements.txt
```
development dependencies (Optional):
```bash
pip install -r requirements-dev.txt
```

## Running the project
To run the project in sync mode:
```bash
python -m src.main
```

To run the project in async mode:
```bash
python -m src.async_demo
```

## Usage
To use the MockLLM in your project, simply instantiate it and call the `generate` method with an `LLMRequest` object. The mock LLM will return either an `LLMResponse` or an `LLMFailure` based on the simulated conditions.

```python
from src.llm.mock import MockLLM
from src.llm.models import LLMRequest

llm = MockLLM()
request = LLMRequest(prompt="Hello, world!")
response = llm.generate(request)

if isinstance(response, LLMResponse):
    print("LLM Response:", response.text)
else:
    print("LLM Failure:", response.reason)
```
## Configuration
You can configure the maximum number of retries for transient errors by passing the `max_retries` parameter when instantiating the `MockLLM`.

```python
llm = MockLLM(max_retries=5)
```
## Logging
The MockLLM uses a Logger to provide detailed information about its operations. You can adjust the logging level as needed for your debugging purposes.

## Testing
The repository includes unit tests to verify the behaviour of the MockLLM under various conditions. You can run the tests using pytest:

```bash
pytest -q
```

## Contributing
Contributions are welcome! Please feel free to submit issues and pull requests for improvements and new features.
