<?php
session_start();
?>
<html>
<head>
<link rel="stylesheet" href="style.css" type="text/css" media="screen, projection" />
<title>Сторінка авторизації панелі керування Cpanel</title>
</head>
<body id="reg">
<img class="background-image" src="images/login-whisp.jpeg" />
<form id="regForm" action="testreg.php" method="post">
<div id="cpanel">
<img src="images/cpanel-logo.png" width="165" height="50" />
</div>
<!--**** testreg.php - это адрес обработчика. То есть, после нажатия на кнопку "Войти", данные из полей отправятся на страничку testreg.php методом "post" ***** -->
  <p>
    <label>Логін:<br></label>
    <input id="login" name="login" placeholder="Уведіть логін" type="text" size="25" maxlength="30">
  </p>
<!--**** В текстовое поле (name="login" type="text") пользователь вводит свой логин ***** -->  
  <p>
    <label>Пароль:<br></label>
    <input id="pass" name="password" placeholder="Уведіть пароль" type="password" size="25" maxlength="30">
  </p>
<!--**** В поле для паролей (name="password" type="password") пользователь вводит свой пароль ***** -->  
<p>
<input type="submit" name="submit" value="Увійти">
<!--**** Кнопочка (type="submit") отправляет данные на страничку testreg.php ***** --> 
<br>
<!--**** ссылка на регистрацию, ведь как-то же должны гости туда попадать ***** --> 
</p></form>
<br>
<?php
// Проверяем, пусты ли пересменные логина и id пользователя
if (empty($_SESSION['login']) or empty($_SESSION['id']))
{
// Если пусты, то мы не выводим ссылку
echo "Ви увійшли до адміністративної панелі, як <b>Гість</b>!<br><a href='#'>Посилання на головну сторінку панелі керування доступне тільки адміністраторам сайту!</a>";
}
else
   {
   // Если не пусты, то мы выводим ссылку
    echo "Ви увійшли, як <b>Адміністратор</b>!<br><a href='main.php'>Увійти у панель керування</a>";
   }
?>
</body>
</html>
