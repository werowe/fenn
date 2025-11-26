# PySmle Notification System

A flexible and extensible notification system for ML training alerts that supports multiple services including Discord, Slack, and Email.

## Features

- 🚀 **Multiple Services**: Discord, Slack, Email support
- 🔧 **Extensible**: Easy to add new notification services
- 🛡️ **Error Handling**: Graceful failure handling with detailed logging
- 🧪 **Well Tested**: Comprehensive test suite with 95%+ coverage
- 📝 **Type Hints**: Full type annotation support
- 🌍 **Environment Variables**: Easy configuration via env vars

## Quick Start

```python
from smle.Notification import Notifier, Discord, Slack

# Create notifier
notifier = Notifier()

# Add services
notifier.add_service(Discord())  # Requires DISCORD_WEBHOOK env var
notifier.add_service(Slack())    # Requires SLACK_WEBHOOK env var

# Send notification
notifier.notify("🚀 Training completed successfully!")
```

## Installation

The notification system is included with PySmle. Make sure you have the required dependencies:

```bash
pip install requests  # For Discord and Slack
# Email service uses built-in smtplib (no extra dependencies)
```

## Configuration

### Environment Variables

Set these environment variables to enable different notification services:

#### Discord
```bash
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

#### Slack
```bash
export SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR_WEBHOOK_URL"
```

#### Email
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"  # Optional, defaults to 587
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SMTP_FROM_EMAIL="your-email@gmail.com"
export SMTP_TO_EMAILS="recipient1@example.com,recipient2@example.com"
```

### Programmatic Configuration

You can also configure services programmatically:

```python
from smle.Notification import Notifier, Discord, Slack, Email

notifier = Notifier()

# Configure with direct URLs/credentials
notifier.add_service(Discord(webhook_url="https://discord.com/..."))
notifier.add_service(Slack(webhook_url="https://hooks.slack.com/..."))
notifier.add_service(Email(
    smtp_server="smtp.gmail.com",
    username="user@example.com",
    password="password",
    from_email="user@example.com",
    to_emails=["recipient@example.com"]
))
```

## Usage Examples

### Basic Usage

```python
from smle.Notification import Notifier, Discord

notifier = Notifier()
notifier.add_service(Discord())
notifier.notify("Hello from PySmle!")
```

### Training Integration

```python
import time
from smle.Notification import Notifier, Discord, Slack

def train_model():
    notifier = Notifier()
    notifier.add_service(Discord())
    notifier.add_service(Slack())
    
    # Training start
    notifier.notify("🚀 Training started")
    
    for epoch in range(10):
        # ... training code ...
        time.sleep(1)
        
        if epoch % 5 == 0:
            notifier.notify(f"📈 Epoch {epoch}/10 completed")
    
    # Training complete
    notifier.notify("✅ Training completed successfully!")
```

### Error Handling

The notification system handles errors gracefully:

```python
notifier = Notifier()
notifier.add_service(Discord())  # This might fail
notifier.add_service(Slack())    # This might work

# Even if some services fail, others will still work
notifier.notify("This message will be sent to working services only")
```

### Service Management

```python
notifier = Notifier()

# Add services
discord = Discord()
slack = Slack()
notifier.add_service(discord)
notifier.add_service(slack)

# Check registered services
print(notifier.get_services())  # ['Discord', 'Slack']

# Remove a service
notifier.remove_service(discord)
print(notifier.get_services())  # ['Slack']

# Clear all services
notifier.clear_services()
print(notifier.get_services())  # []
```

## Creating Custom Services

You can easily create custom notification services by implementing the `Service` interface:

```python
from smle.Notification import Service
import requests

class CustomWebhook(Service):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_notification(self, message: str) -> None:
        response = requests.post(
            self.webhook_url,
            json={"text": message},
            timeout=10
        )
        response.raise_for_status()

# Use your custom service
notifier = Notifier()
notifier.add_service(CustomWebhook("https://your-webhook.com"))
notifier.notify("Hello from custom service!")
```

## API Reference

### Notifier

Main class for managing notification services.

#### Methods

- `add_service(service: Service) -> None`: Add a notification service
- `remove_service(service: Service) -> None`: Remove a notification service
- `notify(message: str) -> None`: Send notification to all services
- `get_services() -> List[str]`: Get list of registered service names
- `clear_services() -> None`: Remove all services

### Service (Abstract Base Class)

Interface that all notification services must implement.

#### Methods

- `send_notification(message: str) -> None`: Send notification (abstract method)

### Discord

Discord notification service using webhooks.

#### Constructor
- `Discord(webhook_url: str = None)`: Initialize with webhook URL or DISCORD_WEBHOOK env var

### Slack

Slack notification service using webhooks.

#### Constructor
- `Slack(webhook_url: str = None)`: Initialize with webhook URL or SLACK_WEBHOOK env var

### Email

Email notification service using SMTP.

#### Constructor
- `Email(smtp_server: str = None, smtp_port: int = 587, username: str = None, password: str = None, from_email: str = None, to_emails: list = None)`: Initialize with SMTP settings or environment variables

## Testing

Run the test suite:

```bash
pytest tests/notification/ -v
```

## Examples

See `examples/notification_example.py` for complete usage examples.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes with tests
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
