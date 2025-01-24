import csv
from typing import Optional
from playwright.sync_api import sync_playwright
from infrastructure.core.executor import Executor
from bini.infrastructure.codegen_script import JS_SCRIPT
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

                log.level.info("Interact with the browser if needed. Close it when you're done.")

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
                        log.level.info(f"Navigation or context issue: {e}")
                        if "closed" in str(e):
                            break
            except Exception as e:
                log.level.info(f"Error during execution: {e}")
            finally:
                try:
                    browser.close()
                except Exception as e:
                    log.level.info(f"Error closing the browser: {e}")

    def save_to_csv(self) -> None:
        """Save the interactions to a CSV file."""
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tag Name", "Element Type", "Element Path", "Action", "Value"])
            writer.writerows(self.interactions)

    def get_interactions(self) -> list:
        """Return the list of recorded interactions."""
        return self.interactions

    def __generate_methods(self, class_name: str) -> str:
        code_cache = []

        for each_list in self.get_interactions():
            action = each_list[3]
            tag_name = each_list[0]
            value = each_list[4]

            if action == 'Clicked on button':
                code_cache.append(f"setup.get_mapped_element('{tag_name}').Action(actions.click())")
            elif action == 'Clicked on input' and value is not None:
                code_cache.append(f"setup.get_mapped_element('{tag_name}').send_text('{value}')")
            elif action == 'Typed in input':
                code_cache.append(f"setup.get_mapped_element('{tag_name}').send_text('{value}')")
            elif action.startswith('Clicked on'):
                code_cache.append(f"setup.get_mapped_element('{tag_name}').Action(actions.click())")

        methods_code = "\n  ".join(code_cache)

        # Ensure indentation for generated code
        final_code = f"""class Test{class_name}:

            def test_{class_name.lower()}(self, setup) -> None:
                {methods_code}
        """
        log.level.info(final_code)
        return final_code

    @staticmethod
    def __create_python_file(output: str) -> None:
        file_path = "generated_test_code.py"
        with open(file_path, "w") as file:
            file.write(output)
        log.level.info(f'python file: {file_path}')

    def execute(self, class_name: Optional[str] = None) -> None:
        self.run()
        self.save_to_csv()

        log.level.info("\nRecorded Interactions:")
        log.level.info(self.get_interactions())
        log.level.info(f"\nInteractions saved to {self.output_csv}")

        code = self.__generate_methods(class_name=class_name)

        if class_name:
            self.__create_python_file(output=code)


app = BrowserRecorder(screen='https://irqa.ai-logix.net')
app.execute(class_name="App")
