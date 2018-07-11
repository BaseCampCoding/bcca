rm -r bcca.egginfo build dist
python setup.py bdist_wheel
python setup.py sdist

twine upload dist/*
