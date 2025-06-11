import time
from selenium import webdriver

# JavaScript code to monitor browser interactions
JS_EVENT_LISTENERS = """
(function() {
    if (window.__LOGGING_INITIALIZED__) return;
    window.__LOGGING_INITIALIZED__ = true;
    window.__capturedEvents__ = [];

    function logEvent(action, element) {
        const details = {
            action: action,
            tag: element.tagName || 'N/A',
            id: element.id || 'N/A',
            name: element.name || 'N/A',
            timestamp: new Date().toISOString()
        };
        window.__capturedEvents__.push(details);
    }

    document.addEventListener('click', function(event) {
        logEvent('click', event.target);
    });

    document.addEventListener('input', function(event) {
        logEvent('input', event.target);
    });

    console.log('Event listeners initialized.');
})();
"""

# JavaScript code to fetch captured logs
JS_FETCH_LOGS = """
if (!window.__capturedEvents__) return [];
const logs = window.__capturedEvents__;
window.__capturedEvents__ = [];
return logs;
"""

def main():
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Replace with the appropriate WebDriver
    driver.get("https://example.com")  # Replace with your target URL

    # Inject JavaScript listeners
    driver.execute_script(JS_EVENT_LISTENERS)
    print("Event listeners attached. Interact with the browser.")

    try:
        while True:
            # Fetch logs periodically
            logs = driver.execute_script(JS_FETCH_LOGS) or []  # Default to an empty list if None
            for log in logs:
                print(f"Action: {log['action']}, Tag: {log['tag']}, ID: {log['id']}, Name: {log['name']}, Timestamp: {log['timestamp']}")
            time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Stopping logging...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
