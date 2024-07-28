# Reddit Outreach

> A simple tool to find Reddit posts that would benefit from sharing a specific YouTube video.

## Setup

### Prerequisites

- Python 3.11+
- pip (upgrade with \`pip install --upgrade pip\` recommeneded)
- Reddit account and app setup

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

### Configuration

Create a Reddit app at [prefs/apps/](https://www.reddit.com/prefs/apps/).
Set the app's redirect URI to `http://localhost:8000`.

**Create a .env file in the root directory with the following content:**

```sh
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="your_user_agent"
export REDDIT_REDIRECT_URI="http://localhost:8000"
```

## Usage

```sh
# Using my video
python outreach.py "https://www.youtube.com/watch?v=bF7WnLk5ix4"
```

## License

[MIT License](LICENSE)
