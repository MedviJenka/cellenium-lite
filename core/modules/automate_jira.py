from atlassian import Jira
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from bini.core.modules.environment import get_dotenv_data


@dataclass
class JiraFactory:

    url: str
    username: str
    password: str
    verify_ssl: bool = False


class JiraBaseModule(ABC):

    @abstractmethod
    def create_ticket(self, *args: Optional[any], **kwargs: Optional[any]) -> None:
        pass


@dataclass
class CreateTicket(JiraFactory, JiraBaseModule):

    @property
    def as_admin(self) -> Jira:
        return Jira(
            url=self.url,
            username=self.username,
            password=self.password,
            verify_ssl=self.verify_ssl,
            cloud=True
        )

    def create_ticket(self) -> None:
        self.as_admin.issue_create(fields={
            'project': {'key': 'STNG'},  # add your Project Key here
            'issuetype': {'name': 'Task'},  # add your issue Type name
            'summary': 'Test Python REST API',
            'description': 'This is the description',
            'priority': {'name': 'Low'},
            'versions': [{'Affects Version/s': '123456'}],
            'components': [{'label': 'Userinterface'}]
        })


credentials = {
    'url': get_dotenv_data('JIRA_PROJECT_URL'),
    'username': get_dotenv_data('JIRA_USERNAME'),
    'password': get_dotenv_data('JIRA_PASSWORD'),
    'verify_ssl': False
}


ticket = CreateTicket(**credentials)
if __name__ == '__main__':
    ticket.create_ticket()
