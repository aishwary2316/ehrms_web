"""
Keep-Alive Service for E-HRMS on Render Free Tier
Pings the application every 14 minutes to prevent it from sleeping
Can be deployed as a separate cron job service on Render or run externally
"""

import requests
import time
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Your Render app URL (change this to your actual URL after deployment)
APP_URL = os.environ.get('APP_URL', 'https://your-app-name.onrender.com')
PING_INTERVAL = 14 * 60  # 14 minutes in seconds
HEALTH_CHECK_ENDPOINT = '/health'
PING_ENDPOINT = '/ping'

def ping_app():
    """Ping the application to keep it alive."""
    try:
        # Try ping endpoint first (lightweight)
        response = requests.get(f"{APP_URL}{PING_ENDPOINT}", timeout=30)
        
        if response.status_code == 200:
            logger.info(f"✅ Ping successful - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ Ping returned status: {response.status_code}")
            
            # Try health check endpoint as fallback
            health_response = requests.get(f"{APP_URL}{HEALTH_CHECK_ENDPOINT}", timeout=30)
            logger.info(f"Health check status: {health_response.status_code}")
            return health_response.status_code == 200
            
    except requests.exceptions.Timeout:
        logger.error(f"❌ Request timeout after 30 seconds")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"❌ Connection error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    """Main keep-alive loop."""
    logger.info(f"🚀 Starting Keep-Alive Service for {APP_URL}")
    logger.info(f"📡 Ping interval: {PING_INTERVAL} seconds ({PING_INTERVAL//60} minutes)")
    
    ping_count = 0
    success_count = 0
    
    while True:
        ping_count += 1
        logger.info(f"\n--- Ping #{ping_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        if ping_app():
            success_count += 1
        
        success_rate = (success_count / ping_count) * 100
        logger.info(f"📊 Success rate: {success_rate:.1f}% ({success_count}/{ping_count})")
        logger.info(f"⏰ Next ping in {PING_INTERVAL//60} minutes...")
        
        time.sleep(PING_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n🛑 Keep-Alive Service stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        raise
