import csv
from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error

from bini.engine.utils import BiniUtils


class BrowserRecorder:
    def __init__(self, output_csv="elements.csv"):
        self.interactions = []  # List to store interactions
        self.recorded_elements = set()  # To track processed elements
        self.output_csv = output_csv

    def run(self, start_url):
        """Run the browser and record interactions."""
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Inject JavaScript to capture interactions and generate XPath
                page.add_init_script("""
                    window.recordedInteractions = [];

                    document.addEventListener('click', (event) => {
                        const target = event.target;
                        const interaction = {
                            action: 'click',
                            tag_name: target.tagName.toLowerCase(),
                            id: target.id || null,
                            name: target.name || null,
                            xpath: generateXPath(target),
                        };
                        window.recordedInteractions.push(interaction);
                    });

                    document.addEventListener('input', (event) => {
                        const target = event.target;
                        const interaction = {
                            action: 'input',
                            tag_name: target.tagName.toLowerCase(),
                            id: target.id || null,
                            name: target.name || null,
                            xpath: generateXPath(target),
                        };
                        window.recordedInteractions.push(interaction);
                    });

                    function generateXPath(element) {
                        if (element.id) return `//*[@id="${element.id}"]`;
                        if (element === document.body) return '/html/body';
                        let ix = 0;
                        const siblings = element.parentNode ? element.parentNode.childNodes : [];
                        for (let i = 0; i < siblings.length; i++) {
                            const sibling = siblings[i];
                            if (sibling === element) {
                                const path = generateXPath(element.parentNode);
                                return `${path}/${element.tagName.toLowerCase()}[${ix + 1}]`;
                            }
                            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                        }
                        return '';
                    }
                """)

                # Navigate to the start URL
                page.goto(start_url)
                print("Interact with the browser. Close it when you're done.")

                while True:
                    try:
                        # Fetch interactions from the browser
                        new_interactions = page.evaluate("window.recordedInteractions || []")
                        if new_interactions:
                            for interaction in new_interactions:
                                # Deduplicate by element identifier
                                element_identifier = (
                                    interaction["tag_name"],
                                    interaction["id"] or interaction["name"] or interaction["xpath"],
                                )
                                if element_identifier not in self.recorded_elements:
                                    tag_name = interaction["tag_name"]
                                    element_type = (
                                        "id" if interaction["id"]
                                        else "name" if interaction["name"]
                                        else "xpath"
                                    )
                                    element_path = interaction["id"] or interaction["name"] or interaction["xpath"]

                                    # Update the tag name for the first input or button
                                    if not any(i[0] in ["button", "input"] for i in self.interactions):
                                        if tag_name in ["button", "input"]:
                                            tag_name = f"primary-{tag_name}"

                                    self.interactions.append([tag_name, element_type, element_path])
                                    self.recorded_elements.add(element_identifier)

                            # Clear interactions in the browser
                            page.evaluate("window.recordedInteractions = []")

                    except Error as e:
                        print(f"Navigation or context issue: {e}")
                        if "closed" in str(e):
                            break
                        page.wait_for_load_state("domcontentloaded")

            except Exception as e:
                print(f"Error during execution: {e}")
            finally:
                try:
                    browser.close()
                except Exception as e:
                    print(f"Error closing the browser: {e}")

    def save_to_csv(self):
        """Save the interactions to a CSV file."""
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tag Name", "Element Type", "Element Path"])
            writer.writerows(self.interactions)

    def get_interactions(self):
        """Return the list of recorded interactions."""
        return self.interactions




bini = BiniUtils()
bini.bini_code(interaction_list=[[1,2,3], [1,2,3], [1,2,3]])
# if __name__ == "__main__":
#
#     recorder = BrowserRecorder(output_csv="elements.csv")
#     start_url = input("Enter the URL to start recording: ")
#     recorder.run(start_url)
#
#     # Save interactions to a CSV file
#     recorder.save_to_csv()
#
#     print("\nRecorded Interactions:")
#     print(recorder.get_interactions())
#
#     print(f"\nInteractions saved to {recorder.output_csv}")
