<?php
header('Content-Type: text/html; charset=utf-8');
?>
<?php

include ("blocks/bd.php");
if (isset($_GET['id'])) 
{
	$id = $_GET['id'];
}


$result = mysql_query("SELECT * FROM kind_troops WHERE id='$id'",$db);
$myrow = mysql_fetch_array($result);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Министерство обороны Российской Федерации 
(Минобороны России)</title>
<meta name="keywords" content="" />
<meta name="description" content="" />
<link href="css/templatemo_style.css" rel="stylesheet" type="text/css" />
<link rel="icon" href="favicon.ico" type="image/x-icon" />
<script type="text/javascript" src="js/swfobject/swfobject.js"></script>
        
<script type="text/javascript">
  var flashvars = {};
  flashvars.cssSource = "css/piecemaker.css";
  flashvars.xmlSource = "piecemaker.xml";
    
  var params = {};
  params.play = "true";
  params.menu = "false";
  params.scale = "showall";
  params.wmode = "transparent";
  params.allowfullscreen = "true";
  params.allowscriptaccess = "always";
  params.allownetworking = "all";
  
  swfobject.embedSWF('piecemaker.swf', 'piecemaker', '560', '340', '10', null, flashvars,    
  params, null);

</script>

<link rel="stylesheet" type="text/css" href="css/ddsmoothmenu.css" />

<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/ddsmoothmenu.js">



</script>

<script type="text/javascript">

ddsmoothmenu.init({
    mainmenuid: "templatemo_menu", 
    orientation: 'h',
    classname: 'ddsmoothmenu', 
    //customtheme: ["#1c5a80", "#18374a"],
    contentsource: "markup" 
})

</script> 

</head>

<body id="home">

<div id="templatemo_wrapper">
    <div id="templatemo_top">
        <div id="templatemo_header">
            <div id="site_title"><h1><a href="#">Министерство обороны Российской Федерации</a></h1></div>
            <div id="templatemo_menu" class="ddsmoothmenu">
                <ul>
                    <li><a href="index.php" class="selected">Главная</a></li>
                    <li><a href="#">Новости</a>
                        <ul>
                            
                            <li><a href="#">Новости СВ</a></li>
                            <li><a href="#">Новости ВВС</a></li>
                            <li><a href="#">Новости ВМФ</a></li>
                        </ul>
                    </li>
                    <li><a href="#">Руководство</a>
                        <ul>
                            <li><a href="#">Руководство 1</a></li>
                            <li><a href="#">Руководство 2</a></li>
                            <li><a href="#">Руководство 3</a></li>
                            <li><a href="#">Руководство 4</a></li>
                            <li><a href="#">Руководство 5</a></li>
                            
                        </ul>
                    </li>
                    <li><a href="#">Структура</a></li>
                    <li><a href="#">Контакты</a></li>
                </ul>
                <br style="clear: left" />
            </div> <!-- end of templatemo_menu -->
            <div class="cleaner"></div>
        </div> <!-- END of header -->
        
        <div id="templatemo_slider">
            <div id="slider_left">
                <h2>Министерство обороны РФ</h2>
                <p>Федеральный орган исполнительной власти (федеральное министерство), проводящий государственную политику и осуществляющий государственное управление в области обороны, а также координирующий деятельность федеральных министерств.</p>
                <a href="#" class="learnmore">Узнать больше</a><a href="#" class="learnmore">Подписаться</a>
            </div>
            <div id="slider_right">
                <div id="piecemaker">
                  <p></p>
                </div>  
            </div>
            <div class="cleaner"></div>
        </div> <!-- END of slider -->
    </div> <!-- END of top -->
    
    <div id="templatemo_main">
        <div class="col one_third fp_services">
            <img src="images/tick-64px.png" alt="Image 01"/>
            <h2><a href="#">Сухопутные войска</a></h2>
            <p>Сухопутные войска (СВ). Вид Вооруженных Сил Российской Федерации (ВС РФ).</p>
        </div>
        
        <div class="col one_third fp_services">
            <img src="images/rosette-64px.png" alt="Image 02"/>
            <h2><a href="#">Военно-воздушные силы</a></h2>
            <p>Военно-воздушные силы (ВВС). Вид Вооруженных Сил Российской Федерации (ВС РФ).</p>
        </div>
        
        <div class="col one_third no_margin_right fp_services">
            <img src="images/post-it-64px.png" alt="Image 03"/>
            <h2><a href="#">Военно-Морской Флот</a></h2>
            <p>Военно-Морской Флот (ВМФ). Вид Вооруженных Сил Российской Федерации (ВС РФ).</p>
        </div>
        
        <div class="cleaner divider"></div>
        
        <div><?php echo $myrow['txt'] ?></div>
          
        <div class="cleaner"></div>
    </div> <!-- END of main -->
</div> <!-- END of wrapper -->

<div id="templatemo_footer_wrapper">
    <div id="templatemo_footer">
    
        <div class="col one_fourth">
            <h4>Министерство обороны РФ</h4>
            <p>Федеральный орган исполнительной власти (федеральное министерство), проводящий государственную политику и осуществляющий государственное управление в области обороны, а также координирующий деятельность федеральных министерств.</p>
        </div>
        
        <div class="col one_fourth">
            <h4>Меню</h4>
            <ul class="footer_list">
                <li><a href="#">Главная</a></li>
                <li><a href="#">Новости</a></li>
                <li><a href="#">Руководство</a></li>
                <li><a href="#">Структура</a></li>
                <li><a href="#">Контакты</a></li>
            </ul>   
        </div>
        
        <div class="col one_fourth">
            <h4>Дополнительная информация</h4>
            <ul class="twitter_post">
                <li>Главное управление кадров Министерства обороны Российской Федерации<a href="#"><br />8(800)200-22-95</a></li>
                <li>Справочная Министерства обороны Российской Федерации<a href="#"><br />8(495)696-88-00</a></li>   
            </ul>
        </div>
        <div class="col one_fourth no_margin_right">
            <h4>Связаться с нами</h4>   
            
            <div class="footer_social_button">
                <a href="#"><img src="images/facebook.png" title="facebook" alt="Facebook" /></a>
                <a href="#"><img src="images/flickr.png" title="flickr" alt="flickr" /></a>
                <a href="#"><img src="images/twitter.png" title="twitter" alt="Twitter" /></a>
                <a href="#"><img src="images/youtube.png" title="youtube" alt="Youtube" /></a>
                <a href="#"><img src="images/feed.png" title="rss" alt="RSS" /></a>
            </div>
        
            Все права защищены © 2013 <a href="#">Министерство обороны РФ</a> | Разработчик<a href="#" target="_parent"> курсант 271 уч. гр. Тучак Евгений Владимирович</a>
            
        </div>
        
        <div class="cleaner"></div>
    </div> <!-- END of footer -->
</div> <!-- END of wrapper -->

</body>
</html>

