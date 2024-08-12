# JinjaX Flowbite Flask Demonstrator

## 2. Setup Development Environment

### 2.1. Toolchain

- Install python 3.11 or newer
- Install Nodejs LTS (`currently v20.9.0`)
- Visual Studio Code

### 2.2. VSCode Extensions

- Pylance: `ms-python.vscode-pylance`
- Tailwind CSS Intellisense: `bradlc.vscode-tailwindcss`
- Jinja: `wholroyd.jinja`
- Jinja2 Snippet Kit: `wyattferguson.jinja2-snippet-kit`
- BetterJinja: `samuelcolvin.jinjahtml`
- Markdown All in One: `yzhang.markdown-all-in-one`
- markdownlint: `davidanson.vscode-markdownlint`

### 2.3. Install the Python Library Dependencies

~~~sh
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
~~~

### 2.4. Install Nodejs Dependencies

This is for the Flowbite and Tailwind CSS minification.

~~~sh
npm install
~~~

## 3. Development

Development consists of two `parallel` command-line tools running simultaneously.

1. tailwindcss minification

    ~~~sh
    npm run watchcss
    ~~~

1. flask web server

    ~~~sh
    .\venv\Scripts\activate
    npm run webdev
    ~~~

With the above vscode extensions installed, one may set breakpoints and run via the vscode debugger by pressing the F5 key.

### 3.1. Desktop Development

~~~sh
.\venv\Scripts\activate
npm run desktop
~~~
