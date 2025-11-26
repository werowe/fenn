import os
import requests
from .service import Service


class Discord(Service):
    """Discord notification service using webhooks."""
    
    def __init__(self, webhook_url: str = None):
        """Initialize Discord service.
        
        Args:
            webhook_url: Discord webhook URL. If None, reads from DISCORD_WEBHOOK env var.
            
        Raises:
            ValueError: If webhook URL is not provided or found in environment.
        """
        self._discord_webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK")
        if not self._discord_webhook_url:
            raise ValueError("Discord webhook URL must be provided or set in DISCORD_WEBHOOK environment variable")

    def send_notification(self, message: str) -> None:
        """Send notification to Discord channel.
        
        Args:
            message: The message to send.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        data = {
            "content": message,
            "username": "pysmle"
        }

        try:
            result = requests.post(self._discord_webhook_url, json=data, timeout=10)
            result.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise requests.exceptions.RequestException(f"Failed to send Discord notification: {err}")