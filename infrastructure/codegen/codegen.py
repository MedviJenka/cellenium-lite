import csv
from playwright.sync_api import sync_playwright
from infrastructure.core.executor import Executor
from infrastructure.codegen.event_listener import JS_SCRIPT, init_code
from infrastructure.core.logger import Logger

log = Logger()


class BrowserRecorder(Executor):

    def __init__(self, screen: str, output_csv="page_base.csv") -> None:
        self.screen = screen
        self.interactions = []
        self.recorded_elements = set()
        self.output_csv = output_csv

    def run(self) -> None:
        """Run the browser and automate interactions."""
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Inject JavaScript to capture interactions
                page.add_init_script(JS_SCRIPT)
                page.goto(self.screen)

                log.log_info("Interact with the browser if needed. Close it when you're done.")

                while True:
                    try:
                        # Evaluate only if the page is still open
                        if not page.is_closed():
                            new_interactions = page.evaluate("window.recordedInteractions || []")
                            if new_interactions:
                                for interaction in new_interactions:
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
                                        action_description = interaction["action_description"]
                                        value = interaction.get("value")

                                        self.interactions.append(
                                            [tag_name, element_type, element_path, action_description, value])
                                        self.recorded_elements.add(element_identifier)

                                # Clear interactions
                                page.evaluate("window.recordedInteractions = []")
                            else:
                                # Avoid tight infinite loop
                                page.wait_for_timeout(100)

                    except Exception as e:
                        log.log_info(f"Navigation or context issue: {e}")
                        if "closed" in str(e):
                            break
            except Exception as e:
                log.log_info(f"Error during execution: {e}")

            finally:
                try:
                    browser.close()
                except Exception as e:
                    log.log_info(f"Error closing the browser: {e}")

    def save_to_csv(self) -> None:
        """Save the interactions to a CSV file."""
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Element Name", "Element Type", "Element Path", "Action", "Value"])
            writer.writerows(self.interactions)

    def get_interactions(self) -> list:
        """Return the list of recorded interactions."""
        return self.interactions

    def __generate_methods(self, class_name: str, device: str) -> str:

        code_cache = []

        for each_list in self.get_interactions():
            tag_name = each_list[0]
            action = each_list[3]
            value = each_list[4]

            if action == 'Clicked on button':
                code_cache.append(f"driver.get_mapped_element('{tag_name}').Action(actions.click())")
            elif action == 'Clicked on input' and value is not None:
                code_cache.append(f"driver.get_mapped_element('{tag_name}').send_text('{value}')")
            elif action == 'Typed in input':
                code_cache.append(f"driver.get_mapped_element('{tag_name}').send_text('{value}')")
            elif action.startswith('Clicked on'):
                code_cache.append(f"driver.get_mapped_element('{tag_name}').Action(actions.click())")
            elif action.startswith('Checkbox checked'):
                code_cache.append(f"driver.get_mapped_element('{tag_name}').Action(actions.click())")

        methods_code = "\n        ".join(code_cache)  # Ensure proper indentation for generated code

        # Ensure overall indentation for the final generated code
        final_code = f"""
        {init_code(device=device)}
        class Test{class_name}:

            def test_{class_name.lower()}(self, driver) -> None:
                {methods_code}
        """
        log.log_info(final_code)
        return final_code

    @staticmethod
    def __create_python_file(output: str) -> None:
        file_path = "generated_test_code.py"
        with open(file_path, "w") as file:
            file.write(output)
        log.log_info(f'python file: {file_path}')

    def execute(self, class_name: str, device: str) -> None:
        self.run()
        self.save_to_csv()

        log.log_info("\nRecorded Interactions:")
        log.log_info(f'{self.get_interactions()}')
        log.log_info(f"\nInteractions saved to {self.output_csv}")

        code = self.__generate_methods(class_name=class_name, device=device)

        if class_name:
            self.__create_python_file(output=code)


if __name__ == '__main__':
    app = BrowserRecorder(screen='https://irqa.ai-logix.net')
    app.execute(class_name="App", device='medrei')
