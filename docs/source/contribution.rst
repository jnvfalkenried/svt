Contributing
============

.. 
    _Guidelines for developers who want to contribute.
    _Coding standards, branching strategy, etc.

We welcome contributions to the project! Please review the following guidelines to ensure a smooth collaboration process.

Workflow
--------

The project follows a **dev → stage → main** branching strategy:

1. **dev**:

   * Active development happens here.
   * New features, bug fixes, and experiments should branch off from `dev`.

2. **stage**:

   * Acts as a testing environment.
   * Changes from `dev` are merged into `stage` for further testing before being released.

3. **main**:

   * The stable release branch.
   * Only thoroughly tested and approved changes are merged into `main`.

Contributions should follow this workflow:

#. Fork the repository.
#. Create a new branch from `dev` for your changes.
#. Submit a pull request (PR) targeting the `dev` branch.
#. Ensure your PR includes:

   * Clear and concise descriptions of the changes.
   * References to any related issues or tickets.

#. Wait for a code review and approval before merging.

Coding Standards
-----------------

To maintain code quality and consistency, please adhere to the following standards:

1. **Code Formatting**:

   * Use **Black** for Python code formatting. It enforces a strict, consistent style.

     * VSCode Extension ID: `ms-python.black-formatter`

2. **Import Sorting**:

   * Use **isort** to automatically sort imports for better readability.

     * VSCode Extension ID: `ms-python.isort`

3. **Static Analysis**:

   * Use **Pylance** for advanced code analysis and autocomplete.

     * VSCode Extension ID: `ms-python.vscode-pylance`

4. **Documentation**:

   * Use **autoDocstring** to generate consistent docstrings for functions and methods.

     * VSCode Extension ID: `njpwerner.autodocstring`

   * Ensure all public methods, classes, and modules have appropriate docstrings.

5. **Testing**:

   * Write unit tests for new features and bug fixes.
   * Ensure all tests pass before submitting a PR.

Development Tools
-----------------

We recommend the following tools for contributors:

* **Visual Studio Code (VSCode)**: A powerful, lightweight code editor.
* Install the extensions listed above for improved productivity and code quality.

Submitting a Pull Request (PR)
------------------------------

#. Ensure your branch is up-to-date with the `dev` branch.
#. Run tests locally to confirm your changes do not break existing functionality.
#. Include a meaningful commit message describing the changes.
#. Submit a PR with the following information:

   * A descriptive title and summary.
   * A list of changes made.
   * Links to related issues (if applicable).

Additional Notes
----------------

* **Code Reviews**: All PRs are reviewed by maintainers or project collaborators. Be open to feedback and willing to make adjustments as needed.
* **Documentation Updates**: If your changes affect the user experience or workflows, update the relevant documentation.
* **Issues**: If you discover a bug or have a feature request, create an issue in the repository.

By following these guidelines, you help us maintain high-quality code and a welcoming development environment.

