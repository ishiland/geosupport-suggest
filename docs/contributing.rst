Contributing
============

Thank you for considering contributing to geosupport-suggest! This package is open source, and we welcome contributions of all kinds: bug reports, feature requests, documentation improvements, bug fixes, or new features.

Setting Up Development Environment
--------------------------------

1. Fork the repository on GitHub.
2. Clone your fork locally:

   .. code-block:: bash

       git clone https://github.com/your-username/geosupport-suggest.git
       cd geosupport-suggest

3. Create a virtual environment and install dependencies:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate
       pip install -e .
       pip install -r tests/requirements.txt

Running Tests
------------

We use the unittest framework for testing. To run tests:

.. code-block:: bash

    python -m unittest discover

To run a specific test:

.. code-block:: bash

    python -m unittest tests.test_suggest_methods

Code Style
---------

We follow PEP 8 style guidelines. Please make sure your code adheres to these standards.

We use the Black code formatter to maintain consistent code style. Before submitting a pull request, please format your code with Black:

.. code-block:: bash

    # Install black if you haven't already
    pip install black
    
    # Format your code
    black suggest tests

For type annotations, we use the typing module. Please include type hints for function arguments and return values.

Pull Request Process
------------------

1. Create a new branch for your feature or bug fix:

   .. code-block:: bash

       git checkout -b feature/your-feature-name

2. Make your changes and add tests if applicable.
3. Run the tests to ensure they pass.
4. Update the documentation if needed.
5. Commit your changes:

   .. code-block:: bash

       git commit -m "Description of your changes"

6. Push to your fork:

   .. code-block:: bash

       git push origin feature/your-feature-name

7. Open a pull request on GitHub.

Reporting Bugs
-------------

When reporting bugs, please include:

* A clear and descriptive title
* Steps to reproduce the bug
* Expected behavior
* Actual behavior
* Your operating system and Python version
* Any relevant logs or error messages

Feature Requests
--------------

When requesting new features, please:

* Clearly describe the feature
* Explain why it would be valuable
* Provide examples of how it would be used
* Indicate if you're willing to help implement it

Documentation
------------

Documentation improvements are always welcome. You can:

* Fix typos or clarify existing documentation
* Add more examples
* Improve API documentation
* Add tutorials or how-to guides

License
------

By contributing to geosupport-suggest, you agree that your contributions will be licensed under the project's MIT License. 