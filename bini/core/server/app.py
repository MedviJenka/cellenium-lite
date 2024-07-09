from flask import Flask
from bini.infrastructure.ai_utils import IRBiniUtils
from bini.infrastructure.logger import Logger


bini = IRBiniUtils(use_agents=False)
app = Flask(__name__)
log = Logger()


@app.route('/')
def main() -> dict:

    result = bini.run(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png",
                      prompt='Is Efrat Lang displayed on the right side of the screen? at the end type Passed if yes')
    log.level.info(result)

    return {
        'result': result
    }
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=90, debug=True)
