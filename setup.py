from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Sanjith',
    author_email='sanjithpalateru10@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=["mcqgenerator"],
    package_dir={"": "src"}
)

#should change the openai to groq in the future and the things with those also to be changed