# Reddit Outreach

> A simple tool to find Reddit posts that would benefit from sharing a specific YouTube video.

## Setup

### Prerequisites

- Python 3.11+
- pip (upgrade with \`pip install --upgrade pip\` recommeneded)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/reddit-outreach.git
    cd reddit-outreach
    ```

2. Create a virtual environment:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Usage

#### Extracting Video Details

To extract and print details of a YouTube video, run:

```sh
python outreach.py "https://www.youtube.com/watch?v=example"
```

## License

[MIT License](LICENSE)
