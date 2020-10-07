=======
Chatbot
=======

A simple chatbot webapp demo with `Flask
<https://flask.palletsprojects.com/en/1.1.x/>`_.

Installation
------------

1. Download the source code for the project.
2. Open a terminal and navigate to the root directory of the project.
3. Try running the ``poetry`` command. If it's not available on your
   system, install it: https://python-poetry.org/.
4. Install dependencies with ``poetry install``.

Running the app
---------------

1. Open a terminal and navigate to the root directory of the project.
2. Start the web app with ``poetry run python chatbot.py``. See also
   Flask's `quickstart docs
   <https://flask.palletsprojects.com/en/1.1.x/quickstart/>`_ for
   alternative instructions and troubleshooting.
3. The app will print a URL which you should enter into your browser,
   typically something like http://127.0.0.1:5000 or
   http://localhost:5000.

If running the app from JupyterLab on https://jupyter.korpus.cz, take
note of the port number (the part after the ``:``, i.e. 5000 in the
previous examples) and put together a URL in the following format, which
you should enter into your browser instead of the one printed by the
app:

.. code-block::

   https://jupyter.korpus.cz/user/<username>/proxy/<port-number>

Replace ``<username>`` with your username and ``<port-number>`` with the
port number you took note of.
