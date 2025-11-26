
import logging
from typing import List
from .service import Service


logger = logging.getLogger(__name__)


class Notifier:
    """Central notification manager that handles multiple notification services."""
    
    def __init__(self):
        """Initialize the notifier with an empty list of services."""
        self.services: List[Service] = []

    def add_service(self, service: Service) -> None:
        """Add a notification service.
        
        Args:
            service: A service implementing the Service interface.
        """
        self.services.append(service)
        logger.info(f"Added notification service: {service.__class__.__name__}")

    def remove_service(self, service: Service) -> None:
        """Remove a notification service.
        
        Args:
            service: The service to remove.
            
        Raises:
            ValueError: If the service is not found.
        """
        try:
            self.services.remove(service)
            logger.info(f"Removed notification service: {service.__class__.__name__}")
        except ValueError:
            logger.warning(f"Service {service.__class__.__name__} not found in services list")
            raise

    def notify(self, message: str) -> None:
        """Send notification to all registered services.
        
        Args:
            message: The message to send.
        """
        if not self.services:
            logger.warning("No notification services registered")
            return
            
        successful_services = []
        failed_services = []
        
        for service in self.services:
            try:
                service.send_notification(message)
                successful_services.append(service.__class__.__name__)
                logger.info(f"Successfully sent notification via {service.__class__.__name__}")
            except Exception as e:
                failed_services.append((service.__class__.__name__, str(e)))
                logger.error(f"Failed to send notification via {service.__class__.__name__}: {e}")
        
        # Log summary
        if successful_services:
            logger.info(f"Notification sent successfully to: {', '.join(successful_services)}")
        if failed_services:
            logger.warning(f"Notification failed for: {', '.join([f'{name} ({error})' for name, error in failed_services])}")

    def get_services(self) -> List[str]:
        """Get list of registered service names.
        
        Returns:
            List of service class names.
        """
        return [service.__class__.__name__ for service in self.services]

    def clear_services(self) -> None:
        """Remove all registered services."""
        count = len(self.services)
        self.services.clear()
        logger.info(f"Cleared {count} notification services")