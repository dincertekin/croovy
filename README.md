# croovy

![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Croovy is a privacy-focused search engine that delivers accurate results without tracking you. The frontend is built with Vue, the backend runs on Flask, and Redis handles search indexing because its NoSQL architecture is well-suited for fast, indexed lookups.

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Vue |
| Backend | Flask (Python 3) |
| Database | Redis |

## Installation

### Prerequisites

- Node.js and npm
- Python 3 and pip
- Redis

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/dincertekin/croovy.git
   cd croovy/
   ```

2. Install frontend dependencies:
   ```bash
   cd client/ && npm install
   ```

3. Install backend dependencies:
   ```bash
   cd server/ && pip install -r requirements.txt
   ```

## Usage

Start Redis first, then the backend, then the frontend:

```bash
redis-server
flask run
npm run dev
```

If Redis isn't responding, verify it's running before starting the backend:
```bash
redis-cli ping
```

## Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

For major changes, please open an issue first to discuss what you'd like to change.

## License

MIT License — see [LICENSE](./LICENSE) for details.
