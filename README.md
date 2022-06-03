# znanium-savebooks

Works on GNU/Linux OS/macOS.

The script allows you to download books from znanium.com. The selenium module is used for this purpose.
For downloading you need:
1. Have an account with the book you bought.
2. Dowsnload geckodriver in folder.
3. In the directory with the script, create a text file auth.txt. In it, put your login and password through the space.
4. Install selenium, img2pdf, PIL moduli via pip install or any other way.
[img2pdf macOS install fix](https://medium.com/@jeremie.lumbroso/installing-pikepdf-with-homebrew-on-macos-big-sur-2a21995d0cfe)

Example of program execution from terminal:

$ python znanium.py https://znanium.com/read?id=xxxxxx 1 x

The first argument is a link to the book in the reader itself.
The second argument - from which page to load.
The third argument - which page to load.

----------------------------------------------------------------------------

Работает на GNU/Linux OS/macOS.

Скрипт позволяет скачивать книги с сайта znanium.com. Для данных целей используется модуль selenium.
Для скачивания вам необходимо:
1. Иметь аккаунт с купленной книгой.
2. Скачать geckodriver в папку
3. В директории со скриптом создать текстовый файла auth.txt. В него через пробел указать логин и пароль.
4. Через pip install или иным образом установить модули selenium, img2pdf, PIL.

[img2pdf macOS исправление установки](https://medium.com/@jeremie.lumbroso/installing-pikepdf-with-homebrew-on-macos-big-sur-2a21995d0cfe)

Пример выполнения программы из терминала:

$ python znanium.py https://znanium.com/read?id=xxxxxx 1 x

Первый аргумент - ссылка на книгу в самом ридере.
Второй аргумент - с какой страницы загружать.
Третий аргумент - по какую страницу загружать.
