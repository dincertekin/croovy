# croovy
Privacy-focused search engine built with Vue and Flask.

## Description
Croovy is a privacy-focused search engine that aims to deliver accurate results without tracking you. The frontend is built with Vue, the backend runs on Python with Flask, and Redis is used as the database for efficient search engine indexing. Redis was chosen because its NoSQL architecture handles indexed data well and provides everything needed for fast, reliable search operations.

## Getting Started

### Dependencies
* Node.js and npm or yarn
* Python 3.x and pip
* Redis

### Installing

* Clone the repository:
```bash
git clone https://github.com/dincertekin/croovy.git
cd croovy/
```

* Install frontend dependencies:
```bash
cd client/
npm install
```

* Install backend dependencies:
```bash
cd server/
pip install -r requirements.txt
```

### Executing program

* Start Redis:
```bash
redis-server
```

* Start the backend:
```bash
flask run
```

* Start the frontend:
```bash
npm run dev
```

## Help
Make sure Redis is running before starting the backend, otherwise the app will fail to connect.

```bash
redis-cli ping
```

## Contributing
Contributions are welcome! To get started:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please open an issue first for major changes to discuss what you'd like to change.

## License
This project is licensed under the [MIT](LICENSE) License - see the LICENSE.md file for details
