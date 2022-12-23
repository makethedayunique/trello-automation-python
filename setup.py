from setuptools import setup

setup(
	name="trello-automation",
	version='0.0.1',
	py_modules=['app'],
	install_requires=[
		'click', 
		'requests', 
		'python-dotenv'
	],
	entry_points={
		'console_scripts': [
			'trello-add = app:main',
		],
	},
)