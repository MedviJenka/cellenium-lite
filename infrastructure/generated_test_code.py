class TestApp:
    
                def test_app(self, setup) -> None:
                    setup.get_mapped_element('button').Action(actions.click())
            